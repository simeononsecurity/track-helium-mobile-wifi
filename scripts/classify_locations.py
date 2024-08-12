import pandas as pd
from geopy.geocoders import Nominatim
import time

# Load the CSV data
csv_file = "data/wigle_results_with_location_type.csv"
df = pd.read_csv(csv_file)

# Initialize geolocator with a valid user-agent
geolocator = Nominatim(user_agent="track-helium-mobile-wifi/1.0")

# Function to determine the category based on class and type
def determine_category(class_name, type_name):
    residential = {
        "building": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace"],
        "amenity": ["dormitory", "kindergarten", "nursery", "nursing_home", "preschool", "retirement_home", "school", "university"],
        "landuse": ["residential", "farmyard"]
    }
    
    commercial = {
        "building": ["commercial", "garage", "hospital", "hotel", "industrial", "office", "public", "retail", "school", "shop", "stadium", "store", "train_station", "university"],
        "amenity": ["airport", "arts_centre", "atm", "auditorium", "bank", "bar", "bicycle_parking", "bicycle_rental", "brothel", "bureau_de_change", "bus_station", "cafe", 
                    "car_rental", "car_wash", "casino", "cinema", "club", "college", "community_centre", "courthouse", "crematorium", "dentist", "doctors", "driving_school", 
                    "embassy", "fast_food", "ferry_terminal", "fuel", "grave_yard", "hall", "health_centre", "hospital", "hotel", "ice_cream", "library", "market", "marketplace", 
                    "nightclub", "office", "park", "parking", "pharmacy", "place_of_worship", "police", "post_office", "pub", "reception_area", "restaurant", "sauna", "shop", 
                    "shopping", "social_club", "studio", "supermarket", "taxi", "theatre", "townhall", "veterinary", "youth_centre"],
        "landuse": ["commercial", "construction", "industrial"]
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
            print(f"Raw data: {location.raw}")
            
            class_name = location.raw.get('class', '')
            type_name = location.raw.get('type', '')
            print(f"Class: {class_name}, Type: {type_name}")
            
            category = determine_category(class_name, type_name)
            print(f"Determined category: {category}")
            return category
        else:
            print("No location found for the given coordinates.")
            return 'Unknown'
    except Exception as e:
        print(f"Error occurred while processing ({lat}, {lon}): {e}")
        return 'Error'

# Process each row one at a time and save the result to CSV
for index, row in df.iterrows():
    if pd.isna(row['location_type']) or row['location_type'] == 'Other':
        try:
            location_type = get_location_type(row['trilat'], row['trilong'])
            print(f"Processed {index + 1}/{len(df)}: ({row['trilat']}, {row['trilong']}) -> {location_type}")
            df.at[index, 'location_type'] = location_type
            
            # Save progress back to the CSV after each lookup
            df.to_csv(csv_file, index=False)
            
            time.sleep(1)  # Add a small delay to avoid overwhelming the geocoding service
        except Exception as e:
            print(f"Error occurred while processing row {index}: {e}")

