#!/usr/bin/env python3
"""
Tunisia Business Scraper V2 - Multiple Data Sources
Uses Google Places API, SerpApi, and improved OpenStreetMap approaches
"""

import requests
import pandas as pd
import time
import json
from typing import List, Dict, Optional, Tuple
import os
from urllib.parse import quote


class TunisiaBusinessScraperV2:
    """Enhanced scraper using multiple data sources"""
    
    def __init__(self, google_api_key: str = None, serpapi_key: str = None):
        self.google_api_key = google_api_key or os.getenv('GOOGLE_PLACES_API_KEY')
        self.serpapi_key = serpapi_key or os.getenv('SERPAPI_KEY')
        
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
        
        # Business type mappings for Google Places API
        self.business_types = {
            'doctors': ['doctor', 'hospital', 'health', 'medical_center'],
            'jewelry': ['jewelry_store', 'jewelry'],
            'lawyers': ['lawyer', 'attorney', 'legal_services']
        }
    
    def scrape_google_places(self, city: str, business_type: str, radius: int = 5000) -> List[Dict]:
        """
        Scrape using Google Places API
        
        Args:
            city: Name of the city
            business_type: Type of business to search for
            radius: Search radius in meters
            
        Returns:
            List of business dictionaries
        """
        if not self.google_api_key:
            print("❌ Google Places API key not provided. Set GOOGLE_PLACES_API_KEY environment variable.")
            return []
        
        if city not in self.tunisia_cities:
            print(f"❌ City '{city}' not found in Tunisia cities list")
            return []
        
        lat, lng = self.tunisia_cities[city]
        businesses = []
        
        # Get search terms for the business type
        search_terms = self.business_types.get(business_type, [business_type])
        
        for search_term in search_terms:
            print(f"🔍 Searching for '{search_term}' in {city}...")
            
            # Use Text Search API for better results
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            
            params = {
                'query': f'{search_term} in {city}, Tunisia',
                'key': self.google_api_key,
                'region': 'tn'  # Tunisia region code
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
                    
                    print(f"✅ Found {len(data.get('results', []))} places for '{search_term}'")
                else:
                    print(f"❌ API Error: {data.get('error_message', 'Unknown error')}")
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ Error searching for '{search_term}': {e}")
        
        return businesses
    
    def _extract_google_place_info(self, place: Dict, business_type: str, city: str) -> Dict:
        """Extract business information from Google Places API response"""
        try:
            # Get place details for more information
            place_id = place.get('place_id')
            details = self._get_place_details(place_id) if place_id else {}
            
            return {
                'name': place.get('name', ''),
                'business_type': business_type,
                'address': place.get('formatted_address', ''),
                'city': city,
                'region': 'Tunisia',
                'phone': details.get('formatted_phone_number', ''),
                'email': details.get('email', ''),
                'website': details.get('website', ''),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'rating': place.get('rating', ''),
                'user_ratings_total': place.get('user_ratings_total', ''),
                'price_level': place.get('price_level', ''),
                'data_source': 'Google Places API'
            }
        except Exception as e:
            print(f"❌ Error extracting place info: {e}")
            return None
    
    def _get_place_details(self, place_id: str) -> Dict:
        """Get detailed information for a place"""
        if not place_id or not self.google_api_key:
            return {}
        
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'formatted_phone_number,website,email,opening_hours',
            'key': self.google_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
        except Exception as e:
            print(f"❌ Error getting place details: {e}")
        
        return {}
    
    def scrape_serpapi(self, city: str, business_type: str) -> List[Dict]:
        """
        Scrape using SerpApi (requires API key)
        
        Args:
            city: Name of the city
            business_type: Type of business to search for
            
        Returns:
            List of business dictionaries
        """
        if not self.serpapi_key:
            print("❌ SerpApi key not provided. Set SERPAPI_KEY environment variable.")
            return []
        
        businesses = []
        
        # Map business types to search terms
        search_terms = {
            'doctors': f'doctors in {city} Tunisia',
            'jewelry': f'jewelry stores in {city} Tunisia',
            'lawyers': f'lawyers in {city} Tunisia'
        }
        
        query = search_terms.get(business_type, f'{business_type} in {city} Tunisia')
        
        url = "https://serpapi.com/search"
        params = {
            'engine': 'google_maps',
            'q': query,
            'api_key': self.serpapi_key,
            'type': 'search'
        }
        
        try:
            print(f"🔍 Searching SerpApi for '{query}'...")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for result in data.get('local_results', []):
                business = self._extract_serpapi_info(result, business_type, city)
                if business:
                    businesses.append(business)
            
            print(f"✅ Found {len(businesses)} businesses via SerpApi")
            
        except Exception as e:
            print(f"❌ SerpApi error: {e}")
        
        return businesses
    
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
                'email': result.get('email', ''),
                'website': result.get('website', ''),
                'latitude': result.get('gps_coordinates', {}).get('latitude', ''),
                'longitude': result.get('gps_coordinates', {}).get('longitude', ''),
                'rating': result.get('rating', ''),
                'reviews': result.get('reviews', ''),
                'data_source': 'SerpApi'
            }
        except Exception as e:
            print(f"❌ Error extracting SerpApi info: {e}")
            return None
    
    def scrape_improved_osm(self, city: str, business_type: str) -> List[Dict]:
        """
        Improved OpenStreetMap scraping using better queries
        
        Args:
            city: Name of the city
            business_type: Type of business to search for
            
        Returns:
            List of business dictionaries
        """
        businesses = []
        
        # Better Overpass queries for Tunisia
        queries = {
            'doctors': f"""
            [out:json][timeout:60];
            (
              node["amenity"="doctors"]["name"]["addr:country"="TN"];
              node["healthcare"="doctor"]["name"]["addr:country"="TN"];
              node["healthcare"="clinic"]["name"]["addr:country"="TN"];
            );
            out center meta;
            """,
            'jewelry': f"""
            [out:json][timeout:60];
            (
              node["shop"="jewelry"]["name"]["addr:country"="TN"];
              node["shop"="watches"]["name"]["addr:country"="TN"];
            );
            out center meta;
            """,
            'lawyers': f"""
            [out:json][timeout:60];
            (
              node["office"="lawyer"]["name"]["addr:country"="TN"];
              node["office"="attorney"]["name"]["addr:country"="TN"];
              node["office"="legal_services"]["name"]["addr:country"="TN"];
            );
            out center meta;
            """
        }
        
        query = queries.get(business_type)
        if not query:
            return businesses
        
        try:
            print(f"🔍 Searching OpenStreetMap for {business_type} in Tunisia...")
            response = requests.post(
                "https://overpass-api.de/api/interpreter",
                data={'data': query},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            for element in data.get('elements', []):
                business = self._extract_osm_info(element, business_type, city)
                if business and self._is_in_city(business, city):
                    businesses.append(business)
            
            print(f"✅ Found {len(businesses)} {business_type} in {city} via OSM")
            
        except Exception as e:
            print(f"❌ OSM error: {e}")
        
        return businesses
    
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
            print(f"❌ Error extracting OSM info: {e}")
            return None
    
    def _is_in_city(self, business: Dict, target_city: str) -> bool:
        """Check if business is in the target city"""
        business_city = business.get('city', '').lower()
        target_city_lower = target_city.lower()
        
        return (target_city_lower in business_city or 
                business_city in target_city_lower or
                target_city_lower == business_city)
    
    def scrape_all_sources(self, city: str, business_types: List[str]) -> pd.DataFrame:
        """
        Scrape from all available sources
        
        Args:
            city: Name of the city
            business_types: List of business types to scrape
            
        Returns:
            Combined DataFrame with all results
        """
        all_businesses = []
        
        for business_type in business_types:
            print(f"\n🔍 Scraping {business_type} in {city}...")
            
            # Try Google Places API first (most reliable)
            if self.google_api_key:
                google_results = self.scrape_google_places(city, business_type)
                all_businesses.extend(google_results)
            
            # Try SerpApi if available
            if self.serpapi_key:
                serpapi_results = self.scrape_serpapi(city, business_type)
                all_businesses.extend(serpapi_results)
            
            # Always try OpenStreetMap as fallback
            osm_results = self.scrape_improved_osm(city, business_type)
            all_businesses.extend(osm_results)
            
            # Rate limiting between business types
            time.sleep(1)
        
        # Remove duplicates based on name and coordinates
        unique_businesses = self._remove_duplicates(all_businesses)
        
        print(f"\n✅ Total unique businesses found: {len(unique_businesses)}")
        
        return pd.DataFrame(unique_businesses)
    
    def _remove_duplicates(self, businesses: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses based on name and coordinates"""
        seen = set()
        unique = []
        
        for business in businesses:
            # Create a key based on name and coordinates
            key = (
                business.get('name', '').lower().strip(),
                round(business.get('latitude', 0), 4),
                round(business.get('longitude', 0), 4)
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(business)
        
        return unique
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save DataFrame to CSV file"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"tunisia_businesses_v2_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Data saved to {filename}")
        return filename
    
    def display_summary(self, df: pd.DataFrame):
        """Display summary statistics"""
        if df.empty:
            print("❌ No data to display")
            return
        
        print(f"\n📊 === SUMMARY ===")
        print(f"Total businesses: {len(df)}")
        print(f"\nBusiness types:")
        print(df['business_type'].value_counts())
        print(f"\nData sources:")
        print(df['data_source'].value_counts())
        print(f"\nCities:")
        print(df['city'].value_counts().head(10))
        
        print(f"\n📋 === FIRST 10 ROWS ===")
        display_cols = ['name', 'business_type', 'address', 'phone', 'city', 'data_source']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].head(10).to_string(index=False))


def main():
    """Main function"""
    print("🇹🇳 Tunisia Business Scraper V2 - Multiple Data Sources")
    print("=" * 60)
    
    # Check for API keys
    google_key = os.getenv('GOOGLE_PLACES_API_KEY')
    serpapi_key = os.getenv('SERPAPI_KEY')
    
    print("🔑 API Keys Status:")
    print(f"Google Places API: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"SerpApi: {'✅ Set' if serpapi_key else '❌ Not set'}")
    print("OpenStreetMap: ✅ Always available")
    
    if not google_key and not serpapi_key:
        print("\n⚠️  No API keys found. Only OpenStreetMap will be used.")
        print("To get better results, set up API keys:")
        print("1. Google Places API: https://console.cloud.google.com/")
        print("2. SerpApi: https://serpapi.com/")
        print("Set them as environment variables: GOOGLE_PLACES_API_KEY and SERPAPI_KEY")
    
    scraper = TunisiaBusinessScraperV2(google_key, serpapi_key)
    
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
    print(f"\n🚀 Starting scrape for {business_types} in {city}...")
    df = scraper.scrape_all_sources(city, business_types)
    
    if not df.empty:
        # Save and display results
        filename = scraper.save_to_csv(df)
        scraper.display_summary(df)
        print(f"\n🎉 Scraping completed! Data saved to: {filename}")
    else:
        print("❌ No businesses found. Try a different city or check your API keys.")


if __name__ == "__main__":
    main()

