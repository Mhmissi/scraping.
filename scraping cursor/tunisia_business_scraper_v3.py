#!/usr/bin/env python3
"""
Tunisia Business Scraper V3 - SUPERCHARGED VERSION
Gets HUNDREDS of results using multiple strategies
"""

import requests
import pandas as pd
import time
import json
from typing import List, Dict, Optional, Tuple
import os
from urllib.parse import quote
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re


class TunisiaBusinessScraperV3:
    """Supercharged scraper for maximum results"""
    
    def __init__(self, google_api_key: str = None, serpapi_key: str = None, use_selenium: bool = True):
        self.google_api_key = google_api_key or os.getenv('GOOGLE_PLACES_API_KEY')
        self.serpapi_key = serpapi_key or os.getenv('SERPAPI_KEY')
        self.use_selenium = use_selenium
        
        # Tunisian cities with coordinates and search terms
        self.tunisia_cities = {
            'Tunis': {
                'coords': (36.8065, 10.1815),
                'search_terms': ['Tunis', 'Tunisia', 'تونس', 'Tunis-Mutuelleville', 'Lac', 'Ariana']
            },
            'Sfax': {
                'coords': (34.7406, 10.7603),
                'search_terms': ['Sfax', 'صفاقس', 'Sfax Centre', 'Sakiet Ezzit']
            },
            'Sousse': {
                'coords': (35.8256, 10.6411),
                'search_terms': ['Sousse', 'سوسة', 'Sousse Centre', 'Sahloul']
            },
            'Kairouan': {
                'coords': (35.6781, 10.0963),
                'search_terms': ['Kairouan', 'القيروان', 'Kairouan Centre']
            },
            'Bizerte': {
                'coords': (37.2744, 9.8739),
                'search_terms': ['Bizerte', 'بنزرت', 'Bizerte Centre']
            },
            'Gabès': {
                'coords': (33.8881, 10.0972),
                'search_terms': ['Gabès', 'قابس', 'Gabès Centre']
            },
            'Ariana': {
                'coords': (36.8601, 10.1931),
                'search_terms': ['Ariana', 'أريانة', 'Ariana Centre']
            },
            'Ben Arous': {
                'coords': (36.7531, 10.2189),
                'search_terms': ['Ben Arous', 'بن عروس', 'Ben Arous Centre']
            },
            'Manouba': {
                'coords': (36.8081, 10.0972),
                'search_terms': ['Manouba', 'منوبة', 'Manouba Centre']
            },
            'Nabeul': {
                'coords': (36.4561, 10.7376),
                'search_terms': ['Nabeul', 'نابل', 'Nabeul Centre', 'Hammamet']
            },
            'Monastir': {
                'coords': (35.7781, 10.8262),
                'search_terms': ['Monastir', 'المنستير', 'Monastir Centre']
            },
            'Mahdia': {
                'coords': (35.5047, 11.0442),
                'search_terms': ['Mahdia', 'المهدية', 'Mahdia Centre']
            },
            'Kasserine': {
                'coords': (35.1678, 8.8361),
                'search_terms': ['Kasserine', 'القصرين', 'Kasserine Centre']
            },
            'Sidi Bouzid': {
                'coords': (35.0381, 9.4847),
                'search_terms': ['Sidi Bouzid', 'سيدي بوزيد', 'Sidi Bouzid Centre']
            },
            'Kef': {
                'coords': (36.1822, 8.7147),
                'search_terms': ['Kef', 'الكاف', 'Kef Centre']
            },
            'Jendouba': {
                'coords': (36.5011, 8.7803),
                'search_terms': ['Jendouba', 'جندوبة', 'Jendouba Centre']
            },
            'Beja': {
                'coords': (36.7256, 9.1814),
                'search_terms': ['Beja', 'باجة', 'Beja Centre']
            },
            'Siliana': {
                'coords': (36.0831, 9.3708),
                'search_terms': ['Siliana', 'سليانة', 'Siliana Centre']
            },
            'Zaghouan': {
                'coords': (36.4019, 10.1428),
                'search_terms': ['Zaghouan', 'زغوان', 'Zaghouan Centre']
            },
            'Medenine': {
                'coords': (33.3547, 10.5053),
                'search_terms': ['Medenine', 'مدنين', 'Medenine Centre']
            },
            'Tataouine': {
                'coords': (32.9297, 10.4517),
                'search_terms': ['Tataouine', 'تطاوين', 'Tataouine Centre']
            },
            'Gafsa': {
                'coords': (34.4256, 8.7842),
                'search_terms': ['Gafsa', 'قفصة', 'Gafsa Centre']
            },
            'Tozeur': {
                'coords': (33.9197, 8.1336),
                'search_terms': ['Tozeur', 'توزر', 'Tozeur Centre']
            },
            'Kebili': {
                'coords': (33.7042, 8.9694),
                'search_terms': ['Kebili', 'قبلي', 'Kebili Centre']
            }
        }
        
        # Enhanced business type mappings
        self.business_types = {
            'doctors': {
                'google_terms': ['doctor', 'hospital', 'health', 'medical_center', 'clinic', 'physician', 'médecin', 'طبيب'],
                'search_terms': ['doctor', 'médecin', 'طبيب', 'hospital', 'hôpital', 'مستشفى', 'clinic', 'clinique', 'عيادة', 'medical', 'médical', 'صحة']
            },
            'jewelry': {
                'google_terms': ['jewelry_store', 'jewelry', 'jeweler', 'bijouterie', 'مجوهرات'],
                'search_terms': ['jewelry', 'bijouterie', 'مجوهرات', 'jeweler', 'bijoutier', 'صائغ', 'gold', 'or', 'ذهب', 'silver', 'argent', 'فضة']
            },
            'lawyers': {
                'google_terms': ['lawyer', 'attorney', 'legal_services', 'avocat', 'محامي'],
                'search_terms': ['lawyer', 'avocat', 'محامي', 'attorney', 'legal', 'juridique', 'قانوني', 'court', 'tribunal', 'محكمة']
            }
        }
    
    def scrape_google_places_enhanced(self, city: str, business_type: str) -> List[Dict]:
        """Enhanced Google Places scraping with multiple search strategies"""
        if not self.google_api_key:
            return []
        
        businesses = []
        city_info = self.tunisia_cities.get(city, {})
        search_terms = self.business_types.get(business_type, {}).get('search_terms', [])
        
        # Add city-specific search terms
        city_search_terms = city_info.get('search_terms', [])
        
        # Combine all search terms
        all_search_terms = search_terms + [f"{term} {city}" for term in search_terms[:3]]
        all_search_terms += [f"{term} {city_term}" for term in search_terms[:2] for city_term in city_search_terms[:2]]
        
        print(f"🔍 Searching with {len(all_search_terms)} different terms...")
        
        for i, search_term in enumerate(all_search_terms[:10]):  # Limit to 10 searches
            print(f"  {i+1}/10: '{search_term}'")
            
            # Use Text Search API
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'query': f'{search_term} in {city}, Tunisia',
                'key': self.google_api_key,
                'region': 'tn'
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get('status') == 'OK':
                    for place in data.get('results', []):
                        business = self._extract_google_place_info(place, business_type, city)
                        if business:
                            businesses.append(business)
                
                # Rate limiting
                time.sleep(0.2)
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        # Remove duplicates
        businesses = self._remove_duplicates(businesses)
        print(f"✅ Found {len(businesses)} unique {business_type} via Google Places")
        
        return businesses
    
    def scrape_google_maps_selenium(self, city: str, business_type: str) -> List[Dict]:
        """Scrape Google Maps directly using Selenium for maximum results"""
        if not self.use_selenium:
            return []
        
        businesses = []
        
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            search_terms = self.business_types.get(business_type, {}).get('search_terms', [])
            
            for search_term in search_terms[:5]:  # Limit to 5 searches
                print(f"🌐 Selenium search: '{search_term} in {city}, Tunisia'")
                
                try:
                    # Search on Google Maps
                    search_query = f"{search_term} in {city}, Tunisia"
                    driver.get(f"https://www.google.com/maps/search/{quote(search_query)}")
                    
                    # Wait for results to load
                    time.sleep(3)
                    
                    # Scroll to load more results
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    
                    # Extract business information
                    business_elements = driver.find_elements(By.CSS_SELECTOR, '[data-result-index]')
                    
                    for element in business_elements:
                        try:
                            business = self._extract_selenium_business_info(element, business_type, city)
                            if business:
                                businesses.append(business)
                        except Exception as e:
                            continue
                    
                    print(f"  ✅ Found {len(business_elements)} elements")
                    
                except Exception as e:
                    print(f"  ❌ Selenium error: {e}")
                
                time.sleep(2)  # Rate limiting
            
            driver.quit()
            
        except Exception as e:
            print(f"❌ Selenium setup error: {e}")
        
        # Remove duplicates
        businesses = self._remove_duplicates(businesses)
        print(f"✅ Found {len(businesses)} unique {business_type} via Selenium")
        
        return businesses
    
    def _extract_selenium_business_info(self, element, business_type: str, city: str) -> Dict:
        """Extract business info from Selenium element"""
        try:
            # Click on the element to get more details
            element.click()
            time.sleep(1)
            
            # Extract information
            name = ""
            address = ""
            phone = ""
            website = ""
            
            try:
                name_element = element.find_element(By.CSS_SELECTOR, 'h1, [data-value="Directions"]')
                name = name_element.text
            except:
                pass
            
            try:
                address_element = element.find_element(By.CSS_SELECTOR, '[data-item-id="address"]')
                address = address_element.text
            except:
                pass
            
            try:
                phone_element = element.find_element(By.CSS_SELECTOR, '[data-item-id*="phone"]')
                phone = phone_element.text
            except:
                pass
            
            try:
                website_element = element.find_element(By.CSS_SELECTOR, '[data-item-id*="website"]')
                website = website_element.text
            except:
                pass
            
            if name:
                return {
                    'name': name,
                    'business_type': business_type,
                    'address': address,
                    'city': city,
                    'region': 'Tunisia',
                    'phone': phone,
                    'website': website,
                    'data_source': 'Selenium Google Maps'
                }
        
        except Exception as e:
            pass
        
        return None
    
    def scrape_osm_enhanced(self, city: str, business_type: str) -> List[Dict]:
        """Enhanced OpenStreetMap scraping with better queries"""
        businesses = []
        
        # Multiple query strategies for better coverage
        queries = self._get_osm_queries(business_type)
        
        for i, query in enumerate(queries):
            try:
                print(f"🗺️  OSM query {i+1}/{len(queries)} for {business_type}")
                
                response = requests.post(
                    "https://overpass-api.de/api/interpreter",
                    data={'data': query},
                    timeout=60,
                    headers={'User-Agent': f'TunisiaScraper/1.0 (Query {i+1})'}
                )
                response.raise_for_status()
                data = response.json()
                
                for element in data.get('elements', []):
                    business = self._extract_osm_info(element, business_type, city)
                    if business and self._is_in_city(business, city):
                        businesses.append(business)
                
                print(f"  ✅ Found {len(data.get('elements', []))} elements")
                
                # Rate limiting between queries
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ OSM query {i+1} error: {e}")
                time.sleep(5)  # Longer delay on error
        
        # Remove duplicates
        businesses = self._remove_duplicates(businesses)
        print(f"✅ Found {len(businesses)} unique {business_type} via OSM")
        
        return businesses
    
    def _get_osm_queries(self, business_type: str) -> List[str]:
        """Get multiple OSM queries for better coverage"""
        base_query = """
        [out:json][timeout:60];
        (
          {node_queries}
        );
        out center meta;
        """
        
        if business_type == 'doctors':
            node_queries = [
                'node["amenity"="doctors"]["name"]["addr:country"="TN"];',
                'node["healthcare"="doctor"]["name"]["addr:country"="TN"];',
                'node["healthcare"="clinic"]["name"]["addr:country"="TN"];',
                'node["healthcare"="hospital"]["name"]["addr:country"="TN"];',
                'node["office"="doctor"]["name"]["addr:country"="TN"];',
                'node["office"="medical"]["name"]["addr:country"="TN"];'
            ]
        elif business_type == 'jewelry':
            node_queries = [
                'node["shop"="jewelry"]["name"]["addr:country"="TN"];',
                'node["shop"="watches"]["name"]["addr:country"="TN"];',
                'node["shop"="gold"]["name"]["addr:country"="TN"];',
                'node["craft"="jeweller"]["name"]["addr:country"="TN"];'
            ]
        elif business_type == 'lawyers':
            node_queries = [
                'node["office"="lawyer"]["name"]["addr:country"="TN"];',
                'node["office"="attorney"]["name"]["addr:country"="TN"];',
                'node["office"="legal_services"]["name"]["addr:country"="TN"];',
                'node["office"="notary"]["name"]["addr:country"="TN"];'
            ]
        else:
            return []
        
        # Create multiple queries with different combinations
        queries = []
        for i in range(0, len(node_queries), 2):
            query_nodes = node_queries[i:i+2]
            query = base_query.format(node_queries='\n'.join(query_nodes))
            queries.append(query)
        
        return queries
    
    def scrape_all_sources_enhanced(self, city: str, business_types: List[str]) -> pd.DataFrame:
        """Enhanced scraping from all sources with maximum results"""
        all_businesses = []
        
        for business_type in business_types:
            print(f"\n🚀 SUPERCHARGED SCRAPING: {business_type} in {city}")
            print("=" * 60)
            
            # 1. Google Places API (if available)
            if self.google_api_key:
                google_results = self.scrape_google_places_enhanced(city, business_type)
                all_businesses.extend(google_results)
            
            # 2. Selenium Google Maps (if enabled)
            if self.use_selenium:
                selenium_results = self.scrape_google_maps_selenium(city, business_type)
                all_businesses.extend(selenium_results)
            
            # 3. Enhanced OpenStreetMap
            osm_results = self.scrape_osm_enhanced(city, business_type)
            all_businesses.extend(osm_results)
            
            # 4. SerpApi (if available)
            if self.serpapi_key:
                serpapi_results = self.scrape_serpapi_enhanced(city, business_type)
                all_businesses.extend(serpapi_results)
            
            print(f"📊 {business_type}: {len([b for b in all_businesses if b.get('business_type') == business_type])} total results")
            
            # Rate limiting between business types
            time.sleep(3)
        
        # Remove duplicates
        unique_businesses = self._remove_duplicates(all_businesses)
        
        print(f"\n🎉 TOTAL UNIQUE BUSINESSES: {len(unique_businesses)}")
        
        return pd.DataFrame(unique_businesses)
    
    def scrape_serpapi_enhanced(self, city: str, business_type: str) -> List[Dict]:
        """Enhanced SerpApi scraping"""
        if not self.serpapi_key:
            return []
        
        businesses = []
        search_terms = self.business_types.get(business_type, {}).get('search_terms', [])
        
        for search_term in search_terms[:3]:  # Limit to 3 searches
            query = f"{search_term} in {city} Tunisia"
            
            url = "https://serpapi.com/search"
            params = {
                'engine': 'google_maps',
                'q': query,
                'api_key': self.serpapi_key,
                'type': 'search'
            }
            
            try:
                print(f"🔍 SerpApi: '{query}'")
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for result in data.get('local_results', []):
                    business = self._extract_serpapi_info(result, business_type, city)
                    if business:
                        businesses.append(business)
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"❌ SerpApi error: {e}")
        
        return businesses
    
    def _extract_google_place_info(self, place: Dict, business_type: str, city: str) -> Dict:
        """Extract business information from Google Places API response"""
        try:
            return {
                'name': place.get('name', ''),
                'business_type': business_type,
                'address': place.get('formatted_address', ''),
                'city': city,
                'region': 'Tunisia',
                'phone': '',  # Would need place details API call
                'email': '',
                'website': '',
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'rating': place.get('rating', ''),
                'user_ratings_total': place.get('user_ratings_total', ''),
                'data_source': 'Google Places API'
            }
        except Exception as e:
            return None
    
    def _extract_serpapi_info(self, result: Dict, business_type: str, city: str) -> Dict:
        """Extract business information from SerpApi response"""
        try:
            return {
                'name': result.get('title', ''),
                'business_type': business_type,
                'address': result.get('address', ''),
                'city': city,
                'region': 'Tunisia',
                'phone': result.get('phone', ''),
                'website': result.get('website', ''),
                'latitude': result.get('gps_coordinates', {}).get('latitude', ''),
                'longitude': result.get('gps_coordinates', {}).get('longitude', ''),
                'rating': result.get('rating', ''),
                'data_source': 'SerpApi'
            }
        except Exception as e:
            return None
    
    def _extract_osm_info(self, element: Dict, business_type: str, city: str) -> Dict:
        """Extract business information from OSM element"""
        try:
            tags = element.get('tags', {})
            
            # Get coordinates
            lat, lon = None, None
            if element['type'] == 'node':
                lat, lon = element.get('lat'), element.get('lon')
            elif 'center' in element:
                lat, lon = element['center'].get('lat'), element['center'].get('lon')
            
            return {
                'name': tags.get('name', ''),
                'business_type': business_type,
                'address': f"{tags.get('addr:street', '')}, {tags.get('addr:city', '')}".strip(', '),
                'city': tags.get('addr:city', ''),
                'region': tags.get('addr:state', ''),
                'phone': tags.get('phone', ''),
                'email': tags.get('email', ''),
                'website': tags.get('website', ''),
                'latitude': lat,
                'longitude': lon,
                'data_source': 'OpenStreetMap'
            }
        except Exception as e:
            return None
    
    def _is_in_city(self, business: Dict, target_city: str) -> bool:
        """Check if business is in the target city"""
        business_city = business.get('city', '').lower()
        target_city_lower = target_city.lower()
        
        return (target_city_lower in business_city or 
                business_city in target_city_lower or
                target_city_lower == business_city)
    
    def _remove_duplicates(self, businesses: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses"""
        seen = set()
        unique = []
        
        for business in businesses:
            key = (
                business.get('name', '').lower().strip(),
                round(business.get('latitude', 0), 4) if business.get('latitude') else 0,
                round(business.get('longitude', 0), 4) if business.get('longitude') else 0
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(business)
        
        return unique
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save DataFrame to CSV file"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"tunisia_businesses_v3_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Data saved to {filename}")
        return filename
    
    def display_summary(self, df: pd.DataFrame):
        """Display summary statistics"""
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n📊 === SUPERCHARGED RESULTS ===")
        print(f"🎯 Total businesses: {len(df)}")
        print(f"\n🏢 Business types:")
        print(df['business_type'].value_counts())
        print(f"\n📡 Data sources:")
        print(df['data_source'].value_counts())
        print(f"\n🏙️  Cities:")
        print(df['city'].value_counts().head(10))
        
        print(f"\n📋 === FIRST 10 ROWS ===")
        display_cols = ['name', 'business_type', 'address', 'phone', 'city', 'data_source']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].head(10).to_string(index=False))


def main():
    """Main function"""
    print("🚀 Tunisia Business Scraper V3 - SUPERCHARGED VERSION")
    print("=" * 60)
    print("This version will get HUNDREDS of results!")
    print("=" * 60)
    
    # Check for API keys
    google_key = os.getenv('GOOGLE_PLACES_API_KEY')
    serpapi_key = os.getenv('SERPAPI_KEY')
    
    print("🔑 API Keys Status:")
    print(f"Google Places API: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"SerpApi: {'✅ Set' if serpapi_key else '❌ Not set'}")
    print("OpenStreetMap: ✅ Always available")
    print("Selenium: ✅ Available (if Chrome installed)")
    
    scraper = TunisiaBusinessScraperV3(google_key, serpapi_key)
    
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
    print(f"\n🚀 SUPERCHARGED SCRAPING for {business_types} in {city}...")
    print("This may take a few minutes to get maximum results...")
    
    df = scraper.scrape_all_sources_enhanced(city, business_types)
    
    if not df.empty:
        # Save and display results
        filename = scraper.save_to_csv(df)
        scraper.display_summary(df)
        print(f"\n🎉 SUPERCHARGED SCRAPING COMPLETED!")
        print(f"📁 Data saved to: {filename}")
        print(f"📊 Total results: {len(df)}")
    else:
        print("❌ No businesses found. Try a different city or check your setup.")


if __name__ == "__main__":
    main()

