#!/usr/bin/env python3
"""
Tunisia Business Scraper using Overpass API
Scrapes doctors, jewelry shops, and lawyers from OpenStreetMap data
"""

import requests
import pandas as pd
import time
import json
from typing import List, Dict, Optional


class TunisiaBusinessScraper:
    """Scraper for Tunisian businesses using Overpass API"""
    
    def __init__(self):
        self.base_url = "https://overpass-api.de/api/interpreter"
        self.headers = {
            'User-Agent': 'Tunisia Business Scraper/1.0'
        }
        
        # Tunisian regions/cities for reference
        self.regions = {
            'Tunis': 'Tunis',
            'Sfax': 'Sfax',
            'Sousse': 'Sousse',
            'Kairouan': 'Kairouan',
            'Bizerte': 'Bizerte',
            'Gabès': 'Gabès',
            'Ariana': 'Ariana',
            'Ben Arous': 'Ben Arous',
            'Manouba': 'Manouba',
            'Nabeul': 'Nabeul',
            'Monastir': 'Monastir',
            'Mahdia': 'Mahdia',
            'Kasserine': 'Kasserine',
            'Sidi Bouzid': 'Sidi Bouzid',
            'Kef': 'Kef',
            'Jendouba': 'Jendouba',
            'Beja': 'Beja',
            'Siliana': 'Siliana',
            'Zaghouan': 'Zaghouan',
            'Medenine': 'Medenine',
            'Tataouine': 'Tataouine',
            'Gafsa': 'Gafsa',
            'Tozeur': 'Tozeur',
            'Kebili': 'Kebili'
        }
    
    def build_overpass_query(self, region: str, business_types: List[str]) -> str:
        """
        Build Overpass QL query for specific region and business types
        
        Args:
            region: Name of the region/city
            business_types: List of business types to search for
            
        Returns:
            Overpass QL query string
        """
        # Define the business type conditions
        business_conditions = []
        
        for business_type in business_types:
            if business_type == 'doctors':
                business_conditions.append('(amenity=doctors or healthcare=doctor)')
            elif business_type == 'jewelry':
                business_conditions.append('shop=jewelry')
            elif business_type == 'lawyers':
                business_conditions.append('office=lawyer')
        
        # Combine conditions with OR
        business_filter = ' or '.join(business_conditions)
        
        # Use country code TN for Tunisia and filter by region after fetching
        # This is more reliable than city name filtering which can cause timeouts
        query = f"""
        [out:json][timeout:300];
        (
          node["{business_filter}"]["name"]["addr:country"="TN"];
          way["{business_filter}"]["name"]["addr:country"="TN"];
          relation["{business_filter}"]["name"]["addr:country"="TN"];
        );
        out center meta;
        """
        
        return query
    
    def make_request(self, query: str) -> Optional[Dict]:
        """
        Make request to Overpass API with rate limiting
        
        Args:
            query: Overpass QL query string
            
        Returns:
            JSON response or None if error
        """
        try:
            print(f"Making request to Overpass API...")
            response = requests.post(
                self.base_url,
                data={'data': query},
                headers=self.headers,
                timeout=300
            )
            response.raise_for_status()
            
            # Rate limiting - be polite to the API
            time.sleep(1)
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    
    def extract_business_info(self, element: Dict) -> Dict:
        """
        Extract business information from OSM element
        
        Args:
            element: OSM element (node/way/relation)
            
        Returns:
            Dictionary with business information
        """
        tags = element.get('tags', {})
        
        # Get coordinates
        lat, lon = None, None
        if element['type'] == 'node':
            lat, lon = element.get('lat'), element.get('lon')
        elif 'center' in element:
            lat, lon = element['center'].get('lat'), element['center'].get('lon')
        
        # Determine business type
        business_type = 'unknown'
        if tags.get('amenity') == 'doctors' or tags.get('healthcare') == 'doctor':
            business_type = 'doctor'
        elif tags.get('shop') == 'jewelry':
            business_type = 'jewelry'
        elif tags.get('office') == 'lawyer':
            business_type = 'lawyer'
        
        # Extract address components
        street = tags.get('addr:street', '')
        city = tags.get('addr:city', '')
        region = tags.get('addr:state', '')
        postcode = tags.get('addr:postcode', '')
        
        # Combine address
        address_parts = [street, city, region, postcode]
        address = ', '.join([part for part in address_parts if part])
        
        return {
            'name': tags.get('name', ''),
            'business_type': business_type,
            'address': address,
            'street': street,
            'city': city,
            'region': region,
            'postcode': postcode,
            'phone': tags.get('phone', ''),
            'email': tags.get('email', ''),
            'website': tags.get('website', ''),
            'latitude': lat,
            'longitude': lon,
            'osm_id': element.get('id'),
            'osm_type': element.get('type')
        }
    
    def scrape_businesses(self, region: str, business_types: List[str] = None) -> pd.DataFrame:
        """
        Scrape businesses for a specific region
        
        Args:
            region: Name of the region/city
            business_types: List of business types to scrape
            
        Returns:
            Pandas DataFrame with business data
        """
        if business_types is None:
            business_types = ['doctors', 'jewelry', 'lawyers']
        
        print(f"Scraping businesses in {region}...")
        print(f"Business types: {', '.join(business_types)}")
        
        # Build and execute query
        query = self.build_overpass_query(region, business_types)
        response = self.make_request(query)
        
        if not response:
            print("Failed to get data from Overpass API")
            return pd.DataFrame()
        
        # Extract business information
        businesses = []
        elements = response.get('elements', [])
        
        print(f"Found {len(elements)} elements in Tunisia")
        
        for element in elements:
            business_info = self.extract_business_info(element)
            if business_info['name']:  # Only include businesses with names
                # Filter by region - check if the business is in the requested region
                business_city = business_info.get('city', '').lower()
                business_region = business_info.get('region', '').lower()
                target_region = region.lower()
                
                # Check if the business is in the target region
                if (target_region in business_city or 
                    target_region in business_region or
                    business_city in target_region or
                    business_region in target_region):
                    businesses.append(business_info)
        
        print(f"Extracted {len(businesses)} businesses in {region}")
        
        # Convert to DataFrame
        df = pd.DataFrame(businesses)
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Save DataFrame to CSV file
        
        Args:
            df: Pandas DataFrame
            filename: Output filename (optional)
            
        Returns:
            Filename of saved file
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"tunisia_businesses_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
        
        return filename
    
    def display_summary(self, df: pd.DataFrame):
        """Display summary statistics of the scraped data"""
        if df.empty:
            print("No data to display")
            return
        
        print(f"\n=== SUMMARY ===")
        print(f"Total businesses found: {len(df)}")
        print(f"Business types:")
        print(df['business_type'].value_counts())
        print(f"Cities:")
        print(df['city'].value_counts().head(10))
        
        print(f"\n=== FIRST 10 ROWS ===")
        print(df.head(10).to_string(index=False))


def main():
    """Main function to run the scraper"""
    scraper = TunisiaBusinessScraper()
    
    # Display available regions
    print("Available regions:")
    for i, region in enumerate(scraper.regions.keys(), 1):
        print(f"{i}. {region}")
    
    # Get user input for region
    while True:
        try:
            choice = input(f"\nEnter region name (or number 1-{len(scraper.regions)}): ").strip()
            
            # Check if it's a number
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(scraper.regions):
                    region = list(scraper.regions.keys())[choice_num - 1]
                    break
                else:
                    print("Invalid number. Please try again.")
            else:
                # Check if it's a valid region name
                if choice in scraper.regions:
                    region = choice
                    break
                else:
                    print("Invalid region name. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            return
    
    print(f"\nSelected region: {region}")
    
    # Ask for business types
    print("\nAvailable business types:")
    print("1. doctors")
    print("2. jewelry")
    print("3. lawyers")
    print("4. all")
    
    business_choice = input("Enter business types (comma-separated, or 'all'): ").strip().lower()
    
    if business_choice == 'all':
        business_types = ['doctors', 'jewelry', 'lawyers']
    else:
        business_types = [bt.strip() for bt in business_choice.split(',')]
        # Validate business types
        valid_types = ['doctors', 'jewelry', 'lawyers']
        business_types = [bt for bt in business_types if bt in valid_types]
        
        if not business_types:
            print("No valid business types selected. Using all types.")
            business_types = ['doctors', 'jewelry', 'lawyers']
    
    # Scrape data
    df = scraper.scrape_businesses(region, business_types)
    
    if not df.empty:
        # Save to CSV
        filename = scraper.save_to_csv(df)
        
        # Display summary and first 10 rows
        scraper.display_summary(df)
        
        print(f"\nData has been saved to: {filename}")
    else:
        print("No businesses found for the selected criteria.")


if __name__ == "__main__":
    main()



