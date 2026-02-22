import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────
#  KONFIGURACJA STRONY
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Asystent KSAT 3 | ELEMENTO",
    page_icon="🏫",
    layout="centered"
)

# ─────────────────────────────────────────────
#  STYL CSS – profesjonalny, czysty design
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

    /* Globalne */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F0F4F8;
    }

    /* Ukryj domyślny header Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── HERO HEADER ── */
    .hero {
        background: linear-gradient(135deg, #0A2540 0%, #1A4B8C 60%, #1E88E5 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(10,37,64,0.18);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -60px; left: 30px;
        width: 160px; height: 160px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        color: #90CAF9;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .hero h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #ffffff;
        margin: 0 0 0.4rem;
        line-height: 1.2;
    }
    .hero p {
        color: rgba(255,255,255,0.65);
        font-size: 0.9rem;
        margin: 0;
        font-weight: 300;
    }
    .hero-status {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-top: 1.2rem;
    }
    .status-dot {
        width: 8px; height: 8px;
        background: #69F0AE;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
    }
    .status-text {
        color: rgba(255,255,255,0.6);
        font-size: 0.78rem;
        font-weight: 400;
    }

    /* ── POWITANIE ── */
    .welcome-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        border-left: 4px solid #1E88E5;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
    }
    .welcome-icon {
        font-size: 1.6rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .welcome-text strong {
        color: #0A2540;
        font-size: 0.95rem;
    }
    .welcome-text p {
        color: #546E7A;
        font-size: 0.85rem;
        margin: 0.2rem 0 0;
        line-height: 1.5;
    }

    /* ── KOMUNIKAT BŁĘDU 429 ── */
    .limit-alert {
        background: linear-gradient(135deg, #FFF3E0, #FFF8E1);
        border: 1.5px solid #FFB300;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin: 0.5rem 0;
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
        box-shadow: 0 4px 16px rgba(255,179,0,0.15);
        animation: slideIn 0.3s ease;
    }
    .limit-alert-icon { font-size: 1.8rem; flex-shrink: 0; }
    .limit-alert-title {
        font-weight: 700;
        color: #E65100;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .limit-alert-text {
        color: #BF360C;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    .limit-alert-tip {
        margin-top: 0.5rem;
        background: rgba(255,179,0,0.15);
        border-radius: 8px;
        padding: 0.4rem 0.7rem;
        font-size: 0.8rem;
        color: #E65100;
    }

    /* ── WIADOMOŚCI CZATU ── */
    .stChatMessage {
        border-radius: 14px !important;
        margin-bottom: 0.5rem !important;
    }

    /* ── INPUT ── */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 1.5px solid #BBDEFB !important;
        box-shadow: 0 2px 12px rgba(30,136,229,0.08) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #1E88E5 !important;
        box-shadow: 0 2px 16px rgba(30,136,229,0.18) !important;
    }

    /* ── STOPKA ── */
    .footer {
        text-align: center;
        color: #90A4AE;
        font-size: 0.75rem;
        padding: 1rem 0 0.5rem;
        border-top: 1px solid #E0E0E0;
        margin-top: 1.5rem;
    }
    .footer strong { color: #546E7A; }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">ELEMENTO · Wsparcie techniczne</div>
    <h1>Asystentka Ela 🏫</h1>
    <p>Pomoc z programem KSAT 3 · dostępna 24/7 dla pracowników przedszkoli</p>
    <div class="hero-status">
        <div class="status-dot"></div>
        <span class="status-text">Gotowa do pomocy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KARTA POWITALNA
# ─────────────────────────────────────────────
st.markdown("""
<div class="welcome-card">
    <div class="welcome-icon">👋</div>
    <div class="welcome-text">
        <strong>Cześć! Tu Asystentka Ela.</strong>
        <p>Opisz mi swój problem z programem KSAT 3, a wytłumaczę wszystko krok po kroku – bez trudnych słów technicznych. Jestem tu po to, żeby Ci pomóc! 😊</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
Jesteś "Asystentką Elą" – cierpliwą i życzliwą ekspertką wsparcia technicznego firmy ELEMENTO.
Pomagasz pracownikom przedszkoli obsługiwać program KSAT 3.

ZASADY:
- Pisz prostym, ciepłym językiem – jakbyś tłumaczyła coś swojej mamie
- ZAKAZ żargonu IT. Zamiast "cache" → "pamięć tymczasowa". Zamiast "restart" → "wyłącz i włącz ponownie"
- Zawsze uspokajaj, gdy użytkownik zgłasza błąd (np. "Nie martw się, to częsty problem!")
- Instrukcje podawaj ZAWSZE krok po kroku, numerując je (1., 2., 3.,...)
- Opisuj kliknięcia dokładnie (np. "Kliknij zielony przycisk 'Wyślij' w prawym dolnym rogu ekranu")
- Jeśli nie znasz odpowiedzi dotyczącej KSAT 3 → napisz: "To pytanie wymaga kontaktu z serwisem ELEMENTO. Możesz napisać na adres: serwis@elemento.pl"
- Jeśli pytanie NIE dotyczy KSAT 3 → uprzejmie odmów i przypomnij swoją rolę

TWOJA ROLA: Obsługujesz WYŁĄCZNIE pytania dotyczące programu KSAT 3 i pracy w przedszkolu z tym systemem.
"""

# ─────────────────────────────────────────────
#  MODELE GROQ
# ─────────────────────────────────────────────
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

# ─────────────────────────────────────────────
#  KONFIGURACJA KLIENTA GROQ
# ─────────────────────────────────────────────
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Brak klucza API. Dodaj GROQ_API_KEY do Secrets na Streamlit Cloud.")
    st.stop()

client = Groq(api_key=api_key)

# ─────────────────────────────────────────────
#  FUNKCJA Z OBSŁUGĄ BŁĘDÓW
# ─────────────────────────────────────────────
LIMIT_HTML = """
<div class="limit-alert">
    <div class="limit-alert-icon">⏳</div>
    <div>
        <div class="limit-alert-title">Limit na dziś został przekroczony</div>
        <div class="limit-alert-text">
            Asystentka Ela odpowiedziała już na bardzo dużo pytań dzisiaj i potrzebuje chwili przerwy.
            Spróbuj ponownie jutro lub skontaktuj się bezpośrednio z serwisem.
        </div>
        <div class="limit-alert-tip">
            📧 Napisz do nas: <strong>serwis@elemento.pl</strong>
        </div>
    </div>
</div>
"""

def get_response(messages):
    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *messages
                ],
                max_tokens=1024,
            )
            return response.choices[0].message.content, False  # (treść, czy_limit)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                continue  # Próbuj kolejny model
            elif any(code in error_str for code in ["404", "503", "unavailable"]):
                continue
            else:
                return f"⚠️ Wystąpił nieoczekiwany problem. Skontaktuj się z serwisem ELEMENTO: serwis@elemento.pl\n\n_(Szczegóły: {e})_", False

    # Wszystkie modele zwróciły 429 – limit przekroczony
    return LIMIT_HTML, True  # (HTML alertu, czy_limit=True)

# ─────────────────────────────────────────────
#  HISTORIA CZATU
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_limit"):
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# ─────────────────────────────────────────────
#  OBSŁUGA NOWEGO ZAPYTANIA
# ─────────────────────────────────────────────
if prompt := st.chat_input("Opisz swój problem z programem KSAT 3..."):

    st.session_state.messages.append({"role": "user", "content": prompt, "is_limit": False})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ela pisze odpowiedź..."):
            answer, is_limit = get_response(st.session_state.messages)

        if is_limit:
            st.markdown(answer, unsafe_allow_html=True)
        else:
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "is_limit": is_limit})

# ─────────────────────────────────────────────
#  STOPKA
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🏢 <strong>ELEMENTO Sp. z o.o.</strong> · Wsparcie techniczne KSAT 3 · serwis@elemento.pl
</div>
""", unsafe_allow_html=True)
