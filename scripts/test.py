def determine_category(class_name, type_name):
    # Categories
    residential = {
        "building": ["apartments", "block", "dormitory", "flats", "house", "home", "residential", "terrace", "yes", "detached", "church", "construction", "semidetached_house"],
        "place": ["apartments", "block", "dormitory", "flats", "house", "residential", "terrace", "yes"],
        "highway": ["residential", "cycleway", "tertiary", "footway", "living_street", "construction"],
        "amenity": ["dormitory"],
        "landuse": ["residential", "farmyard"],
        "leisure": ["garden"]
    }

    commercial = {
        "man_made": ["bridge"],
        "shop": ["money_lender", "convenience", "tattoo", "shoes", "funeral_directors", "mall", "clothes", "locksmith", "tobacco", "supermarket", "hunting", 
                "car_repair", "jewelry", "music", "mobile_phone", "houseware", "car", "car_parts", "department_store", "deli", "dry_cleaning", "laundry", 
                "fortune_teller", "chemist", "hearing_aids", "yes", "furniture", "newsagent", "hairdresser", "party", "car_rental", "beauty", "cannabis", 
                "country_store", "rental"],
        "highway": ["primary", "secondary", "trunk", "service", "motorway", "bus_stop", "pedestrian", "primary_link", "unclassified"],
        "tourism": ["attraction", "hotel", "artwork", "motel", "museum"],
        "historic": ["factory", "district", "building", "park"],
        "craft": ["plumber", "brewery", "hvac"],
        "healthcare": ["rehabilitation", "optometrist", "alternative"],
        "office": ["yes", "ngo", "tax_advisor", "estate_agent", "company"],
        "building": ["commercial", "garage", "hospital", "hotel", "industrial", "office", "public", "retail", "school", "shop", "stadium", "store", "train_station", "university"],
        "amenity": [
            "airport", "arts_centre", "atm", "auditorium", "bank", "bar", "bicycle_parking", "bicycle_rental", "brothel", "bureau_de_change", "bus_station", 
            "cafe", "car_rental", "car_wash", "casino", "cinema", "club", "college", "community_centre", "courthouse", "crematorium", "dentist", "doctors", 
            "driving_school", "embassy", "fast_food", "ferry_terminal", "fuel", "grave_yard", "hall", "health_centre", "hospital", "hotel", "ice_cream", 
            "library", "market", "marketplace", "nightclub", "office", "park", "parking", "pharmacy", "place_of_worship", "police", "post_office", "pub", 
            "reception_area", "restaurant", "sauna", "shop", "shopping", "social_club", "studio", "supermarket", "taxi", "theatre", "townhall", "veterinary", 
            "youth_centre", "kindergarten", "nursery", "nursing_home", "preschool", "retirement_home", "school", "university", "waste_disposal", "post_box", 
            "clinic", "conference_centre", "food_court", "social_centre", "waste_basket", "parking_entrance", "car_wash", "college", "bicycle_parking", 
            "bus_station", "social_centre", "casino", "conference_centre", "food_court", "marketplace", "fast_food", "dentist", "school", "waste_disposal", 
            "restaurant", "university", "arts_centre", "bar", "pharmacy", "place_of_worship", "bench", "parking"
        ],
        "landuse": ["commercial", "construction", "industrial"],
        "aeroway": ["terminal"],
        "railway": ["platform", "signal_box"],
        "leisure": ["fitness_centre", "playground", "pitch", "common", "golf_course", "swimming_pool", "sports_centre"],
        "boundary": ["administrative"],
        "junction": ["yes"]
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

# Example usage
category = determine_category('amenity', 'University')
print(category)  # Should print "Business"
category = determine_category('building', 'house')
print(category)  # Should print "Residential"