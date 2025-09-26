#!/usr/bin/env python3
"""
Demo script showing how to use the Tunisia Business Scraper programmatically
"""

from tunisia_business_scraper import TunisiaBusinessScraper

def demo():
    """Demonstrate the scraper functionality"""
    scraper = TunisiaBusinessScraper()
    
    # Example: Scrape doctors in Tunis
    print("=== DEMO: Scraping doctors in Tunis ===")
    df_doctors = scraper.scrape_businesses('Tunis', ['doctors'])
    
    if not df_doctors.empty:
        print(f"Found {len(df_doctors)} doctors in Tunis")
        print("\nFirst 5 doctors:")
        print(df_doctors[['name', 'address', 'phone', 'latitude', 'longitude']].head().to_string(index=False))
        
        # Save to CSV
        filename = scraper.save_to_csv(df_doctors, 'tunis_doctors.csv')
        print(f"\nSaved to: {filename}")
    else:
        print("No doctors found in Tunis")
    
    print("\n" + "="*50)
    
    # Example: Scrape all business types in Sfax
    print("=== DEMO: Scraping all business types in Sfax ===")
    df_all = scraper.scrape_businesses('Sfax', ['doctors', 'jewelry', 'lawyers'])
    
    if not df_all.empty:
        print(f"Found {len(df_all)} businesses in Sfax")
        print("\nBusiness type distribution:")
        print(df_all['business_type'].value_counts())
        
        print("\nFirst 10 businesses:")
        print(df_all[['name', 'business_type', 'address', 'phone']].head(10).to_string(index=False))
        
        # Save to CSV
        filename = scraper.save_to_csv(df_all, 'sfax_businesses.csv')
        print(f"\nSaved to: {filename}")
    else:
        print("No businesses found in Sfax")

if __name__ == "__main__":
    demo()




