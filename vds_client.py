#!/usr/bin/env python3
"""
Minimal RadiantOne VDS 7.4 REST client
- Tests connectivity to the REST endpoint
- Runs an LDAP search via REST and returns JSON results
"""
import os
import json
import logging
from typing import Iterable, Optional, Dict, Any
import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

VDS_BASE_URL = os.getenv("VDS_BASE_URL", "https://your-vds-host:8443")
REST_ROOT_CANDIDATES = ["/vds/rest","/rest","/vds-server/rest"]
USERNAME = os.getenv("VDS_USERNAME", "cn=directory manager")
PASSWORD = os.getenv("VDS_PASSWORD", "changeme")
BEARER_TOKEN = os.getenv("VDS_BEARER_TOKEN")
SSL_VERIFY = os.getenv("VDS_SSL_VERIFY", "false").lower() in ("1", "true", "yes")
TIMEOUT_SECS = float(os.getenv("VDS_TIMEOUT", "15"))

def _auth():
    if BEARER_TOKEN:
        return None
    return HTTPBasicAuth(USERNAME, PASSWORD)

def _headers():
    if BEARER_TOKEN:
        return {"Authorization": f"Bearer {BEARER_TOKEN}"}
    return {}

def _first_alive_endpoint(session: requests.Session) -> Optional[str]:
    ping_variants = [(root, "/ping") for root in REST_ROOT_CANDIDATES] + [(root, "/server/info") for root in REST_ROOT_CANDIDATES]
    for root, path in ping_variants:
        url = f"{VDS_BASE_URL.rstrip('/')}{root}{path}"
        try:
            r = session.get(url, auth=_auth(), headers=_headers(), verify=SSL_VERIFY, timeout=TIMEOUT_SECS)
            if r.status_code == 200:
                logging.info(f"Detected REST root at: {root} (probe {path} OK)")
                return root
        except requests.RequestException:
            continue
    return None

def _search_endpoint(root: str) -> str:
    return f"{VDS_BASE_URL.rstrip('/')}{root}/ldap/search"

def test_connection() -> bool:
    with requests.Session() as s:
        root = _first_alive_endpoint(s)
        if not root:
            logging.error("No REST root responded to ping/info probes.")
            return False
    logging.info("✅ Connected to RadiantOne VDS REST successfully.")
    return True

def ldap_query(base_dn: str, filter_exp: str = "(objectClass=*)", attributes: Optional[Iterable[str]] = None, scope: str = "sub", size_limit: int = 100, time_limit: int = 0) -> Optional[Dict[str, Any]]:
    with requests.Session() as s:
        root = _first_alive_endpoint(s)
        if not root:
            logging.error("Cannot run search — REST root not detected.")
            return None
        url = _search_endpoint(root)
        params = {"base": base_dn, "scope": scope, "filter": filter_exp, "sizeLimit": size_limit, "timeLimit": time_limit}
        if attributes:
            params["attributes"] = ",".join(attributes)
        try:
            r = s.get(url, params=params, auth=_auth(), headers=_headers(), verify=SSL_VERIFY, timeout=TIMEOUT_SECS)
            if r.status_code == 200:
                return r.json()
            else:
                logging.error(f"Search failed {r.status_code}: {r.text[:500]}")
                return None
        except requests.RequestException as e:
            logging.error(f"HTTP error: {e}")
            return None

if __name__ == "__main__":
    if test_connection():
        result = ldap_query("ou=targetou,dc=acme,dc=com", "(cn=*)", ["cn","mail","uid"], "sub", 25)
        if result is not None:
            print(json.dumps(result, indent=2)[:5000])
        else:
            print("No results (or error).")
