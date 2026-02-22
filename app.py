import streamlit as st
from groq import Groq
import PyPDF2
import io

# ─────────────────────────────────────────────
#  KONFIGURACJA STRONY
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Asystent KSAT 3 | ELEMENTO",
    page_icon="🏫",
    layout="centered"
)

# ─────────────────────────────────────────────
#  DARK MODE CSS z geometrycznym patternem
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'DM Sans', sans-serif;
        color: #E2E8F0;
    }

    /* ── DARK BACKGROUND z geometrycznym patternem ── */
    .stApp {
        background-color: #0D1117;
        background-image:
            linear-gradient(rgba(30,136,229,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(30,136,229,0.06) 1px, transparent 1px),
            radial-gradient(ellipse at 20% 50%, rgba(30,136,229,0.08) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(99,179,237,0.06) 0%, transparent 50%);
        background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%;
    }

    /* Ukryj Streamlit UI */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── HERO ── */
    .hero {
        background: linear-gradient(135deg, #0A1628 0%, #0D2144 60%, #0F3460 100%);
        border: 1px solid rgba(30,136,229,0.25);
        border-radius: 20px;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(30,136,229,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 20px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(30,136,229,0.15);
        color: #63B3ED;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(30,136,229,0.3);
    }
    .hero h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #ffffff;
        margin: 0 0 0.4rem;
        line-height: 1.2;
    }
    .hero p {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        margin: 0;
        font-weight: 300;
    }
    .hero-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1.2rem;
    }
    .status-dot {
        width: 8px; height: 8px;
        background: #48BB78;
        border-radius: 50%;
        box-shadow: 0 0 8px #48BB78;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #48BB78; }
        50% { opacity: 0.6; transform: scale(1.3); box-shadow: 0 0 14px #48BB78; }
    }
    .status-text { color: rgba(255,255,255,0.45); font-size: 0.78rem; }

    /* ── WELCOME CARD ── */
    .welcome-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(30,136,229,0.2);
        border-left: 4px solid #1E88E5;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
    }
    .welcome-icon { font-size: 1.6rem; flex-shrink: 0; }
    .welcome-text strong { color: #E2E8F0; font-size: 0.95rem; }
    .welcome-text p { color: #718096; font-size: 0.85rem; margin: 0.2rem 0 0; line-height: 1.5; }

    /* ── UPLOAD SEKCJA ── */
    .upload-section {
        background: rgba(255,255,255,0.03);
        border: 1px dashed rgba(30,136,229,0.3);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .upload-title {
        color: #63B3ED;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .upload-desc {
        color: #4A5568;
        font-size: 0.8rem;
        margin-bottom: 0.7rem;
    }
    .file-loaded {
        background: rgba(72,187,120,0.1);
        border: 1px solid rgba(72,187,120,0.3);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        color: #68D391;
        font-size: 0.82rem;
        margin-top: 0.5rem;
    }

    /* ── STREAMLIT DARK OVERRIDES ── */
    .stChatMessage {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 14px !important;
    }
    .stChatInputContainer textarea {
        background: rgba(255,255,255,0.05) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(30,136,229,0.3) !important;
    }
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploader"] label { color: #A0AEC0 !important; }

    /* ── LIMIT ALERT ── */
    .limit-alert {
        background: linear-gradient(135deg, rgba(237,137,54,0.12), rgba(236,201,75,0.08));
        border: 1.5px solid rgba(237,137,54,0.4);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin: 0.5rem 0;
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
        box-shadow: 0 4px 16px rgba(237,137,54,0.1);
        animation: slideIn 0.3s ease;
    }
    .limit-alert-icon { font-size: 1.8rem; flex-shrink: 0; }
    .limit-alert-title { font-weight: 700; color: #F6AD55; font-size: 0.95rem; margin-bottom: 0.3rem; }
    .limit-alert-text { color: #CBD5E0; font-size: 0.85rem; line-height: 1.5; }
    .limit-alert-tip {
        margin-top: 0.5rem;
        background: rgba(237,137,54,0.12);
        border-radius: 8px;
        padding: 0.4rem 0.7rem;
        font-size: 0.8rem;
        color: #F6AD55;
    }

    /* ── STOPKA ── */
    .footer {
        text-align: center;
        color: #2D3748;
        font-size: 0.75rem;
        padding: 1rem 0 0.5rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 1.5rem;
    }
    .footer strong { color: #4A5568; }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
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
#  WELCOME CARD
# ─────────────────────────────────────────────
st.markdown("""
<div class="welcome-card">
    <div class="welcome-icon">👋</div>
    <div class="welcome-text">
        <strong>Cześć! Tu Asystentka Ela.</strong>
        <p>Opisz mi swój problem z programem KSAT 3, a wytłumaczę wszystko krok po kroku – bez trudnych słów technicznych. Możesz też wgrać plik PDF z błędem lub instrukcją! 😊</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  UPLOAD PLIKU PDF
# ─────────────────────────────────────────────
st.markdown("""
<div class="upload-section">
    <div class="upload-title">📎 Wgraj plik (opcjonalnie)</div>
    <div class="upload-desc">Możesz wgrać plik <strong style="color:#63B3ED">wyłącznie w formacie PDF</strong> (np. instrukcję lub raport z błędem) – inne formaty nie są obsługiwane.</div>
</div>
""", unsafe_allow_html=True)

st.caption("⚠️ Akceptujemy **tylko pliki .PDF** – Word, Excel, zdjęcia i inne formaty nie będą działać.")
uploaded_file = st.file_uploader(
    "Wybierz plik PDF",
    type=["pdf"],
    label_visibility="collapsed"
)

pdf_context = ""
if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""

        if pdf_text.strip():
            pdf_context = f"\n\n[WGRANY PLIK: {uploaded_file.name}]\n{pdf_text[:4000]}"
            st.markdown(f"""
            <div class="file-loaded">
                ✅ Plik wczytany: <strong>{uploaded_file.name}</strong>
                ({len(pdf_reader.pages)} str.) – Ela weźmie go pod uwagę w odpowiedzi.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Nie udało się odczytać tekstu z PDF. Spróbuj opisać problem słowami.")
    except Exception as e:
        st.warning(f"Problem z odczytaniem pliku: {e}")

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
- Jeśli w wiadomości użytkownika znajduje się tekst z wgranego pliku PDF, przeanalizuj go i odnieś się do jego treści

TWOJA ROLA: Obsługujesz WYŁĄCZNIE pytania dotyczące programu KSAT 3 i pracy w przedszkolu z tym systemem.
"""

# ─────────────────────────────────────────────
#  GROQ
# ─────────────────────────────────────────────
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Brak klucza API. Dodaj GROQ_API_KEY do Secrets na Streamlit Cloud.")
    st.stop()

client = Groq(api_key=api_key)

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
    # Wyślij do Groq tylko pola role i content – bez is_limit i innych
    clean_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, *clean_messages],
                max_tokens=1024,
            )
            return response.choices[0].message.content, False
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                continue
            elif any(c in error_str for c in ["404", "503", "unavailable"]):
                continue
            else:
                return f"⚠️ Wystąpił nieoczekiwany problem. Skontaktuj się z serwisem ELEMENTO: serwis@elemento.pl\n\n_(Szczegóły: {e})_", False
    return LIMIT_HTML, True

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
#  NOWE ZAPYTANIE
# ─────────────────────────────────────────────
if prompt := st.chat_input("Opisz swój problem z programem KSAT 3..."):
    # Dodaj kontekst PDF do wiadomości jeśli plik wgrany
    full_prompt = prompt + pdf_context

    st.session_state.messages.append({"role": "user", "content": full_prompt, "is_limit": False})
    with st.chat_message("user"):
        st.markdown(prompt)  # Pokaż tylko pytanie, bez surowego tekstu PDF

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
