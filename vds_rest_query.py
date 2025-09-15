import requests
from requests.auth import HTTPBasicAuth
import json

# ===== CONFIGURATION =====
VDS_HOST = "http://10.0.0.1:8090"         # VDS host + port (use http:// or https://)
BASE_DN = "o=companydirectory"            # Base DN for the search
LDAP_FILTER = "(uid=*)"                   # LDAP filter
USER_DN = "cn=admin,dc=example,dc=com"    # VDS bind DN
PASSWORD = "password"                     # VDS password

# ===== FUNCTION TO QUERY VDS =====
def query_vds_rest(base_dn, ldap_filter):
    # Build the URL with filter as a query param
    url = f"{VDS_HOST}/adap/{base_dn}?contextFilter={ldap_filter}"

    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(USER_DN, PASSWORD),  # Basic Auth
            headers={"Accept": "application/json"}, # Request JSON format
            verify=False   # Disable SSL verification if using self-signed certs
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {e}")
        return None


# ===== MAIN =====
if __name__ == "__main__":
    results = query_vds_rest(BASE_DN, LDAP_FILTER)

    if results:
        print("LDAP Query Results:")
        print(json.dumps(results, indent=2))
    else:
        print("No results or error occurred.")
