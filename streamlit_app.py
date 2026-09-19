import streamlit as st
import collections
import string

# Set up mobile page configuration
st.set_page_config(page_title="Xenocrypt Solver", page_icon="📝", layout="centered")

st.title("📝 Xenocrypt Analyzer Pro")
st.write("Paste your Spanish text below to extract key Codebusters data.")

# Large, mobile-friendly text input area
user_input = st.text_area("Spanish Text Input:", placeholder="Paste text here...", height=150)

# Reference Dictionary for the most common words (Spanish to English equivalents)
common_words_dict = {
    "EL / LA / LOS / LAS": "the",
    "Y": "and",
    "EN": "in / on / at",
    "DE": "of / from",
    "QUE": "that / which / who",
    "UN / UNA": "a / an",
    "ES / SON": "is / are",
    "POR / PARA": "for / by",
    "CON": "with",
    "SU": "his / her / their",
    "LO": "it (object marker)",
    "SI": "if / yes",
    "COMO": "as / like",
    "PERO": "but"
}

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

# Sidebar / Expander Reference (Always visible or toggleable on mobile)
with st.expander("📖 Top Spanish Word Dictionary", expanded=False):
    st.write("These represent English fundamentals ('the', 'and', 'it', 'is') mapped to Spanish equivalents:")
    # Display as a clean table
    st.table([{"Spanish Word": k, "English Meaning": v} for k, v in common_words_dict.items()])

if user_input:
    # Standardize to uppercase and include Spanish Ñ
    text = user_input.upper()
    valid_letters = string.ascii_uppercase + "Ñ"
    
    words = text.split()
    two_letter_words = set()
    three_letter_words = set()
    clean_letter_list = []
    
    for word in words:
        cleaned_word = "".join([c for c in word if c in valid_letters])
        if len(cleaned_word) == 2:
            two_letter_words.add(cleaned_word)
        elif len(cleaned_word) == 3:
            three_letter_words.add(cleaned_word)
        for letter in cleaned_word:
            clean_letter_list.append(letter)

    total_letters = len(clean_letter_list)
    letter_counts = collections.Counter(clean_letter_list)
    
    # Display Results
    st.subheader("📊 Letter Frequencies")
    st.caption("Standard Spanish Expected Top Letters: E, A, O, S, N")
    
    freq_output = ""
    for letter, count in letter_counts.most_common():
        percentage = (count / total_letters) * 100
        freq_output += f"**Letter {letter}:** {count} times ({percentage:.1f}%)\n\n"
    st.markdown(freq_output)
        
    st.subheader("📌 2-Letter Words Found")
    if two_letter_words:
        st.write(", ".join(sorted(two_letter_words)))
        
        # New Feature: Smart Rule Engine based on his parsed text
        st.markdown("##### 💡 Cryptographic Breakdowns:")
        for w in sorted(two_letter_words):
            first_char = w[0]
            if first_char in spanish_two_letter_rules:
                st.info(f"Since your word starts with **{first_char}**, in Spanish it can practically only be: **{spanish_two_letter_rules[first_char]}**")
            else:
                st.warning(f"Word **{w}** starts with **{first_char}**. This is highly uncommon for valid Spanish starter letters. Check for an alignment or wrap-around error!")
    else:
        st.write("_None found_")
    
    st.subheader("📌 3-Letter Words Found")
    st.caption("Look for: QUE, LOS, LAS, CON, POR")
    st.write(", ".join(sorted(three_letter_words)) if three_letter_words else "_None found_")
