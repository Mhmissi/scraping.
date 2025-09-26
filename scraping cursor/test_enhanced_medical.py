#!/usr/bin/env python3
"""
Test Enhanced Google Maps Scraper with Medical Terms
This will test the scraper with the new comprehensive medical search terms
"""

from google_maps_scraper import GoogleMapsScraper

def test_enhanced_medical_terms():
    """Test the enhanced medical terms"""
    print("🩺 Testing Enhanced Medical Terms Scraper")
    print("=" * 60)
    print("This will search with 50+ medical terms!")
    print("=" * 60)
    
    scraper = GoogleMapsScraper(headless=False)  # Set to True for headless
    
    try:
        # Test with enhanced medical terms
        print("\n🔍 Testing: Enhanced Medical Search in Tunis")
        print("Searching with:")
        print("🩺 General Medical Practitioners")
        print("👨‍⚕️ Specialized Doctors") 
        print("🏥 Clinics & Health Centers")
        print("🦷 Dentists & Oral Care")
        print("👁 Optical & Vision")
        print("💊 Pharmacy & Paramedical")
        
        df = scraper.scrape_all_business_types('Tunis', ['doctors'])
        
        if not df.empty:
            print(f"\n✅ SUCCESS: Found {len(df)} medical businesses!")
            print("\nFirst 15 results:")
            print(df[['name', 'address', 'phone', 'rating', 'city']].head(15).to_string(index=False))
            
            # Save to CSV
            filename = scraper.save_to_csv(df, 'enhanced_medical_tunis.csv')
            print(f"\n💾 Saved to: {filename}")
            
            # Show unique business types found
            print(f"\n📊 Medical businesses found:")
            print(f"Total: {len(df)}")
            
        else:
            print("❌ No medical businesses found")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    test_enhanced_medical_terms()

