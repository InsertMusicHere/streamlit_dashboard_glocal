import streamlit as st
import altair as alt
import pandas as pd
from io import StringIO
import requests

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

st.title("Interactive Dashboard - Provincial Insights")

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
        theta=alt.Theta("VALUE", type="quantitative", aggregate="sum", title="Totla Number of Employees"),
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
st.altair_chart(top_row, use_container_width=True)

st.write("---")

# Placeholder for KPI and Table
kpi_placeholder = st.empty()
# table_placeholder = st.empty()

# Function to display KPI and Table
def display_kpi_and_table(selected_region):
    if selected_region:
        region_data = sales_data[sales_data["GEO"] == selected_region]
        total_value = region_data["VALUE"].sum()
        
        total_employees = region_data["VALUE"].sum().astype("int")
        total_employees_mean = int(total_employees/6)

        total_employees_mean = format_int_with_commas(total_employees_mean)

        kpi_placeholder.metric(label="Selected Region", value=selected_region)
        kpi_placeholder.metric(label="Total Value", value=f"${total_value:,.2f}")
        kpi_placeholder.metric(label="Average Employees (2018-2023)", value=total_employees_mean)

        # Group by Year and calculate sum of VALUE
        summary_table = region_data.groupby("Year").agg({"VALUE": "sum"}).reset_index()
        summary_table["VALUE"] = summary_table["VALUE"].astype("int")
        summary_table.columns = ["Year", "Total VALUE"]
        # table_placeholder.table(summary_table)
        st.dataframe(summary_table,width=800)
        # st.write(table_placeholder.table(summary_table))


c1,c2 = st.columns([1.5,1.75])

with c1:
    # Dropdown for region selection
    selected_region = st.selectbox("Select a region:", options=[""] + regions)
    # Display KPI and Table for selected region

with c2:
    if selected_region:
        display_kpi_and_table(selected_region)
    else:
        kpi_placeholder.write("Select a region to display the KPI and summary table")


st.empty()
st.divider()

label = '''
Data Ref: [Statistics Canada. Table 14-10-0201-01  Employment by industry, monthly, unadjusted for seasonality](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020101)
'''

st.write(label)
