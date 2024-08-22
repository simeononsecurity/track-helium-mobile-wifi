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

# Function to calculate percentage growth
def calculate_percentage_growth(values):
    daily_growth = []
    for i in range(1, len(values)):
        if values[i - 1] != 0:
            growth = ((values[i] - values[i - 1]) / values[i - 1]) * 100
        else:
            growth = 0
        daily_growth.append(growth)
    return daily_growth

# Function to calculate weekly growth from daily values
def calculate_weekly_growth(daily_values):
    weekly_growth = []
    for i in range(7, len(daily_values), 7):
        week_start = i - 7
        if daily_values[week_start] != 0:
            growth = ((daily_values[i] - daily_values[week_start]) / daily_values[week_start]) * 100
        else:
            growth = 0
        weekly_growth.append(growth)
    return weekly_growth

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

    # Calculate daily and weekly growth percentages for data transfer, subscribers, and hotspots
    daily_transfer_growth = calculate_percentage_growth(daily_data_transfer_values)
    weekly_transfer_growth = calculate_weekly_growth(cumulative_data_values)

    daily_subscribers_growth = calculate_percentage_growth(daily_subscribers_values)
    weekly_subscribers_growth = calculate_weekly_growth(cumulative_subscribers_values)

    daily_hotspots_growth = calculate_percentage_growth(daily_hotspots_values)
    weekly_hotspots_growth = calculate_weekly_growth(hotspots_values)

    # Generate Markdown tables for percentage growth
    transfer_growth_table = generate_markdown_table(
        ['Date', 'Daily Growth (%)', 'Weekly Growth (%)'],
        [(dates_transfer[i], f"{daily_transfer_growth[i-1]:.2f}%", f"{weekly_transfer_growth[i//7-1]:.2f}%" if i >= 7 else "N/A") 
        for i in range(7, len(dates_transfer))]
    )

    subscribers_growth_table = generate_markdown_table(
        ['Date', 'Daily Growth (%)', 'Weekly Growth (%)'],
        [(dates_subscribers[i], f"{daily_subscribers_growth[i-1]:.2f}%", f"{weekly_subscribers_growth[i//7-1]:.2f}%" if i >= 7 else "N/A") 
        for i in range(7, len(dates_subscribers))]
    )

    hotspots_growth_table = generate_markdown_table(
        ['Date', 'Daily Growth (%)', 'Weekly Growth (%)'],
        [(dates_hotspots[i], f"{daily_hotspots_growth[i-1]:.2f}%", f"{weekly_hotspots_growth[i//7-1]:.2f}%" if i >= 7 else "N/A") 
        for i in range(7, len(dates_hotspots))]
    )

    # Create growth charts for data transfer, subscribers, and hotspots
    daily_transfer_growth_chart = create_line_chart(
        dates_transfer[1:], daily_transfer_growth,
        'Daily Percentage Growth in Data Transfer',
        'Growth (%)',
        'daily_transfer_growth.png'
    )

    daily_subscribers_growth_chart = create_line_chart(
        dates_subscribers[1:], daily_subscribers_growth,
        'Daily Percentage Growth in Subscribers',
        'Growth (%)',
        'daily_subscribers_growth.png'
    )

    daily_hotspots_growth_chart = create_line_chart(
        dates_hotspots[1:], daily_hotspots_growth,
        'Daily Percentage Growth in Hotspots',
        'Growth (%)',
        'daily_hotspots_growth.png'
    )

    return (active_inactive_table, residential_business_table, top_class_type_table, 
            cumulative_data_transfer_chart, cumulative_subscribers_chart, daily_subscribers_chart, hotspots_serving_chart,
            transfer_growth_table, subscribers_growth_table, hotspots_growth_table,
            daily_transfer_growth_chart, daily_subscribers_growth_chart, daily_hotspots_growth_chart)

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
 cumulative_data_transfer_chart, cumulative_subscribers_chart, daily_subscribers_chart, hotspots_serving_chart,
 transfer_growth_table, subscribers_growth_table, hotspots_growth_table,
 daily_transfer_growth_chart, daily_subscribers_growth_chart, daily_hotspots_growth_chart) = analyze_data(
    networks_data, categorized_data, cumulative_data, subscribers_data, daily_subscribers_data, hotspots_data)

# Replacement content
replacement_content = (
    f"### Device Status\n\n{active_inactive_table}\n\n"
    f"### Residential vs Business\n\n{residential_business_table}\n\n"
    f"### Top 10 Class-Type Combinations\n\n{top_class_type_table}\n\n"
    f"![Daily Data Transfer](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_data_transfer.png)\n\n"
    f"#### Data Transfer Growth\n\n{transfer_growth_table}\n\n"
    f"![Daily Transfer Growth](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_transfer_growth.png)\n\n"
    f"![Daily Subscribers](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_subscribers.png)\n\n"
    f"#### Subscribers Growth\n\n{subscribers_growth_table}\n\n"
    f"![Daily Subscribers Growth](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_subscribers_growth.png)\n\n"
    f"![Daily Hotspots Serving Carrier Partners](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_hotspots_serving.png)\n\n"
    f"#### Hotspots Growth\n\n{hotspots_growth_table}\n\n"
    f"![Daily Hotspots Growth](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/daily_hotspots_growth.png)\n"
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
