"""
app.py - the Streamlit page.
Start the back end first (uvicorn api:app --reload), then run:  streamlit run app.py
"""

import html

import requests
import streamlit as st
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FixIt Booking Agent", layout="centered")

# ----------------------------------------------------------------------
# Look of the page (CSS)
# ----------------------------------------------------------------------

st.markdown("""
<style>
/* Background: deep blue to teal gradient, with white cards on top */
.stApp { background: radial-gradient(circle at 12% 6%, rgba(255,255,255,0.16), transparent 40%),
                     linear-gradient(160deg, #0A2A6B 0%, #1747C9 45%, #0E8FA8 100%) !important;
         background-attachment: fixed !important; }
.stApp p, .stApp label, .stApp span { color: #0F172A; }

/* Hide the default Streamlit menu, header and footer */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 980px; padding-top: 1.8rem; padding-bottom: 3rem; }

/* Top bar (on the gradient) */
.topbar { display: flex; justify-content: space-between; align-items: center;
          padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.28); margin-bottom: 34px; }
.stApp .brand { font-size: 1.7rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px; }
.stApp .brand span { color: #7DD3FC; }
.stApp .topnote { font-size: 1.05rem; color: #DBEAFE; font-weight: 600; }

/* Heading (on the gradient) */
.stApp .hero h1, .stApp .hero h1 * { color: #FFFFFF !important; }
.stApp .hero h1 { font-size: 3.2rem !important; font-weight: 800 !important; color: #FFFFFF !important; line-height: 1.12 !important;
                  letter-spacing: -1px; margin: 0 0 14px 0 !important; padding: 0 !important; }
.stApp .hero p { font-size: 1.35rem; color: #E3EDFF; margin: 0 0 20px 0; max-width: 760px; line-height: 1.5; }
.stApp .pill { display: inline-block; font-size: 1rem; font-weight: 600; color: #FFFFFF;
               background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.38);
               padding: 6px 16px; border-radius: 999px; margin: 0 8px 8px 0; }

/* Small labels (on the gradient) */
.stApp .small-label { font-size: 0.95rem; font-weight: 700; color: #C7DBFF; text-transform: uppercase;
                      letter-spacing: 0.8px; margin: 26px 0 10px 0; }

/* Example buttons (glass look on the gradient) */
div[data-testid="stButton"] button { background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.55);
                                     border-radius: 12px; padding: 0.65rem 1.3rem; }
div[data-testid="stButton"] button, div[data-testid="stButton"] button * { color: #FFFFFF !important;
                                     font-size: 1.1rem; font-weight: 600; }
div[data-testid="stButton"] button:hover { background: rgba(255,255,255,0.28); border-color: #FFFFFF; }

/* The request form (white card) */
div[data-testid="stForm"] { background: #FFFFFF; border: none; border-radius: 20px;
                            padding: 28px 28px 20px 28px; box-shadow: 0 12px 34px rgba(5,20,60,0.35); }
div[data-testid="stForm"] > div, div[data-testid="stForm"] div[data-baseweb="textarea"],
div[data-testid="stForm"] div[data-baseweb="base-input"] { background: #FFFFFF !important; }
div[data-testid="stTextAreaRootElement"], div[data-testid="stForm"] div[data-baseweb="textarea"] {
        border: 1.5px solid #CBD5E1 !important; border-radius: 12px !important; background: #FFFFFF !important; }
div[data-testid="stTextAreaRootElement"]:focus-within, div[data-testid="stForm"] div[data-baseweb="textarea"]:focus-within {
        border-color: #1D4ED8 !important; box-shadow: 0 0 0 4px rgba(29,78,216,0.16); }
div[data-testid="stForm"] div[data-baseweb="textarea"] { border: none !important; box-shadow: none !important; border-radius: 12px !important; }
div[data-testid="stTextAreaRootElement"] { overflow: hidden !important; }
div[data-testid="InputInstructions"] { display: none !important; }
div[data-testid="stForm"] textarea { background: #FFFFFF !important; color: #0F172A !important; font-size: 1.2rem !important;
        line-height: 1.55 !important; border: none !important; outline: none !important; box-shadow: none !important; }
div[data-testid="stForm"] textarea::placeholder { color: #94A3B8 !important; opacity: 1; }
div[data-testid="stForm"] button { background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 0.65rem 1.4rem; }
div[data-testid="stForm"] button, div[data-testid="stForm"] button * { color: #0F172A !important; font-size: 1.1rem; font-weight: 700; }
div[data-testid="stForm"] button:hover { border-color: #1D4ED8; }
div[data-testid="stForm"] button:hover, div[data-testid="stForm"] button:hover * { color: #1D4ED8 !important; }
div[data-testid="stForm"] button[kind="primaryFormSubmit"] { background: #1D4ED8; border: 1.5px solid #1D4ED8; }
div[data-testid="stForm"] button[kind="primaryFormSubmit"], div[data-testid="stForm"] button[kind="primaryFormSubmit"] * { color: #FFFFFF !important; }
div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover { background: #1E40AF; border-color: #1E40AF; }
.hint { font-size: 1rem; color: #64748B; margin: -4px 0 14px 0; }
div[data-testid="stSpinner"], div[data-testid="stSpinner"] * { color: #FFFFFF !important; font-size: 1.1rem; }

/* Result card (white) */
.result { background: #FFFFFF; border-left: 8px solid #94A3B8; border-radius: 18px;
          padding: 26px 28px; margin-top: 26px; box-shadow: 0 12px 34px rgba(5,20,60,0.35); }
.result.ok { border-left-color: #16A34A; }
.result.warn { border-left-color: #D97706; }
.result.err { border-left-color: #DC2626; }
.result.info { border-left-color: #1D4ED8; }
.badge { display: inline-block; font-size: 0.85rem; font-weight: 800; text-transform: uppercase;
         letter-spacing: 0.8px; padding: 5px 12px; border-radius: 8px; margin-bottom: 12px; }
.ok .badge { background: #DCFCE7; color: #166534; }
.warn .badge { background: #FEF3C7; color: #92400E; }
.err .badge { background: #FEE2E2; color: #991B1B; }
.info .badge { background: #DBEAFE; color: #1E40AF; }
.stApp .ok .badge { color: #166534; }
.stApp .warn .badge { color: #92400E; }
.stApp .err .badge { color: #991B1B; }
.stApp .info .badge { color: #1E40AF; }
.stApp .message { font-size: 1.4rem; color: #0F172A; line-height: 1.5; margin: 0 0 6px 0; font-weight: 500; }

/* Details and price table */
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 18px 0 8px 0; }
.cell { background: #F1F5FB; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px 16px; }
.stApp .cell .k { font-size: 0.82rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.6px; }
.stApp .cell .v { font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-top: 4px; }
table.price { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 1.18rem; }
table.price td { padding: 12px 6px; border-bottom: 1px solid #EEF2F7; color: #334155; }
table.price td.amt { text-align: right; font-variant-numeric: tabular-nums; }
table.price tr.total td { border-bottom: none; border-top: 3px solid #0F172A; padding-top: 16px;
                          font-weight: 800; font-size: 1.4rem; color: #0F172A; }

/* Bookings section */
.stApp .section-title { font-size: 1.7rem; font-weight: 800; color: #FFFFFF; margin: 44px 0 4px 0; }
.stApp .section-sub { font-size: 1.05rem; color: #D5E3FF; margin-bottom: 12px; }
.table-wrap { overflow-x: auto; background: #FFFFFF; border-radius: 18px; box-shadow: 0 12px 34px rgba(5,20,60,0.35); }
table.bookings { width: 100%; border-collapse: collapse; font-size: 1.02rem; }
table.bookings th { text-align: left; background: #EEF3FB; color: #475569; font-size: 0.8rem; font-weight: 800;
                    text-transform: uppercase; letter-spacing: 0.6px; padding: 14px 14px; }
table.bookings td { padding: 14px 14px; border-top: 1px solid #EEF2F7; color: #0F172A; }
table.bookings td.num { text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }
table.bookings td.nw { white-space: nowrap; }
.stApp .tag { display: inline-block; font-size: 0.82rem; font-weight: 800; padding: 3px 12px; border-radius: 999px; }
.stApp .tag.booked { background: #DCFCE7; color: #166534; }
.stApp .tag.cancelled { background: #E2E8F0; color: #475569; }
.stApp .footer { margin-top: 44px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.28);
                 font-size: 0.98rem; color: #D5E3FF; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Small helper functions
# ----------------------------------------------------------------------

EXAMPLES = {
    "Get a price": "How much for fixing a leaking pipe under my kitchen sink on Wednesday? I live in 411004.",
    "Book a visit": "My kitchen tap is leaking. Please send a plumber on Tuesday morning. Meera Joshi, 9876543210, pin 411038.",
    "Cancel a booking": "Cancel booking FX-1001.",
}

STATUS_LABELS = {
    "booked": ("Booked", "ok"),
    "quote_only": ("Price quote", "info"),
    "cancelled": ("Cancelled", "ok"),
    "need_more_info": ("More information needed", "warn"),
    "cannot_help": ("Unable to help", "warn"),
    "stopped": ("Stopped", "err"),
}


def clear_all():
    """Clear button: empty the request box and remove the last result."""
    st.session_state["prefill"] = ""
    st.session_state["box_version"] = st.session_state["box_version"] + 1
    st.session_state["result"] = None


def use_example(text):
    """Example button: put the example text in the request box."""
    st.session_state["prefill"] = text
    st.session_state["box_version"] = st.session_state["box_version"] + 1
    st.session_state["result"] = None


def safe(text):
    """Make text safe to show inside HTML."""
    return html.escape(str(text))


def cell(label, value):
    """One small box in the details row."""
    return '<div class="cell"><div class="k">' + safe(label) + '</div><div class="v">' + safe(value) + '</div></div>'


def show_result(answer):
    """Show the agent's answer as a card."""
    status = answer["status"]
    label, kind = STATUS_LABELS.get(status, (status, "info"))

    card = '<div class="result ' + kind + '">'
    card += '<span class="badge">' + safe(label) + '</span>'
    card += '<p class="message">' + safe(answer["message"]) + '</p>'

    if status in ("booked", "quote_only"):
        # Details row: booking ID (if any), service, date, slot (if any)
        card += '<div class="grid">'
        if answer["booking_id"] != "":
            card += cell("Booking ID", answer["booking_id"])
        card += cell("Service", answer["service_name"])
        card += cell("Date", answer["date"])
        if answer["slot"] != "":
            card += cell("Time slot", answer["slot"])
        card += '</div>'

        # Price table
        card += '<table class="price">'
        card += '<tr><td>Service price</td><td class="amt">Rs ' + str(answer["job_price"]) + '</td></tr>'
        card += '<tr><td>Visit charge</td><td class="amt">Rs ' + str(answer["visit_charge"]) + '</td></tr>'
        card += '<tr><td>Weekend extra</td><td class="amt">Rs ' + str(answer["weekend_extra"]) + '</td></tr>'
        card += '<tr><td>GST (18%)</td><td class="amt">Rs ' + str(answer["gst"]) + '</td></tr>'
        card += '<tr class="total"><td>Total</td><td class="amt">Rs ' + str(answer["total_price"]) + '</td></tr>'
        card += '</table>'

    elif status == "cancelled":
        card += '<div class="grid">'
        card += cell("Booking ID", answer["booking_id"])
        card += cell("Cancellation fee", "Rs " + str(answer["cancellation_fee"]))
        card += '</div>'

    card += '</div>'
    st.markdown(card, unsafe_allow_html=True)


def show_error(message):
    """Show an error card (for example when the back end is not running)."""
    card = '<div class="result err"><span class="badge">Problem</span>'
    card += '<p class="message">' + safe(message) + '</p></div>'
    st.markdown(card, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Page header
# ----------------------------------------------------------------------

# The request box gets a new key each time it is cleared or filled with an example.
# A new key means a brand new box, so old typed text can never be sent by mistake.
if "box_version" not in st.session_state:
    st.session_state["box_version"] = 0
if "prefill" not in st.session_state:
    st.session_state["prefill"] = ""
if "result" not in st.session_state:
    st.session_state["result"] = None

st.markdown("""
<div class="topbar">
  <div class="brand">Fix<span>It</span> Home Services</div>
  <div class="topnote">Pune</div>
</div>
<div class="hero">
  <h1>Book a home repair in one message</h1>
  <p>Tell us what needs fixing, where and when. Our agent will book the visit, give you a price
  or cancel a booking for you.</p>
  <span class="pill">Plumber</span><span class="pill">Electrician</span><span class="pill">AC Technician</span><span class="pill">Carpenter</span>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Request form
# ----------------------------------------------------------------------

st.markdown('<div class="small-label">Try an example</div>', unsafe_allow_html=True)
example_columns = st.columns(3)
position = 0
for example_name, example_text in EXAMPLES.items():
    example_columns[position].button(example_name, key="example_" + str(position),
                                     on_click=use_example, args=(example_text,))
    position = position + 1

st.markdown('<div class="small-label">Your request</div>', unsafe_allow_html=True)
with st.form("request_form", border=False):
    request_text = st.text_area(
        "Your request",
        value=st.session_state["prefill"],
        key="request_box_" + str(st.session_state["box_version"]),
        height=140,
        label_visibility="collapsed",
        placeholder="Example: My kitchen tap is leaking. Please send a plumber on Tuesday morning. "
                    "Meera Joshi, 9876543210, pin 411038.",
    )
    st.markdown('<div class="hint">Press Enter to send. Press Shift + Enter for a new line.</div>',
                unsafe_allow_html=True)
    button_columns = st.columns([1.5, 1, 3.5])
    send_clicked = button_columns[0].form_submit_button("Send request", type="primary")
    button_columns[1].form_submit_button("Clear", on_click=clear_all)

# Make the Enter key send the request (Shift + Enter still makes a new line)
components.html("""
<script>
const parentDoc = window.parent.document;
function bindEnter() {
  const box = parentDoc.querySelector('div[data-testid="stForm"] textarea');
  if (!box || box.dataset.enterBound === "yes") { return; }
  box.dataset.enterBound = "yes";
  box.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey && !event.ctrlKey && !event.metaKey && !event.altKey && !event.isComposing) {
      event.preventDefault();
      box.blur();
      setTimeout(function () {
        const buttons = parentDoc.querySelectorAll('div[data-testid="stForm"] button');
        for (const button of buttons) {
          if (button.innerText.trim() === "Send request") { button.click(); }
        }
      }, 120);
    }
  });
}
bindEnter();
setInterval(bindEnter, 400);
</script>
""", height=0)

# ----------------------------------------------------------------------
# Send the request to the back end
# ----------------------------------------------------------------------

if send_clicked:
    if request_text.strip() == "":
        st.session_state["result"] = {"error": "Please type your request first."}
    else:
        try:
            with st.spinner("Working on your request..."):
                response = requests.post(API_URL + "/request", json={"message": request_text}, timeout=120)
            if response.status_code != 200:
                st.session_state["result"] = {"error": "The back end could not handle this request. Please try again."}
            else:
                st.session_state["result"] = response.json()
        except requests.exceptions.ConnectionError:
            st.session_state["result"] = {"error": "The back end is not running. Please start it with: uvicorn api:app --reload"}
        except requests.exceptions.Timeout:
            st.session_state["result"] = {"error": "The back end took too long to answer. Please try again."}

result = st.session_state["result"]
if result is not None:
    if "error" in result:
        show_error(result["error"])
    else:
        show_result(result)

# ----------------------------------------------------------------------
# All bookings
# ----------------------------------------------------------------------

st.markdown('<div class="section-title">All bookings</div>', unsafe_allow_html=True)
try:
    bookings_response = requests.get(API_URL + "/bookings", timeout=10)
    all_bookings = bookings_response.json()
    if len(all_bookings) == 0:
        st.markdown('<div class="section-sub">There are no bookings yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-sub">' + str(len(all_bookings)) + ' in total, newest first.</div>',
                    unsafe_allow_html=True)
        table = '<div class="table-wrap"><table class="bookings"><tr>'
        for heading in ["Booking ID", "Customer", "Phone", "Area", "Service", "Date", "Slot", "Total (Rs)", "Status"]:
            table += "<th>" + heading + "</th>"
        table += "</tr>"
        for booking in reversed(all_bookings):
            table += "<tr>"
            table += '<td class="nw">' + safe(booking["booking_id"]) + "</td>"
            table += "<td>" + safe(booking["name"]) + "</td>"
            table += '<td class="nw">' + safe(booking["phone"]) + "</td>"
            table += "<td>" + safe(booking["area"]) + "</td>"
            table += "<td>" + safe(booking["service_name"]) + "</td>"
            table += '<td class="nw">' + safe(booking["date"]) + "</td>"
            table += '<td class="nw">' + safe(booking["slot"]) + "</td>"
            table += '<td class="num">' + safe(booking["total_price"]) + "</td>"
            table += '<td class="nw"><span class="tag ' + safe(booking["status"]) + '">' + safe(booking["status"]) + "</span></td>"
            table += "</tr>"
        table += "</table></div>"
        st.markdown(table, unsafe_allow_html=True)
except requests.exceptions.RequestException:
    st.markdown('<div class="section-sub">Bookings cannot be shown because the back end is not running.</div>',
                unsafe_allow_html=True)

st.markdown('<div class="footer">Booking week: Monday 2 to Sunday 8 November 2026. '
            'Prices include the visit charge and 18% GST.</div>', unsafe_allow_html=True)