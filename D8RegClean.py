import re
import nltk
from nltk.corpus import stopwords

# --- Email Masking Example ---
text = "Contact me at test@example.com"
# Replace email addresses with a placeholder
masked = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', text)
print(masked)  # Output: "Contact me at [EMAIL]"

# --- Raw Text Cleaning ---
raw_text = """
🚨 Breaking!!! Visit https://bit.ly/3XyzAbC NOW!!! 💥💥
Get 50% OFF on all items @ our store 🛒🛍️. Offer valid till 31st Dec, 2025.
Email us at: support@deals4u.com or call 📞 +91-9876543210.
#Sale #Discount #2025 #🔥🔥🔥
"""

# Step 1: Convert to lowercase
raw_updated = raw_text.lower()
print(raw_updated)

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F1E0-\U0001F1FF"
    "]+", flags=re.UNICODE)
raw_updated = emoji_pattern.sub(r'', raw_updated)
print(raw_updated)

# Step 2: Remove URLs (http or https)
raw_updated = re.sub(r'https?://\S+', '', raw_updated)
print(raw_updated)

# Step 3: Remove special characters (except hashtags, dots, @ for emails)
raw_updated = re.sub(r'[^\w\s#\.@]+', '', raw_updated)
print(raw_updated)

# Step 4: Normalize whitespace
raw_updated = re.sub(r'\s+', ' ', raw_updated).strip()
print(raw_updated)

# Step 5: Remove space before periods
raw_updated = re.sub(r' \.', '.', raw_updated)
print(raw_updated)

# Step 6: Extract hashtags
print(re.findall(r'#\w+', raw_updated))  # ['#sale', '#discount', '#2025']

# Step 7: Extract email addresses
print(re.findall(r'[\w\-]+@[\w\-\.]+', raw_updated))  # ['support@deals4u.com']

# Step 8: Extract 12-digit numbers (may include invalids)
print(re.findall(r'\d{12}', raw_updated))  # ['919876543210']

# Step 9: Extract Indian phone numbers with country code
print(re.findall(r'\b91\d{10}\b', raw_updated))  # ['919876543210']

# --- Tokenization and Stopword Removal ---
text = "This is a sample sentence, with punctuation!"

# Tokenize using regex (removes punctuation)
tokens = re.findall(r'\b\w+\b', text)
print(tokens)  # ['This', 'is', 'a', 'sample', 'sentence', 'with', 'punctuation']

# Compare with basic split (punctuation remains)
print(text.split())  # ['This', 'is', 'a', 'sample', 'sentence,', 'with', 'punctuation!']

# Download stopwords (only needs to be done once)
nltk.download('stopwords')

# Load English stopwords
stop_words = set(stopwords.words('english'))

# Filter out stopwords from tokens
filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
print(filtered_tokens)  # ['sample', 'sentence', 'punctuation']