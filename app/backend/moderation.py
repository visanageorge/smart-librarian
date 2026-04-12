import re
import unicodedata

# Exemplu lista de baza 
BAD_WORDS = {
    "dumb",
    "idiot",
    "stupid",
    "fuck"
}

# Regex pentru variante mai ascunse
BAD_PATTERNS = [
    r"\bprost\w*\b",
    r"\bidiot\w*\b",
    r"\bstupid\w*\b",
    r"\bf+u+c+k+\b",
]

def normalize_text(text) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text);
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text

def tokenize_text(text) -> list[str]:
    return re.findall(r'\b\w+\b', text)

def find_offensive_words(text):
    normalized = normalize_text(text)
    tokens = tokenize_text(normalized)

    found = []

    for word in tokens:
        if word in BAD_WORDS:
            found.append(word)

    for pattern in BAD_PATTERNS:
        matches = re.findall(pattern, normalized)
        found.extend(matches)

    return list(set(found))

def is_offensive(text):
    return len(find_offensive_words(text)) > 0