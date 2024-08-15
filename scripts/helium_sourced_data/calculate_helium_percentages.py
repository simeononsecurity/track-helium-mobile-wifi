import json

# File path to the categorized JSON file
categorized_json_file = "data/networks-categorized.json"

def calculate_percentages(categorized_file):
    with open(categorized_file, 'r') as f:
        categorized_data = json.load(f)

    # Counters for active and inactive devices
    total_active_items = 0
    total_inactive_items = 0
    residential_active_count = 0
    business_active_count = 0
    other_active_count = 0
    residential_inactive_count = 0
    business_inactive_count = 0
    other_inactive_count = 0

    # Count the occurrences of each category for both active and inactive devices
    for item in categorized_data['items']:
        is_active = item.get('is_active', False)
        location_type = item.get('location_type', None)
        
        if is_active:
            total_active_items += 1
            if location_type == "Residential":
                residential_active_count += 1
            elif location_type == "Business":
                business_active_count += 1
            else:
                other_active_count += 1
        else:
            total_inactive_items += 1
            if location_type == "Residential":
                residential_inactive_count += 1
            elif location_type == "Business":
                business_inactive_count += 1
            else:
                other_inactive_count += 1

    # Debugging output
    print(f"Total Active Items: {total_active_items}")
    print(f"Residential Count (Active): {residential_active_count}")
    print(f"Business Count (Active): {business_active_count}")
    print(f"Other Count (Active): {other_active_count}")
    print(f"Total Inactive Items: {total_inactive_items}")
    print(f"Residential Count (Inactive): {residential_inactive_count}")
    print(f"Business Count (Inactive): {business_inactive_count}")
    print(f"Other Count (Inactive): {other_inactive_count}")

    # Calculate percentages relative to the count of active devices
    if total_active_items > 0:
        residential_percentage = (residential_active_count / total_active_items) * 100
        business_percentage = (business_active_count / total_active_items) * 100
    else:
        residential_percentage = 0
        business_percentage = 0

    print(f"Residential Percentage (Active): {residential_percentage:.2f}%")
    print(f"Business Percentage (Active): {business_percentage:.2f}%")

# Calculate and print the counts and percentages
calculate_percentages(categorized_json_file)
