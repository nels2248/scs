import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://www.teamscs.com/superior-spotlight-blogs"

article_links = []

# Loop through pages 1 to 4
for page in range(1, 5):
    if page == 1:
        url = base_url
    else:
        url = f"{base_url}/page/{page}"

    print(f"Scraping: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error on page {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Find blog post containers
    posts = soup.find_all("div", class_="post-content")

    for post in posts:
        a_tag = post.find("a", href=True)
        if a_tag:
            href = a_tag["href"]

            # Safety check to ensure we're only grabbing blog posts
            if "/superior-spotlight-blogs/" in href:
                article_links.append(href)

    time.sleep(1)  # respectful delay

# Remove duplicates & sort
unique_links = sorted(set(article_links))

# Convert to DataFrame
df = pd.DataFrame(unique_links, columns=["Article Link"])

# Save to Excel
output_file = "teamscs_superior_spotlight_blog_links.xlsx"
df.to_excel(output_file, index=False)

print(f"\n✅ Saved {len(unique_links)} article links to '{output_file}'")
