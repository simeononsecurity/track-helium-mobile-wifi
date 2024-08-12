import pandas as pd
from geopy.geocoders import Nominatim
import time
import os

# File paths
csv_file = "data/wigle_results.csv"
others_file = "data/other_class_type_combos.csv"

# Check if the main CSV file exists
if not os.path.exists(csv_file):
    # Create the file with necessary columns if it doesn't exist
    df = pd.DataFrame(columns=[
        'trilat', 'trilong', 'ssid', 'qos', 'transid', 'firsttime', 'lasttime', 'lastupdt', 
        'netid', 'name', 'type', 'comment', 'wep', 'bcninterval', 'freenet', 'dhcp', 
        'paynet', 'userfound', 'channel', 'rcois', 'encryption', 'country', 'region', 
        'road', 'city', 'housenumber', 'postalcode', 'location_type'
    ])
    df.to_csv(csv_file, index=False)
else:
    # Load the existing CSV file
    df = pd.read_csv(csv_file)

    # Ensure the 'location_type' column exists, add it if not
    if 'location_type' not in df.columns:
        df['location_type'] = pd.NA

# Initialize the geolocator with a valid user-agent
geolocator = Nominatim(user_agent="track-helium-mobile-wifi/1.0")

# Updated function to determine the category based on class and type
def determine_category(class_name, type_name):
    residential = {
        "building": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace", "yes", "detached", "church", "construction"],
        "place": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace", "yes"],
        "highway": ["residential", "cycleway", "tertiary", "footway"],
        "amenity": ["dormitory"],
        "landuse": ["residential", "farmyard"],
        "leisure": ["garden"]
    }
    
    commercial = {
        "man_made": ["bridge"],
        "shop": ["money_lender", "convenience", "tattoo", "shoes", "funeral_directors", "mall", "clothes", "locksmith", "tobacco", "supermarket", "hunting"],
        "highway": ["primary", "secondary", "trunk", "service", "motorway"],
        "tourism": ["attraction", "hotel", "artwork"],
        "historic": ["factory"],
        "craft": ["plumber", "brewery"],
        "healthcare": ["rehabilitation"],
        "office": ["yes", "ngo"],
        "building": ["commercial", "garage", "hospital", "hotel", "industrial", "office", "public", "retail", "school", "shop", "stadium", "store", "train_station", "university"],
        "amenity": ["airport", "arts_centre", "atm", "auditorium", "bank", "bar", "bicycle_parking", "bicycle_rental", "brothel", "bureau_de_change", "bus_station", "cafe", 
                    "car_rental", "car_wash", "casino", "cinema", "club", "college", "community_centre", "courthouse", "crematorium", "dentist", "doctors", "driving_school", 
                    "embassy", "fast_food", "ferry_terminal", "fuel", "grave_yard", "hall", "health_centre", "hospital", "hotel", "ice_cream", "library", "market", "marketplace", 
                    "nightclub", "office", "park", "parking", "pharmacy", "place_of_worship", "police", "post_office", "pub", "reception_area", "restaurant", "sauna", "shop", 
                    "shopping", "social_club", "studio", "supermarket", "taxi", "theatre", "townhall", "veterinary", "youth_centre", "kindergarten", "nursery", "nursing_home", "preschool", "retirement_home", "school", "university", "waste_disposal", "post_box"],
        "landuse": ["commercial", "construction", "industrial"],
        "aeroway": ["terminal"],
        "railway": ["platform"],
        "leisure": ["fitness_centre", "playground", "pitch"],
        "amenity": ["bench"]
    }
    
    if class_name in residential and type_name in residential[class_name]:
        return "Residential"
    elif class_name in commercial and type_name in commercial[class_name]:
        return "Business"
    else:
        return "Other"

# Function to get location type and print out all associated values
def get_location_type(lat, lon):
    try:
        print(f"Attempting to reverse geocode for coordinates: ({lat}, {lon})")
        location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
        
        if location:
            print(f"Location found: {location}")
            print(f"Full address: {location.address}")
            class_name = location.raw.get('class', '')
            type_name = location.raw.get('type', '')
            print(f"Class: {class_name}, Type: {type_name}")
            
            category = determine_category(class_name, type_name)
            print(f"Determined category: {category}")
            return category, class_name, type_name
        else:
            print("No location found for the given coordinates.")
            return 'Unknown', '', ''
    except Exception as e:
        print(f"Error occurred while processing ({lat}, {lon}): {e}")
        return 'Error', '', ''

# Function to save class/type combinations that are categorized as "Other"
def save_other_combos(class_name, type_name):
    if not os.path.exists(others_file):
        others_df = pd.DataFrame(columns=['class', 'type'])
    else:
        others_df = pd.read_csv(others_file)

    # Append new "Other" class/type combination
    if not ((others_df['class'] == class_name) & (others_df['type'] == type_name)).any():
        new_row = pd.DataFrame({'class': [class_name], 'type': [type_name]})
        others_df = pd.concat([others_df, new_row], ignore_index=True)
        others_df.to_csv(others_file, index=False)
        print(f"Saved 'Other' combination: class={class_name}, type={type_name}")

# Process each row one at a time and save the result to CSV
for index, row in df.iterrows():
    if pd.isna(row['location_type']) or row['location_type'] == 'Other':
        try:
            location_type, class_name, type_name = get_location_type(row['trilat'], row['trilong'])
            print(f"Processed {index + 1}/{len(df)}: ({row['trilat']}, {row['trilong']}) -> {location_type}")
            df.at[index, 'location_type'] = location_type
            
            # Save progress back to the CSV after each lookup
            df.to_csv(csv_file, index=False)
            
            # Save class/type combinations that are categorized as "Other"
            if location_type == "Other" and class_name and type_name:
                save_other_combos(class_name, type_name)
            
            time.sleep(1)  # Add a small delay to avoid overwhelming the geocoding service
        except Exception as e:
            print(f"Error occurred while processing row {index}: {e}")

