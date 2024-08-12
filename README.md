# Track Helium Mobile WiFi

[![Sponsor](https://img.shields.io/badge/Sponsor-Click%20Here-ff69b4)](https://github.com/sponsors/simeononsecurity) [![Interactive Map](https://img.shields.io/badge/Interactive%20Map-View%20Here-blue)](https://heliummap.simeononsecurity.com)

A collection of scripts and tools that tracks the availability of Helium Mobile WiFi networks in the wild.

Pulls from the Wigle.net dataset. 

> **Note**: Information here may not be entirely accurate or complete, but it's the best semi-public dataset available for tracking this kind of information that is verified by 3rd parties. 
The stats are dynamic, we only pull year to date stats. But ultimately we'll update it to do devices mapped in the last 365 days.

> **Note:**: All of the categorizations and identifiers were discovered from public documentation and research that is repeatable with google searches. 

<!-- STATS START -->

### Helium Mobile WiFi Stats Table
| Statistic | Count | Description |
|-----------|-------|-------------|
| Total APs | 426 | Total count of all Hotspot 2.0 access points |
| Residential Locations | 248 | 58.22% of total locations |
| Business Locations | 174 | 40.85% of total locations |
| OpenRoaming Unsettled | 0 | Count of devices with RCOI matching any OpenRoaming unsettled RCOI |
| OpenRoaming Settled | 0 | Count of devices with RCOI matching any OpenRoaming settled RCOI |
| Google Orion Devices | 0 | Count of devices with RCOI containing 'f4f5e8f5f4' |
| IronWiFi Devices | 0 | Count of devices with RCOI containing 'aa146b0000' |
| Helium Devices | 426 | Count of devices with SSID containing 'Helium Mobile' |
| Helium Free WiFi Devices | 0 | Count of devices with SSID containing 'Helium Free WiFi' |
| Other Devices | 0 | Count of devices that do not match any of the above categories |


### SSIDS Tracked
| SSID | Count |
|------|-------|
| Helium Mobile | 426 |

### Unique RCOIs
| RCOI | Definition | Count |
|------|------------|-------|
| 0.0 | Unknown | 382 |
| nan | Unknown | 44 |

<!-- STATS END -->

### Helium Mobile WiFi Table Mapped

![OpenRoaming and Hotspot 2.0 Table Map](https://github.com/simeononsecurity/track-helium-mobile-wifi/blob/main/output/global_wifi_map.png)

## Table of Contents

- [Track Helium Mobile WiFi](#track-helium-mobile-wifi)
    - [Helium Mobile WiFi Stats Table](#helium-mobile-wifi-stats-table)
    - [SSIDS Tracked](#ssids-tracked)
    - [Unique RCOIs](#unique-rcois)
    - [Helium Mobile WiFi Table Mapped](#helium-mobile-wifi-table-mapped)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Scripts](#scripts)
      - [map\_wigle\_devices.py](#map_wigle_devicespy)
      - [filter\_sort\_wigle\_results.py](#filter_sort_wigle_resultspy)
      - [generate\_map\_html.py](#generate_map_htmlpy)
      - [generate\_map\_png.py](#generate_map_pngpy)
      - [update\_readme\_stats.py](#update_readme_statspy)
      - [classify\_locations.py](#classify_locationspy)
    - [Running the Scripts](#running-the-scripts)
  - [Automated Workflow](#automated-workflow)
    - [Workflow: `.github/workflows/update_statistics.yml`](#workflow-githubworkflowsupdate_statisticsyml)
  - [GitHub Pages](#github-pages)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This project aims to track the availability of Hotspot 2.0, Passpoint, and OpenRoaming networks using data collected from WiGLE and other sources. The collected data is processed and visualized using various scripts.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/track-helium-mobile-wifi.git
   cd track-openroaming-passpoint
   ```

2. Set up a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API credentials:
   ```env
   API_NAME=your_api_name
   API_TOKEN=your_api_token
   AUTH_HEADER=your_auth_header
   ```

## Usage

### Scripts

#### map_wigle_devices.py

Fetches data from the WiGLE API and saves it to a CSV file.

#### filter_sort_wigle_results.py

Filters and sorts the fetched WiGLE results and processes them for further analysis.

#### generate_map_html.py

Generates an interactive HTML map using Folium, displaying WiGLE data points. The HTML map files are saved to the `Output` directory and an `archive` subdirectory with the current year appended.

#### generate_map_png.py

Generates a static PNG map using Matplotlib and Basemap, displaying WiGLE data points. The PNG map files are saved to the `Output` directory and an `archive` subdirectory with the current year appended.

#### update_readme_stats.py

Updates the `README.md` file with statistics about the WiGLE data.

#### classify_locations.py

Classifies SSIDs from the WiGLE data as Residential, Business, or Public based on heuristics and performs reverse geocoding to add location information. The results are saved to a new CSV file.

### Running the Scripts

1. **Fetch data from WiGLE**:
   ```sh
   python scripts/map_wigle_devices.py
   ```

2. **Filter and sort the results**:
   ```sh
   python scripts/filter_sort_wigle_results.py
   ```

3. **Generate the HTML map**:
   ```sh
   python scripts/generate_map_html.py
   ```

4. **Generate the PNG map**:
   ```sh
   python scripts/generate_map_png.py
   ```

5. **Update the README with statistics**:
   ```sh
   python scripts/update_readme_stats.py
   ```

6. **Classify SSIDs and perform reverse geocoding**:
   ```sh
   python scripts/classify_locations.py
   ```

## Automated Workflow

The project includes a GitHub Actions workflow that runs the scripts automatically every 24 hours and updates the repository.

### Workflow: `.github/workflows/update_statistics.yml`

- Installs the pip requirements.
- Runs the scripts in order:
  - `map_wigle_devices.py`
  - `generate_map_html.py`
  - `generate_map_png.py`
  - `update_readme_stats.py`
- Commits the changes back to the repository.

## GitHub Pages

The HTML maps are made available through GitHub Pages. The workflow ensures the HTML files are copied to the `docs` folder, which is configured for GitHub Pages.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
