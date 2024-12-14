import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse

def get_internal_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc: 
            links.add(full_url.split('#')[0])  
    return links

def crawl_website(base_url, max_pages=50):
    visited = set()
    to_visit = set([base_url])
    all_links = set()

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url not in visited:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                visited.add(url)
                new_links = get_internal_links(base_url, response.text)
                to_visit.update(new_links - visited)
                all_links.update(new_links)
            except requests.exceptions.RequestException:
                pass  
    return list(all_links)

def scrape_page_metadata(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string.strip() if soup.title else "N/A"
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'].strip() if meta_description else "N/A"

        if title == "N/A" or description == "N/A":
            h1_tag = soup.find('h1')
            h1_text = h1_tag.text.strip() if h1_tag else "N/A"

            first_paragraph = soup.find('p')
            paragraph_text = first_paragraph.text.strip() if first_paragraph else "N/A"
            
            if title == "N/A":
                title = f"H1: {h1_text}" if h1_text != "N/A" else "No Title Available"
            if description == "N/A":
                description = f"Paragraph: {paragraph_text}" if paragraph_text != "N/A" else "No Description Available"
        
        return {'URL': url, 'Title': title, 'Meta Description': description}
    
    except requests.exceptions.RequestException:
        return None  
    except Exception:
        return None  

st.title("Website Crawler and Scraper")
st.write("Enter a website URL to crawl pages and scrape metadata (title and meta description).")

website_url = st.text_input("Website URL", placeholder="https://example.com")
max_pages = st.number_input("Max Pages to Crawl", min_value=1, max_value=500, value=50)

if st.button("Start Crawling and Scraping"):
    if not website_url:
        st.error("Please enter a website URL.")
    else:
        with st.spinner("Crawling the website for internal links..."):
            discovered_urls = crawl_website(website_url, max_pages)
        
        if discovered_urls:
            st.success(f"Discovered {len(discovered_urls)} URLs.")
            scraped_data = []
            with st.spinner("Scraping metadata from each URL..."):
                for url in discovered_urls:
                    result = scrape_page_metadata(url)
                    if result: 
                        scraped_data.append(result)
            
            if scraped_data:
                df = pd.DataFrame(scraped_data)
                st.dataframe(df)
                
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="scraped_data.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No accessible pages found on the provided website.")
        else:
            st.warning("No links found on the provided website.")
