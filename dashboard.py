import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Airline Brands Comparison Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2196f3;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the three datasets"""
    try:
        # Load with tab separation and proper error handling
        george_airline = pd.read_csv(
            'data/george_airline_level.csv',
            sep='\t',
            na_values=['', 'null', 'NULL', 'NaN'],
            keep_default_na=True,
            encoding='utf-8'
        )
        
        george_source = pd.read_csv(
            'data/george_airline_source_level.csv',
            sep='\t',
            na_values=['', 'null', 'NULL', 'NaN'],
            keep_default_na=True,
            encoding='utf-8'
        )
        
        teo_source = pd.read_csv(
            'data/teo_airline_source.csv',
            sep='\t',
            na_values=['', 'null', 'NULL', 'NaN'],
            keep_default_na=True,
            encoding='utf-8'
        )
        
        # Clean the data - fill empty values
        george_airline['outbound_fare_family'] = george_airline['outbound_fare_family'].fillna('Unknown').replace('', 'Unknown')
        george_source['outbound_fare_family'] = george_source['outbound_fare_family'].fillna('Unknown').replace('', 'Unknown')
        george_source['source'] = george_source['source'].fillna('Unknown').replace('', 'Unknown')
        
        return george_airline, george_source, teo_source
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Fallback parsing
        try:
            george_airline = pd.read_csv('data/george_airline_level.csv', sep=None, engine='python', on_bad_lines='skip')
            george_source = pd.read_csv('data/george_airline_source_level.csv', sep=None, engine='python', on_bad_lines='skip')
            teo_source = pd.read_csv('data/teo_airline_source.csv', sep=None, engine='python', on_bad_lines='skip')
            
            # Clean the data
            george_airline['outbound_fare_family'] = george_airline['outbound_fare_family'].fillna('Unknown').replace('', 'Unknown')
            george_source['outbound_fare_family'] = george_source['outbound_fare_family'].fillna('Unknown').replace('', 'Unknown')
            george_source['source'] = george_source['source'].fillna('Unknown').replace('', 'Unknown')
            
            return george_airline, george_source, teo_source
            
        except Exception as e2:
            st.error(f"Failed to load data: {e2}")
            return None, None, None

def raw_data_page():
    """Raw data exploration page"""
    st.markdown('<p class="section-header">📊 Raw Data Exploration</p>', unsafe_allow_html=True)
    
    george_airline, george_source, teo_source = load_data()
    
    if any(df is None for df in [george_airline, george_source, teo_source]):
        st.error("Unable to load data files. Please check the data directory.")
        return
    
    # Dataset selection
    dataset_choice = st.selectbox(
        "Select dataset to explore:",
        ["George Airline Level", "George Source Level", "Teo Brand Analysis"]
    )
    
    if dataset_choice == "George Airline Level":
        st.subheader("George Airline Level Data")
        st.markdown("**Description:** Aggregated fare family data by carrier")
        st.markdown(f"**Shape:** {george_airline.shape[0]} rows × {george_airline.shape[1]} columns")
        
        # Show data with filters
        carriers = ['All'] + sorted(george_airline['carrier'].unique().tolist())
        selected_carrier = st.selectbox("Filter by Carrier:", carriers)
        
        if selected_carrier != 'All':
            filtered_data = george_airline[george_airline['carrier'] == selected_carrier]
        else:
            filtered_data = george_airline
            
        st.dataframe(filtered_data, use_container_width=True)
        
        # Download button
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="george_airline_level_filtered.csv",
            mime="text/csv"
        )
    
    elif dataset_choice == "George Source Level":
        st.subheader("George Source Level Data")
        st.markdown("**Description:** Detailed breakdown by carrier and booking source")
        st.markdown(f"**Shape:** {george_source.shape[0]} rows × {george_source.shape[1]} columns")
        
        # Show data with filters
        col1, col2 = st.columns(2)
        with col1:
            carriers = ['All'] + sorted(george_source['carrier'].unique().tolist())
            selected_carrier = st.selectbox("Filter by Carrier:", carriers)
        with col2:
            sources = ['All'] + sorted(george_source['source'].unique().tolist())
            selected_source = st.selectbox("Filter by Source:", sources)
        
        filtered_data = george_source.copy()
        if selected_carrier != 'All':
            filtered_data = filtered_data[filtered_data['carrier'] == selected_carrier]
        if selected_source != 'All':
            filtered_data = filtered_data[filtered_data['source'] == selected_source]
            
        st.dataframe(filtered_data, use_container_width=True)
        
        # Download button
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="george_source_level_filtered.csv",
            mime="text/csv"
        )
    
    else:  # Teo Brand Analysis
        st.subheader("Teo Brand Analysis Data")
        st.markdown("**Description:** Advanced brand detection with price analysis")
        st.markdown(f"**Shape:** {teo_source.shape[0]} rows × {teo_source.shape[1]} columns")
        
        # Show data with filters
        airlines = ['All'] + sorted(teo_source['airline'].unique().tolist())
        selected_airline = st.selectbox("Filter by Airline:", airlines)
        
        if selected_airline != 'All':
            filtered_data = teo_source[teo_source['airline'] == selected_airline]
        else:
            filtered_data = teo_source
            
        st.dataframe(filtered_data, use_container_width=True)
        
        # Download button
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="teo_brand_analysis_filtered.csv",
            mime="text/csv"
        )

def overview_page():
    """Overview page with key stats and summaries"""
    st.markdown('<p class="section-header">📈 Overview & Key Statistics</p>', unsafe_allow_html=True)
    
    george_airline, george_source, teo_source = load_data()
    
    if any(df is None for df in [george_airline, george_source, teo_source]):
        st.error("Unable to load data files. Please check the data directory.")
        return
    
    # High-level metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Airlines (George Airline)", george_airline['carrier'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Airlines (George Source)", george_source['carrier'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Airlines (Teo)", teo_source['airline'].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_ods = george_airline['ods'].sum()
        st.metric("Total ODs", f"{total_ods:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dataset summaries in tabs
    tab1, tab2, tab3 = st.tabs(["George Airline Level", "George Source Level", "Teo Analysis"])
    
    with tab1:
        st.subheader("George Airline Level Summary")
        
        # Top carriers by ODs
        top_carriers = george_airline.groupby('carrier')['ods'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=top_carriers.values, 
            y=top_carriers.index, 
            orientation='h',
            title="Top 10 Carriers by ODs Volume",
            labels={'x': 'ODs', 'y': 'Carrier'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Fare family distribution
        fare_families = george_airline.groupby('outbound_fare_family')['ods'].sum().sort_values(ascending=False).head(10)
        fig2 = px.bar(
            x=fare_families.values,
            y=fare_families.index,
            orientation='h',
            title="Top 10 Fare Families by ODs Volume"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("George Source Level Summary")
        
        # Source distribution
        sources = george_source.groupby('source')['ods'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=sources.values,
            names=sources.index,
            title="ODs Distribution by Source"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top carrier-source combinations
        top_combos = george_source.groupby(['carrier', 'source'])['ods'].sum().sort_values(ascending=False).head(15)
        combo_labels = [f"{carrier} - {source}" for carrier, source in top_combos.index]
        
        fig2 = px.bar(
            x=top_combos.values,
            y=combo_labels,
            orientation='h',
            title="Top 15 Carrier-Source Combinations by ODs"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("Teo Analysis Summary")
        
        # Basic economy identification rate
        total_records = len(teo_source)
        has_basic_economy = teo_source['identified_basic_economy_brand'].notna().sum()
        basic_economy_rate = (has_basic_economy / total_records) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Basic Economy ID Rate", f"{basic_economy_rate:.1f}%")
        with col2:
            avg_brands = teo_source['all_detected_brands'].str.split(',').str.len().mean()
            st.metric("Avg Brands per Record", f"{avg_brands:.1f}")
        with col3:
            avg_min_price = teo_source['min_price_inc'].mean()
            st.metric("Avg Min Price", f"${avg_min_price:.2f}")
        
        # Price distribution
        fig = px.histogram(
            teo_source[teo_source['min_price_inc'] < teo_source['min_price_inc'].quantile(0.95)],
            x='min_price_inc',
            nbins=30,
            title="Distribution of Minimum Prices (95th percentile cutoff)"
        )
        st.plotly_chart(fig, use_container_width=True)

def lowest_brands_page():
    """Page showing lowest brands identified by each dataset"""
    st.markdown('<p class="section-header">🏆 Lowest Brands by Airline</p>', unsafe_allow_html=True)
    
    george_airline, george_source, teo_source = load_data()
    
    if any(df is None for df in [george_airline, george_source, teo_source]):
        st.error("Unable to load data files. Please check the data directory.")
        return
    
    st.markdown("""
    <div class="info-box">
    This page shows the lowest fare brands identified by each dataset for each airline. 
    The methodology differs across datasets:
    <ul>
    <li><strong>George Airline:</strong> Most frequent fare family (highest ODs volume)</li>
    <li><strong>George Source:</strong> Most frequent fare family across all sources</li>
    <li><strong>Teo:</strong> Explicitly identified basic economy brand + lowest minimum price</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all unique airlines across datasets
    george_airlines = set(george_airline['carrier'].unique())
    george_source_airlines = set(george_source['carrier'].unique())
    teo_airlines = set(teo_source['airline'].unique())
    all_airlines = sorted(george_airlines | george_source_airlines | teo_airlines)
    
    # Create comparison dataframe
    comparison_data = []
    
    for airline in all_airlines:
        row = {'Airline': airline}
        
        # George Airline Level - most frequent fare family
        george_a_data = george_airline[george_airline['carrier'] == airline]
        if not george_a_data.empty:
            top_brand = george_a_data.groupby('outbound_fare_family')['ods'].sum().idxmax()
            top_ods = george_a_data.groupby('outbound_fare_family')['ods'].sum().max()
            row['George_Airline_Brand'] = top_brand
            row['George_Airline_ODs'] = top_ods
        else:
            row['George_Airline_Brand'] = 'N/A'
            row['George_Airline_ODs'] = 0
        
        # George Source Level - most frequent fare family across sources
        george_s_data = george_source[george_source['carrier'] == airline]
        if not george_s_data.empty:
            top_brand = george_s_data.groupby('outbound_fare_family')['ods'].sum().idxmax()
            top_ods = george_s_data.groupby('outbound_fare_family')['ods'].sum().max()
            row['George_Source_Brand'] = top_brand
            row['George_Source_ODs'] = top_ods
        else:
            row['George_Source_Brand'] = 'N/A'
            row['George_Source_ODs'] = 0
        
        # Teo Analysis - basic economy brand with lowest price
        teo_data = teo_source[teo_source['airline'] == airline]
        if not teo_data.empty:
            # Find the record with the lowest minimum price
            min_price_idx = teo_data['min_price_inc'].idxmin()
            lowest_price_record = teo_data.loc[min_price_idx]
            
            basic_brand = lowest_price_record['identified_basic_economy_brand']
            min_price = lowest_price_record['min_price_inc']
            source = lowest_price_record['source']
            
            row['Teo_Basic_Brand'] = basic_brand if pd.notna(basic_brand) else 'Not Identified'
            row['Teo_Min_Price'] = min_price
            row['Teo_Source'] = source
        else:
            row['Teo_Basic_Brand'] = 'N/A'
            row['Teo_Min_Price'] = None
            row['Teo_Source'] = 'N/A'
        
        comparison_data.append(row)
    
    # Create DataFrame and display
    comparison_df = pd.DataFrame(comparison_data)
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_all = st.checkbox("Show all airlines", value=True)
        if not show_all:
            available_airlines = st.multiselect(
                "Select airlines to display:",
                options=all_airlines,
                default=all_airlines[:10]
            )
            comparison_df = comparison_df[comparison_df['Airline'].isin(available_airlines)]
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Airline", "George_Airline_ODs", "George_Source_ODs", "Teo_Min_Price"]
        )
        ascending = st.checkbox("Ascending order", value=True)
        
        if sort_by in comparison_df.columns:
            comparison_df = comparison_df.sort_values(sort_by, ascending=ascending)
    
    # Display the comparison table
    st.subheader("Lowest Brands Comparison (Only Brands)")
    
    # Select only the requested columns for display
    display_df = comparison_df[['Airline', 'George_Airline_Brand', 'George_Source_Brand', 'Teo_Basic_Brand']].copy()
    
    st.dataframe(display_df, use_container_width=True)
    
    # Download button for the full comparison (optional, but useful if user wants detailed data later)
    csv = comparison_df.to_csv(index=False)
    st.download_button(
        label="Download Full Comparison Data as CSV",
        data=csv,
        file_name="lowest_brands_full_comparison.csv",
        mime="text/csv"
    )
    
    # Summary insights - simplified
    st.subheader("Key Insights (Simplified)")
    
    st.markdown("""
    This simplified view focuses on the identified lowest brands.
    For detailed metrics (like ODs volume and minimum prices) and dataset coverage,
    please refer to the full downloadable CSV.
    """)

def main():
    """Main dashboard function"""
    st.markdown('<p class="main-header">✈️ Airline Brands Comparison Dashboard</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose Page:",
        ["📊 Raw Data", "📈 Overview", "🏆 Lowest Brands"]
    )
    
    # Route to appropriate page
    if page == "📊 Raw Data":
        raw_data_page()
    elif page == "📈 Overview":
        overview_page()
    elif page == "🏆 Lowest Brands":
        lowest_brands_page()

if __name__ == "__main__":
    main() 