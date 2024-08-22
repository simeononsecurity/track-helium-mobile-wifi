import requests
import json
import os
import pandas as pd

# Directory to save the downloaded JSON files
output_dir = "data/helium_data"
os.makedirs(output_dir, exist_ok=True)

# List of URLs to download the JSON files
urls = [
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_count_hotspots_onboarded.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_count_subscriber_nfts.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/daily_subscribers_per_hmh_on_carrier_2.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/hotspots_serving_carrier_2.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_data_transfer_gb_on_carrier_2.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_subscribers_on_carrier_2.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/daily_subscribers_per_hmh_on_carrier_1.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/hotspots_serving_carrier_1.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_data_transfer_gb_on_carrier_1.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_subscribers_on_carrier_1.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/daily_subscribers_per_hmh_on_carrier_partners.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/hotspots_serving_carrier_partners.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_data_transfer_gb_on_carrier_partners.json",
    "https://helium-mobile-prod-metrics.s3.us-west-2.amazonaws.com/v0/latest/cumulative_subscribers_on_carrier_partners.json"
]

# Download the JSON files
for url in urls:
    filename = os.path.join(output_dir, os.path.basename(url))
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'w') as file:
            json.dump(response.json(), file)
        print(f"Downloaded and saved: {filename}")
    else:
        print(f"Failed to download: {url}")
