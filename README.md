# FixIt Booking Agent

An agent for FixIt Home Services, a made-up home repair company in Pune. A customer types one
request in plain words. The agent books a visit, gives a price without booking, or cancels a
booking, and follows the company rules in `data/policies.md`.

Every price and fee is worked out by plain Python code (`tools.py`). The model only decides which
tool to call and copies the numbers. It never does the maths.

Built with the OpenAI Agents SDK, Pydantic, FastAPI and Streamlit. The model is run on Groq
(booking agent `openai/gpt-oss-20b`, formatter `qwen/qwen3.8-27b`), through Groq's OpenAI-compatible
address, so a Groq API key is used.

## Files

| File | What it does |
|------|--------------|
| `tools.py` | The six tools (check_area, find_services, get_price_quote, check_slots, book_visit, cancel_booking) and the hidden-instruction check. No AI inside. |
| `agent.py` | The agent, its instructions and the Pydantic answer form |
| `api.py` | FastAPI back end: POST /request, GET /bookings, GET /health |
| `app.py` | Streamlit page |
| `test_tools.py` | Tests the tools with no AI |
| `run_practice.py` | Sends the practice requests to the agent and writes `test_results.md` |
| `data/` | The company files (do not change them) |
| `bookings.json` | Created by the code when the first booking is made |

## Setup

1. Open a terminal in the project folder and create a virtual environment:

   ```
   python -m venv .venv
   ```

2. Activate it.
   - Windows: `.venv\Scripts\activate`
   - Mac or Linux: `source .venv/bin/activate`

3. Install the packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project folder (copy `.env.example`) and put your Groq key in it
   (get one free at https://console.groq.com):

   ```
   GROQ_API_KEY=your-key-here
   ```

   Also add these two lines (the models used for the two steps):

   ```
   GROQ_MODEL=openai/gpt-oss-20b
   GROQ_FORMAT_MODEL=qwen/qwen3.8-27b
   ```

   Never share this file. It is already in `.gitignore`.

## How to run

Test the tools first (no AI, no key needed):

```
python test_tools.py
```

Test the agent in the terminal:

```
python agent.py
```

Run the back end. Keep this terminal open:

```
uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs and try each endpoint.

Run the page in a second terminal:

```
streamlit run app.py
```

To run the six practice requests and write `test_results.md`:

```
python run_practice.py
```

To start again from zero, delete `bookings.json`.

## Company rules in short

- Today is fixed as Monday 2 November 2026. Bookings are open from 2 to 8 November 2026.
- Slots: Morning, Afternoon, Evening. One technician per type of work per slot. Electricians do not work on Sundays.
- Price = service price + visit charge (inner Rs 99, outer Rs 149) + Rs 100 on Saturday and Sunday, then 18% GST rounded to the nearest rupee.
- Cancelling is free before the day of the visit and costs Rs 99 on the day. A cancelled slot becomes free again.
- Gas leaks, the main meter or street pole, painting, waterproofing and fridge, washing machine and TV repairs are never booked.

## How the agent works with Groq (and a known limitation)

Groq does not allow tool calling and structured (Pydantic) answers in the same request. So each
request runs in two steps:

1. The booking agent calls the tools (area, services, price, slots, book, cancel) and writes a plain-text reply.
2. A formatter agent with no tools turns the result into the Pydantic form `FixItAnswer` (`output_type`).

After step 2, `fix_answer()` in `agent.py` copies the booking ID, date, slot, every price and the
cancellation fee from the tool results. The model never decides a price or a fee.

Known limitation and the models used: Groq's `openai/gpt-oss-120b` often failed step 2
(error `json_validate_failed`), so step 2 uses `qwen/qwen3.8-27b` (`GROQ_FORMAT_MODEL`). The booking
agent uses `openai/gpt-oss-20b` (`GROQ_MODEL`) because the free daily token limit of `gpt-oss-120b`
ran out. If step 2 ever fails, the program prints "Formatter step failed" and `fallback_answer()`
builds the same `FixItAnswer` in plain Python from the tool results, so the final answer is still correct.