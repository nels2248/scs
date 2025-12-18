import os
import pandas as pd
from bs4 import BeautifulSoup

# Folder where HTML files are stored
html_dir = "teamscs_blog_html"

# Lists to store data
titles = []
dates = []
contents = []
filenames = []

# Loop through each HTML file
for filename in os.listdir(html_dir):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(html_dir, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # -------------------------
        # Title
        # -------------------------
        title_tag = soup.find("h1", class_="heading")
        title_text = title_tag.get_text(strip=True) if title_tag else ""

        # -------------------------
        # Published Date
        # (h6 directly under title)
        # -------------------------
        date_text = ""
        if title_tag:
            date_tag = title_tag.find_next("h6")
            date_text = date_tag.get_text(strip=True) if date_tag else ""

        # -------------------------
        # Blog Content
        # -------------------------
        content_div = soup.find("div", class_="blog-content")
        content_text = (
            content_div.get_text(separator="\n", strip=True)
            if content_div else ""
        )

        titles.append(title_text)
        dates.append(date_text)
        contents.append(content_text)
        filenames.append(filename)

# Create DataFrame
df = pd.DataFrame({
    "filename": filenames,
    "title": titles,
    "published_date": dates,
    "content": contents
})

# Save to Excel
output_file = "teamscs_blog_content.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Extracted {len(df)} blog posts into '{output_file}'")
