import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
import numpy as np

# --------------------------------------------------
# 1. Load data
# --------------------------------------------------
df = pd.read_excel("teamscs_blog_content.xlsx")

# --------------------------------------------------
# 2. Convert published_date to datetime
# Example: "October 3, 2024"
# --------------------------------------------------
df["published_date"] = pd.to_datetime(
    df["published_date"],
    errors="coerce"
)

# Drop rows without valid dates (safety)
df = df.dropna(subset=["published_date"])

# --------------------------------------------------
# 3. Vectorize text
# --------------------------------------------------
custom_stop_words = list(
    ENGLISH_STOP_WORDS.union({
        "teamscs",
        "superior",
        "consulting",
        "services",
        "scs",
        "data",
        "use",
        "used",
        "using",
        "based",
        "business",
        "solution",
        "solutions",
        "read"
    })
)

texts = df["content"].fillna("")

vectorizer = TfidfVectorizer(
    stop_words=custom_stop_words,
    max_features=1000
)

X = vectorizer.fit_transform(texts)

# --------------------------------------------------
# 4. Cluster with KMeans
# --------------------------------------------------
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

df["cluster"] = kmeans.labels_

# --------------------------------------------------
# 5. Get cluster names from top keywords
# --------------------------------------------------
terms = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

cluster_names = {}
for i in range(num_clusters):
    top_words = [terms[ind] for ind in order_centroids[i, :3]]
    cluster_names[i] = ", ".join(top_words)

# --------------------------------------------------
# 6. Assign year-month
# --------------------------------------------------
df["year_month"] = df["published_date"].dt.to_period("M")

# --------------------------------------------------
# 7. Count posts per month per cluster
# --------------------------------------------------
counts = (
    df.groupby(["year_month", "cluster"])
      .size()
      .reset_index(name="post_count")
)

# --------------------------------------------------
# 8. Create full month range
# --------------------------------------------------
all_months = pd.period_range(
    df["year_month"].min(),
    df["year_month"].max(),
    freq="M"
)

# --------------------------------------------------
# 9. Build cumulative totals with dominant cluster
# --------------------------------------------------
cumulative = []
running_total = 0

for ym in all_months:
    month_data = counts[counts["year_month"] == ym]
    total_posts = month_data["post_count"].sum()

    if not month_data.empty:
        dominant_cluster = (
            month_data.sort_values("post_count", ascending=False)
            .iloc[0]["cluster"]
        )
    else:
        dominant_cluster = np.nan

    running_total += total_posts
    cumulative.append((ym.to_timestamp(), running_total, dominant_cluster))

cum_df = pd.DataFrame(
    cumulative,
    columns=["date", "cumulative_count", "cluster"]
)

# --------------------------------------------------
# 10. Plot single cumulative line with color segments
# --------------------------------------------------
plt.figure(figsize=(12, 7))

colors = plt.get_cmap("tab10").colors
cluster_color_map = {
    cid: colors[i % len(colors)]
    for i, cid in enumerate(cluster_names)
}

for i in range(1, len(cum_df)):
    c1 = cum_df.iloc[i - 1]
    c2 = cum_df.iloc[i]
    cluster = c2["cluster"]
    color = cluster_color_map.get(cluster, "gray")

    plt.plot(
        [c1["date"], c2["date"]],
        [c1["cumulative_count"], c2["cumulative_count"]],
        color=color,
        linewidth=2
    )

plt.xlabel("Date")
plt.ylabel("Cumulative Blog Posts")
plt.title("TeamSCS Superior Spotlight Blogs – Cumulative Posts by Topic")

# Clean x-axis ticks
tick_indices = np.linspace(0, len(cum_df) - 1, 6, dtype=int)
tick_positions = [cum_df.iloc[i]["date"] for i in tick_indices]
tick_labels = [d.strftime("%b %Y") for d in tick_positions]
plt.xticks(tick_positions, tick_labels, rotation=45)

# Legend
legend_items = [
    Line2D(
        [0], [0],
        color=cluster_color_map[cid],
        lw=3,
        label=cluster_names[cid]
    )
    for cid in cluster_names
]

plt.legend(handles=legend_items, title="Cluster Topics")
plt.grid(True)
plt.tight_layout()

# --------------------------------------------------
# 11. Save outputs
# --------------------------------------------------
chart_file = "teamscs_cumulative_blog_clusters.png"
plt.savefig(chart_file)
plt.close()

output_excel = "teamscs_blog_content_with_clusters.xlsx"

#add cluster names to data frame
df["cluster_name"] = df["cluster"].map(cluster_names)

df.to_excel(output_excel, index=False)

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TeamSCS Blog Topic Timeline</title>
</head>
<body>
    <h1>Cumulative Blog Posts Over Time</h1>
    <p><strong>Line color indicates dominant content topic.</strong></p>
    <img src="{chart_file}" style="max-width:100%; height:auto;">
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Created cumulative cluster timeline")
print(f"   - Chart: {chart_file}")
print("   - HTML: index.html")
