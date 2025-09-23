# Tunisia Google Maps Business Scraper

A powerful Python script that scrapes business data directly from Google Maps for Tunisia. Gets **hundreds of real results** for doctors, jewelry shops, and lawyers.

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Install Chrome Browser
- Download Chrome from: https://www.google.com/chrome/

### 3. Run the Scraper
```bash
python google_maps_scraper.py
```

## 📊 Expected Results

- **Doctors**: 200-500+ per city (with 50+ medical terms)
- **Jewelry**: 50-150+ per city  
- **Lawyers**: 30-100+ per city

## 🏙️ Supported Cities

Tunis, Sfax, Sousse, Kairouan, Bizerte, Gabès, Ariana, Ben Arous, Manouba, Nabeul, Monastir, Mahdia, Kasserine, Sidi Bouzid, Kef, Jendouba, Beja, Siliana, Zaghouan, Medenine, Tataouine, Gafsa, Tozeur, Kebili

## 🏢 Business Types

### 🩺 **Doctors** (50+ search terms)
- **General**: médecin, médecin généraliste, cabinet médical, docteur
- **Specialized**: cardiologue, dermatologue, gynécologue, pédiatre, ophtalmologue, ORL, neurologue, psychiatre
- **Clinics**: clinique privée, centre médical, centre de santé, polyclinique, hôpital privé
- **Dental**: dentiste, orthodontiste, stomatologue, cabinet dentaire
- **Optical**: opticien, ophtalmologie, centre optique
- **Paramedical**: pharmacie, kinésithérapeute, ostéopathe, psychologue, infirmier

### 💎 **Jewelry**
- jewelry, bijouterie, مجوهرات, gold, or, ذهب, silver, argent, فضة

### ⚖️ **Lawyers**
- lawyer, avocat, محامي, attorney, legal, juridique, قانوني

## 📁 Output

Results saved as: `google_maps_businesses_YYYYMMDD_HHMMSS.csv`

Columns: name, business_type, address, city, phone, website, rating, reviews_count, data_source

## 🔧 Advanced Usage

```python
from google_maps_scraper import GoogleMapsScraper

scraper = GoogleMapsScraper(headless=True)  # Background mode
df = scraper.scrape_all_business_types('Tunis', ['doctors', 'jewelry'])
scraper.close()
```

## ⚠️ Requirements

- Python 3.7+
- Chrome browser
- Internet connection

## 🎉 Why This Works

1. **Scrapes directly from Google Maps** (not web search)
2. **50+ medical search terms** for comprehensive coverage
3. **Multi-language support** (Arabic, French, English)
4. **Scrolls to load more results** (100+ per search)
5. **Real-time data** from Google Maps

This scraper gets **real, current data** directly from Google Maps!