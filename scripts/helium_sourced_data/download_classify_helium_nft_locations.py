import os
import json
import time
import requests
import csv
from geopy.geocoders import Nominatim

# File paths
json_file = "data/network.json"
categorized_json_file = "data/networks-categorized.json"
other_class_type_file = "data/other_class_type_combos.csv"
json_url = "https://entities.nft.helium.io/v2/hotspots?subnetwork=mobile"

# Function to check if a file is empty
def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

# Download the network.json file
def download_json(url, file_path):
    response = requests.get(url)
    with open(file_path, 'w') as f:
        f.write(response.text)
    print(f"Downloaded JSON data to {file_path}")

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
        location = geolocator.reverse((lat, lon), exactly_one=True)  # Fixing the coordinate pair format
        
        if location:
            class_name = location.raw.get('class', '')
            type_name = location.raw.get('type', '')
            
            print(f"Location found: Class = {class_name}, Type = {type_name}")
            
            category = determine_category(class_name, type_name)
            return category, class_name, type_name
        else:
            print("No location found for the given coordinates.")
            return 'Unknown', '', ''
    except Exception as e:
        print(f"Error occurred while processing ({lat}, {lon}): {e}")
        return 'Error', '', ''

# Function to process the JSON data and save it every 10 locations
def process_json_data(input_file, output_file, other_class_type_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            categorized_data = json.load(f)
    else:
        categorized_data = {"items": []}
    
    total_items = len(data['items'])
    processed_count = 0

    with open(other_class_type_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        for index, item in enumerate(data['items']):
            lat = item.get('lat')
            lon = item.get('long')
            is_active = item.get('is_active', True)

            # Skip processing if the location is not active
            if not is_active:
                print(f"Skipping inactive item at ({lat}, {lon})")
                processed_count += 1
                continue

            existing_item = next((existing_item for existing_item in categorized_data['items']
                                  if existing_item.get('lat') == lat and existing_item.get('long') == lon), None)

            # Skip if the item is categorized as something other than "Other" and already known
            if existing_item and existing_item.get('location_type') not in [None, 'Other']:
                print(f"Skipping already categorized item at ({lat}, {lon})")
                processed_count += 1
                continue

            if lat is not None and lon is not None:
                location_type, class_name, type_name = get_location_type(lat, lon)
                item['location_type'] = location_type
                item['class'] = class_name
                item['type'] = type_name
                item['category'] = location_type  # Save the category in the JSON output

                # If categorized as 'Other', save class and type to CSV
                if location_type == 'Other':
                    print(f"Saving 'Other' category for ({class_name}, {type_name})")
                    csvwriter.writerow([class_name, type_name])

                categorized_data['items'].append(item)
                processed_count += 1
                
                # Show progress indicator
                print(f"Processed {processed_count}/{total_items} locations ({(processed_count/total_items)*100:.2f}% complete)")

                time.sleep(1)  # To avoid overwhelming the geocoding service

                # Save every 10 locations
                if processed_count % 10 == 0 or index == len(data['items']) - 1:
                    with open(output_file, 'w') as f_out:
                        json.dump(categorized_data, f_out, indent=4)
                    print(f"Processed data saved to {output_file}. {processed_count} locations processed.")

# Download the network.json file if it doesn't exist or is empty
if not os.path.exists(json_file) or is_file_empty(json_file):
    download_json(json_url, json_file)

# Process the JSON data and save it to the categorized JSON file
process_json_data(json_file, categorized_json_file, other_class_type_file)
