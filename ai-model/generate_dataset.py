import csv
import random

random.seed(42)

data = {
    "Account Access": {
        "Low": [
            "I forgot my password for {service}",
            "I cannot remember my {service} password",
            "I need help resetting my password for {service}",
            "Please send me a password reset for {service}",
            "The password reset link for {service} has expired",
            "I want to change my {service} password",
        ],
        "Medium": [
            "My {service} account is locked",
            "I cannot sign into {service}",
            "Login to {service} keeps failing",
            "My credentials are being rejected by {service}",
            "I am unable to authenticate to {service}",
            "I cannot access my {service} account after several attempts",
        ],
        "High": [
            "My {service} account was disabled and important work is blocked",
            "I urgently need access to {service} for business operations",
            "My access to {service} suddenly stopped during critical work",
            "I have completely lost access to {service} and cannot continue working",
        ],
    },

    "Billing": {
        "Low": [
            "I need a copy of my invoice for {item}",
            "Please explain a charge for {item}",
            "Where can I download my {item} invoice",
            "I need billing details for {item}",
            "Please provide the receipt for {item}",
        ],
        "Medium": [
            "My refund for {item} has not arrived",
            "The amount on my {item} invoice is incorrect",
            "I was charged the wrong price for {item}",
            "There is an unexpected charge for {item}",
            "My refund for {item} is delayed",
        ],
        "High": [
            "I was billed twice for the same {item}",
            "Payment failed but money was deducted for {item}",
            "A duplicate charge appeared for {item}",
            "My account was charged multiple times for {item}",
            "Money was taken even though the {item} transaction failed",
        ],
    },

    "Hardware": {
        "Low": [
            "The keyboard on my {device} has a few keys that do not work",
            "My {device} is making a strange noise",
            "The mouse connected to my {device} is not responding correctly",
            "The printer connected to my {device} has a minor issue",
        ],
        "Medium": [
            "The display on my {device} keeps flickering",
            "My {device} screen flashes while I am working",
            "The {device} freezes randomly during work",
            "My {device} overheats and shuts down occasionally",
            "The monitor connected to my {device} keeps disconnecting",
        ],
        "High": [
            "My {device} will not turn on",
            "The {device} has completely stopped working",
            "My {device} continuously restarts and I cannot work",
            "The hard drive in my {device} appears to have failed",
            "My {device} shuts down immediately after startup",
        ],
    },

    "Infrastructure": {
        "Medium": [
            "The {system} is running unusually slowly",
            "Performance of the {system} has degraded",
            "Some employees are having trouble accessing the {system}",
            "The {system} is responding slowly to requests",
        ],
        "High": [
            "The {system} is unavailable for many users",
            "The {system} keeps crashing during business hours",
            "A major component of the {system} is failing",
            "Many employees cannot access the {system}",
            "The {system} is experiencing a serious service disruption",
        ],
        "Critical": [
            "The entire {system} is offline and nobody can use it",
            "The {system} has completely crashed for all users",
            "There is a complete outage of the {system}",
            "All customers have lost access to the {system}",
            "The production {system} is down across the organization",
            "The {system} is unavailable company wide",
            "The entire production environment for {system} has gone offline",
        ],
    },

    "Network": {
        "Low": [
            "WiFi signal is weak in the {location}",
            "Internet speed is slightly slow in the {location}",
            "Network performance is inconsistent in the {location}",
            "WiFi coverage is poor in the {location}",
        ],
        "Medium": [
            "Internet disconnects several times a day in the {location}",
            "The network connection keeps dropping in the {location}",
            "WiFi disconnects frequently in the {location}",
            "Internet latency is very high in the {location}",
            "The connection becomes unstable throughout the day in the {location}",
            "Employees keep losing network connectivity in the {location}",
        ],
        "High": [
            "The {location} cannot connect to the corporate network",
            "Network access is completely unavailable in the {location}",
            "Employees in the {location} cannot connect to the company VPN",
            "The entire {location} has lost network connectivity",
        ],
    },

    "Security": {
        "Medium": [
            "I received a suspicious email related to {service}",
            "There was an unusual login attempt on {service}",
            "I received an unexpected security alert from {service}",
            "A suspicious attachment was sent to my {service} account",
        ],
        "High": [
            "Someone may have stolen my {service} login credentials",
            "I received a phishing message asking for my {service} password",
            "Suspicious activity was detected on my {service} account",
            "Someone logged into my {service} account without permission",
            "My {service} credentials may have been compromised",
        ],
        "Critical": [
            "Confidential information from {service} was accessed without permission",
            "Administrator credentials for {service} have been compromised",
            "Malware has infected systems connected to {service}",
            "Sensitive company data from {service} may have been stolen",
            "An attacker gained administrator access to {service}",
            "A security breach exposed confidential data in {service}",
        ],
    },

    "Software": {
        "Low": [
            "I need help installing {software}",
            "The latest update for {software} will not install",
            "I need help configuring {software}",
            "{software} installation fails on my computer",
        ],
        "Medium": [
            "{software} closes unexpectedly when I use it",
            "{software} crashes whenever I open it",
            "{software} freezes during normal work",
            "{software} displays an unexpected error",
            "{software} stops responding after a few minutes",
            "{software} crashes when I try to open a file",
            "{software} closes whenever I try to read a message",
        ],
        "High": [
            "{software} is completely unusable and blocking my work",
            "{software} crashes continuously for several employees",
            "An important feature in {software} has completely stopped working",
            "{software} failure is preventing the team from completing critical work",
        ],
    },
}

values = {
    "service": [
        "Microsoft 365",
        "company email",
        "employee portal",
        "HR portal",
        "admin dashboard",
        "customer portal",
        "company account",
        "cloud account",
    ],

    "item": [
        "monthly subscription",
        "software license",
        "service plan",
        "company purchase",
        "cloud subscription",
        "support plan",
    ],

    "device": [
        "laptop",
        "desktop computer",
        "workstation",
        "office computer",
        "company laptop",
    ],

    "system": [
        "database server",
        "production server",
        "web application",
        "internal portal",
        "backend service",
        "customer platform",
        "cloud platform",
        "production environment",
    ],

    "location": [
        "main office",
        "finance department",
        "engineering floor",
        "branch office",
        "meeting area",
        "support department",
    ],

    "software": [
        "Outlook",
        "Microsoft Teams",
        "CRM application",
        "accounting software",
        "company application",
        "Excel",
        "ERP system",
        "desktop application",
    ],
}


rows = []

for category, priorities in data.items():
    for priority, templates in priorities.items():
        for template in templates:

            placeholder = None

            for key in values:
                if "{" + key + "}" in template:
                    placeholder = key
                    break

            if placeholder:
                for value in values[placeholder]:
                    text = template.format(
                        **{placeholder: value}
                    )

                    rows.append([
                        text,
                        category,
                        priority
                    ])

            else:
                rows.append([
                    template,
                    category,
                    priority
                ])


# Add small natural variations
expanded_rows = []

prefixes = [
    "",
    "Please help. ",
    "I need assistance because ",
    "Urgent issue: ",
    "Support needed: "
]

for text, category, priority in rows:

    expanded_rows.append([
        text,
        category,
        priority
    ])

    prefix = random.choice(prefixes)

    if prefix:
        expanded_rows.append([
            prefix + text[0].lower() + text[1:],
            category,
            priority
        ])


# Remove duplicates
unique_rows = list({
    (text, category, priority)
    for text, category, priority in expanded_rows
})

random.shuffle(unique_rows)


with open(
    "tickets_dataset.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "text",
        "category",
        "priority"
    ])

    writer.writerows(unique_rows)


print("Dataset generated successfully!")
print("Total tickets:", len(unique_rows))

print("\nTickets per category:")

category_counts = {}

for _, category, _ in unique_rows:
    category_counts[category] = (
        category_counts.get(category, 0) + 1
    )

for category, count in sorted(category_counts.items()):
    print(category, ":", count)

print("\nTickets per priority:")

priority_counts = {}

for _, _, priority in unique_rows:
    priority_counts[priority] = (
        priority_counts.get(priority, 0) + 1
    )

for priority, count in sorted(priority_counts.items()):
    print(priority, ":", count)