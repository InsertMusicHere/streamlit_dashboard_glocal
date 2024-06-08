import streamlit as st

st.set_page_config(layout = "wide")


st.write("**Data Description**")
st.markdown('''

**Reference Date (REF_DATE):** The data is recorded monthly, starting from January 2018. This allows for a detailed time-series analysis of trends within the goods-producing industries.

**Geographic Location (GEO):** The dataset focuses exclusively on Canada, providing a national perspective on the employment trends within the specified industries.

**North American Industry Classification System (NAICS):** The dataset covers a wide range of sectors such as manufacturing, agriculture, and mining. This classification helps in understanding the distribution and performance of various sub-sectors within the goods-producing category.
            
**Number of Employees (VALUE):** The VALUE column indicates the number of employees within the goods-producing industries for each month. This metric is crucial for assessing labor market trends, employment growth, and sectoral shifts over time.

**Status (STATUS):**
Talks about the status of the data that is collected.
''')

st.write("---")

st.write("**Data Pre-processing**")

st.markdown('''
**1. I have decided to use three different tables for this visualization task.**

First Table: Includes all the values.
Second Table: Excludes all three aggregate values. which are "[00-91N]","[11-91N]" and "[41-91N]"
Third Table: Contains data specific to 'Canada' as a whole.
''')

st.code('''
First Table: Includes all the values.\n
Second Table: Excludes all three aggregate values. which are "[00-91N]","[11-91N]" and "[41-91N]".\n
Third Table: Contains data specific to 'Canada' as a whole.\n
''')

st.markdown('''
**2. Columns with single values, such as 'person' or 'UID', have been removed.**

**3. Empty data points from the 'Values' column have been deleted and data points with a quality status lower than "E" have also been removed.**
''')