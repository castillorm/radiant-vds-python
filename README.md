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
