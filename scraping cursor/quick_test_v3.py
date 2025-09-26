#!/usr/bin/env python3
"""
Quick test of Tunisia Business Scraper V3 - SUPERCHARGED VERSION
Tests the scraper to get HUNDREDS of results
"""

from tunisia_business_scraper_v3 import TunisiaBusinessScraperV3

def test_supercharged():
    """Test the supercharged scraper"""
    print("🚀 Testing Tunisia Business Scraper V3 - SUPERCHARGED")
    print("=" * 60)
    print("This will get HUNDREDS of results!")
    print("=" * 60)
    
    # Test without Selenium first (to avoid Chrome dependency issues)
    scraper = TunisiaBusinessScraperV3(use_selenium=False)
    
    # Test with doctors in Tunis
    print("\n🔍 SUPERCHARGED TEST: Doctors in Tunis")
    print("Using multiple search strategies for maximum results...")
    
    df = scraper.scrape_all_sources_enhanced('Tunis', ['doctors'])
    
    if not df.empty:
        print(f"✅ SUCCESS: Found {len(df)} doctors!")
        print("\nFirst 10 results:")
        print(df[['name', 'address', 'phone', 'city', 'data_source']].head(10).to_string(index=False))
        
        # Save to CSV
        filename = scraper.save_to_csv(df, 'supercharged_doctors_tunis.csv')
        print(f"\n💾 Saved to: {filename}")
        
        # Show data source breakdown
        print(f"\n📊 Data source breakdown:")
        print(df['data_source'].value_counts())
        
    else:
        print("❌ No doctors found")
    
    print("\n" + "=" * 60)
    
    # Test with all business types
    print("\n🔍 SUPERCHARGED TEST: All business types in Tunis")
    print("This will take longer but get even MORE results...")
    
    df_all = scraper.scrape_all_sources_enhanced('Tunis', ['doctors', 'jewelry', 'lawyers'])
    
    if not df_all.empty:
        print(f"✅ SUCCESS: Found {len(df_all)} businesses!")
        print("\nBusiness type distribution:")
        print(df_all['business_type'].value_counts())
        print("\nData source distribution:")
        print(df_all['data_source'].value_counts())
        
        # Save to CSV
        filename = scraper.save_to_csv(df_all, 'supercharged_all_tunis.csv')
        print(f"\n💾 Saved to: {filename}")
        
        print(f"\n🎉 SUPERCHARGED TEST COMPLETED!")
        print(f"📊 Total unique businesses: {len(df_all)}")
        
    else:
        print("❌ No businesses found")

if __name__ == "__main__":
    test_supercharged()

