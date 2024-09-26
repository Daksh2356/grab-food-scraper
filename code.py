import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
import json
import gzip

class WebScraper:
    def __init__(self, url):
        # Initialize the WebScraper class with the provided URL
        self.url = url
        
        # An empty dictionary to store scraped data
        self.data = {
            "Restuarant Name": [],
            "Restaurant Cuisine": [],
            "Restaurant Rating": [],
            "Estimate Delivery Time": [],
            "Restaurant Distance": [],
            "Promotional Offers": [],
            "Restaurant Notice": [],
            "Restaurant Image Link": [],
            "Promo Availability": [],
            "Unique ID": []
        }
        
        # Threading lock to handle concurrent access to shared data
        self.lock = threading.Lock()
        
        # Defining user-agent header for accessing any website for scraping
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
        }
        
        # Define proxy settings (commented out for now)
        # self.username = 'USERNAME'
        # self.password = 'PASSWORD'
        # self.proxies = {
        #     'http': "http://customer-user_name:password@pr.oxylabs.io:7777",
        #     'https': "https://customer-user_name:password@pr.oxylabs.io:7777"
        # }


    def _sanitize_restaurant_name(self, name):
        # Function to sanitize restaurant names by removing emojis and extra spaces
        if "🏍" in name:
            name = name.replace("🏍", "")
        return name.strip()

    def _extract_restaurant_rating(self, rating):
        # Function to extract restaurant ratings, handling cases with 'mins'
        if "mins" in rating:
            rating = "No Rating"
        else:
            rating = rating.split("\u00a0\u00a0\u2022\u00a0\u00a0")[0]
        return rating
    
    def _check_offer(self, promo_container):
        # Function to check if there are promotional offers
        if promo_container:
            return promo_container.get_text()
        return "No Offer"
    
    def _check_notice(self, notice_container):
        # Function to check if there are restaurant notices
        if notice_container:
            return notice_container.get_text()
        return "No Notice"

    def _extract_promo_availability(self, promo_tag):
        # Function to extract promotional availability
        return bool(promo_tag)

    def _extract_data_from_restaurant(self, restaurant):

        # Function to extract data from each restaurant element
        detailsContainer = restaurant.select("div.ant-col-24.colInfo___3iLqj.ant-col-md-24.ant-col-lg-24")
        restro_name = self._sanitize_restaurant_name(detailsContainer[0].find("p").get_text())
        basic_info_container = restaurant.select_one("div.basicInfoContainer___1DcNs")
        restro_cuisine = basic_info_container.find_all("div")[0].get_text()
        ratingContainer = basic_info_container.select_one("div.numbersChild___2qKMV:first-child")
        restro_rating = self._extract_restaurant_rating(ratingContainer.get_text())
        numbers = basic_info_container.select_one("div.numbersChild___2qKMV:last-child")
        delivery_info = numbers.get_text().strip().split("•")
        est_delivery_time = delivery_info[0].strip()
        restro_distance = delivery_info[1].strip()
        promoContainer = restaurant.select_one("div.basicInfoRow___UZM8d.discount___3h-0m")
        offer = self._check_offer(promoContainer)
        noticeContainer = restaurant.select_one("div.closeSoon___1eGf8")
        notice = self._check_notice(noticeContainer)
        topContainer = restaurant.select_one("div.ant-col-24.colPhoto___3vb-o.ant-col-md-24.ant-col-lg-24")
        imageSrc = topContainer.find("img").get("src")
        isPromo = topContainer.select_one("div.promoTagHead___1bjRG")
        isPromo = self._extract_promo_availability(isPromo)
        link_container = restaurant.find("a")
        link = link_container.get("href")
        unique_id = link.split("/")[-1].split("?")[0]
        
        # Make a new HTTP request to fetch the content of the restaurant's page
        # restaurant_page_req = requests.get(url="https://food.grab.com" + link, headers=self.headers, proxies=self.proxies)
        # restaurant_page_soup = BeautifulSoup(restaurant_page_req.content, 'html.parser')

        # Parse the individual restaurant page to extract latitude, longitude, and delivery fee
        # latitude = restaurant_page_soup.find("meta", {"property": "og:latitude"}).get("content")
        # longitude = restaurant_page_soup.find("meta", {"property": "og:longitude"}).get("content")
        # delivery_fee = restaurant_page_soup.find("div", class_="className").text

        return restro_name, restro_cuisine, restro_rating, est_delivery_time, restro_distance, offer, notice, imageSrc, isPromo, unique_id

    def scrape_restaurants(self):
        # Function to scrape restaurant data
        req = requests.get(url=self.url, headers=self.headers  ) 
        # req = requests.get(url=self.url, headers=self.headers, proxies=self.proxies)
        soup = BeautifulSoup(req.content, 'html.parser')
        restaurants = soup.select("div.ant-col-24.RestaurantListCol___1FZ8V.ant-col-md-12.ant-col-lg-6")
        for restaurant in restaurants:
            restro_name, restro_cuisine, restro_rating, est_delivery_time, restro_distance, offer, notice, imageSrc, isPromo, unique_id = self._extract_data_from_restaurant(restaurant)
            self.lock.acquire()     # acquire the lock
            try:  
                self.data["Restuarant Name"].append(restro_name)
                self.data["Restaurant Cuisine"].append(restro_cuisine)
                self.data["Restaurant Rating"].append(restro_rating)
                self.data["Estimate Delivery Time"].append(est_delivery_time)
                self.data["Restaurant Distance"].append(restro_distance)
                self.data["Promotional Offers"].append(offer)
                self.data["Restaurant Notice"].append(notice)
                self.data["Restaurant Image Link"].append(imageSrc)
                self.data["Promo Availability"].append(isPromo)
                self.data["Unique ID"].append(unique_id)
            finally:
                self.lock.release()   # release the lock

    def run(self, num_threads=5):
        # Function to run the scraping process using multiple threads
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=self.scrape_restaurants) # create a new thread
            threads.append(t)  # append the current thread to the list
            t.start()   # start the current thread

        for t in threads:
            t.join()  # join the current thread

    def save_data_to_gzip_ndjson(self, filename):
        # Function to save data to gzip-compressed ndjson file
        with gzip.open(filename, 'wt') as f:    # open the file in write mode
            for item in self.data:  
                json.dump(item, f)  # dump the data to the file
                f.write('\n') 

# Main function to run the web scraper

if __name__ == "__main__":
    # URL for scraping restaurant data
    URL = "https://food.grab.com/sg/en/restaurants" # the url extract information for the above location
    
    # Create an instance of the WebScraper class
    scraper = WebScraper(URL)
    
    # Run the scraping process
    scraper.run()

    # Calculate the length of data stored
    print("Number of records : " , len(scraper.data["Unique ID"]))
    
    # Convert scraped data to DataFrame
    df = pd.DataFrame.from_dict(scraper.data)
    
    # Save scraped data to JSON file
    df.to_json("data.json", orient="records")
    
    # Save scraped data to gzip-compressed ndjson file
    scraper.save_data_to_gzip_ndjson("data.gzip.ndjson")