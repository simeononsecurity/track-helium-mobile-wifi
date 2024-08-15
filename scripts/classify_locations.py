import pandas as pd
from geopy.geocoders import Nominatim
import time
import os

# File paths
csv_file = "data/wigle_results.csv"
others_file = "data/other_class_type_combos.csv"

# Function to check if a file is empty
def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

# Check if the main CSV file exists and is not empty
if not os.path.exists(csv_file) or is_file_empty(csv_file):
    # Create the file with necessary columns if it doesn't exist or is empty
    df = pd.DataFrame(columns=[
        'trilat', 'trilong', 'ssid', 'qos', 'transid', 'firsttime', 'lasttime', 'lastupdt', 
        'netid', 'name', 'type', 'comment', 'wep', 'bcninterval', 'freenet', 'dhcp', 
        'paynet', 'userfound', 'channel', 'rcois', 'encryption', 'country', 'region', 
        'road', 'city', 'housenumber', 'postalcode', 'location_type'
    ])
    df.to_csv(csv_file, index=False)
else:
    # Load the existing CSV file
    print(f"Loading CSV file: {csv_file}")
    try:
        df = pd.read_csv(csv_file)
        print(f"CSV file loaded. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        df = pd.DataFrame(columns=[
            'trilat', 'trilong', 'ssid', 'qos', 'transid', 'firsttime', 'lasttime', 'lastupdt', 
            'netid', 'name', 'type', 'comment', 'wep', 'bcninterval', 'freenet', 'dhcp', 
            'paynet', 'userfound', 'channel', 'rcois', 'encryption', 'country', 'region', 
            'road', 'city', 'housenumber', 'postalcode', 'location_type'
        ])
        df.to_csv(csv_file, index=False)

# Initialize the geolocator with a valid user-agent
geolocator = Nominatim(user_agent="track-helium-mobile-wifi/1.0")

def determine_category(class_name, type_name):
    # Updated Categories
    residential = {
        "building": ["apartments", "block", "dormitory", "flats", "house", "home", "residential", "terrace", "yes", "detached", "construction", "semidetached_house"],
        "place": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace", "yes"],
        "highway": ["residential", "cycleway", "tertiary", "footway", "living_street", "construction"],
        "amenity": ["dormitory"],
        "landuse": ["residential", "farmyard"],
        "leisure": ["garden"]
    }

    commercial = {
        "man_made": ["bridge", "tower", "flagpole", "pier", "manhole", "mast", "works", "tunnel", "water_tower", "wastewater_plant", "storage_tank", "silo", "petroleum_well"],
        "shop": ["money_lender", "convenience", "tattoo", "shoes", "funeral_directors", "mall", "clothes", "locksmith", "tobacco", "supermarket", "hunting", 
                "car_repair", "jewelry", "music", "mobile_phone", "houseware", "car", "car_parts", "department_store", "deli", "dry_cleaning", "laundry", 
                "fortune_teller", "chemist", "hearing_aids", "yes", "furniture", "newsagent", "hairdresser", "party", "car_rental", "beauty", "cannabis", 
                "country_store", "rental", "dental_supplies", "motorcycle", "bicycle", "lighting", "alcohol", "variety_store", "garden_centre", "trade", 
                "doityourself", "radiotechnics", "art", "motorcycle_repair", "stationery", "tyres", "boutique", "beverages", "health_food", "toys", 
                "sports", "bakery", "gift", "wholesale", "caravan", "electronics", "copyshop", "e-cigarette", "storage_rental", "erotic", "antiques", 
                "vacant", "cosmetics", "yes", "optician", "charity", "books", "kitchen", "online", "fuel", "repair"],
        "highway": ["primary", "secondary", "trunk", "service", "motorway", "bus_stop", "pedestrian", "primary_link", "unclassified", "path", "track", 
                    "motorway_junction", "services", "trunk_link", "steps", "turning_loop"],
        "tourism": ["attraction", "hotel", "artwork", "motel", "museum", "viewpoint", "picnic_site", "gallery", "apartment", "theme_park"],
        "historic": ["factory", "district", "building", "park", "maritime", "memorial", "cemetery", "locomotive"],
        "craft": ["plumber", "brewery", "hvac", "insulation"],
        "healthcare": ["rehabilitation", "optometrist", "alternative"],
        "office": ["yes", "ngo", "tax_advisor", "estate_agent", "company", "coworking", "telecommunication", "government", "lawyer", "insurance", 
                "accountant", "association", "property_management", "financial"],
        "building": ["commercial", "church", "garage", "hospital", "hotel", "industrial", "office", "public", "retail", "school", "shop", "stadium", 
                    "store", "train_station", "university", "mixed", "storage", "warehouse", "civic", "transportation", "government"],
        "amenity": [
            "airport", "arts_centre", "atm", "auditorium", "bank", "bar", "bicycle_parking", "bicycle_rental", "brothel", "bureau_de_change", 
            "bus_station", "cafe", "car_rental", "car_wash", "casino", "cinema", "club", "college", "community_centre", "courthouse", 
            "crematorium", "dentist", "doctors", "driving_school", "embassy", "fast_food", "ferry_terminal", "fuel", "grave_yard", 
            "hall", "health_centre", "hospital", "hotel", "ice_cream", "library", "market", "marketplace", "nightclub", "office", 
            "park", "parking", "pharmacy", "place_of_worship", "police", "post_office", "pub", "reception_area", "restaurant", "sauna", 
            "shop", "shopping", "social_club", "studio", "supermarket", "taxi", "theatre", "townhall", "veterinary", "youth_centre", 
            "kindergarten", "nursery", "nursing_home", "preschool", "retirement_home", "school", "university", "waste_disposal", "post_box", 
            "clinic", "conference_centre", "food_court", "social_centre", "waste_basket", "parking_entrance", "car_wash", "college", 
            "bicycle_parking", "bus_station", "social_centre", "casino", "conference_centre", "food_court", "marketplace", "fast_food", 
            "dentist", "school", "waste_disposal", "restaurant", "university", "arts_centre", "bar", "pharmacy", "place_of_worship", 
            "bench", "parking", "fire_station", "loading_dock", "parking_space", "bicycle_repair_station", "toilets", "shelter", 
            "animal_boarding", "childcare", "social_facility", "recycling", "fountain", "research_institute", "animal_shelter", 
            "telephone", "vending_machine", "lifeguard", "drinking_water", "reception_desk"
        ],
        "landuse": ["commercial", "construction", "industrial"],
        "aeroway": ["terminal", "aerodrome", "hangar", "apron", "holding_position"],
        "railway": ["platform", "signal_box", "stop", "station", "junction", "subway_entrance", "yard"],
        "leisure": ["fitness_centre", "playground", "pitch", "common", "golf_course", "swimming_pool", "sports_centre", "dog_park", "outdoor_seating", 
                    "marina", "nature_reserve", "stadium", "village_green", "psychic", "picnic_table", "disc_golf_course", "bowling_alley"],
        "boundary": ["administrative"],
        "junction": ["yes"],
        "emergency": ["phone", "assembly_point", "lifeguard"],
        "club": ["social"]
    }

    # Convert inputs to lowercase to ensure case-insensitive comparison
    class_name = class_name.lower()
    type_name = type_name.lower()

    # Determine category
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
    if not os.path.exists(others_file) or is_file_empty(others_file):
        others_df = pd.DataFrame(columns=['class', 'type'])
    else:
        try:
            others_df = pd.read_csv(others_file)
        except pd.errors.EmptyDataError:
            print(f"Empty file encountered: {others_file}. Creating a new one.")
            others_df = pd.DataFrame(columns=['class', 'type'])

    # Append new "Other" class/type combination
    if not ((others_df['class'] == class_name) & (others_df['type'] == type_name)).any():
        new_row = pd.DataFrame({'class': [class_name], 'type': [type_name]})
        others_df = pd.concat([others_df, new_row], ignore_index=True)
        others_df.to_csv(others_file, index=False)
        print(f"Saved 'Other' combination: class={class_name}, type={type_name}")

# Process each row one at a time and save the result to the DataFrame in memory
save_counter = 0  # Counter to track how many changes have been made
for index, row in df.iterrows():
    if 'location_type' not in df.columns:
        print(f"Adding 'location_type' column for row {index}.")
        df['location_type'] = pd.NA

    print(f"Processing row {index + 1}/{len(df)}:")
    print(f"Data: {row.to_dict()}")
    
    if pd.isna(row['location_type']) or row['location_type'] == 'Other':
        try:
            location_type, class_name, type_name = get_location_type(row['trilat'], row['trilong'])
            print(f"Processed {index + 1}/{len(df)}: ({row['trilat']}, {row['trilong']}) -> {location_type}")
            
            if location_type == 'Other':
                save_other_combos(class_name, type_name)
                
            df.at[index, 'location_type'] = location_type
            
            save_counter += 1
            
            # Save every 10 rows or at the end of the loop
            if save_counter >= 10 or index == len(df) - 1:
                print(f"Saving data to CSV. {save_counter} rows updated.")
                df.to_csv(csv_file, index=False)
                save_counter = 0  # Reset counter
                time.sleep(3)  # Wait 3 seconds before continuing to avoid overwhelming services
        except Exception as e:
            print(f"Error occurred while processing row {index}: {e}")
            print(f"Data for failed row: {row.to_dict()}")
