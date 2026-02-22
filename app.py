import streamlit as st
from openai import OpenAI

# ─────────────────────────────────────────────
#  KONFIGURACJA STRONY
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Asystent KSAT 3 | ELEMENTO",
    page_icon="🏫",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E88E5, #0D47A1);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 1.8rem; }
    .main-header p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.95rem; }
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #1E88E5;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🏫 Asystentka Ela – Pomoc KSAT 3</h1>
    <p>Wsparcie techniczne dla przedszkoli | ELEMENTO Sp. z o.o.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    👋 Witaj! Jestem <strong>Asystentką Elą</strong> i jestem tu, żeby pomóc Ci z programem <strong>KSAT 3</strong>.
    Opisz swój problem, a wytłumaczę wszystko krok po kroku – bez trudnych słów technicznych. 😊
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
#  LISTA DARMOWYCH MODELI (zapasowych)
#  Jeśli pierwszy nie działa, próbuje kolejnego
# ─────────────────────────────────────────────
FREE_MODELS = [
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-r1-distill-llama-70b:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwen2.5-vl-72b-instruct:free",
]

# ─────────────────────────────────────────────
#  KONFIGURACJA KLIENTA
# ─────────────────────────────────────────────
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ Brak klucza API. Dodaj OPENROUTER_API_KEY do Secrets na Streamlit Cloud.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# ─────────────────────────────────────────────
#  FUNKCJA Z AUTOMATYCZNYM PRZEŁĄCZANIEM MODELI
# ─────────────────────────────────────────────
def get_response(messages):
    for model in FREE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *messages
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            # Jeśli rate limit lub niedostępny - próbuj następny model
            if "429" in error_str or "404" in error_str or "rate" in error_str.lower():
                continue
            else:
                # Inny błąd - zwróć komunikat
                return f"⚠️ Wystąpił problem z połączeniem. Spróbuj odświeżyć stronę (klawisz F5). Jeśli problem się powtarza, skontaktuj się z serwisem ELEMENTO: serwis@elemento.pl\n\n_(Szczegóły: {e})_"
    
    return "⚠️ Wszystkie serwery są chwilowo przeciążone. Odczekaj kilka minut i spróbuj ponownie. Jeśli problem się powtarza, skontaktuj się z serwisem ELEMENTO: serwis@elemento.pl"

# ─────────────────────────────────────────────
#  HISTORIA CZATU
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
#  OBSŁUGA NOWEGO ZAPYTANIA
# ─────────────────────────────────────────────
if prompt := st.chat_input("Opisz swój problem z programem KSAT 3..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ela pisze odpowiedź..."):
            answer = get_response(st.session_state.messages)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ─────────────────────────────────────────────
#  STOPKA
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.8rem;'>"
    "🏢 ELEMENTO Sp. z o.o. | Wsparcie techniczne KSAT 3 | serwis@elemento.pl"
    "</p>",
    unsafe_allow_html=True
)
