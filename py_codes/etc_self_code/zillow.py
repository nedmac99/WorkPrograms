from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import time

# Replace this with your actual Zillow Web Services ID
ZWSID = "YOUR_ZWSID_HERE"

def fetch_property_data(address, zipcode):
    zillow_data = ZillowWrapper(ZWSID)
    try:
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        result = GetDeepSearchResults(deep_search_response)

        print(f"\n🏡 Property Info for {address}, {zipcode}")
        print(f"Zestimate: ${result.zestimate_amount}")
        print(f"Bedrooms: {result.bedrooms}")
        print(f"Bathrooms: {result.bathrooms}")
        print(f"Home Type: {result.home_type}")
        print(f"Year Built: {result.year_built}")
        print(f"Square Feet: {result.home_size}")
        print(f"Last Sold Date: {result.last_sold_date}")
        print(f"Last Sold Price: ${result.last_sold_price}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    address = input("Enter street address (e.g., 123 Main St): ").strip()
    zipcode = input("Enter ZIP code: ").strip()
    
    while True:
        fetch_property_data(address, zipcode)
        print("\n⏳ Waiting 5 minutes before next update...\n")
        time.sleep(300)  # Waits 5 minutes before updating

if __name__ == "__main__":
    main()