import json
from collections import Counter
import os

# Paths to the JSON files and the HTML file
networks_file_path = 'data/networks.json'
categorized_file_path = 'data/networks-categorized.json'
html_file_path = 'README.md'

# Function to generate markdown table
def generate_markdown_table(headers, rows):
    table = '| ' + ' | '.join(headers) + ' |\n'
    table += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
    for row in rows:
        table += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
    return table

# Function to analyze the data and create tables
def analyze_data(networks_data, categorized_data):
    inactive_count = sum(1 for item in networks_data['items'] if not item['is_active'])
    active_count = len(categorized_data['items'])
    total_devices = active_count + inactive_count
    
    # Updated counts only for active devices using categorized_data
    residential_count = sum(1 for item in categorized_data['items'] if item['location_type'] == 'Residential')
    business_count = sum(1 for item in categorized_data['items'] if item['location_type'] == 'Business')

    # Updated class-type combinations only for active devices using categorized_data
    class_type_combinations = [(item['class'], item['type']) for item in categorized_data['items']]
    top_class_type_combos = Counter(class_type_combinations).most_common(10)

    # Calculate the total number of active devices
    total_active_devices = len(categorized_data['items'])

    # Creating tables
    active_inactive_table = generate_markdown_table(
        ['Status', 'Count'],
        [['Active', active_count], ['Inactive', inactive_count]]
    )
    
    # Updated residential vs business table relative to total active devices
    residential_business_table = generate_markdown_table(
        ['Category', 'Percentage'],
        [['Residential', f"{(residential_count / total_active_devices) * 100:.2f}%"],
        ['Business', f"{(business_count / total_active_devices) * 100:.2f}%"]]
    )
    
    top_class_type_table = generate_markdown_table(
        ['Class', 'Type', 'Count'],
        [(cls, typ, count) for (cls, typ), count in top_class_type_combos]
    )

    return active_inactive_table, residential_business_table, top_class_type_table

# Load the JSON data
with open(networks_file_path, 'r') as file:
    networks_data = json.load(file)

with open(categorized_file_path, 'r') as file:
    categorized_data = json.load(file)

# Analyze the data
active_inactive_table, residential_business_table, top_class_type_table = analyze_data(networks_data, categorized_data)

# Replacement content
replacement_content = (
    f"## Device Status\n\n{active_inactive_table}\n\n"
    f"## Residential vs Business\n\n{residential_business_table}\n\n"
    f"## Top 10 Class-Type Combinations\n\n{top_class_type_table}\n"
)

# Read the HTML file
with open(html_file_path, 'r') as file:
    html_content = file.read()

# Replace the content between the comments
start_marker = '<!-- HELIUM PROVIDED LOCATION STATS START -->'
end_marker = '<!-- HELIUM PROVIDED LOCATION STATS END -->'

if start_marker in html_content and end_marker in html_content:
    start_index = html_content.index(start_marker) + len(start_marker)
    end_index = html_content.index(end_marker)
    new_html_content = html_content[:start_index] + '\n\n' + replacement_content + '\n' + html_content[end_index:]
    
    # Write the new content back to the file
    with open(html_file_path, 'w') as file:
        file.write(new_html_content)

    print("Content replaced successfully!")
else:
    print("Markers not found in the file. Please ensure the start and end markers are present.")
