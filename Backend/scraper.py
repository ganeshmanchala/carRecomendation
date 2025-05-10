# car_scraper.py
import time
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from database import CarDatabase

# --- Helper functions for full spec extraction ---
def parse_table(table):
    """Extract key-value pairs from a table element."""
    data = {}
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            data[key] = value
    return data

def parse_full_specifications(soup):
    """
    Extract complete specifications by parsing key tables and sections.
    Returns a dictionary with various sections (e.g., Key Specifications, Top Features).
    """
    specs = {}
    # Try to extract tables with class "keyfeature"
    tables = soup.find_all("table", class_="keyfeature")
    if tables:
        for idx, table in enumerate(tables):
            parent = table.find_parent("div", attrs={"data-track-section": True})
            section_name = parent.get("data-track-section") if parent else f"Table_{idx+1}"
            specs[section_name] = parse_table(table)
    else:
        # Fallback to overview section
        overview_section = soup.find("section", class_="quickOverviewNew")
        if overview_section:
            key_specs_div = overview_section.find("div", attrs={"data-track-section": "Key Specifications"})
            if key_specs_div:
                table = key_specs_div.find("table")
                if table:
                    specs["Key Specifications"] = parse_table(table)
            top_features_div = overview_section.find("div", attrs={"data-track-section": "Top Features"})
            if top_features_div:
                ul = top_features_div.find("ul")
                if ul:
                    features = [li.get_text(strip=True) for li in ul.find_all("li")]
                    specs["Top Features"] = {"Features": ", ".join(features)}
        else:
            container = soup.find("div", class_="gsc_container")
            if container:
                model_img_div = container.find("div", class_="modelTopImg")
                if model_img_div:
                    img_tag = model_img_div.find("img")
                    if img_tag and img_tag.get("src"):
                        specs["Image"] = img_tag.get("src")
                price_div = container.find("div", class_="price")
                if price_div:
                    full_price_text = price_div.get_text(" ", strip=True)
                    match = re.search(r"Rs\.\s*([\d,\.]+\s*\w+)", full_price_text)
                    if match:
                        specs["Price"] = match.group(1).strip()
    if "Price" not in specs:
        price_div = soup.find("div", class_="price")
        if price_div:
            full_price_text = price_div.get_text(" ", strip=True)
            match = re.search(r"Rs\.\s*([\d,\.]+\s*\w+)", full_price_text)
            if match:
                specs["Price"] = match.group(1).strip()
    features_div = soup.find("div", class_="featuresIocnsSec")
    if features_div:
        feature_table = features_div.find("table", class_="keyfeature")
        if feature_table:
            specs["Feature Icons"] = parse_table(feature_table)
    return specs
# --- End of helper functions ---

class CarScraper:
    def __init__(self):
        self.db = CarDatabase()
        self.base_url = "https://www.cardekho.com"
        self.endpoints = [
            "https://www.marutisuzuki.com/celerio",
            "https://www.marutisuzuki.com/",
            "https://www.toyotabharat.com/",
            "https://www.hondacarindia.com/",
            "https://auto.mahindra.com/",
            "https://cars.tatamotors.com/",
            "https://www.bmw.in/en-in/sl/stocklocator#/results?filters=is_installment=%27true%27",
            "https://www.audi.in/en/",
            "https://www.hyundai.com/in/en",
            
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
        time.sleep(3)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        html = driver.page_source
        driver.quit()
        return html

    def parse_spec_page(self, spec_url):
        try:
            res = requests.get(spec_url, headers=self.headers)
            if res.status_code != 200:
                print(f"Failed to fetch specs page: {spec_url} (Status: {res.status_code})")
                return None
            soup = BeautifulSoup(res.text, "html.parser")
            return self.extract_car_data(soup, spec_url)
        except Exception as e:
            print(f"Error parsing {spec_url}: {str(e)}")
            return None

    def extract_car_data(self, soup, spec_url):
        # Get complete specifications from all key sections
        full_specs = parse_full_specifications(soup)
        car_data = {
            'specs': full_specs,         # Complete specifications as a dict
            'media': self.get_media(soup),
            'category': 'ev' if self.is_electric(soup) else 'fuel',
            'spec_url': spec_url,
            'raw_data': {}               # Optionally store raw HTML if needed
        }
        # Also extract key base specifications for easier queries
        base = {
            'img'
            'price': self.extract_price(soup),
            'model': self.extract_model(soup),
            'transmission': self.extract_transmission(soup),
            'seating': self.extract_seating(soup),
            'safety_rating': self.extract_safety_rating(soup)
            
        }
        car_data['base_specs'] = {k: v for k, v in base.items() if v is not None}
        if car_data['category'] == 'ev':
            ev_spec = {
                'battery': self.extract_battery_info(soup),
                'range': self.extract_range_info(soup)
            }
            car_data['ev_specific'] = {k: v for k, v in ev_spec.items() if v is not None}
        else:
            fuel_spec = {
                'engine': self.extract_engine_info(soup),
                'mileage': self.extract_mileage(soup)
            }
            car_data['fuel_specific'] = {k: v for k, v in fuel_spec.items() if v is not None}
        return car_data
    
    def extract_price(self, soup):
        price_div = soup.find("div", class_="price")
        if price_div:
            match = re.search(r"Rs\.\s*([\d,\.]+)", price_div.get_text())
            return float(match.group(1).replace(',', '')) if match else None
        return None

    def extract_model(self, soup):
        h1 = soup.find("h1", class_="heading")
        return h1.get_text(strip=True) if h1 else "Unknown Model"

    def extract_transmission(self, soup):
        td = soup.find("td", string=re.compile(r"Transmission", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            return next_td.get_text(strip=True) if next_td else None
        return None

    def extract_seating(self, soup):
        td = soup.find("td", string=re.compile(r"Seating Capacity", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            try:
                return int(re.search(r"(\d+)", next_td.get_text()).group(1))
            except:
                return None
        return None

    def extract_safety_rating(self, soup):
        td = soup.find("td", string=re.compile(r"Global NCAP", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            if next_td:
                text = next_td.get_text(strip=True)
                try:
                    return float(re.search(r"(\d+)", text).group(1))
                except:
                    return None
        return None

    def get_media(self, soup):
        media = {}
        img_div = soup.find("div", class_="modelTopImg")
        if img_div:
            img = img_div.find("img")
            if img and (src := img.get("src") or img.get("data-src")):
                media['image'] = urljoin(self.base_url, src)
        return media

    def is_electric(self, soup):
        fuel_td = soup.find("td", string=re.compile("Fuel Type", re.I))
        if fuel_td:
            next_td = fuel_td.find_next_sibling("td")
            if next_td and "electric" in next_td.get_text().lower():
                return True
        return False

    def extract_battery_info(self, soup):
        td = soup.find("td", string=re.compile(r"Battery Capacity", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            return next_td.get_text(strip=True) if next_td else None
        return None

    def extract_range_info(self, soup):
        td = soup.find("td", string=re.compile(r"Range", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            return next_td.get_text(strip=True) if next_td else None
        return None

    def extract_engine_info(self, soup):
        td = soup.find("td", string=re.compile(r"Displacement", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            return next_td.get_text(strip=True) if next_td else None
        return None

    def extract_mileage(self, soup):
        td = soup.find("td", string=re.compile(r"Mileage", re.I))
        if td:
            next_td = td.find_next_sibling("td")
            if next_td:
                try:
                    return float(re.search(r"(\d+\.?\d*)", next_td.get_text()).group(1))
                except:
                    return None
        return None

    def process_endpoint(self, endpoint):
        html = self.load_full_page(endpoint)
        soup = BeautifulSoup(html, "html.parser")
        # Try to select car cards from one of the known selectors
        car_cards = soup.select("section.card.card_new.shadowWPadding.overviewTop") or soup.select("div.append_list section")
        for card in car_cards:
            h3 = card.find("h3")
            car_name = h3.get_text(strip=True) if h3 else "Unknown"
            img_tag = card.find("img")
            image_url = None
            if img_tag:
                src = img_tag.get("src") or img_tag.get("data-src")
                if src:
                    image_url = urljoin(self.base_url, src)
            spec_link = card.select_one("a[href*='spec']")
            spec_url = urljoin(self.base_url, spec_link["href"]) if spec_link else None
            main_specs = self.parse_spec_page(spec_url) if spec_url else {}
            merged_image = main_specs.get("Image", image_url)
            self.db.collection.update_one(
                {"spec_url": spec_url},
                {"$set": {
                    "name": car_name,
                    "image_url": merged_image,
                    "spec_url": spec_url,
                    "specs": main_specs,
                    "price_endpoint": endpoint,
                    "last_updated": None
                }},
                upsert=True
            )
            # Process variants from matching and other sections
            for variant_type in ["matching", "other"]:
                section = card.find("div", class_=f"expandcollapse {variant_type} clear")
                if section:
                    for link in section.find_all("a"):
                        variant_name = link.get_text(strip=True)
                        variant_path = link.get("href")
                        if not variant_path:
                            continue
                        variant_url = urljoin(self.base_url, variant_path)
                        variant_specs = self.parse_spec_page(variant_url)
                        if not variant_specs:
                            continue
                        merged_specs = {**main_specs, **variant_specs}
                        variant_image = merged_specs.get("Image", image_url)
                        self.db.collection.update_one(
                            {"spec_url": variant_url},
                            {"$set": {
                                "name": variant_name,
                                "image_url": variant_image,
                                "spec_url": variant_url,
                                "specs": merged_specs,
                                "price_endpoint": endpoint,
                                "last_updated": None
                            }},
                            upsert=True
                        )
                        time.sleep(1)

    def run(self):
        for endpoint in self.endpoints:
            print(f"Processing {endpoint}")
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
