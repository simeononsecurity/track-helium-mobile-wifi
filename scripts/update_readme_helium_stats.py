import json
import os
import matplotlib.pyplot as plt
from collections import Counter

# Paths to the JSON files and the HTML file
networks_file_path = 'data/helium_data/networks.json'
categorized_file_path = 'data/helium_data/networks-categorized.json'
cumulative_data_transfer_path = 'data/helium_data/cumulative_data_transfer_gb_on_carrier_partners.json'
cumulative_subscribers_path = 'data/helium_data/cumulative_subscribers_on_carrier_partners.json'
daily_subscribers_path = 'data/helium_data/daily_subscribers_per_hmh_on_carrier_partners.json'
hotspots_serving_path = 'data/helium_data/hotspots_serving_carrier_partners.json'
html_file_path = 'README.md'
images_dir = os.path.join('output')  # Set images directory to "output"

# Ensure the images directory exists
os.makedirs(images_dir, exist_ok=True)

# Function to generate markdown table
def generate_markdown_table(headers, rows):
    table = '| ' + ' | '.join(headers) + ' |\n'
    table += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
    for row in rows:
        table += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
    return table

# Function to compute daily values from cumulative data
def compute_daily_values(cumulative_values):
    daily_values = []
    for i in range(1, len(cumulative_values)):
        daily_values.append(cumulative_values[i] - cumulative_values[i - 1])
    return daily_values

# Function to create a line chart and save it as an image
def create_line_chart(dates, values, title, ylabel, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    image_path = os.path.join(images_dir, filename)
    plt.savefig(image_path)
    plt.close()
    return image_path

# Function to analyze the data, create tables, and generate charts
def analyze_data(networks_data, categorized_data, cumulative_data, subscribers_data, daily_subscribers_data, hotspots_data):
    inactive_count = sum(1 for item in networks_data['items'] if not item['is_active'])
    active_count = len(categorized_data['items'])
    total_devices = active_count + inactive_count
    
    # Updated counts only for active devices using categorized_data
    residential_count = sum(1 for item in categorized_data['items'] if item['location_type'] == 'Residential')
    business_count = sum(1 for item in categorized_data['items'] if item['location_type'] == 'Business')

    # Creating tables
    active_inactive_table = generate_markdown_table(
        ['Status', 'Count'],
        [['Active', active_count], ['Inactive', inactive_count]]
    )
    
    # Updated residential vs business table relative to the total number of devices with locations
    residential_business_table = generate_markdown_table(
        ['Category', 'Percentage'],
        [['Residential', f"{(residential_count / (residential_count + business_count)) * 100:.2f}%"],
        ['Business', f"{(business_count / (residential_count + business_count)) * 100:.2f}%"]]
    )

    # Top class-type combinations
    top_class_type_combos = Counter((item['class'], item['type']) for item in categorized_data['items']).most_common(10)
    top_class_type_table = generate_markdown_table(
        ['Class', 'Type', 'Count'],
        [(cls, typ, count) for (cls, typ), count in top_class_type_combos]
    )

    # Extracting dates and cumulative values
    dates_transfer = [entry['time'] for entry in cumulative_data['historical_daily']]
    cumulative_data_values = [entry['value'] for entry in cumulative_data['historical_daily']]
    
    dates_subscribers = [entry['time'] for entry in subscribers_data['historical_daily']]
    cumulative_subscribers_values = [entry['value'] for entry in subscribers_data['historical_daily']]
    
    dates_hotspots = [entry['time'] for entry in hotspots_data['historical_daily']]
    hotspots_values = [entry['value'] for entry in hotspots_data['historical_daily']]

    # Compute daily values from cumulative data
    daily_data_transfer_values = compute_daily_values(cumulative_data_values)
    daily_subscribers_values = compute_daily_values(cumulative_subscribers_values)
    daily_hotspots_values = hotspots_values  # Keep as it is now, without cumulative conversion

    # Adjusting dates to match daily values (removing the first date)
    dates_transfer = dates_transfer[1:]
    dates_subscribers = dates_subscribers[1:]
    # dates_hotspots stays unchanged

    # Creating charts
    cumulative_data_transfer_chart = create_line_chart(
        dates_transfer, daily_data_transfer_values,
        'Daily Data Transfer on Carrier Partners',
        'Data Transfer (GB)',
        'daily_data_transfer.png'
    )

    cumulative_subscribers_chart = create_line_chart(
        dates_subscribers, daily_subscribers_values,
        'Daily Subscribers on Carrier Partners',
        'Subscribers',
        'daily_subscribers.png'
    )

    hotspots_serving_chart = create_line_chart(
        dates_hotspots, daily_hotspots_values,
        'Daily Hotspots Serving Carrier Partners',
        'Hotspots',
        'daily_hotspots_serving.png'
    )

    # Daily Subscribers Per HMH Table (this already represents daily values)
    daily_subscribers_chart = create_line_chart(
        [entry['time'] for entry in daily_subscribers_data['historical_daily']],
        [entry['value'] for entry in daily_subscribers_data['historical_daily']],
        'Daily Subscribers per HMH on Carrier Partners',
        'Subscribers per HMH',
        'daily_subscribers_per_hmh.png'
    )

    return (active_inactive_table, residential_business_table, top_class_type_table, 
            cumulative_data_transfer_chart, cumulative_subscribers_chart, daily_subscribers_chart, hotspots_serving_chart)

# Load the JSON data
with open(networks_file_path, 'r') as file:
    networks_data = json.load(file)

with open(categorized_file_path, 'r') as file:
    categorized_data = json.load(file)

with open(cumulative_data_transfer_path, 'r') as file:
    cumulative_data = json.load(file)

with open(cumulative_subscribers_path, 'r') as file:
    subscribers_data = json.load(file)

with open(daily_subscribers_path, 'r') as file:
    daily_subscribers_data = json.load(file)

with open(hotspots_serving_path, 'r') as file:
    hotspots_data = json.load(file)

# Analyze the data
(active_inactive_table, residential_business_table, top_class_type_table, 
 cumulative_data_transfer_chart, cumulative_subscribers_chart, daily_subscribers_chart, hotspots_serving_chart) = analyze_data(
    networks_data, categorized_data, cumulative_data, subscribers_data, daily_subscribers_data, hotspots_data)

# Replacement content
replacement_content = (
    f"### Device Status\n\n{active_inactive_table}\n\n"
    f"### Residential vs Business\n\n{residential_business_table}\n\n"
    f"### Top 10 Class-Type Combinations\n\n{top_class_type_table}\n\n"
    f"![Daily Data Transfer](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_data_transfer.png)\n\n"
    f"![Daily Subscribers](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_subscribers.png)\n\n"
    f"![Daily Subscribers per HMH](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_subscribers_per_hmh.png)\n\n"
    f"![Daily Hotspots Serving Carrier Partners](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_hotspots_serving.png)\n"
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
