import requests
import csv
import json
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# API credentials from environment variables
api_name = os.getenv("API_NAME")
api_token = os.getenv("API_TOKEN")
auth_header = os.getenv("AUTH_HEADER")

# Check that the API credentials are not null
if not api_name or not api_token or not auth_header:
    raise ValueError("API_NAME, API_TOKEN, and AUTH_HEADER must be set in the environment variables.")

# Initial API URL
base_url = "https://api.wigle.net/api/v2/network/search"

# Define the folder paths
current_path = os.getcwd()
data_path = os.path.join(current_path, 'data')
output_path = os.path.join(current_path, 'output')

# Ensure directories exist
os.makedirs(data_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

# File paths
last_page_file = os.path.join(data_path, "last_page.json")
csv_file = os.path.join(data_path, "wigle_results.csv")

# Load the last "searchAfter" value if it exists
if os.path.exists(last_page_file):
    with open(last_page_file, 'r') as f:
        last_page_data = json.load(f)
        last_search_after = last_page_data.get("searchAfter", "")
else:
    last_search_after = "0"

# Set headers
headers = {
    "Authorization": auth_header,
    "Accept": "application/json"
}

def fetch_data(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def save_last_page(search_after_value):
    with open(last_page_file, 'w') as f:
        json.dump({"searchAfter": search_after_value}, f)

def append_to_csv(data, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if the file does not exist
            writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
    print(f"Appended {len(data)} results to {csv_file}")

error_count = 0
start_time = datetime.now()
successfully_finished = False

ssid_patterns = ["Helium Mobile", "Helium Free WiFi", "Helium Free Wi-Fi"]
ssidlike = "Helium %"  # Use wildcard to search for Helium-related SSIDs

params = {
    "onlymine": "false",
    "startTransID": "20240101-00000",
    "freenet": "false",
    "paynet": "false",
    "ssidlike": ssidlike,
    "resultsPerPage": "1000",
    "searchAfter": last_search_after
}

while error_count <= 1 and not successfully_finished:
    try:
        # Check if 20 minutes have passed since the start time
        if datetime.now() - start_time > timedelta(minutes=20):
            print("20 minutes have elapsed. Exiting.")
            break

        # Fetch data
        data = fetch_data(base_url, params, headers)

        # Extract results
        results = data.get("results", [])
        if not results:
            print("No more results for SSID pattern:", ssidlike)
            successfully_finished = True
            break

        print(f"Fetched {len(results)} results for SSID pattern: {ssidlike}")

        # Filter results for the desired SSIDs
        filtered_results = [
            result for result in results
            if result.get("ssid") in ssid_patterns
        ]

        if filtered_results:
            # Append filtered results to CSV
            append_to_csv(filtered_results, csv_file)

        # Get the next "searchAfter" value
        search_after = data.get("searchAfter")
        if not search_after:
            print("No searchAfter value found. Exiting.")
            successfully_finished = True
            break

        # Save the last "searchAfter" value
        save_last_page(search_after)

        # Update the params for the next request
        params["searchAfter"] = search_after

        # Reset error count after a successful loop
        error_count = 0

        # To avoid hitting rate limits or being blocked
        time.sleep(5)  # Adjust the sleep time as necessary

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

        if error_count > 1:
            print("Too many errors. Stopping the loop.")
            break  # Stop the loop after more than one error

        if e.response and e.response.status_code == 429:  # Too Many Requests
            retry_after = int(e.response.headers.get("Retry-After", 60))  # Default to 60 seconds if not provided
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            error_count += 1  # Increment error count for rate limit errors
        else:
            error_count += 1  # Increment error count for other errors

    except Exception as e:
        print(f"An error occurred: {e}")
        error_count += 1  # Increment error count for other exceptions
        if error_count > 1:
            print("Too many errors. Stopping the loop.")
            break  # Stop the loop after more than one error

print(f'Data has been saved to {csv_file}')
