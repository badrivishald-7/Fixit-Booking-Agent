# Test results

Each request was sent to the agent in order, starting with no bookings.json.

## Request 1: Price only

Request: How much for fixing a leaking pipe under my kitchen sink on Wednesday? I live in 411004.

- Status: quote_only (expected quote_only)
- Booking ID: none (expected none)
- Total or fee: Rs 529 (expected Rs 529)
- Agent message: The cost for fixing the pipe leak under your kitchen sink on Wednesday 4 November 2026 is Rs 529.
- Verdict: Right.

## Request 2: Normal booking, weekday

Request: My kitchen tap is leaking. Please send a plumber on Tuesday morning. Meera Joshi, 9876543210, pin 411038.

- Status: booked (expected booked)
- Booking ID: FX-1001 (expected FX-1001)
- Total or fee: Rs 352 (expected Rs 352)
- Agent message: Your visit has been booked. The plumber will arrive on 3 November 2026 in the Morning slot. Your booking ID is FX-1001. The total cost will be Rs 352.
- Verdict: Right.

## Request 3: Weekend extra, outer zone, phone with a space

Request: Please install a new ceiling fan on Saturday afternoon. Arjun Mehta, 98230 12345, pin code 411021.

- Status: booked (expected booked)
- Booking ID: FX-1002 (expected FX-1002)
- Total or fee: Rs 588 (expected Rs 588)
- Agent message: Your visit for fan installation is booked for 7 November 2026, Afternoon slot. Booking ID FX-1002. Total cost Rs 588.
- Verdict: Right.

## Request 4: Same booking sent twice

Request: My kitchen tap is leaking. Please send a plumber on Tuesday morning. Meera Joshi, 9876543210, pin 411038.

- Status: booked (expected booked)
- Booking ID: FX-1001 (expected FX-1001)
- Total or fee: Rs 352 (expected Rs 352)
- Agent message: Your visit has been booked. The plumber will arrive on 3 November 2026 in the Morning slot. Booking ID: FX-1001. Total cost: Rs 352.
- Verdict: Right.

bookings.json rows at the end: 2
