import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from io import StringIO
import requests


st.set_page_config(layout = "wide")


url = 'https://raw.githubusercontent.com/InsertMusicHere/streamlit_dashboard_glocal/main/1410020101_databaseLoadingData.csv'
response = requests.get(url)
if response.status_code == 200:
   df =  pd.read_csv(StringIO(response.text))
else:
   st.error("Failed to load data from GitHub.")

# --------------
# Split the 'date_data' column into 'year' and 'month' columns
# --------------

df[['Year', 'Month']] = df['REF_DATE'].str.split('-', expand=True)

df = df.rename(columns={"North American Industry Classification System (NAICS)":"NAICS"})

df = df[['Year', 'Month', 'GEO', 
       'NAICS', 'VALUE',
       'STATUS', 'Lat', 'Lang']]

list_4 = ["2024"]
df = df[~df["Year"].isin(list_4)]

# ----------
# Making three different dataframes which are, Overall Canada information, only aggregated and only provinces excluding overall
# ----------
list_3 = ["Industrial aggregate including unclassified businesses [00-91N]","Industrial aggregate excluding unclassified businesses [11-91N]","Service producing industries [41-91N]"]
only_canada_df = df[df['GEO']=="Canada"]
only_canada_df = only_canada_df[~only_canada_df["NAICS"].isin(list_3)]

only_aggregrated_industries = df[(df['NAICS'] == "Industrial aggregate including unclassified businesses [00-91N]") | 
                                 (df['NAICS'] == "Industrial aggregate excluding unclassified businesses [11-91N]")|
                                 (df['NAICS'] == "Service producing industries [41-91N]")]

# print(only_aggregrated_industries)

list_1 = ["Canada"]
list_2 = ["Industrial aggregate including unclassified businesses [00-91N]","Industrial aggregate excluding unclassified businesses [11-91N]","Service producing industries [41-91N]"]

only_provinces = df[~df["GEO"].isin(list_1)]
only_provinces = df[~df["NAICS"].isin(list_2)]

# -------------
# Data and Preprocessing
# -------------

st.title("Employment Trends in Canada")
st.markdown("This page features analysis and visualizations on employment trends across various Canadian industries.")

# st.markdown("After using several different algorithms, Randomforest regressor finalized as it gave the best :green[$R^2$] score as compare to other algorithms.")
# st.code("Final model\n 1.R^2 score = 0.93\n 2.Mean Absolute Arror: 16.08\n 3.Mean Squared Error: 26.70")


# Group by 'Month' and 'NAICS' and calculate the average 'VALUE'
df_grouped = only_canada_df.groupby(['Year', 'NAICS']).agg({'VALUE': 'mean'}).reset_index()


# Display the chart in Streamlit
# Calculate total VALUE for each NAICS class
total_value_by_naics = only_canada_df.groupby('NAICS')['VALUE'].sum().reset_index()

# Calculate grand total of VALUE
grand_total_value = total_value_by_naics['VALUE'].sum()

# Calculate the percentage of each NAICS class
total_value_by_naics['Percentages'] = ((total_value_by_naics['VALUE'] / grand_total_value) * 100)
total_value_by_naics['Percentages'] = total_value_by_naics['Percentages'].round(2)

# Display the table with NAICS and their Percentagess


# st.write("---")
st.subheader("Annual Employment Trends by Industry")
# st.write("---")


# --------
# Analysis
# --------
regions = ['Goods producing industries [11-33N]','Forestry, logging and support [11N]','Mining, quarrying, and oil and gas extraction [21]','Utilities [22,221]','Construction [23]','Manufacturing [31-33]','Trade [41-45N]','Transportation and warehousing [48-49]','Information and cultural industries [51]','Finance and insurance [52]','Real estate and rental and leasing [53]','Professional, scientific and technical services [54,541]','Management of companies and enterprises [55,551,5511]','Administrative and support, waste management and remediation services [56]','Educational services [61,611]','Health care and social assistance [62]','Arts, entertainment and recreation [71]','Accommodation and food services [72]','Other services (except public administration) [81]','Public administration [91]','Unclassified businesses [00]']

industry_analysis = {
   "Goods producing industries [11-33N]": "There is a steady increase in employment from 2020 onwards, indicating robust growth and expansion in this sector during the period. This trend highlights the sector's ability to generate new job opportunities consistently.",

   "Forestry, logging and support [11N]": "Since 2018, it has shown a downward trend in employment. Although there was a slight increase in the number of employees post-COVID, it continues to gradually decline through 2023.",

   "Mining, quarrying, and oil and gas extraction [21]": "Noticeable growth in employment from January to May 2018 reflects a positive upward trend, driven by increased demand and production in this industry. This growth underscores the sector's vital role in the national economy and resource extraction.",

   "Utilities [22,221]": "Employment remains relatively constant with minor fluctuations, suggesting long-term stability and consistent operational demands in the utilities sector. The steadiness in this sector is essential for maintaining reliable infrastructure services.",

   "Construction [23]": "There is a gradual increase in employment from January to May 2018, indicating ongoing growth and development activities in the construction industry. This upward trend signifies a healthy investment environment and expanding infrastructure projects.",

   "Manufacturing [31-33]": "A consistent rise in employment throughout the observed months highlights positive growth and increased production capacity in manufacturing. This trend points to a strong manufacturing base and improved industrial output.",

   "Wholesale and Retail Trade [41, 44-45]": "Stable employment with slight increases reflects steady demand and consumer confidence in wholesale and retail trade sectors. This consistency is vital for economic stability and consumer market dynamics.",

   "Transportation and Warehousing [48-49]": "Employment shows a mild upward trend, indicating gradual growth and expansion in transportation and warehousing services. This growth suggests improved logistics and distribution networks catering to increased commercial activities.",

   "Information and Cultural Industries [51]": "Employment remains stable with minor variations, suggesting a steady state and consistent performance in this sector. This stability supports ongoing innovation and cultural development within the industry.",

   "Finance and Insurance [52]": "A slight upward trend in employment points to gradual growth and increased financial activities within the finance and insurance industries. This positive trend indicates a robust financial sector capable of supporting economic development.",

   "Real Estate and Rental and Leasing [53]": "Employment is stable with minimal fluctuations, indicating consistency and ongoing demand in real estate and rental services. This steadiness reflects a healthy property market and sustained leasing activities.",

   "Professional, scientific and technical services [54,541]": "There is a gradual increase in employment, reflecting ongoing growth and investment in professional and technical services. This upward trend highlights the sector's importance in driving innovation and providing specialized expertise.",

   "Management of companies and enterprises [55,551,5511]": "Employment remains relatively constant, showing stability and sustained performance in the management of companies and enterprises. This stability is crucial for strategic corporate governance and long-term business planning.",

   "Administrative and Support, Waste Management and Remediation Services [56]": "Slight growth in employment over the observed period suggests modest yet positive development in administrative and support services. This growth is indicative of increasing demand for efficient business operations and environmental management services.",

   "Educational services [61,611]": "Employment shows a steady upward trend, indicating continuous growth and increased demand in educational services. This trend underscores the importance of education in fostering skill development and knowledge dissemination.",

   "Health Care and Social Assistance [62]": "Consistent rise in employment highlights positive growth and expanding needs in the health care and social assistance sectors. This growth is essential for meeting the increasing demands of an aging population and advancing healthcare services.",

   "Arts, Entertainment and Recreation [71]": "Employment remains stable with slight fluctuations, suggesting a consistent and resilient performance in arts, entertainment, and recreation. This stability is vital for cultural enrichment and the sustainable development of creative industries.",

   "Accommodation and Food Services [72]": "There is a gradual increase in employment, indicating growth and rising demand in accommodation and food services. This positive trend reflects the sector's recovery and expansion, driven by increased tourism and dining activities.",

   "Other Services (except Public Administration) [81]": "Employment is stable with minor increases, reflecting steady demand and ongoing activities in other services. This consistency is crucial for supporting diverse community needs and ancillary services.",

   "Public Administration [91]": "Employment shows a slight upward trend, indicating gradual growth and sustained government activities in public administration. This growth is essential for maintaining public services and effective governance.",
   
   "Trade [41-45N]":"Employment in the Trade sector shows a stable trend with slight increases, reflecting steady demand and consumer confidence. This consistency highlights the sector's resilience and its crucial role in facilitating commercial activities and economic stability.",

   "Unclassified businesses [00]":"Despite the fluctuations, the presence of employment in this category indicates the existence of emerging or transitional businesses that do not fit traditional industry classifications, suggesting dynamism and potential growth areas within the economy."
}



# ------------
# Analysis of the aggregated data
# ------------

regions = ['Goods producing industries [11-33N]','Forestry, logging and support [11N]','Mining, quarrying, and oil and gas extraction [21]','Utilities [22,221]','Construction [23]','Manufacturing [31-33]','Trade [41-45N]','Transportation and warehousing [48-49]','Information and cultural industries [51]','Finance and insurance [52]','Real estate and rental and leasing [53]','Professional, scientific and technical services [54,541]','Management of companies and enterprises [55,551,5511]','Administrative and support, waste management and remediation services [56]','Educational services [61,611]','Health care and social assistance [62]','Arts, entertainment and recreation [71]','Accommodation and food services [72]','Other services (except public administration) [81]','Public administration [91]','Unclassified businesses [00]']


# Dropdown for region selection
selected_region = st.selectbox("Select an Industry:", options=[""] + regions)

st.write("---")

def format_int_with_commas(x):
   """
   Formats an integer with commas as thousand separators.
   """
   return f"{x:,}"

# ----
# KPIs
# ----

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
   kpi_year = only_canada_df[(only_canada_df['NAICS'] == selected_region) & (only_canada_df['Year'] == year)]
   total_value = int(kpi_year['VALUE'].sum())
   kpi_values.append(total_value)

# Display KPIs with YOY delta

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



c1,c2 = st.columns([1.5,2.5])

with c1:
   st.write("Percentage of Employees in Specific Industries")
   if selected_region:
      df = total_value_by_naics[['NAICS', 'Percentages']]
      df = df[df['NAICS']==selected_region]
      st.dataframe(df,width=200,use_container_width=True)

      st.empty()
      st.empty()
      st.empty()
      st.empty()

      st.write("---")

      if industry_analysis.get(selected_region) != None:
         
         st.markdown(f"### Analysis of {selected_region}:")
         st.markdown(f"**What the data says:** {industry_analysis.get(selected_region)}")
         
         st.write("---")

   else:
      st.dataframe(total_value_by_naics[['NAICS', 'Percentages']],width=200,use_container_width=True)

with c2:
   
   # st.write("Average Number of Employees in Specific Industries")
   if selected_region:

      # only_canada_df['VALUE'] = only_canada_df['VALUE'] / 1000000
      # Grouping data and filtering for selected NAICS
      df_grouped = only_canada_df.groupby(['Year', 'NAICS']).agg({'VALUE': 'mean'}).reset_index()
      df_grouped = df_grouped[df_grouped['NAICS'] == selected_region]

      # Creating the line chart
      small_line_chart = px.line(
         df_grouped,
         x='Year',
         y='VALUE',
         color='NAICS',
         labels={'VALUE': 'Average Employee Numbers', 'Year': 'Year', 'NAICS': 'NAICS'},
         title='Average Number of Employees in Specific Industries (Hover over line markers for details)'
      )

      # Removing legends
      small_line_chart.update_layout(showlegend=False)

      # Adding hover information
      small_line_chart.update_traces(
         mode='lines+markers'
      )

      # Update layout to increase plot area
      small_line_chart.update_layout(
         margin=dict(l=40, r=40, t=40, b=40),
         autosize=True,
         height=450  # Increase height for better visibility
      )

      # Displaying the chart
      st.plotly_chart(small_line_chart, use_container_width=True)

   else:

      df_grouped = only_canada_df.groupby(['Year', 'NAICS']).agg({'VALUE': 'mean'}).reset_index()

      small_line_chart = px.line(
         df_grouped,
         x='Year',
         y='VALUE',
         color='NAICS',
         labels={'VALUE': 'Average Employee Numbers', 'Year': 'Year', 'NAICS': 'NAICS'},
         title='Average Number of Employees in Specific Industries (Hover over line markers for details)'
      )

      # Removing legends
      small_line_chart.update_layout(showlegend=False)

      # Adding hover information
      small_line_chart.update_traces(
         mode='lines+markers',
         # hovertemplate='<b>%{y}</b> Employees<br>' + selected_region + '<extra></extra>'
      )

      # Update layout to increase plot area
      small_line_chart.update_layout(
         margin=dict(l=40, r=40, t=40, b=40),
         autosize=True,
         height=450  # Increase height for better visibility
      )
      
      st.plotly_chart(small_line_chart, use_container_width=True)






news_keywords = {
   "Goods producing industries [11-33N]": ["Dairy","packaged foods","products"],
   "Forestry, logging and support [11N]": ["Forestry","lumber","timber"],
   "Mining, quarrying, and oil and gas extraction [21]": ["Mining","oil","gold"],
   "Utilities [22,221]": ["Utilities","gas Utilities","water Utilities"],
   "Construction [23]": ["Construction","home building","Houses"],
   "Manufacturing [31-33]": ["Manufacturing","auto Manufacturers","electronics Manufacturing"],
   "Wholesale and Retail Trade [41, 44-45]": ["Retail","Ecommerce","wholesale"],
   "Transportation and Warehousing [48-49]": ["Transportation","Warehousing","trucking"],
   "Information and Cultural Industries [51]": ["entertainment","media","publishing"],
   "Finance and Insurance [52]": ["Finance","banking","insurance"],
   "Real Estate and Rental and Leasing [53]": ["Real Estate","Rental","Leasing"],
   "Professional, scientific and technical services [54,541]": ["legal","scientific research","accounting"],
   "Management of companies and enterprises [55,551,5511]": ["corporates","enterprises","consultation"],
   "Administrative and Support, Waste Management and Remediation Services [56]": ["Admin","Waste Management","Remediation"],
   "Educational services [61,611]": ["Education","schools","colleges"],
   "Health Care and Social Assistance [62]": ["Health care","hospital","doctors"],
   "Arts, Entertainment and Recreation [71]": ["Entertainment","Arts","Recreation"],
   "Accommodation and Food Services [72]": ["Food","Accommodation","Food Services"],
   "Public Administration [91]": ["Public Administration","urban","community"]
}

# API key
API_TOKEN = st.secrets["db_username"]

# Base URL for the News API
BASE_URL = 'https://api.thenewsapi.com/v1/news/all'



def func_news(param_1,param_2,param_3):

   # Parameters for the request
   params = {
      'api_token': API_TOKEN,  # API token
      'search': "employment OR " + param_1 + " OR " +  param_2 + " OR "  + param_3 + " AND Canada",  # Keywords including Canada
      'language': 'en',  # Language of the articles
      'search_fields': 'title,main_text',  # Fields to search
      'limit': 3,  # Number of articles to return
      'published_after': '2018-01-01T00:00:00',  # Fetch articles published after this date
      'published_before': '2024-12-31T23:59:59',  # Fetch articles published before this date
      'sort': 'relevance_score'  # Sort by relevance
   }

   # Make the GET request
   response = requests.get(BASE_URL, params=params)
   # Check if the request was successful
   if response.status_code == 200:
      # Parse the JSON response
      articles = response.json()
      
      # Print the results with numbering and formatted date
      for i, article in enumerate(articles['data'], start=1):
         # Convert date to mm-dd-yyyy format
         date_str = str(article['published_at'])[:10]
         
         # Display article details
         st.markdown(f"### {i}. {article['title']}")
         st.markdown(f"**Published on:** {date_str}")
         st.markdown(f"**Description:** {article['description']}")
         st.markdown(f"**URL:** [Read more]({article['url']})")
         st.markdown("---")  # Separator line
   else:
      st.error(f"Failed to fetch articles: {response.status_code}")


st.info("Click the button below to fetch the latest news articles related to the "+  selected_region +" Industry in Canada:")

news_button = st.button("Get relevant news articles!")

try:

   if news_button:
      if news_keywords.get(selected_region) != None:
         param1 = news_keywords.get(selected_region)[0]
         param2 = news_keywords.get(selected_region)[1]
         param3 = news_keywords.get(selected_region)[2]

         func_news(param_1=param1,param_2=param2,param_3=param3)
      else:
         func_news(param_1="service industry",param_2="Jobs",param_3="work")
except:
   st.info("No relevant news found!")


st.empty()
st.divider()

label = '''
Data Ref: [Statistics Canada. Table 14-10-0201-01  Employment by industry, monthly, unadjusted for seasonality](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020101)
'''

st.write(label)
