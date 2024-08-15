import json

# File path to the categorized JSON file
categorized_json_file = "data/networks-categorized.json"

def calculate_percentage_for_inactive(categorized_file):
    with open(categorized_file, 'r') as f:
        categorized_data = json.load(f)

    # Counters for each category
    total_inactive_items = 0
    residential_count = 0
    business_count = 0
    other_count = 0

    # Count the occurrences of each category for inactive devices
    for item in categorized_data['items']:
        is_active = item.get('is_active', True)
        if not is_active:
            total_inactive_items += 1
            location_type = item.get('location_type', None)
            
            if location_type == "Residential":
                residential_count += 1
            elif location_type == "Business":
                business_count += 1
            else:
                other_count += 1

    # Debugging output
    print(f"Total Inactive Items: {total_inactive_items}")
    print(f"Residential Count: {residential_count}")
    print(f"Business Count: {business_count}")
    print(f"Other Count: {other_count}")

    # Calculate percentages
    if total_inactive_items > 0:
        residential_percentage = (residential_count / total_inactive_items) * 100
        business_percentage = (business_count / total_inactive_items) * 100
    else:
        residential_percentage = 0
        business_percentage = 0

    print(f"Residential Percentage: {residential_percentage:.2f}%")
    print(f"Business Percentage: {business_percentage:.2f}%")

# Calculate and print the percentages
calculate_percentage_for_inactive(categorized_json_file)
