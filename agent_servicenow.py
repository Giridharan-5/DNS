import requests

# ===== ServiceNow Config =====
SERVICENOW_INSTANCE = "https://dev270315.service-now.com"
SERVICENOW_USER = "admin"
SERVICENOW_PASS = "Cj$yD6c-rC2P"
TABLE = "incident"

# Giridharan caller sys_id
CALLER_SYS_ID = "a1b8794a83313210a88ff2d6feaad3fd"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def fetch_ticket():
    """
    Fetch ONE open incident raised by Giridharan
    """
    url = f"{SERVICENOW_INSTANCE}/api/now/table/{TABLE}"

    query = (
        f"caller_id={CALLER_SYS_ID}"
        "^state!=7"  # not closed
        "^ORDERBYsys_created_on"
    )

    params = {
        "sysparm_query": query,
        "sysparm_limit": 1
    }

    r = requests.get(
        url,
        auth=(SERVICENOW_USER, SERVICENOW_PASS),
        headers=HEADERS,
        params=params,
        timeout=20
    )

    r.raise_for_status()
    results = r.json().get("result", [])

    return results[0] if results else None


def update_ticket(sys_id, summary):
    """
    Update work notes ONLY (safe, no ACL issues)
    """
    url = f"{SERVICENOW_INSTANCE}/api/now/table/{TABLE}/{sys_id}"

    payload = {
        "work_notes": summary
    }

    r = requests.patch(
        url,
        auth=(SERVICENOW_USER, SERVICENOW_PASS),
        headers=HEADERS,
        json=payload,
        timeout=20
    )

    r.raise_for_status()
