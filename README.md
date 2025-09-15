# RadiantOne VDS 7.4 – Minimal Python REST Client

Minimal Python client for RadiantOne VDS 7.4 REST API. Supports Basic or Bearer auth, tests connectivity, and runs LDAP-style search queries. Auto-detects common REST roots for quick scripts, testing, and demos.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
export VDS_BASE_URL="https://your-vds-host:8443"
export VDS_USERNAME="cn=directory manager"
export VDS_PASSWORD="changeme"
python vds_client.py
```

Perfect — I’ll give you both the **Python script** (in a `vds_rest_query.py` file) and a clean **README.md** you can drop into a GitHub repo.

---

### 📄 `vds_rest_query.py`

```python
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
```

---

### 📘 `README.md`

````markdown
# Radiant Logic VDS REST Query Example

This repository contains a simple Python script to query a Radiant Logic Virtual Directory Server (VDS) instance using its **REST API** with an **LDAP filter**.

## 📋 Requirements

- Python 3.x
- `requests` library (`pip install requests`)
- Access to a running Radiant VDS instance with the REST service enabled

## ⚙️ Configuration

Edit the following variables in `vds_rest_query.py`:

```python
VDS_HOST = "http://localhost:8080"   # VDS host/port
BASE_DN = "dc=example,dc=com"        # Base DN
LDAP_FILTER = "(uid=*)"              # LDAP filter
USER = "cn=admin"                    # VDS username
PASSWORD = "password"                # VDS password
````

## ▶️ Usage

Run the script from your terminal:

```bash
python vds_rest_query.py
```

It will send the query and print the results in JSON format.

## 🔒 Notes

* If your VDS server uses **self-signed certificates**, the script disables SSL verification (`verify=False`). You may want to update this for production use.
* The query scope is set to `sub` (subtree search). You can change it to `base` or `one` if needed.

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

```

---

