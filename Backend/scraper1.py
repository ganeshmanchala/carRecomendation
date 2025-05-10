# car_scraper.py
import time
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from database import CarDatabase
import datetime

class CarScraper:
    def __init__(self):
        self.db = CarDatabase()
        self.base_url = "https://www.cardekho.com"
        self.endpoints = [
        "https://www.cardekho.com/new-cars+under-5-lakh",
        "https://www.cardekho.com/new-cars+under-10-lakh",
        "https://www.cardekho.com/new-cars+10-lakh-15-lakh",
        "https://www.cardekho.com/new-cars+15-lakh-20-lakh",
        "https://www.cardekho.com/new-cars+20-lakh-35-lakh",
        "https://www.cardekho.com/new-cars+35-lakh-50-lakh",
        "https://www.cardekho.com/new-cars+50-lakh-1-crore",
        "https://www.cardekho.com/new-cars+above-1-crore"
        ]
        self.headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/112.0.0.0 Safari/537.36")
        }
    
    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=chrome_options)

    def load_full_page(self, url):
        driver = self.init_driver()
        driver.get(url)
        time.sleep(3)  # Initial load
        no_change_count = 0
        max_no_change = 6
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while no_change_count < max_no_change:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                no_change_count += 1
            else:
                no_change_count = 0
            last_height = new_height
        html = driver.page_source
        driver.quit()
        return html

    def get_variant_urls_from_card(self,card):
        """
        From a car card element, extract specs page hrefs from the
        "Variant Matching Your Search Criteria" and "Other Variants" sections.
        Construct the full URL as follows:
          - If href starts with "/overview": base_url + href + "#specification"
          - Otherwise: base_url + href (if it starts with a slash) or as is.
        """
        urls = []
        for cls in ["expandcollapse matching clear", "expandcollapse other clear"]:
            section = card.find("div", class_=cls)
            if section:
                ul = section.find("ul", class_="gsc_thin_scroll")
                if ul:
                    for li in ul.find_all("li"):
                        a_tag = li.find("a")
                        if a_tag:
                            href = a_tag.get("href")
                            if href:
                                if href.startswith("/overview"):
                                    full_url = self.base_url + href + "#specification"
                                else:
                                    full_url = self.base_url + href if href.startswith("/") else href
                                urls.append(full_url)
        return urls

    def scrape_results_page(self,url):
        """
        Load the listing page using Selenium (via load_full_page) and extract specs page URLs.
        """
        full_html = self.load_full_page(url)
        soup = BeautifulSoup(full_html, 'html.parser')
        variant_urls = []
        cards = soup.find_all("div", class_="gsc_col-md-12 gsc_col-sm-12 gsc_col-xs-12 append_list")
        print(f"Found {len(cards)} car cards on endpoint: {url}")
        for card in cards:
            urls = self.get_variant_urls_from_card(card)
            variant_urls.extend(urls)
        return list(set(variant_urls))

    @staticmethod
    def parse_table(table):
        """
        Extract key-value pairs from a table element.
        If the value cell contains an <i> tag:
          - If class contains 'icon-check', set value to "Yes"
          - If class contains 'icon-deletearrow', set value to "No"
        Otherwise, use the text in the cell.
        """
        data = {}
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value_cell = cols[1]
                i_tag = value_cell.find("i")
                if i_tag:
                    classes = i_tag.get("class", [])
                    if "icon-check" in classes:
                        value = "Yes"
                    elif "icon-deletearrow" in classes:
                        value = "No"
                    else:
                        value = value_cell.get_text(strip=True)
                else:
                    value = value_cell.get_text(strip=True)
                data[key] = value
        return data

    def parse_spec_page(self,spec_url):
   
        print(f"Fetching spec page: {spec_url}")
        try:
            res = requests.get(spec_url, headers=self.headers)
            if res.status_code != 200:
                print(f"Failed to fetch specs page: {spec_url} (Status: {res.status_code})")
                return {}
            soup = BeautifulSoup(res.text, "html.parser")
            specs = {}

            # Extract image from the standard container if available
            model_img_div = soup.find("div", class_="modelTopImg")
            if model_img_div:
                img_tag = model_img_div.find("img")
                if img_tag and img_tag.get("src"):
                    specs["Image"] = img_tag.get("src")
            
            # New gallery-based image extraction if the standard image is missing
            if "Image" not in specs:
                # Attempt to find gallery section with data-track-section="gallery"
                gallery_section = soup.find("div", attrs={"data-track-section": "gallery"})
                if gallery_section:
                    # First try to find a ul with data-carousel="OverviewTop"
                    overview_ul = gallery_section.find("ul", attrs={"data-carousel": "OverviewTop"})
                    if not overview_ul:
                        # Fallback: look for a ul with data-carousel="gallery"
                        overview_ul = gallery_section.find("ul", attrs={"data-carousel": "gallery"})
                    if overview_ul:
                        # Find the first li with data-track-section="image"
                        first_li = overview_ul.find("li", attrs={"data-track-section": "image"})
                        if first_li:
                            img_tag = first_li.find("img")
                            if img_tag and img_tag.get("src"):
                                specs["Image"] = img_tag.get("src")

            quick_overview = soup.find("section", class_="quickOverviewNew")
            if quick_overview:
                # Sometimes overviewdetail may be missing in quickOverview pages, so try to capture model info from <h2>
                h2 = quick_overview.find("h2")
                if h2 and "overview" in h2.get_text(strip=True).lower():
                    specs["Overview Title"] = h2.get_text(strip=True)
                # Extract Key Specifications
                key_specs_section = quick_overview.find("div", attrs={"data-track-section": "Key Specifications"})
                if key_specs_section:
                    # Look inside qccontent first
                    qc = key_specs_section.find("div", class_="qccontent")
                    if qc:
                        table = qc.find("table")
                    else:
                        table = key_specs_section.find("table")
                    if table:
                        specs["Key Specifications"] = self.parse_table(table)
                # Extract Top Features
                top_features_section = quick_overview.find("div", attrs={"data-track-section": "Top Features"})
                if top_features_section:
                    qc = top_features_section.find("div", class_="qccontent")
                    if qc:
                        ul = qc.find("ul")
                    else:
                        ul = top_features_section.find("ul")
                    if ul:
                        features = [li.get_text(strip=True) for li in ul.find_all("li")]
                        specs["Top Features"] = {"Features": ", ".join(features)}

            # Extract overview detail block data (if available)
            overview_detail = soup.find("div", class_="overviewdetail")
            if overview_detail:
                h1 = overview_detail.find("h1", class_="displayInlineBlock")
                if h1:
                    specs["Model"] = h1.get_text(strip=True)
                start_rating = overview_detail.find("div", class_="startRating")
                if start_rating:
                    rating_span = start_rating.find("span", class_="ratingStarNew")
                    if rating_span:
                        specs["Rating"] = rating_span.get_text(strip=True)
                    reviews_span = start_rating.find("span", class_="reviews")
                    if reviews_span:
                        specs["Reviews"] = reviews_span.get_text(strip=True)
                price_div = soup.find("div", class_="price")
                if price_div:
                    price_text = ' '.join(price_div.get_text().split())
                    match = re.search(r"Rs\.\s*([\d,\.]+\s*\w+)", price_text)
                    if match:
                        specs["Price"] = match.group(1).strip()

            # Extract specs from scrollDiv section if available
            scroll_div = soup.find("div", id="scrollDiv")
            if scroll_div:
                for header in scroll_div.find_all("h3"):
                    section_title = header.get_text(strip=True)
                    table = header.find_next("table")
                    if table:
                        specs[section_title] = self.parse_table(table)

            # Process quickOverviewNew section if available (this captures the missed structure)
            # Fallback: if no overview or scrollDiv found, try any table with class "keyfeature"
            if "Key Specifications" not in specs:
                table = soup.find("table", class_="keyfeature")
                if table:
                    specs["Key Specifications"] = self.parse_table(table)

            # --- Additional extraction: Look for any <div class="qccontent"> blocks not already captured.
            additional_count = 1
            for qc in soup.find_all("div", class_="qccontent"):
                # If this qccontent block contains a table and its parent section is not already handled, add it.
                table = qc.find("table")
                if table:
                    key_name = f"Additional Specs {additional_count}"
                    # Only add if this key is not already present
                    if key_name not in specs:
                        specs[key_name] = self.parse_table(table)
                        additional_count += 1

            return specs
        except Exception as e:
            print("Error in parse_spec_page:", e)
            return {}

    def extract_car_data(self, specs, spec_url):
        if not specs:
            return None
        base_specs = {
            'price': specs.get('Price'),
            'model': specs.get('Model', 'Unknown Model'),
            'transmission': specs.get('Key Specifications_Transmission'),
            'seating': self.extract_seating(specs),
            'safety_rating': self.extract_safety_rating(specs)
        }
        category = 'ev' if self.is_electric(specs) else 'fuel'
        media = {'image': specs.get('Image', '')}
        car_data = {
            'specs': specs,
            'media': media,
            'category': category,
            'base_specs': {k: v for k, v in base_specs.items() if v is not None},
            'spec_url': spec_url
        }
        if category == 'ev':
            car_data['ev_specific'] = {
                'battery': specs.get('Key Specifications_Battery Capacity'),
                'range': specs.get('Key Specifications_Range')
            }
        else:
            car_data['fuel_specific'] = {
                'engine': specs.get('Key Specifications_Engine'),
                'mileage': specs.get('Key Specifications_Mileage')
            }
        return car_data

    def extract_seating(self, specs):
        seating_str = specs.get('Key Specifications_Seating Capacity', '')
        match = re.search(r'\d+', seating_str)
        return int(match.group()) if match else None

    def extract_safety_rating(self, specs):
        for section_name, section in specs.items():
            if isinstance(section, dict):
                for key, value in section.items():
                    if 'Global NCAP' in key:
                        match = re.search(r'\d+\.?\d*', str(value))
                        return float(match.group()) if match else None
        return None

    def is_electric(self, specs):
        fuel_type = specs.get('Key Specifications_Fuel Type', '').lower()
        return 'electric' in fuel_type

    def process_endpoint(self, endpoint):
        print(f"\nProcessing endpoint: {endpoint}")
        variant_urls = self.scrape_results_page(endpoint)  # Corrected line
        print(f"Found {len(variant_urls)} specs page URLs.")
        for spec_url in variant_urls:
            specs = self.parse_spec_page(spec_url)
            if not specs:
                continue
            car_data = self.extract_car_data(specs, spec_url)
            if not car_data:
                continue
            # Prepare document
            # print(specs)
            document = {
                'spec_url': spec_url,
                'price_endpoint': endpoint,
                'specs': car_data['specs'],
                'media': car_data['media'],
                'category': car_data['category'],
                'base_specs': car_data['base_specs'],
                'ev_specific': car_data.get('ev_specific'),
                'fuel_specific': car_data.get('fuel_specific'),
                'last_updated': datetime.datetime.now()
            }
            # Upsert into MongoDB
            self.db.collection.update_one(
                {"spec_url": spec_url},
                {"$set": document},
                upsert=True
            )
            time.sleep(1)  # Polite delay# Polite delay

    def run(self):
        for endpoint in self.endpoints:
            try:
                self.process_endpoint(endpoint)
                time.sleep(2)
            except Exception as e:
                print(f"Error processing {endpoint}: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.client.close()

if __name__ == "__main__":
    with CarScraper() as scraper:
        scraper.run()