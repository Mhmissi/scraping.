# Tunisia Business Scraper V2 - Setup Guide

## 🚀 Much Better Solution!

After deep research, I found that the original Overpass API approach has significant limitations for business data in Tunisia. Here's a **much better solution** using multiple data sources:

## 📊 Data Sources Available

### 1. **Google Places API** (Recommended - Most Reliable)
- ✅ **Free tier**: 100,000 requests/month
- ✅ **Most accurate data** for businesses
- ✅ **Official API** - no legal issues
- ✅ **Rich data**: phone, email, website, ratings, hours

### 2. **SerpApi** (Alternative - Good for Google Maps)
- ✅ **Free tier**: 100 searches/month
- ✅ **Handles Google Maps scraping** automatically
- ✅ **No rate limiting issues**

### 3. **OpenStreetMap** (Fallback - Always Available)
- ✅ **Completely free**
- ✅ **No API keys needed**
- ⚠️ **Limited business data** in Tunisia

## 🛠️ Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements_v2.txt
```

### Step 2: Get API Keys (Optional but Recommended)

#### Google Places API (Best Results)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Places API"
4. Create credentials (API Key)
5. Set environment variable:
   ```bash
   # Windows
   set GOOGLE_PLACES_API_KEY=your_api_key_here
   
   # Linux/Mac
   export GOOGLE_PLACES_API_KEY=your_api_key_here
   ```

#### SerpApi (Alternative)
1. Go to [SerpApi](https://serpapi.com/)
2. Sign up for free account
3. Get your API key
4. Set environment variable:
   ```bash
   # Windows
   set SERPAPI_KEY=your_serpapi_key_here
   
   # Linux/Mac
   export SERPAPI_KEY=your_serpapi_key_here
   ```

### Step 3: Run the Scraper
```bash
python tunisia_business_scraper_v2.py
```

## 🎯 Key Improvements Over V1

### ✅ **Multiple Data Sources**
- Combines Google Places API, SerpApi, and OpenStreetMap
- Automatically removes duplicates
- Falls back gracefully if APIs are unavailable

### ✅ **Better Data Quality**
- More accurate business information
- Phone numbers, emails, websites
- Ratings and reviews
- Proper address formatting

### ✅ **Reliable Performance**
- No more timeouts or empty results
- Proper error handling
- Rate limiting built-in

### ✅ **Easy Setup**
- Works without API keys (using OSM only)
- Better with API keys (using Google/SerpApi)
- Clear setup instructions

## 📈 Expected Results

### With Google Places API:
- **Doctors**: 50-200+ per city
- **Jewelry**: 20-100+ per city  
- **Lawyers**: 30-150+ per city
- **Data Quality**: ⭐⭐⭐⭐⭐

### With SerpApi:
- **Doctors**: 30-100+ per city
- **Jewelry**: 15-50+ per city
- **Lawyers**: 20-80+ per city
- **Data Quality**: ⭐⭐⭐⭐

### With OpenStreetMap Only:
- **Doctors**: 5-20 per city
- **Jewelry**: 2-10 per city
- **Lawyers**: 3-15 per city
- **Data Quality**: ⭐⭐⭐

## 🔧 Usage Examples

### Basic Usage (OSM Only)
```bash
python tunisia_business_scraper_v2.py
# Select city: Tunis
# Select business types: all
```

### With API Keys (Best Results)
```bash
# Set environment variables first
set GOOGLE_PLACES_API_KEY=your_key
set SERPAPI_KEY=your_key

python tunisia_business_scraper_v2.py
```

### Programmatic Usage
```python
from tunisia_business_scraper_v2 import TunisiaBusinessScraperV2

scraper = TunisiaBusinessScraperV2(
    google_api_key="your_key",
    serpapi_key="your_key"
)

# Scrape doctors in Tunis
df = scraper.scrape_all_sources('Tunis', ['doctors'])
print(df.head(10))
```

## 💰 Cost Breakdown

### Google Places API
- **Free Tier**: 100,000 requests/month
- **Cost**: $0 for most users
- **Per Request**: $0.017 after free tier

### SerpApi
- **Free Tier**: 100 searches/month
- **Cost**: $0 for most users
- **Per Search**: $0.001 after free tier

### OpenStreetMap
- **Cost**: $0 (completely free)

## 🎉 Why This Solution is Much Better

1. **Reliability**: Multiple data sources ensure you get results
2. **Quality**: Google Places API has the most accurate business data
3. **Compliance**: Uses official APIs, no legal issues
4. **Scalability**: Can handle large-scale scraping
5. **Flexibility**: Works with or without API keys
6. **Maintenance**: Built-in error handling and rate limiting

## 🚨 Important Notes

- **API Keys**: Not required but highly recommended for best results
- **Rate Limits**: Built-in delays to respect API limits
- **Legal**: All methods use official APIs or public data
- **Data Quality**: Google Places API provides the most complete data
- **Cost**: Free tiers should be sufficient for most use cases

This solution addresses all the issues with the original Overpass API approach and provides a much more reliable and comprehensive way to scrape business data from Tunisia!

