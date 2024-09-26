# Grab Food Scraper
A high-performance web scraper built using Python, BeautifulSoup, and threading to collect restaurant details from the Grab Food Delivery platform in Singapore. The project aims to efficiently scrape and save data while minimizing bandwidth usage through JSON and compressed formats.

# 🚀 Features
* <b>Efficient Multi-threading</b>: Implements Python threading to handle multiple requests concurrently, significantly improving scraping speed.
* <b>Comprehensive Data Extraction</b>: Scrapes detailed restaurant information such as name, cuisine, ratings, delivery times, distances, offers, delivery fees, and more.
* <b>Data Optimization</b>: Saves scraped data in a compressed format (gzip-compressed ndjson) to optimize storage and retrieval.
* <b>Configurable Output</b>: Allows easy configuration of output formats (JSON, ndjson) based on specific project needs.
  
# 📋 Prerequisites
Before running the project, ensure you have the following installed:
*   <b> Python 3.x </b>
*   <b> BeautifulSoup for web scraping </b>
*   <b> Requests for HTTP requests </b>
*   <b> lxml for HTML/XML parsing </b>
  
## Installation

Run the following commands to install dependencies:

```bash
pip install beautifulsoup4 requests lxml

```
