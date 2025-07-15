# Airline Brands Comparison Dashboard ✈️

A comprehensive Streamlit dashboard for exploring and comparing three different approaches to identifying lowest fare airline brands.

## Overview

This dashboard analyzes three datasets that represent different methodologies for identifying and categorizing airline fare brands:

1. **George Airline Level** (`george_airline_level.csv`): Aggregated fare family data by carrier
2. **George Source Level** (`george_airline_source_level.csv`): Detailed breakdown by carrier and booking source
3. **Teo Analysis** (`teo_airline_source.csv`): Advanced brand detection with comprehensive price analysis

## Features

### 📊 Dashboard Sections

- **Overview**: Key metrics and insights across all datasets
- **Fare Family Analysis**: Deep dive into fare family distributions and patterns
- **Cross-Dataset Comparison**: Compare airlines and approaches across datasets
- **Airline Deep Dive**: Detailed analysis for specific airlines
- **Raw Data**: Explore and download the original datasets

### 🔍 Key Analytics

- **Volume Analysis**: ODs (Origin-Destination pairs) distribution
- **Brand Detection**: Success rates and methodology comparison
- **Price Analysis**: Min, average, and median price distributions
- **Source Distribution**: Booking channel analysis
- **Carrier Comparison**: Cross-airline insights

### 📈 Visualizations

- Interactive bar charts and histograms
- Heatmaps for carrier vs source analysis
- Pie charts for distribution analysis
- Comparative metrics and KPIs

## Installation & Setup

1. **Clone or download** this repository to your local machine

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files** are in the `data/` directory:
   - `data/george_airline_level.csv`
   - `data/george_airline_source_level.csv`
   - `data/teo_airline_source.csv`

4. **Run the dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

5. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

## Data Structure

### George Airline Level
- `carrier`: Airline code (e.g., AA, DL, UA)
- `outbound_fare_family`: Fare family name
- `ods`: Number of Origin-Destination pairs

### George Source Level
- `carrier`: Airline code
- `source`: Booking source (e.g., GDS, Direct, OTA)
- `outbound_fare_family`: Fare family name
- `ods`: Number of Origin-Destination pairs

### Teo Analysis
- `airline`: Airline code
- `source`: Booking source
- `all_detected_brands`: All fare brands detected
- `identified_basic_economy_brand`: Identified basic economy brand
- `min_price_inc`: Minimum price including taxes
- `avg_price_inc`: Average price including taxes
- `median_price_inc`: Median price including taxes

## Key Insights

The dashboard reveals several important patterns:

1. **Methodology Differences**: George's approach focuses on fare family categorization and volume, while Teo's approach emphasizes brand detection algorithms and price analysis.

2. **Coverage Variation**: Different datasets cover different airlines and sources, providing complementary views of the market.

3. **Brand Complexity**: Airlines use varying naming conventions for similar fare products, making standardization challenging.

4. **Source Impact**: The booking source significantly affects fare family availability and pricing.

## Technical Requirements

- Python 3.7+
- Streamlit 1.28.1
- Pandas 2.1.3
- Plotly 5.17.0
- Other dependencies listed in `requirements.txt`

## Usage Tips

1. **Start with Overview**: Get familiar with the data scope and key metrics
2. **Use Filters**: Leverage the sidebar navigation to focus on specific analyses
3. **Download Data**: Use the Raw Data section to export filtered datasets
4. **Airline Deep Dive**: Select specific airlines to compare methodologies
5. **Interactive Charts**: Hover over charts for detailed information

## Contributing

Feel free to enhance the dashboard by:
- Adding new visualizations
- Implementing additional filters
- Creating export functionality
- Improving the UI/UX

## Support

For questions or issues with the dashboard, please check:
1. Data file locations and formats
2. Python environment and dependencies
3. Streamlit installation and configuration

---

**Note**: This dashboard is designed for analytical purposes to compare different approaches to airline fare brand identification. The insights should be used in conjunction with domain expertise for business decisions. 