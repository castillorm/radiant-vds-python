import requests
from requests.auth import HTTPBasicAuth
import json

# ===== CONFIGURATION =====
VDS_HOST = "http://localhost:8080"   # Change to your VDS host/port
BASE_DN = "dc=example,dc=com"        # Base DN for the query
LDAP_FILTER = "(uid=*)"              # Your LDAP query filter
USER = "cn=admin"                    # VDS username
PASSWORD = "password"                # VDS password

# ===== FUNCTION TO QUERY VDS =====
def query_vds_rest(base_dn, ldap_filter):
    url = f"{VDS_HOST}/rest/search"

    payload = {
        "dn": base_dn,
        "scope": "sub",   # can be "base", "one", or "sub"
        "filter": ldap_filter,
        "attributes": ["*"]   # return all attributes
    }

    try:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(USER, PASSWORD),
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            verify=False   # disable SSL verification if using self-signed certs
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
