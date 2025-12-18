import pandas as pd
import requests
import os
import re
from urllib.parse import urlparse

# Load the Excel file
df = pd.read_excel("teamscs_superior_spotlight_blog_links.xlsx")

# Output directory for HTML files
output_dir = "teamscs_blog_html"
os.makedirs(output_dir, exist_ok=True)

def slugify(url):
    """
    Converts a blog URL into a safe filename.
    Example:
    https://www.teamscs.com/superior-spotlight-blogs/power-bi-and-generative-ai
    → power-bi-and-generative-ai.html
    """
    parsed = urlparse(url)
    slug = parsed.path.rstrip("/").split("/")[-1]
    return re.sub(r'[^a-zA-Z0-9_-]', '', slug) + ".html"

# Loop through each URL
for i, row in df.iterrows():
    full_url = row["Article Link"]

    filename = slugify(full_url)
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading: {full_url} → {filename}")

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)

    except Exception as e:
        print(f"❌ Failed to download {full_url}: {e}")

print("\n✅ Finished downloading all blog HTML pages.")
