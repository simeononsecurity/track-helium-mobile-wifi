import os
import pandas as pd

# Define the folder paths
current_path = os.getcwd()
data_path = os.path.join(current_path, 'data')
readme_path = os.path.join(current_path, 'README.md')

# Define the path to the CSV file in the Data folder
csv_file = os.path.join(data_path, 'wigle_results.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Ensure that the 'rcois' column contains string values before applying string operations
df['rcois'] = df['rcois'].astype(str).str.lower()

# Create a unique identifier for each device based on all columns
df['device_id'] = df.apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

# Calculate statistics
total_hotspots = len(df)

# Split the RCOIs into separate rows
rcois_expanded = df['rcois'].str.split(expand=True).stack().reset_index(level=1, drop=True)
rcois_expanded.name = 'rcoi'

# Create a DataFrame from the expanded RCOIs
rcoi_df = df.join(rcois_expanded).drop(columns=['rcois'])

# Calculate counts for residential and business locations
total_residential = df[df['location_type'] == 'Residential'].shape[0]
total_business = df[df['location_type'] == 'Business'].shape[0]

# Calculate percentages
residential_percentage = (total_residential / total_hotspots) * 100
business_percentage = (total_business / total_hotspots) * 100

# Boolean series for each category
openroaming_unsettled_match = rcoi_df['rcoi'].str.contains(
    '5a03ba|4096|5a03ba0000|500b|5a03ba1000|502a|5a03ba0a00|50a7|5a03ba1a00|5014|5a03ba0200|50bd|5a03ba1200|503e|5a03ba0300|50d1|5a03ba1300|5050|50e2|5053|5a03ba0b00|50f0|5a03ba1b00|5054|5a03ba0600|562b|5a03ba1600|5073|5a03ba0100|57d2|5a03ba1100|5a03ba0400|5a03ba0500|5a03ba0800|5a03ba0900',
    na=False
)
openroaming_settled_match = rcoi_df['rcoi'].str.contains(
    'baa2d|500f|baa2d00000|baa2d00100|baa2d01100|baa2d02100|baa2d03100|baa2d04100|baa2d05100|baa2d00500|baa2d0|baa2d06000',
    na=False
) & ~openroaming_unsettled_match
google_orion_devices_match = rcoi_df['rcoi'].str.contains('f4f5e8f5f4', na=False)
ironwifi_devices_match = rcoi_df['rcoi'].str.contains('aa146b0000', na=False)
helium_devices_match = rcoi_df['ssid'].str.contains('Helium Mobile', na=False, case=False)
helium_free_devices_match = rcoi_df['ssid'].str.contains('Helium Free WiFi', na=False, case=False)

# Function to count unique devices for each match
def count_unique_devices(df, match):
    unique_devices = df[match].drop_duplicates(subset=['device_id']).shape[0]
    return unique_devices

# Count unique devices for each category
openroaming_unsettled = count_unique_devices(rcoi_df, openroaming_unsettled_match)
openroaming_settled = count_unique_devices(rcoi_df, openroaming_settled_match)
google_orion_devices = count_unique_devices(rcoi_df, google_orion_devices_match)
ironwifi_devices = count_unique_devices(rcoi_df, ironwifi_devices_match)
helium_devices = count_unique_devices(rcoi_df, helium_devices_match)
helium_free_devices = count_unique_devices(rcoi_df, helium_free_devices_match)

# Boolean series for devices that have been matched
matched_devices = (
    openroaming_unsettled_match |
    openroaming_settled_match |
    google_orion_devices_match |
    ironwifi_devices_match |
    helium_devices_match |
    helium_free_devices_match
)

# Calculate count of devices that don't match any of the previous rules
other_devices = rcoi_df[~matched_devices].drop_duplicates(subset=['device_id']).shape[0]

# Print the results
print("Total Hotspots:", total_hotspots)
print("Residential Locations:", total_residential, f"({residential_percentage:.2f}%)")
print("Business Locations:", total_business, f"({business_percentage:.2f}%)")
print("OpenRoaming Unsettled:", openroaming_unsettled)
print("OpenRoaming Settled:", openroaming_settled)
print("Google Orion Devices:", google_orion_devices)
print("IronWiFi Devices:", ironwifi_devices)
print("Helium Mobile Devices:", helium_devices)
print("Helium Free WiFi Devices:", helium_free_devices)
print("Other Devices:", other_devices)

# Calculate counts for each unique RCOI
rcoi_counts = rcoi_df['rcoi'].value_counts()

# Get a list of all unique RCOIs, deduplicate, and sort alphabetically
unique_rcois = sorted(set(rcoi_counts.index))

# Define the RCOI definitions accurately without unnecessary leading zeros
rcoi_definitions = {
    '4096': 'OpenRoaming Unsettled Legacy / Samsung OneUI (All)',
    '500b': 'OpenRoaming Unsettled Legacy (All with real ID)',
    '500f': 'OpenRoaming Settled Legacy (All paid members)',
    '502a': 'OpenRoaming Unsettled Legacy (Device manufacturer all ID)',
    '50a7': 'OpenRoaming Unsettled Legacy (Device manufacturer real ID only)',
    '5014': 'OpenRoaming Unsettled Legacy (Cloud or Social ID)',
    '50bd': 'OpenRoaming Unsettled Legacy (Cloud or Social real ID)',
    '503e': 'OpenRoaming Unsettled Legacy (Enterprise Employee ID)',
    '50d1': 'OpenRoaming Unsettled Legacy (Enterprise Employee real ID)',
    '5050': 'OpenRoaming Unsettled Legacy (Enterprise Customer ID)',
    '50e2': 'OpenRoaming Unsettled Legacy (Enterprise Customer real ID)',
    '5053': 'OpenRoaming Unsettled Legacy (Loyalty Retail ID)',
    '50f0': 'OpenRoaming Unsettled Legacy (Loyalty Retail real ID)',
    '5054': 'OpenRoaming Unsettled Legacy (Loyalty Hospitality ID)',
    '562b': 'OpenRoaming Unsettled Legacy (Loyalty Hospitality real ID)',
    '5073': 'OpenRoaming Unsettled Legacy (SP free Bronze QoS)',
    '57d2': 'OpenRoaming Unsettled Legacy (SP free Bronze QoS Real ID)',
    'baa2d': 'OpenRoaming Settled',
    'baa2d00100': 'OpenRoaming Settled (SP paid Bronze QoS)',
    'baa2d01100': 'OpenRoaming Settled (SP paid Bronze QoS real ID)',
    'baa2d02100': 'OpenRoaming Settled (SP paid Silver QoS)',
    'baa2d03100': 'OpenRoaming Settled (SP paid Silver QoS real ID)',
    'baa2d04100': 'OpenRoaming Settled (SP paid Gold QoS)',
    'baa2d05100': 'OpenRoaming Settled (SP paid Gold QoS real ID)',
    'baa2d00500': 'OpenRoaming Settled (Automotive Paid)',
    '5a03ba0000': 'OpenRoaming Unsettled (All)',
    '5a03ba1000': 'OpenRoaming Unsettled (All with real ID)',
    '5a03ba0a00': 'OpenRoaming Unsettled (Device Manufacturer)',
    '5a03ba1a00': 'OpenRoaming Unsettled (Device Manufacturer real ID)',
    '5a03ba0200': 'OpenRoaming Unsettled (Cloud ID)',
    '5a03ba1200': 'OpenRoaming Unsettled (Cloud ID real ID)',
    '5a03ba0300': 'OpenRoaming Unsettled (Enterprise ID)',
    '5a03ba1300': 'OpenRoaming Unsettled (Enterprise ID real ID)',
    '5a03ba0b00': 'OpenRoaming Unsettled (Loyalty Retail)',
    '5a03ba1b00': 'OpenRoaming Unsettled (Loyalty Retail real ID)',
    '5a03ba0600': 'OpenRoaming Unsettled (Loyalty Hospitality)',
    '5a03ba1600': 'OpenRoaming Unsettled (Loyalty Hospitality real ID)',
    '5a03ba0100': 'OpenRoaming Unsettled (SP free Bronze QoS)',
    '5a03ba1100': 'OpenRoaming Unsettled (SP free Bronze QoS Real ID)',
    '5a03ba0400': 'OpenRoaming Unsettled (Government ID free)',
    '5a03ba0500': 'OpenRoaming Unsettled (Automotive ID free)',
    '5a03ba0800': 'OpenRoaming Unsettled (Education or Research ID free)',
    '5a03ba0900': 'OpenRoaming Unsettled (Cable ID free)',
    'f4f5e8f5f4': 'Google Orion Devices',
    'aa146b0000': 'IronWiFi Devices',
    '3af521': 'SingleDigits Testing RCOI',
    '1bc50460': 'Eduroam Legacy',
    '310280': 'ATT Offload ?',
    '310410': 'ATT Offload ?',
    '313100': 'ATT Offload ?',
    'f4f5e8f5d4': 'Alternative Orion Offload?',
    'f4f5e8f5e4': 'Alternative Orion Offload?',
}

# Create markdown table for unique RCOIs and their definitions with counts
rcoi_table = "### Unique RCOIs\n| RCOI | Definition | Count |\n|------|------------|-------|\n"
for rcoi, count in rcoi_counts.items():
    definition = rcoi_definitions.get(rcoi.lower(), "Unknown")
    rcoi_table += f"| {rcoi} | {definition} | {count} |\n"

# Calculate most common SSIDs
common_ssids = df['ssid'].value_counts().head(10)

# Create markdown table with descriptions
stats_table = f"""
### Helium Mobile WiFi Stats Table
| Statistic | Count | Description |
|-----------|-------|-------------|
| Total APs | {total_hotspots} | Total count of all Hotspot 2.0 access points |
| Residential Locations | {total_residential} | {residential_percentage:.2f}% of total locations |
| Business Locations | {total_business} | {business_percentage:.2f}% of total locations |
| OpenRoaming Unsettled | {openroaming_unsettled} | Count of devices with RCOI matching any OpenRoaming unsettled RCOI |
| OpenRoaming Settled | {openroaming_settled} | Count of devices with RCOI matching any OpenRoaming settled RCOI |
| Google Orion Devices | {google_orion_devices} | Count of devices with RCOI containing 'f4f5e8f5f4' |
| IronWiFi Devices | {ironwifi_devices} | Count of devices with RCOI containing 'aa146b0000' |
| Helium Devices | {helium_devices} | Count of devices with SSID containing 'Helium Mobile' |
| Helium Free WiFi Devices | {helium_free_devices} | Count of devices with SSID containing 'Helium Free WiFi' |
| Other Devices | {other_devices} | Count of devices that do not match any of the above categories |
"""

# Create markdown table for most common SSIDs
ssids_table = """
### SSIDS Tracked
| SSID | Count |
|------|-------|
"""
for ssid, count in common_ssids.items():
    ssids_table += f"| {ssid} | {count} |\n"

# Output the result
print(rcoi_table)

# Read the README file
with open(readme_path, 'r') as f:
    readme_content = f.read()

# Ensure the markers are present in the README
if '<!-- STATS START -->' in readme_content and '<!-- STATS END -->' in readme_content:
    before_stats, after_stats = readme_content.split('<!-- STATS START -->')[0], readme_content.split('<!-- STATS END -->')[1]
    new_readme_content = before_stats + '<!-- STATS START -->\n' + stats_table + '\n' + ssids_table + '\n' + rcoi_table + '\n<!-- STATS END -->' + after_stats

    # Write the new content back to the README file
    with open(readme_path, 'w') as f:
        f.write(new_readme_content)

    print("README.md has been updated with new statistics.")
else:
    print("Error: Markers <!-- STATS START --> and <!-- STATS END --> not found in README.md.")
