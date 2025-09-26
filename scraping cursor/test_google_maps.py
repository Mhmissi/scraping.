#!/usr/bin/env python3
"""
Test Google Maps Direct Scraper
This will scrape REAL data from Google Maps
"""

from google_maps_scraper import GoogleMapsScraper

def test_google_maps():
    """Test the Google Maps scraper"""
    print("🗺️  Testing Google Maps Direct Scraper")
    print("=" * 50)
    print("This will open Chrome and scrape from Google Maps!")
    print("=" * 50)
    
    scraper = GoogleMapsScraper(headless=False)  # Set to True for headless
    
    try:
        # Test with doctors in Tunis
        print("\n🔍 Testing: Doctors in Tunis")
        print("This will search Google Maps for doctors...")
        
        df = scraper.scrape_all_business_types('Tunis', ['doctors'])
        
        if not df.empty:
            print(f"✅ SUCCESS: Found {len(df)} doctors from Google Maps!")
            print("\nFirst 10 results:")
            print(df[['name', 'address', 'phone', 'rating', 'city']].head(10).to_string(index=False))
            
            # Save to CSV
            filename = scraper.save_to_csv(df, 'google_maps_doctors_tunis.csv')
            print(f"\n💾 Saved to: {filename}")
            
        else:
            print("❌ No doctors found")
        
        print("\n" + "=" * 50)
        
        # Test with all business types
        print("\n🔍 Testing: All business types in Tunis")
        print("This will search for doctors, jewelry, and lawyers...")
        
        df_all = scraper.scrape_all_business_types('Tunis', ['doctors', 'jewelry', 'lawyers'])
        
        if not df_all.empty:
            print(f"✅ SUCCESS: Found {len(df_all)} businesses from Google Maps!")
            print("\nBusiness type distribution:")
            print(df_all['business_type'].value_counts())
            
            # Save to CSV
            filename = scraper.save_to_csv(df_all, 'google_maps_all_tunis.csv')
            print(f"\n💾 Saved to: {filename}")
            
            print(f"\n🎉 GOOGLE MAPS TEST COMPLETED!")
            print(f"📊 Total unique businesses: {len(df_all)}")
            
        else:
            print("❌ No businesses found")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    test_google_maps()

