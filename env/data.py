import random

def get_tickets():
    base = [
        {
            "ticket_id": "1",
            "message": "Payment failed but money deducted",
            "tier": "pro",
            "class": "billing",
            "priority": "high",
            "route": "billing_team"
        },
        {
            "ticket_id": "2",
            "message": "App crashes on login",
            "tier": "free",
            "class": "technical",
            "priority": "medium",
            "route": "tier2"
        },
        {
            "ticket_id": "3",
            "message": "My account got hacked, urgent help needed",
            "tier": "enterprise",
            "class": "account",
            "priority": "urgent",
            "route": "security_team"
        },
        {
            "ticket_id": "4",
            "message": "Refund not received after cancellation",
            "tier": "pro",
            "class": "billing",
            "priority": "high",
            "route": "billing_team"
        },
        {
            "ticket_id": "5",
            "message": "Unable to update profile information",
            "tier": "free",
            "class": "account",
            "priority": "low",
            "route": "tier1"
        },
        {
            "ticket_id": "6",
            "message": "System lagging badly during usage",
            "tier": "pro",
            "class": "technical",
            "priority": "medium",
            "route": "tier2"
        },
        {
            "ticket_id": "7",
            "message": "Double charged for subscription",
            "tier": "enterprise",
            "class": "billing",
            "priority": "high",
            "route": "billing_team"
        },
        {
            "ticket_id": "8",
            "message": "Password reset not working",
            "tier": "free",
            "class": "account",
            "priority": "medium",
            "route": "tier1"
        },
        {
            "ticket_id": "9",
            "message": "Server error while uploading files",
            "tier": "pro",
            "class": "technical",
            "priority": "high",
            "route": "tier2"
        },
        {
            "ticket_id": "10",
            "message": "Suspicious login detected",
            "tier": "enterprise",
            "class": "account",
            "priority": "urgent",
            "route": "security_team"
        }
    ]

    # Expand dataset to 30 tickets
    tickets = base * 3

    # Shuffle but deterministic
    random.seed(42)
    random.shuffle(tickets)

    return tickets