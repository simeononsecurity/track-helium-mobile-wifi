import os
import json
import time
import requests
import csv
from geopy.geocoders import Nominatim

# File paths
json_file = "data/networks.json"
categorized_json_file = "data/networks-categorized.json"
other_class_type_file = "data/other_class_type_combos.csv"
json_url = "https://entities.nft.helium.io/v2/hotspots?subnetwork=mobile"

# Function to check if a file is empty
def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

# Download the network.json file, handling pagination with cursor
def download_json(url, file_path):
    all_data = []
    while url:
        response = requests.get(url)
        if response.status_code == 404:
            print("No more data available, stopping download.")
            break
        
        data = response.json()
        all_data.extend(data.get('items', []))
        
        # Check if a cursor is provided for the next page
        cursor = data.get('cursor')
        if cursor:
            url = f"{json_url}&cursor={cursor}"
            print(f"Fetching next page with cursor: {cursor}")
        else:
            print("No cursor found, stopping download.")
            break

        time.sleep(1)  # Add a short delay to avoid overwhelming the server

    # Save all concatenated data into a single JSON file
    with open(file_path, 'w') as f:
        json.dump({"items": all_data}, f, indent=4)
    print(f"Downloaded and saved JSON data to {file_path}")

# Initialize the geolocator with a valid user-agent
geolocator = Nominatim(user_agent="track-helium-mobile-wifi/1.0")

# Function to categorize the class and type of a location
def determine_category(class_name, type_name):
    # Your existing residential and commercial categories here
    residential = {
        "building": ["apartments", "block", "dormitory", "flats", "house", "home", "residential", "terrace", "yes", "detached", "construction", "semidetached_house", "static_caravan"],
        "place": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace", "yes"],
        "highway": ["residential", "cycleway", "tertiary", "footway", "living_street", "construction", "bridleway", "elevator", "raceway"],
        "amenity": ["dormitory", "trailer_park", "events_venue"],
        "landuse": ["residential", "farmyard"],
        "leisure": ["garden", "recreation_ground", "fitness_station", "slipway"],
        "historic": ["heritage"],
        "club": ["religion"]
    }

    commercial = {
        "man_made": ["bridge", "tower", "flagpole", "pier", "manhole", "mast", "works", "tunnel", "water_tower", "wastewater_plant", "storage_tank", "silo", "petroleum_well", "water_tower", "flare", "surveillance", "reservoir_covered", "chimney", "lighthouse", "water_works"],
        "shop": ["money_lender", "convenience", "tattoo", "shoes", "funeral_directors", "mall", "clothes", "locksmith", "tobacco", "supermarket", "hunting", 
                "car_repair", "jewelry", "music", "mobile_phone", "houseware", "car", "car_parts", "department_store", "deli", "dry_cleaning", "laundry", 
                "fortune_teller", "chemist", "hearing_aids", "yes", "furniture", "newsagent", "hairdresser", "party", "car_rental", "beauty", "cannabis", 
                "country_store", "rental", "dental_supplies", "motorcycle", "bicycle", "lighting", "alcohol", "variety_store", "garden_centre", "trade", 
                "doityourself", "radiotechnics", "art", "motorcycle_repair", "stationery", "tyres", "boutique", "beverages", "health_food", "toys", 
                "sports", "bakery", "gift", "wholesale", "caravan", "electronics", "copyshop", "e-cigarette", "storage_rental", "erotic", "antiques", 
                "vacant", "cosmetics", "yes", "optician", "charity", "books", "kitchen", "online", "fuel", "repair", "paint", "hardware", "craft", "watches", "florist", "clothes;_wedding", "hairdresser_supply", "weapons"],
        "highway": ["primary", "secondary", "trunk", "service", "motorway", "bus_stop", "pedestrian", "primary_link", "unclassified", "path", "track", 
                    "motorway_junction", "services", "trunk_link", "steps", "turning_loop", "motorway_link", "toll_gantry"],
        "tourism": ["attraction", "hotel", "artwork", "motel", "museum", "viewpoint", "picnic_site", "gallery", "apartment", "theme_park", "camp_site", "zoo", "aquarium", "caravan_site"],
        "historic": ["factory", "district", "building", "park", "maritime", "memorial", "cemetery", "locomotive", "tomb", "ruins", "heritage"],
        "craft": ["plumber", "brewery", "hvac", "insulation", "stonemason", "electronics_repair", "welder", "window_construction", "upholsterer"],
        "healthcare": ["rehabilitation", "optometrist", "alternative", "nurse"],
        "office": ["yes", "ngo", "tax_advisor", "estate_agent", "company", "coworking", "telecommunication", "government", "lawyer", "insurance", 
                "accountant", "association", "property_management", "financial", "therapist", "educational_institution", "consulting", "software"],
        "building": ["commercial", "church", "garage", "hospital", "hotel", "industrial", "office", "public", "retail", "school", "shop", "stadium", 
                    "store", "train_station", "university", "mixed", "storage", "warehouse", "civic", "transportation", "government", "fire_station", "parking"],
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
            "telephone", "vending_machine", "lifeguard", "drinking_water", "reception_desk", "paint", "post_depot", "money_transfer", "events_venue", "prison", "charging_station"],
        "landuse": ["commercial", "construction", "industrial"],
        "aeroway": ["terminal", "aerodrome", "hangar", "apron", "holding_position", "runway", "windsock", "navigationaid"],
        "railway": ["platform", "signal_box", "stop", "station", "junction", "subway_entrance", "yard", "service_station"],
        "leisure": ["fitness_centre", "playground", "pitch", "common", "golf_course", "swimming_pool", "sports_centre", "dog_park", "outdoor_seating", 
                    "marina", "nature_reserve", "stadium", "village_green", "psychic", "picnic_table", "disc_golf_course", "bowling_alley", "track", 
                    "recreation_ground", "slipway", "ice_rink", "water_park", "amusement_arcade", "trampoline_park", "resort"],
        "boundary": ["administrative"],
        "junction": ["yes"],
        "emergency": ["phone", "assembly_point", "lifeguard", "ambulance_station", "psap"],
        "club": ["social", "religion", "yes"]
    }

    class_name = class_name.lower()
    type_name = type_name.lower()

    if class_name in residential and type_name in residential[class_name]:
        return "Residential"
    elif class_name in commercial and type_name in commercial[class_name]:
        return "Business"
    else:
        return "Other"

# Function to get location type and print out all associated values
def get_location_type(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            class_name = location.raw.get('class', '')
            type_name = location.raw.get('type', '')
            category = determine_category(class_name, type_name)
            return category, class_name, type_name
        else:
            return 'Unknown', '', ''
    except Exception as e:
        print(f"Error occurred while processing ({lat}, {lon}): {e}")
        return 'Error', '', ''

# Function to process the JSON data
def process_json_data(input_file, output_file, other_class_type_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            categorized_data = json.load(f)
    else:
        categorized_data = {"items": []}

    categorized_items_dict = {
        (item['key_to_asset_key'], item['entity_key_str']): item for item in categorized_data['items']
    }

    total_items = len(data['items'])
    processed_count = 0

    with open(other_class_type_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        for index, item in enumerate(data['items']):
            lat = item.get('lat')
            lon = item.get('long')
            is_active = item.get('is_active', True)
            key_to_asset_key = item.get('key_to_asset_key')
            entity_key_str = item.get('entity_key_str')

            if not is_active:
                processed_count += 1
                continue

            existing_item = categorized_items_dict.get((key_to_asset_key, entity_key_str))

            # If the item exists and either lacks a location or is categorized as "Other" or location changed, update it
            if existing_item:
                if (
                    existing_item.get('location_type') == 'Other' or
                    existing_item.get('lat') != lat or
                    existing_item.get('long') != lon or
                    not existing_item.get('lat') or not existing_item.get('long')
                ):
                    # Process and update the item
                    location_type, class_name, type_name = get_location_type(lat, lon)
                    item['location_type'] = location_type
                    item['class'] = class_name
                    item['type'] = type_name
                    item['category'] = location_type

                    if location_type == 'Other':
                        csvwriter.writerow([class_name, type_name])

                    existing_item.update(item)
                    print(f"Updated existing item: {key_to_asset_key}, {entity_key_str}")
                    print(f"Location Type: {location_type}, Class: {class_name}, Type: {type_name}")
                else:
                    print(f"Skipping unchanged item: {key_to_asset_key}, {entity_key_str}")
                    processed_count += 1
                    continue
            else:
                # Process and add the new item
                if lat is not None and lon is not None:
                    location_type, class_name, type_name = get_location_type(lat, lon)
                    item['location_type'] = location_type
                    item['class'] = class_name
                    item['type'] = type_name

                    if location_type == 'Other':
                        csvwriter.writerow([class_name, type_name])

                    categorized_data['items'].append(item)
                    print(f"Added new item: {key_to_asset_key}, {entity_key_str}")
                    print(f"Location Type: {location_type}, Class: {class_name}, Type: {type_name}")

            processed_count += 1

            # Progress indicator
            progress = (processed_count / total_items) * 100
            print(f"Progress: {progress:.2f}% ({processed_count}/{total_items} locations processed)")

            time.sleep(1)  # Avoid overwhelming the geocoding service

            if processed_count % 10 == 0 or index == len(data['items']) - 1:
                with open(output_file, 'w') as f_out:
                    json.dump(categorized_data, f_out, indent=4)
                print(f"Processed data saved to {output_file}")

# Download the network.json file if it doesn't exist or is empty
if not os.path.exists(json_file) or is_file_empty(json_file):
    download_json(json_url, json_file)

# Process the JSON data and save it to the categorized JSON file
process_json_data(json_file, categorized_json_file, other_class_type_file)
