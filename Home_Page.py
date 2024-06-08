import streamlit as st

st.set_page_config(layout = "wide")

st.title("NAICS - Employment Data")

st.write("**This dashboard displays employee data across various industries and provinces in Canada, categorized according to the North American Industry Classification System (NAICS). The data covers the period from January 2018 to December 2023.**")

st.subheader("**Analysis:**")

st.markdown('''
Overall, most industries follow a similar trend: a sudden drop in employment due to the COVID-19 pandemic, which caused widespread lockdowns and affected industries globally, followed by a gradual recovery in employment. However, there are some exceptions to this pattern.\n\n

The **Real estate** industry experienced a significant decline and, as of 2023, has not yet surpassed its 2019 peak. In contrast, the number of employees in the **Transportation and warehousing** industries has nearly doubled, as has the workforce in the **Finance and insurance** industry.

One particularly notable industry is **Forestry and support**. Since 2018, it has shown a downward trend in employment. Although there was a slight increase in the number of employees post-COVID, it continues to gradually decline through 2023.
            
**To observe additional trends, please interact with the visuals in this dashboard.**
''')