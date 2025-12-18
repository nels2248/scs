# Scrape of Castlelake Article Posts To Display Blogs into 5 Groups by 2 Common Keywords

## Overview
This project scapes the Superior Consulting Services Blog Postings and groups them into 5 categories by the 3 most common words.  It then displays a line chart of the cumulative posts over time.  
This contains 4 Python scripts, each designed to handle a different data processing or analysis task. The outputs from these scripts are consolidated and written to an `index.html` file, providing a simple web-based display of the results.

## File Descriptions

- **1_scrape_blog_links.py** — This goes to https://www.teamscs.com/superior-spotlight-blogs and srapes all of the article links.  Uses python beautiful soup package and saves to excel file.  
- **2_save_html_pages.py** — This reads each specific blog post and saves the .html file in local path.  Did this for quicker processing while developing.
- **3_read_html_pages_save_ext_date_published.py** — Scrapes the locallly saved .html files and pulls the text out of them them and saves into a new excel.  As with step 3, did this for faster processing during development.  
- **4_single_line_cluster_over_time.py** — Uses Sklearn to group each blog post into 5 different categories

## Output
- The final output of running these scripts is saved to an `index.html` file located in the project root directory.
- This HTML file can be opened in any browser to view the processed results.

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. (Optional) Set up a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the scripts:
    ```bash
    python 1_scrape_blog_links.py
    python 2_save_html_pages.py
    python 3_read_html_pages_save_ext_date_published.py
    python 4_single_line_cluster_over_time.py
    ```

4. Open `index.html` in your browser to view the results.

## Notes
- Python version: >=3.11 recommended

## Final Output
Here is the ouptput as .png file if you don't want to open the .html that was also created
![Cumulative Line Chart](single_colored_cumulative_line.png)

## Findings/Analysis
Based upon the chart above and data found here are is what I found:
1. 68 Total Article Posts from Janurary of 2011 to December of 2025
2. 2021 and 2022 saw an emergence of items related to backups and isnurance
3. Although the first blog was posted in 2011, not many article were posted until 2021
4. Fabric and Azure saw emergence in late 2023