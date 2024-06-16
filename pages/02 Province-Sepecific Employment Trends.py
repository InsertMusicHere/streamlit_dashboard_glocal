import streamlit as st
import altair as alt
import pandas as pd
from io import StringIO
import requests
import altair as alt
import pydeck as pdk

st.set_page_config(layout="wide")

def format_int_with_commas(x):
   """
   Formats an integer with commas as thousand separators.
   """
   return f"{x:,}"

# Define your custom CSS
style = """
<style>
div[data-testid="metric-container"] {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 10px;
}
</style>
"""

# Inject custom CSS with markdown
st.markdown(style, unsafe_allow_html=True)



regions = [
    'Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia',
    'New Brunswick', 'Quebec', 'Ontario', 'Manitoba', 'Saskatchewan',
    'Alberta', 'British Columbia', 'Yukon', 'Northwest Territories', 'Nunavut'
]

colors = [
    "#bfc8d2", "#a5b1be", "#8692a0", "#768699", "#59708a", "#3fdbff", 
    "#5ecaff", "#87a7ff", "#7498ef", "#c8daff", "#d1b844", "#8db6d8"
]

st.title("Provincial Insights")

@st.cache_data
def get_data():

    # reading file from github

    url = 'https://raw.githubusercontent.com/InsertMusicHere/streamlit_dashboard_glocal/main/1410020101_databaseLoadingData.csv'
    response = requests.get(url)
    if response.status_code == 200:
        df =  pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        

    df[['Year', 'Month']] = df['REF_DATE'].str.split('-', expand=True)
    df = df.rename(columns={"North American Industry Classification System (NAICS)":"NAICS"})
    df = df[['Year', 'Month', 'GEO', 'NAICS', 'VALUE', 'STATUS', 'Lat', 'Lang']]
    
    list_1 = ["Canada"]
    list_2 = ["Industrial aggregate including unclassified businesses [00-91N]", 
              "Industrial aggregate excluding unclassified businesses [11-91N]", 
              "Service producing industries [41-91N]"]
    list_3 = ["2024"]

    only_provinces = df[~df["GEO"].isin(list_1)]
    only_provinces = only_provinces[~only_provinces["NAICS"].isin(list_2)]
    only_provinces = only_provinces[~only_provinces["Year"].isin(list_3)]

    return only_provinces

sales_data = get_data()

print(sales_data.columns)

lat_long_data = sales_data[['GEO', 'NAICS', 'VALUE', 'Lat', 'Lang']].rename(columns={"Lat":"lat","Lang":"lon"})

# ----------------------
#
# ----------------------

# Convert the data to a DataFrame
df = sales_data

df = df.dropna()

# Placeholder for KPI and Table
kpi_placeholder = st.empty()

# Function to display KPI and Table
def display_kpi_and_table(selected_region):
    if selected_region:
        region_data = df[df["GEO"] == selected_region]
        
        total_value = region_data["VALUE"].sum()
        
        total_employees = region_data["VALUE"].sum().astype("int")
        total_employees_mean = int(total_employees / len(region_data["Year"].unique()))

        # Group by Year and calculate sum of VALUE
        summary_table = region_data.groupby("Year").agg({"VALUE": "sum"}).reset_index()
        summary_table["VALUE"] = summary_table["VALUE"].astype("int")
        summary_table.columns = ["Year", "Total VALUE"]
        
        st.dataframe(summary_table, width=800)

info_ = st.empty()
# Dropdown for region selection
selected_region = st.selectbox(label="Regions", options=[""] + regions,key="uniq")

# ----------------------
# For KPI cards
# ----------------------

def format_int_with_commas(value):
    return f"{value:,}"

def calculate_yoy(current_value, previous_value):
    if previous_value == 0:
        return None
    return ((current_value - previous_value) / previous_value) * 100

years = ["2018", "2019", "2020", "2021", "2022", "2023"]
kpi_values = []

# Calculate values for each year
for year in years:
    kpi_year = sales_data[(sales_data['GEO'] == selected_region) & (sales_data['Year'] == year)]
    total_value = int(kpi_year['VALUE'].sum())
    kpi_values.append(total_value)

# st.write(kpi_values)

# ------------
# Display KPIs with YOY delta
# ------------

if selected_region:

    columns = st.columns(6)
    for i, (year, value) in enumerate(zip(years, kpi_values)):
        with columns[i]:
            if i > 0:
                previous_value = kpi_values[i - 1]
                yoy = calculate_yoy(value, previous_value)
                if yoy is not None:
                    yoy = round(yoy, 2)
                    delta = f"{yoy}%"
                else:
                    delta = "N/A"
            else:
                delta = "N/A"  # No YOY calculation for the first year

            formatted_value = format_int_with_commas(value)
            if year != "2018":
                st.metric(label=f"Total Employees ({year})", value=formatted_value, delta=delta)
            else:
                st.metric(label=f"Total Employees ({year})", value=formatted_value, delta="N/A", delta_color="off")
            st.write("---")
else:
    info_.info("Please select a region")

if selected_region:

    try:
        region_data = df[df["GEO"] == selected_region]
        latitude = region_data["Lat"].iloc[0]
        longitude = region_data["Lang"].iloc[0]

        total_employees = region_data["VALUE"].sum().astype("int")
        total_employees_mean = int(total_employees / len(region_data["Year"].unique()))

        st.markdown('<p style="font-size:20px">Please hover over the red circle to view average employee count in the selected region.</p>', unsafe_allow_html=True)

        chart_data = region_data[["Lat", "Lang", "VALUE"]].dropna()

        INITIAL_VIEW_STATE = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=8,
            max_zoom=26,
            pitch=45,
            bearing=0
        )

        column_layer = pdk.Layer(
            "ColumnLayer",
            data=chart_data,
            get_position="[Lang, Lat]",
            get_elevation="VALUE",
            elevation_scale=0,
            radius=2500,
            get_fill_color=[200, 30, 0, 160],
            pickable=True,
            auto_highlight=True, 
        )

        formatted_value = format_int_with_commas(total_employees_mean)

        tooltip={
                "html": f"<b>Average Employee Count:</b> {formatted_value}",
                "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
            }

        r = pdk.Deck(
            layers=[column_layer],
            initial_view_state=INITIAL_VIEW_STATE,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/light-v10" 
        )

        st.pydeck_chart(r)
        # st.pydeck_chart(r)
    except SyntaxError as e:
        status1 = '0'
        message1 = str(e)
        st.write(str(e))
            
else:

    try:
        
        info_.info("Please select a region")
        sales_data = sales_data.rename(columns={"Lat":"lat","Lang":"lon"})
        st.map(sales_data)
    except:
        st.write("Please select a region to display the map")

# ---------------------
#
# ---------------------

st.divider()

regions = [
    'Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia',
    'New Brunswick', 'Quebec', 'Ontario', 'Manitoba', 'Saskatchewan',
    'Alberta', 'British Columbia', 'Yukon', 'Northwest Territories', 'Nunavut'
]


region_select = alt.selection_single(fields=["GEO"], empty="all")

st.info("Please click on a slice to view the trend in the adjacent graph.")

region_pie = (
    alt.Chart(sales_data)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("VALUE", type="quantitative", aggregate="sum", title="Total Number of Employees"),
        color=alt.Color(field="GEO", type="nominal", scale=alt.Scale(domain=regions, range=colors), title="Regions"),
        opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
    )
    .add_selection(region_select)
    .properties(title="Distribution of Employees Across Canadian Provinces (%)")
)



region_summary = (
    alt.Chart(sales_data)
    .mark_bar()
    .encode(
        x=alt.X("Year", type="ordinal"),
        y=alt.Y(field="VALUE", type="quantitative", aggregate="sum", title="Total Sales"),
        color=alt.Color("GEO", type="nominal", scale=alt.Scale(domain=regions, range=colors)),
    )
    .transform_filter(region_select)
    .properties(width=700, title="Number of Employees by Province (#Abs)")
)

# Combine charts into two columns
top_row = alt.hconcat(region_pie, region_summary)

# Display the charts
st.altair_chart(top_row,use_container_width=True)

st.write("---")



label = '''
data source: [Statistics Canada. Table 14-10-0201-01  Employment by industry, monthly, unadjusted for seasonality](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020101)
'''

st.write(label)