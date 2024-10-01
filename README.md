# Grab Food Scraper
A high-performance web scraper built using Python, BeautifulSoup, and threading to collect restaurant details from the Grab Food Delivery platform in Singapore. The project aims to efficiently scrape and save data while minimizing bandwidth usage through JSON and compressed formats.

## 🚀 Features
* <b>Efficient Multi-threading</b>: Implements Python threading to handle multiple requests concurrently, significantly improving scraping speed.
* <b>Comprehensive Data Extraction</b>: Scrapes detailed restaurant information such as name, cuisine, ratings, delivery times, distances, offers, delivery fees, and more.
* <b>Data Optimization</b>: Saves scraped data in a compressed format (gzip-compressed ndjson) to optimize storage and retrieval.
* <b>Configurable Output</b>: Allows easy configuration of output formats (JSON, ndjson) based on specific project needs.

## 🛠 Technologies Used
- Python
- BeautifulSoup for HTML parsing and scraping
- Requests for handling HTTP requests
- Threading for concurrent scraping
- gzip and ndjson for efficient data storage

## 📋 Prerequisites
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


## ⚙️Usage
<h3>Running the Scraper</h4>

  1 . Clone the repository:

```bash
git clone https://github.com/yourusername/grab-food-scraper.git
cd grab-food-scraper
```

  2 . Install dependencies:
```bash
pip install -r requirements.txt
```

  3 . Run the scraper:
```bash
python grab_food_scraper.py
```

<h3>Configuration </h3> 
<li> The script is designed to scrape restaurant data in Singapore.</li>
<li> You can modify the target URL or scraping logic in the code as needed. </li>
<li> By default, the scraped data is saved in a compressed .ndjson.gz format for better performance.</li>


## 📊Output Format

The script outputs a compressed `ndjson.gz` file, which contains restaurant details in the following format:

```bash

{
    "restaurant_name": "Example Restaurant",
    "cuisine": "Italian",
    "rating": 4.5,
    "delivery_time": "25-30 min",
    "distance": "2.5 km",
    "offer": "10% Off",
    "delivery_fee": "$2.50"
}


```

## Example Output

```bash
restaurants_2024.ndjson.gz
```

## 🧩 Future Enhancements
- <b> API Integration</b>: Potential to integrate with Grab's API (if available) for more reliable data access.
- <b> Automated Scheduling</b>: Add a feature to run the scraper periodically to keep data up to date.
- <b> Data Analysis</b>: Use the scraped data for visual analysis (e.g., restaurant trends, delivery patterns).

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any feature additions or improvements.


## Feedback

If you have any feedback, please reach out to me at dakshmakhija@gmail.com

