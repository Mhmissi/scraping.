#!/usr/bin/env python3
"""
Google Maps Direct Scraper for Tunisia Businesses
Scrapes directly from Google Maps to get HUNDREDS of real results
"""

import pandas as pd
import time
import json
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import re
from urllib.parse import quote


class GoogleMapsScraper:
    """Direct Google Maps scraper for maximum results"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        
        # Tunisian cities with coordinates
        self.tunisia_cities = {
            'Tunis': (36.8065, 10.1815),
            'Sfax': (34.7406, 10.7603),
            'Sousse': (35.8256, 10.6411),
            'Kairouan': (35.6781, 10.0963),
            'Bizerte': (37.2744, 9.8739),
            'Gabès': (33.8881, 10.0972),
            'Ariana': (36.8601, 10.1931),
            'Ben Arous': (36.7531, 10.2189),
            'Manouba': (36.8081, 10.0972),
            'Nabeul': (36.4561, 10.7376),
            'Monastir': (35.7781, 10.8262),
            'Mahdia': (35.5047, 11.0442),
            'Kasserine': (35.1678, 8.8361),
            'Sidi Bouzid': (35.0381, 9.4847),
            'Kef': (36.1822, 8.7147),
            'Jendouba': (36.5011, 8.7803),
            'Beja': (36.7256, 9.1814),
            'Siliana': (36.0831, 9.3708),
            'Zaghouan': (36.4019, 10.1428),
            'Medenine': (33.3547, 10.5053),
            'Tataouine': (32.9297, 10.4517),
            'Gafsa': (34.4256, 8.7842),
            'Tozeur': (33.9197, 8.1336),
            'Kebili': (33.7042, 8.9694)
        }
        
        # Business search terms in multiple languages
        self.business_terms = {
            'doctors': [
                # General Medical Practitioners
                'médecin', 'médecin généraliste', 'cabinet médical', 'docteur', 
                'consultation médicale', 'médecin de famille', 'doctors', 'طبيب', 'طبيبة',
                
                # Specialized Doctors
                'cardiologue', 'dermatologue', 'gynécologue', 'pédiatre', 
                'ophtalmologue', 'orthopédiste', 'ORL', 'oto-rhino-laryngologiste',
                'neurologue', 'psychiatre', 'endocrinologue', 'urologue', 'radiologue',
                
                # Clinics & Health Centers
                'clinique privée', 'centre médical', 'centre de santé', 'polyclinique',
                'centre hospitalier', 'hôpital privé', 'hospital', 'hôpital', 'مستشفى',
                'clinic', 'clinique', 'عيادة', 'medical center', 'مركز طبي',
                
                # Dentists & Oral Care
                'dentiste', 'orthodontiste', 'stomatologue', 'cabinet dentaire',
                
                # Optical & Vision
                'opticien', 'ophtalmologie', 'centre optique',
                
                # Pharmacy & Paramedical
                'pharmacie', 'parapharmacie', 'laboratoire d\'analyses médicales',
                'centre de radiologie', 'kinésithérapeute', 'ostéopathe', 'psychologue',
                'infirmier cabinet', 'infirmier', 'sage-femme',
                
                # Additional terms
                'health', 'santé', 'صحة', 'médecine', 'طب'
            ],
            'jewelry': [
                'jewelry', 'bijouterie', 'مجوهرات', 'jeweler', 'bijoutier', 'صائغ',
                'gold', 'or', 'ذهب', 'silver', 'argent', 'فضة', 'diamonds', 'diamants', 'ألماس'
            ],
            'lawyers': [
                'lawyer', 'avocat', 'محامي', 'attorney', 'legal', 'juridique', 'قانوني',
                'court', 'tribunal', 'محكمة', 'notary', 'notaire', 'كاتب عدل'
            ]
        }
    
    def setup_driver(self):
        """Setup Chrome driver with proper options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Chrome driver setup failed: {e}")
            print("Please install Chrome and ChromeDriver")
            return False
    
    def search_google_maps(self, city: str, business_type: str) -> List[Dict]:
        """Search Google Maps for businesses in a specific city"""
        if not self.driver:
            if not self.setup_driver():
                return []
        
        businesses = []
        search_terms = self.business_terms.get(business_type, [])
        
        print(f"🗺️  Searching Google Maps for {business_type} in {city}")
        print(f"Using {len(search_terms)} different search terms...")
        
        for i, search_term in enumerate(search_terms[:15]):  # Limit to 15 searches per type
            print(f"  {i+1}/15: '{search_term}'")
            
            try:
                # Search on Google Maps
                search_query = f"{search_term} in {city}, Tunisia"
                self.driver.get(f"https://www.google.com/maps/search/{quote(search_query)}")
                
                # Wait for results to load
                time.sleep(3)
                
                # Scroll to load more results
                self._scroll_to_load_more()
                
                # Extract business information
                business_elements = self._extract_business_elements()
                
                for element in business_elements:
                    business = self._extract_business_info(element, business_type, city)
                    if business:
                        businesses.append(business)
                
                print(f"    ✅ Found {len(business_elements)} elements")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"    ❌ Error with '{search_term}': {e}")
                continue
        
        # Remove duplicates
        unique_businesses = self._remove_duplicates(businesses)
        print(f"✅ Total unique {business_type}: {len(unique_businesses)}")
        
        return unique_businesses
    
    def _scroll_to_load_more(self):
        """Scroll to load more results on Google Maps"""
        try:
            # Find the results panel
            results_panel = self.driver.find_element(By.CSS_SELECTOR, '[role="main"]')
            
            # Scroll down multiple times to load more results
            for _ in range(5):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                time.sleep(2)
                
                # Check if "Show more results" button exists and click it
                try:
                    show_more_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Show more results') or contains(text(), 'Afficher plus de résultats')]")
                    if show_more_button.is_displayed():
                        show_more_button.click()
                        time.sleep(2)
                except:
                    pass
                    
        except Exception as e:
            print(f"    ⚠️  Scroll error: {e}")
    
    def _extract_business_elements(self) -> List:
        """Extract business elements from the page"""
        try:
            # Multiple selectors to catch different result formats
            selectors = [
                '[data-result-index]',
                '[jsaction*="pane.resultSection.click"]',
                '.Nv2PK',
                '.THOPZb',
                '.lI9IFe'
            ]
            
            elements = []
            for selector in selectors:
                try:
                    found_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    elements.extend(found_elements)
                except:
                    continue
            
            # Remove duplicates
            unique_elements = []
            seen = set()
            for element in elements:
                try:
                    element_id = element.get_attribute('data-result-index') or str(element.location)
                    if element_id not in seen:
                        seen.add(element_id)
                        unique_elements.append(element)
                except:
                    continue
            
            return unique_elements
            
        except Exception as e:
            print(f"    ❌ Element extraction error: {e}")
            return []
    
    def _extract_business_info(self, element, business_type: str, city: str) -> Optional[Dict]:
        """Extract business information from a Google Maps element"""
        try:
            # Click on the element to get more details
            try:
                element.click()
                time.sleep(1)
            except:
                pass
            
            business_info = {
                'name': '',
                'business_type': business_type,
                'address': '',
                'city': city,
                'region': 'Tunisia',
                'phone': '',
                'website': '',
                'rating': '',
                'reviews_count': '',
                'latitude': '',
                'longitude': '',
                'data_source': 'Google Maps Direct'
            }
            
            # Extract name
            try:
                name_selectors = [
                    'h1[data-attrid="title"]',
                    'h1',
                    '[data-attrid="title"]',
                    '.x3AX1-LfntMc-header-title-title',
                    '.SPZz6b h1'
                ]
                
                for selector in name_selectors:
                    try:
                        name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        business_info['name'] = name_element.text.strip()
                        break
                    except:
                        continue
            except:
                pass
            
            # Extract address
            try:
                address_selectors = [
                    '[data-item-id="address"]',
                    '.Io6YTe',
                    '.LrzXr',
                    '[data-attrid="kc:/location/location:address"]'
                ]
                
                for selector in address_selectors:
                    try:
                        address_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        business_info['address'] = address_element.text.strip()
                        break
                    except:
                        continue
            except:
                pass
            
            # Extract phone
            try:
                phone_selectors = [
                    '[data-item-id*="phone"]',
                    '[data-attrid="kc:/business/phone:phone"]',
                    '.Io6YTe[data-value*="+"]'
                ]
                
                for selector in phone_selectors:
                    try:
                        phone_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        phone_text = phone_element.text.strip()
                        if re.search(r'[\+]?[0-9\s\-\(\)]+', phone_text):
                            business_info['phone'] = phone_text
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract website
            try:
                website_selectors = [
                    '[data-item-id*="website"]',
                    '[data-attrid="kc:/business/website:website"]',
                    'a[href*="http"]'
                ]
                
                for selector in website_selectors:
                    try:
                        website_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        href = website_element.get_attribute('href')
                        if href and 'http' in href:
                            business_info['website'] = href
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract rating
            try:
                rating_selectors = [
                    '.ceNzKf',
                    '.MW4etd',
                    '[data-attrid="kc:/business/rating:rating"]'
                ]
                
                for selector in rating_selectors:
                    try:
                        rating_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        rating_text = rating_element.text.strip()
                        if re.search(r'[0-9]+\.[0-9]+', rating_text):
                            business_info['rating'] = rating_text
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract reviews count
            try:
                reviews_selectors = [
                    '.UY7F9',
                    '.HHrUdb',
                    '[data-attrid="kc:/business/rating:review_count"]'
                ]
                
                for selector in reviews_selectors:
                    try:
                        reviews_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        reviews_text = reviews_element.text.strip()
                        if re.search(r'[0-9]+', reviews_text):
                            business_info['reviews_count'] = reviews_text
                            break
                    except:
                        continue
            except:
                pass
            
            # Only return if we have at least a name
            if business_info['name']:
                return business_info
            
        except Exception as e:
            print(f"    ⚠️  Business info extraction error: {e}")
        
        return None
    
    def scrape_all_business_types(self, city: str, business_types: List[str]) -> pd.DataFrame:
        """Scrape all business types for a city"""
        all_businesses = []
        
        for business_type in business_types:
            print(f"\n🔍 Scraping {business_type} in {city}...")
            businesses = self.search_google_maps(city, business_type)
            all_businesses.extend(businesses)
            
            # Rate limiting between business types
            time.sleep(3)
        
        # Remove duplicates
        unique_businesses = self._remove_duplicates(all_businesses)
        
        print(f"\n🎉 TOTAL UNIQUE BUSINESSES: {len(unique_businesses)}")
        
        return pd.DataFrame(unique_businesses)
    
    def _remove_duplicates(self, businesses: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses"""
        seen = set()
        unique = []
        
        for business in businesses:
            key = (
                business.get('name', '').lower().strip(),
                business.get('address', '').lower().strip()
            )
            
            if key not in seen and business.get('name'):
                seen.add(key)
                unique.append(business)
        
        return unique
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save DataFrame to CSV file"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"google_maps_businesses_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Data saved to {filename}")
        return filename
    
    def display_summary(self, df: pd.DataFrame):
        """Display summary statistics"""
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n📊 === GOOGLE MAPS RESULTS ===")
        print(f"🎯 Total businesses: {len(df)}")
        print(f"\n🏢 Business types:")
        print(df['business_type'].value_counts())
        print(f"\n🏙️  Cities:")
        print(df['city'].value_counts().head(10))
        
        print(f"\n📋 === FIRST 10 ROWS ===")
        display_cols = ['name', 'business_type', 'address', 'phone', 'rating', 'city']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].head(10).to_string(index=False))
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()


def main():
    """Main function"""
    print("🗺️  Google Maps Direct Scraper for Tunisia")
    print("=" * 50)
    print("This scrapes DIRECTLY from Google Maps for real results!")
    print("=" * 50)
    
    scraper = GoogleMapsScraper(headless=False)  # Set to True for headless mode
    
    try:
        # Get user input
        print(f"\n🏙️  Available cities: {', '.join(scraper.tunisia_cities.keys())}")
        city = input("Enter city name: ").strip()
        
        if city not in scraper.tunisia_cities:
            print(f"❌ City '{city}' not found. Using 'Tunis' as default.")
            city = 'Tunis'
        
        print("\n🏢 Available business types: doctors, jewelry, lawyers")
        business_input = input("Enter business types (comma-separated, or 'all'): ").strip().lower()
        
        if business_input == 'all':
            business_types = ['doctors', 'jewelry', 'lawyers']
        else:
            business_types = [bt.strip() for bt in business_input.split(',')]
            business_types = [bt for bt in business_types if bt in ['doctors', 'jewelry', 'lawyers']]
            
            if not business_types:
                print("❌ No valid business types. Using all types.")
                business_types = ['doctors', 'jewelry', 'lawyers']
        
        # Scrape data
        print(f"\n🚀 SCRAPING GOOGLE MAPS for {business_types} in {city}...")
        print("This will open Chrome and scrape directly from Google Maps...")
        
        df = scraper.scrape_all_business_types(city, business_types)
        
        if not df.empty:
            # Save and display results
            filename = scraper.save_to_csv(df)
            scraper.display_summary(df)
            print(f"\n🎉 GOOGLE MAPS SCRAPING COMPLETED!")
            print(f"📁 Data saved to: {filename}")
            print(f"📊 Total results: {len(df)}")
        else:
            print("❌ No businesses found. Try a different city.")
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
