from agent_servicenow import fetch_ticket, update_ticket
from agent_classifier import classify_ticket


def run():
    print("\n--- TICKET PROCESSING STARTED ---")

    ticket = fetch_ticket()
    if not ticket:
        print("No tickets found for the specified caller.")
        return

    steps = []

    ticket_number = ticket["number"]
    short_desc = ticket.get("short_description", "")
    desc = ticket.get("description", "")
    sys_id = ticket["sys_id"]

    steps.append(f"Ticket Number: {ticket_number}")

    classification = classify_ticket(short_desc, desc)
    steps.append(f"Ticket classified as: {classification}")

    # ---- Decision Logic ----
    if classification != "DNS_ADD":
        steps.append("Action: Ticket is not DNS-related. No DNS changes performed.")
        final_status = "CLOSED (No Action Required)"
    else:
        # DNS logic can be plugged here later
        steps.append("Action: DNS ticket detected (processing skipped for now).")
        final_status = "PENDING DNS ACTION"

    steps.append(f"Final Status: {final_status}")

    summary = "\n".join(steps)

    print("\n".join(steps))
    print("\n--------------------------------------------------\n")

    # Update ticket in ServiceNow
    update_ticket(sys_id, summary)


if __name__ == "__main__":
    run()
