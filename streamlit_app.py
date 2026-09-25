import streamlit as st
import collections
import string
from deep_translator import GoogleTranslator

# Set up mobile page configuration
st.set_page_config(page_title="Xenocrypt Solver Pro", page_icon="📝", layout="centered")

st.title("📝 Xenocrypt Analyzer Pro v5")
st.write("Paste your Spanish text below to extract key Codebusters data.")

# Initialize persistent session storage arrays
if "accumulated_text" not in st.session_state:
    st.session_state.accumulated_text = ""
if "past_prompts_list" not in st.session_state:
    st.session_state.past_prompts_list = []

# Base Spanish Dictionary (Expanded Structure Words)
common_words_dict = {
    "EL / LA / LOS / LAS": "the",
    "Y / E": "and",
    "O / U": "or",
    "EN": "in / on / at",
    "DE": "of / from",
    "QUE": "that / which / who / than",
    "UN / UNA / UNOS / UNAS": "a / an / some",
    "ES / SON / ESTA / ESTAN": "is / are",
    "POR / PARA": "for / by / to",
    "CON": "with",
    "SIN": "without",
    "SU / SUS": "his / her / their / your",
    "LO / LE / LA / LOS / LES": "it / him / her / them (pronouns)",
    "SI": "if / yes",
    "COMO": "as / like / how",
    "PERO": "but",
    "MAS / MENOS": "more / less",
    "ESTE / ESTA / ESTO": "this",
    "TODO / TODOS": "all / everything / everyone",
    "MUY": "very"
}

# Standard Spanish Letter Frequencies Benchmark Data
esp_freq_data = [
    {"Letter": "E", "Pct": "13.7%"}, {"Letter": "A", "Pct": "11.7%"}, {"Letter": "O", "Pct": "9.7%"},
    {"Letter": "L", "Pct": "5.5%"},  {"Letter": "S", "Pct": "7.2%"},  {"Letter": "N", "Pct": "6.8%"},
    {"Letter": "R", "Pct": "6.4%"},  {"Letter": "I", "Pct": "5.3%"},  {"Letter": "D", "Pct": "4.7%"},
    {"Letter": "T", "Pct": "4.6%"},  {"Letter": "C", "Pct": "4.1%"},  {"Letter": "U", "Pct": "4.0%"},
    {"Letter": "M", "Pct": "2.7%"},  {"Letter": "P", "Pct": "2.4%"},  {"Letter": "B", "Pct": "1.4%"},
    {"Letter": "G", "Pct": "1.0%"},  {"Letter": "V", "Pct": "1.1%"},  {"Letter": "Y", "Pct": "0.9%"},
    {"Letter": "Q", "Pct": "0.9%"},  {"Letter": "H", "Pct": "0.9%"},  {"Letter": "F", "Pct": "0.7%"},
    {"Letter": "Z", "Pct": "0.5%"},  {"Letter": "J", "Pct": "0.5%"},  {"Letter": "Ñ", "Pct": "0.3%"},
    {"Letter": "X", "Pct": "0.2%"},  {"Letter": "W", "Pct": "0.1%"},  {"Letter": "K", "Pct": "0.1%"}
]

# Cryptographic rules lookup for Spanish 2-letter starting letters
spanish_two_letter_rules = {
    "A": "AL (to the), AS (ace/you have), AN (they have)",
    "D": "DE (of/from), DI (I gave/say)",
    "E": "EL (the), EN (in), ES (is), EX (ex)",
    "L": "LA (the), LO (it/the), LE (to him/her)",
    "M": "ME (me), MI (my/me)",
    "N": "NO (no/not), NI (neither/nor)",
    "S": "SU (his/her), SE (himself/oneself), SI (if/yes)",
    "T": "TU (your), TE (you/to you)",
    "U": "UN (a/an)"
}

# Translation helper map for length-specific automated dictionary lookups
word_translator = {
    "EL": "the", "LA": "the", "LOS": "the", "LAS": "the", "DE": "of/from", "EN": "in/on", "UN": "a/an", "UNA": "a/an", "ES": "is", "SON": "are", "SU": "his/her", "AL": "to the", "LO": "it", "NO": "no", "SI": "if/yes", "ME": "me", "MI": "my", "SE": "oneself", "TE": "you", "TU": "your", "NI": "neither", "Y": "and", "E": "and", "O": "or", "U": "or", "CON": "with", "POR": "for/by", "PARA": "for/to", "QUE": "that/which", "DEL": "of the", "MAS": "more", "UNO": "one", "SIN": "without", "MUY": "very", "LES": "them", "ASI": "like this", "COMO": "like/as", "TODO": "all", "ESTE": "this", "ESTA": "this/is", "PERO": "but", "BIEN": "well", "CUAN": "how", "AÑO": "year", "DIAS": "days", "ERAN": "were", "ESOS": "those", "ESAS": "those"
}

# Main Input Layout
user_input = st.text_area("Spanish Text Input:", placeholder="Paste text here...", height=120)

# Sidebar UI Elements for References
with st.sidebar:
    st.header("📊 Reference Center")
    if st.button("🗑️ Reset Prompt History"):
        st.session_state.accumulated_text = ""
        st.session_state.past_prompts_list = []
        st.success("History reset completely!")
        
    with st.expander("🇪🇸 ESP Frequency (Standard Spanish)"):
        st.table(esp_freq_data)

    with st.expander("📖 Structural Word Dictionary"):
        st.table([{"Spanish": k, "English Equivalent": v} for k, v in common_words_dict.items()])

if user_input:
    clean_input_upper = user_input.strip().upper()
    if not st.session_state.past_prompts_list or st.session_state.past_prompts_list[-1] != clean_input_upper:
        st.session_state.accumulated_text += " " + clean_input_upper
        st.session_state.past_prompts_list.append(clean_input_upper)
    
    valid_letters = string.ascii_uppercase + "Ñ"
    
    def process_data(target_text):
        words = target_text.split()
        two_l, three_l, four_l = [], [], []
        letters_list = []
        for word in words:
            cleaned = "".join([c for c in word if c in valid_letters])
            if len(cleaned) == 2: two_l.append(cleaned)
            elif len(cleaned) == 3: three_l.append(cleaned)
            elif len(cleaned) == 4: four_l.append(cleaned)
            for letter in cleaned: letters_list.append(letter)
        return letters_list, two_l, three_l, four_l

    hist_letters, hist_2, hist_3, hist_4 = process_data(st.session_state.accumulated_text)
    curr_letters, curr_2, _, _ = process_data(user_input.upper())

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Current Text Analysis")
        # FIXED: Feed ONLY the letter list index [0] to the Counter engine instead of the full tuple response object
        letter_counts = collections.Counter(curr_letters)
        total_curr = len(curr_letters) or 1
        curr_freq = ""
        for letter, count in letter_counts.most_common(10):
            curr_freq += f"**{letter}:** {count} times ({(count/total_curr)*100:.1f}%)\n\n"
        st.markdown(curr_freq)

    with col2:
        st.subheader("📈 Prompt Frequency (All Inputs)")
        hist_counts = collections.Counter(hist_letters)
        total_hist = len(hist_letters) or 1
        prompt_freq_table = []
        for letter, count in hist_counts.most_common():
            prompt_freq_table.append({"Letter": letter, "Count": f"{count} ({(count/total_hist)*100:.1f}%)"})
        st.table(prompt_freq_table[:12])

    st.subheader("🏆 5 Most Frequent Word Forms in Prompts")
    
    def get_top_5_table(word_list):
        counts = collections.Counter(word_list).most_common(5)
        table_out = []
        for rank, (word, count) in enumerate(counts, start=1):
            translation = word_translator.get(word, "_Unknown / Name_")
            table_out.append({"Rank": rank, "Word": word, "Count Found": count, "Likely Meaning": translation})
        return table_out

    t1, t2, t3 = st.tabs(["2-Letter Top 5", "3-Letter Top 5", "4-Letter Top 5"])
    with t1: st.table(get_top_5_table(hist_2))
    with t2: st.table(get_top_5_table(hist_3))
    with t3: st.table(get_top_5_table(hist_4))

    if curr_2:
        st.subheader("💡 Active Cryptographic Breakdowns")
        for w in sorted(list(set(curr_2))):
            if w in spanish_two_letter_rules:
                st.info(f"Since **{w}** starts with **{w}**: It typically matches: {spanish_two_letter_rules[w]}")

# Section 4: History Ledger (With Direct Paragraph Translation)
if st.session_state.past_prompts_list:
    st.markdown("---")
    st.subheader("📜 Past Inputs Ledger & Translations")
    
    history_table_data = []
    for idx, prompt in enumerate(st.session_state.past_prompts_list, start=1):
        try:
            clean_english_translation = GoogleTranslator(source='es', target='en').translate(prompt)
        except Exception:
            clean_english_translation = "[Translation Service Offline]"

        history_table_data.append({
            "ID": idx,
            "Original Spanish Input": prompt if len(prompt) < 60 else prompt[:57] + "...",
            "English Translation": clean_english_translation
        })
    st.table(history_table_data)

    st.subheader("🔍 Look Up Letter Frequencies of a Past Input")
    dropdown_options = [f"Input #{i}: {p[:40]}..." for i, p in enumerate(st.session_state.past_prompts_list, start=1)]
    selected_option = st.selectbox("Select a prompt to isolate its letter breakdowns:", dropdown_options)
    
    if selected_option:
        # Fixed calculation parsing string safely to extract index integer
        selected_index = int(selected_option.split(":")[0].replace("Input #", "")) - 1
        chosen_prompt = st.session_state.past_prompts_list[selected_index]
        
        chosen_letters = [c for c in chosen_prompt if c in (string.ascii_uppercase + "Ñ")]
        chosen_total = len(chosen_letters) or 1
        chosen_counts = collections.Counter(chosen_letters)
        
        isolated_table = []
        for letter, count in chosen_counts.most_common():
            isolated_table.append({
                "Letter": letter, 
                "Count": count, 
                "Percentage": f"{(count/chosen_total)*100:.1f}%"
            })
        st.write(f"**Letter Distribution Details for Input #{selected_index + 1}:**")
        st.table(isolated_table[:8])
