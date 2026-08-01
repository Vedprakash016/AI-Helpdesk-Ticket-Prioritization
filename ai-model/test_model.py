import joblib

category_model = joblib.load("category_model.pkl")
priority_model = joblib.load("priority_model.pkl")

test_tickets = [
    "The entire production environment has gone offline and customers cannot use any services",
    "I was billed twice for the same monthly subscription",
    "Someone stole my login credentials and accessed confidential company information",
    "My laptop display sometimes flashes while I am working",
    "I cannot remember the password for my employee portal",
    "The office internet disconnects several times during the day",
    "Outlook closes unexpectedly whenever I try to read an email"
]

for ticket in test_tickets:
    category = category_model.predict([ticket])[0]
    priority = priority_model.predict([ticket])[0]

    category_confidence = category_model.predict_proba([ticket]).max() * 100
    priority_confidence = priority_model.predict_proba([ticket]).max() * 100

    print("\nTicket:", ticket)
    print("Category:", category)
    print("Priority:", priority)
    print("Category Confidence:", round(category_confidence, 2), "%")
    print("Priority Confidence:", round(priority_confidence, 2), "%")