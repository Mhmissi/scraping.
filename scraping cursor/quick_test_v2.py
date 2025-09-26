#!/usr/bin/env python3
"""
Quick test of Tunisia Business Scraper V2
Tests the scraper without API keys (OSM only)
"""

from tunisia_business_scraper_v2 import TunisiaBusinessScraperV2

def test_without_api_keys():
    """Test the scraper without API keys (OSM only)"""
    print("🧪 Testing Tunisia Business Scraper V2 (OSM Only)")
    print("=" * 50)
    
    scraper = TunisiaBusinessScraperV2()
    
    # Test with doctors in Tunis
    print("\n🔍 Testing: Doctors in Tunis")
    df = scraper.scrape_all_sources('Tunis', ['doctors'])
    
    if not df.empty:
        print(f"✅ SUCCESS: Found {len(df)} doctors")
        print("\nFirst 5 results:")
        print(df[['name', 'address', 'phone', 'city', 'data_source']].head().to_string(index=False))
        
        # Save to CSV
        filename = scraper.save_to_csv(df, 'test_doctors_tunis.csv')
        print(f"\n💾 Saved to: {filename}")
    else:
        print("❌ No doctors found")
    
    print("\n" + "=" * 50)
    
    # Test with all business types
    print("\n🔍 Testing: All business types in Tunis")
    df_all = scraper.scrape_all_sources('Tunis', ['doctors', 'jewelry', 'lawyers'])
    
    if not df_all.empty:
        print(f"✅ SUCCESS: Found {len(df_all)} businesses")
        print("\nBusiness type distribution:")
        print(df_all['business_type'].value_counts())
        print("\nData source distribution:")
        print(df_all['data_source'].value_counts())
        
        # Save to CSV
        filename = scraper.save_to_csv(df_all, 'test_all_tunis.csv')
        print(f"\n💾 Saved to: {filename}")
    else:
        print("❌ No businesses found")

if __name__ == "__main__":
    test_without_api_keys()

