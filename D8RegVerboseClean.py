import re

# --- Unified Verbose Regex Pattern ---
pattern = re.compile(r'''
    (?P<url>                 # --- Match URLs ---
        https?://\S+
    )
    |
    (?P<email>               # --- Match Emails ---
        [\w\.-]+@[\w\.-]+
    )
    |
    (?P<phone>
    (?:\+91[\-\s]?)?     # Optional +91 with optional dash or space
    \d{10}               # Exactly 10 digits
    )
    |
    (?P<hashtag>             # --- Match Hashtags ---
        \#\w+
    )
    |
    (?P<special>             # --- Match Unwanted Special Characters ---
        [^
            \w              # Word characters
            \s              # Whitespace
            \#\.@           # Keep #, . and @
        ]+
    )
''', re.VERBOSE)

# --- Sample Raw Text ---
raw_text = """
🚨 Breaking!!! Visit https://bit.ly/3XyzAbC NOW!!! 💥💥
Get 50% OFF on all items @ our store 🛒🛍️. Offer valid till 31st Dec, 2025.
Email us at: support@deals4u.com or call 📞 +91-9876543210.
#Sale #Discount #2025 #🔥🔥🔥
"""

# --- Lowercase the Text ---
text = raw_text.lower()

# --- Containers for Extracted Info ---
hashtags = []
emails = []
phones = []

# --- Replacement Function ---
def replacer(match):
    if match.group('url'):
        return ''  # Remove URL
    elif match.group('email'):
        emails.append(match.group('email'))
        return '[EMAIL]'
    elif match.group('phone'):
        phones.append(match.group('phone'))
        return '[PHONE]'
    elif match.group('hashtag'):
        hashtags.append(match.group('hashtag'))
        return match.group('hashtag')  # Keep hashtags
    elif match.group('special'):
        return ''  # Remove unwanted characters
    return match.group(0)

# --- Apply Regex Substitution ---
cleaned_text = pattern.sub(replacer, text)

# --- Normalize Whitespace and Punctuation ---
cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
cleaned_text = re.sub(r' \.', '.', cleaned_text)

# --- Final Output ---
print("🧼 Cleaned Text:\n", cleaned_text)
print("🏷️ Hashtags:", hashtags)
print("📧 Emails:", emails)
print("📞 Phones:", phones)