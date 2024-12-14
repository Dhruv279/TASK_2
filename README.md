
# Web Scraper

This project allows users to crawl a website, extract internal URLs, and scrape metadata (title and meta description) from each page. It provides a simple user interface using **Streamlit** to input the website URL and control the crawling and scraping process.

## Features:
- Crawl a website to extract internal URLs.
- Scrape metadata (title and meta description) from each page.
- Display the scraped data in a table format.
- Allow users to download the scraped data as a CSV file.

## Requirements:
1. **Python 3.7+**
2. **Dependencies**:
   - Streamlit
   - Requests
   - BeautifulSoup4
   - Pandas

## Install Dependencies:

To install the required dependencies, run:

```bash
pip install streamlit requests beautifulsoup4 pandas
```

## Run the Application:

To run the application, use the following command:

```bash
streamlit run app.py
```

This will open the web application in your default browser. Here, you can:

- Enter the website URL you wish to crawl.
- Specify the maximum number of pages to crawl.
- Click the "Start Crawling and Scraping" button to begin the process.

The application will crawl the website, extract internal URLs, scrape metadata (title and meta description) from each page, and display the results in a table. You can download the scraped data as a CSV file by clicking the "Download CSV" button.


