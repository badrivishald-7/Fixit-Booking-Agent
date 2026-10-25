"""
run_practice.py - sends the practice requests to the agent in order and writes test_results.md.
Run with:  python run_practice.py
It deletes bookings.json first, so every run starts from the beginning.
This needs your GROQ_API_KEY in the .env file.

If your practice_requests.txt has more requests (the brief says 6), add them to the
PRACTICE list below, in the same order, with the answer you expect.
"""

import os

import tools
from agent import handle_request

# Each item: the request, a short name, the expected status, booking ID and total (or fee)
PRACTICE = [
    {
        "request": "How much for fixing a leaking pipe under my kitchen sink on Wednesday? I live in 411004.",
        "tests": "Price only",
        "status": "quote_only", "booking_id": "", "amount": 529,
    },
    {
        "request": "My kitchen tap is leaking. Please send a plumber on Tuesday morning. Meera Joshi, 9876543210, pin 411038.",
        "tests": "Normal booking, weekday",
        "status": "booked", "booking_id": "FX-1001", "amount": 352,
    },
    {
        "request": "Please install a new ceiling fan on Saturday afternoon. Arjun Mehta, 98230 12345, pin code 411021.",
        "tests": "Weekend extra, outer zone, phone with a space",
        "status": "booked", "booking_id": "FX-1002", "amount": 588,
    },
    {
        "request": "My kitchen tap is leaking. Please send a plumber on Tuesday morning. Meera Joshi, 9876543210, pin 411038.",
        "tests": "Same booking sent twice",
        "status": "booked", "booking_id": "FX-1001", "amount": 352,
    },
]

# Start from a clean file
if os.path.exists(tools.BOOKINGS_FILE):
    os.remove(tools.BOOKINGS_FILE)

lines = ["# Test results", "",
         "Each request was sent to the agent in order, starting with no bookings.json.", ""]

number = 1
for item in PRACTICE:
    answer = handle_request(item["request"])

    # For a cancellation the amount is the fee, otherwise it is the total
    if answer["status"] == "cancelled":
        got_amount = answer["cancellation_fee"]
    else:
        got_amount = answer["total_price"]

    status_ok = answer["status"] == item["status"]
    id_ok = answer["booking_id"] == item["booking_id"]
    amount_ok = got_amount == item["amount"]
    verdict = "Right." if (status_ok and id_ok and amount_ok) else "Not right."

    lines.append("## Request " + str(number) + ": " + item["tests"])
    lines.append("")
    lines.append("Request: " + item["request"])
    lines.append("")
    lines.append("- Status: " + answer["status"] + " (expected " + item["status"] + ")")
    lines.append("- Booking ID: " + (answer["booking_id"] or "none") + " (expected " + (item["booking_id"] or "none") + ")")
    lines.append("- Total or fee: Rs " + str(got_amount) + " (expected Rs " + str(item["amount"]) + ")")
    lines.append("- Agent message: " + answer["message"])
    lines.append("- Verdict: " + verdict)
    lines.append("")
    print("Request", number, verdict)
    number = number + 1

lines.append("bookings.json rows at the end: " + str(len(tools.load_bookings())))

with open(os.path.join(tools.BASE_FOLDER, "test_results.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Written to test_results.md")
