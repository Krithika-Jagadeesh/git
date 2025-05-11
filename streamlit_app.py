import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from mysql.connector import connect 
from sqlalchemy import create_engine
from Project_2_python import *

# Creating connection with SQL

connection = connect(
    host = 'localhost',
    port = '3306',
    user = 'root',
    password = '123456',
    database = 'phonepe'
)

# Configuring streamlit layout

r = st.sidebar.radio("**Navigation**", ["Home", "Case Studies"])

if r == "Home" :
    st.title("PhonePe Pulse | The Beat of Progress")

# Case Studies page by defaultly the 1st case study will appear

if r == "Case Studies" :
    sb = st.sidebar.selectbox("Select any case study", 
        [
            "Case Study 1",
            "Case Study 2",
            "Case Study 3",
            "Case Study 4",
            "Case Study 5"
        ]
    )

    # Case Study 1 

    if sb == "Case Study 1" :
        st.markdown("# Decoding Transaction Dynamics on PhonePe")
        st.markdown("## Total Transaction Amount Analysis")

        # Replacing the unmatched states with empty spaces

        agg_tr_df['State'] = agg_tr_df['State'].str.replace("-"," ").str.title()
        agg_tr_df['State'] = agg_tr_df['State'].str.replace("Andaman-&-Nicobar-Islands","Andaman & Nicobar")
        agg_tr_df['State'] = agg_tr_df['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
        agg_tr_df["State"] = agg_tr_df["State"].str.lower().str.strip()    

        # Loading geojson file        

        with open("E:\guvi\Project_2\Project_2\india_states.geojson", "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            feature["properties"]["ST_NM"] = feature["properties"]["ST_NM"].lower()

        # Select the year and Quarter for map

        col1, col2 = st.columns(2, gap = "medium")
        selected_year = col1.selectbox("Year", sorted(agg_tr_df["Year"].unique()))
        selected_quarter = col2.selectbox("Quarter", sorted(agg_tr_df["Quarter"].unique()))

        # Filter data based on selected Year and Quarter

        filtered_df = agg_tr_df[(agg_tr_df["Year"] == selected_year) & (agg_tr_df["Quarter"] == selected_quarter)]

        # Create Choropleth Map

        fig1 = go.Figure(data = go.Choropleth(
            geojson = geojson_data,
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = filtered_df['State'],
            z = filtered_df['Transaction_Amount'] / 1e6,  
            autocolorscale = False,
            colorscale = 'greens',  
            marker_line_color = 'White',
            marker_line_width = 1.5,
            zmin = 0,
            zmax = 1000,

            colorbar = dict(
                title = {'text': "Transaction_Amount (in Millions)"},
                thickness = 15,
                len = 0.80,
                bgcolor = 'rgba(255,255,255,0.6)',
                xanchor = 'left',
                x = 0.01,
                yanchor = 'bottom',
                y = 0.10
            )
                
        ))

        fig1.update_geos(
            visible = False,
            projection = dict(
                type = 'conic conformal',
                parallels = [12.472944444, 35.172805555556],
                rotation = {'lat': 24, 'lon': 80}
            ),
            lonaxis = {'range': [68, 98]},
            lataxis = {'range': [6, 38]}
        )

        fig1.update_layout(
            title = dict(
                text=f"PhonePe Transactions in {selected_year} Q{selected_quarter} by State",
                xanchor = 'center',
                x = 0.5,
                yref = 'paper',
                yanchor = 'bottom',
                y = 1,
                pad = {'b': 10}
            ),
            margin = {'r': 0, 't': 30, 'l': 0, 'b': 0},
            height = 550,
            width = 550
        )
        st.subheader("📌 Choropleth Map")
        st.plotly_chart(fig1)

        # Payment Method Popularity using donut charts

        st.write("### Payment Method Popularity")
        filtered_df = agg_tr_df[(agg_tr_df["Year"] == selected_year) & (agg_tr_df["Quarter"] == selected_quarter)]
        summary_1 = filtered_df.groupby("Transaction_Type")["Transaction_Count"].sum().nlargest(10).reset_index()
        fig = px.pie(
            summary_1, 
            values = "Transaction_Count", 
            names = "Transaction_Type", 
            title = "Transaction Count by Transaction Type",
            hole = 0.4 
        )

        summary_2 = filtered_df.groupby("Transaction_Type")["Transaction_Amount"].sum().nlargest(10).reset_index()
        fig2 = px.pie(
            summary_2, 
            values = "Transaction_Amount", 
            names = "Transaction_Type", 
            title = "Transaction Amount by Transaction Type",
            hole = 0.4 
        )
        
        cola, colb = st.columns(2)
        with cola:
            st.plotly_chart(fig, use_container_width = True)
        with colb:
            st.plotly_chart(fig2, use_container_width = True)
        
        # Transactions by State 

        st.write("### Transactions by State")
        state_summary = filtered_df.groupby("State")["Transaction_Amount"].sum().nlargest(10).sort_values(ascending = False).reset_index()
        state_summary["Transaction_Amount"] = state_summary["Transaction_Amount"] / 1e12
        fig3 = px.bar(
            state_summary, 
            y = "Transaction_Amount", 
            x = "State", 
            text = state_summary["Transaction_Amount"].round(2).apply(lambda x: f"{x:.2f}T"),
            title = "Top 10 States by Transaction Amount",
            orientation = "v", 
            color = "State"
        )
        fig3.update_traces(textposition = 'outside')
        st.plotly_chart(fig3)

        # Transactions by State and Transaction Type

        st.write("### Transactions by State and Transaction Type")
        agg_tr_df["State"] = agg_tr_df["State"].str.title()
        selected_state = st.selectbox("Select a State", agg_tr_df["State"].unique())

        filtered_data_1 = agg_tr_df[agg_tr_df["State"] == selected_state]
        aggregated_data = filtered_data_1.groupby("Transaction_Type", as_index = False)["Transaction_Amount"].sum()

        fig4 = px.line(
            aggregated_data, 
            x = "Transaction_Type", 
            y = "Transaction_Amount", 
            title = f"Transaction Distribution in {selected_state}",
            markers = True
        )

        fig4.update_layout(
            yaxis = dict(
                dtick = 20000000000
            )
        )
        st.plotly_chart(fig4)

        # Trend Analysis

        st.write("### Trend Analysis")
        selected_year = st.selectbox("Select a year", sorted(agg_tr_df["Year"].unique()))
        filtered_data_2 = agg_tr_df[agg_tr_df["Year"] == selected_year]
        quarterly_summary = filtered_data_2.groupby("Quarter", as_index = False)["Transaction_Amount"].sum()
        fig3 = px.bar(
            quarterly_summary,
            x = "Quarter",
            y = "Transaction_Amount",
            title = f"Transaction Amount Trend Analysis for Year {selected_year}",
            text_auto = True,  
            color = "Quarter"  
        )
        st.plotly_chart(fig3)

    
    # Case Study 2

    if sb == "Case Study 2" :
        st.markdown("# Device Dominance and User Engagement Analysis")
        st.markdown("## Heat Map Analysis on Transactions by States")

        # Replacing the unmatched states with empty spaces

        top_tr_df['State'] = top_tr_df['State'].str.replace("-"," ").str.title()
        top_tr_df['State'] = top_tr_df['State'].str.replace("Andaman-&-Nicobar-Islands","Andaman & Nicobar")
        top_tr_df['State'] = top_tr_df['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
        top_tr_df["State"] = top_tr_df["State"].str.lower().str.strip()    

        # Loading geojson file        

        with open("E:\guvi\Project_2\Project_2\india_states.geojson", "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            feature["properties"]["ST_NM"] = feature["properties"]["ST_NM"].lower()

         # Select the year and Quarter for map

        col1, col2 = st.columns(2, gap = "medium")
        selected_year = col1.selectbox("Year", sorted(top_tr_df["Year"].unique()))
        selected_quarter = col2.selectbox("Quarter", sorted(top_tr_df["Quarter"].unique()))

        # Filter data based on selected Year and Quarter

        filtered_df = top_tr_df[(top_tr_df["Year"] == selected_year) & (top_tr_df["Quarter"] == selected_quarter)]

        # Create Choropleth Map

        fig1 = go.Figure(data = go.Choropleth(
            geojson = geojson_data,
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = filtered_df['State'],
            z = filtered_df['Transaction_Amount'] / 1e6,  
            autocolorscale = False,
            colorscale = 'magenta',  
            marker_line_color = 'White',
            marker_line_width = 1.5,
            zmin = 0,
            zmax = 1000,

            colorbar = dict(
                title = {'text': "Transaction_Amount (in Millions)"},
                thickness = 15,
                len = 0.80,
                bgcolor = 'rgba(255,255,255,0.6)',
                xanchor = 'left',
                x = 0.01,
                yanchor = 'bottom',
                y = 0.10
            )
                
        ))

        fig1.update_geos(
            visible = False,
            projection = dict(
                type = 'conic conformal',
                parallels = [12.472944444, 35.172805555556],
                rotation = {'lat': 24, 'lon': 80}
            ),
            lonaxis = {'range': [68, 98]},
            lataxis = {'range': [6, 38]}
        )

        fig1.update_layout(
            title = dict(
                text=f"PhonePe Transactions in {selected_year} Q{selected_quarter} by State",
                xanchor = 'center',
                x = 0.5,
                yref = 'paper',
                yanchor = 'bottom',
                y = 1,
                pad = {'b': 10}
            ),
            margin = {'r': 0, 't': 30, 'l': 0, 'b': 0},
            height = 550,
            width = 550
        )
        st.subheader("📌 Choropleth Map")
        st.plotly_chart(fig1)

        # Top Performing states using donut charts

        st.write("### Top Performing States by Transaction Count and Transaction Amount")
        filtered_df = top_tr_df[(top_tr_df["Year"] == selected_year) & (top_tr_df["Quarter"] == selected_quarter)]
        summary_1 = filtered_df.groupby("State")["Transaction_Count"].sum().nlargest(10).reset_index()
        fig1 = px.pie(
            summary_1, 
            values = "Transaction_Count", 
            names = "State", 
            title = "Top Performing State by Transaction Count",
            hole = 0.4 
        )
        st.plotly_chart(fig1, use_container_width = True)

        summary_2 = filtered_df.groupby("State")["Transaction_Amount"].sum().nlargest(10).reset_index()
        fig2 = px.pie(
            summary_2, 
            values = "Transaction_Amount", 
            names = "State", 
            title = "Top Performing State by Transaction Amount",
            hole = 0.4 
        )
        st.plotly_chart(fig2, use_container_width = True)

        # Top Performing districts using bar chart

        st.write("### Top Performing Districts by Transaction Count and Transaction Amount")
        col1, col2 = st.columns(2, gap = "medium")
        selected_state = col1.selectbox("Select State", sorted(top_tr_df['State'].unique()))
        metric = col2.selectbox("Select Metric", ["Transaction_Count", "Transaction_Amount"])
        filtered_data = top_tr_df[(top_tr_df['Year'] == selected_year) & (top_tr_df['State'] == selected_state) &
                     (top_tr_df['Quarter'] == selected_quarter)]

        fig3 = px.bar(
            filtered_data, x = 'District', 
            y = metric, 
            title = f"Top Performing Districts by {metric}",
            color = 'District', 
            height = 500
        )
        st.plotly_chart(fig3)

        # Top Performing pincode using histogram chart

        st.write("### Top Performing Pincodes by Transaction Count and Transaction Amount")
        col3, col4 = st.columns(2, gap = "medium")
        selected_state_2 = col3.selectbox("Select State", sorted(top_tr_df['State'].unique()), key="state_filter_2")
        metric2 = col4.selectbox("Select Metric", ["Transaction_Count", "Transaction_Amount"], key="metric_filter_2")
        filtered_data_3 = top_tr_df[(top_tr_df['Year'] == selected_year) & (top_tr_df['State'] == selected_state_2) &
                     (top_tr_df['Quarter'] == selected_quarter)]
        
        fig4 = px.line(
            filtered_data_3, 
            x='Pincode', 
            y=metric2, 
            title=f"Top Performing Pincode by {metric2}",
            color='Pincode', 
            markers=True,  
            height=500
        )
        st.plotly_chart(fig4)

        # Low Engagement Regions - Transaction Trends
        
        region_summary = filtered_df.groupby('State').agg({
            'Transaction_Count': 'sum',
            'Transaction_Amount': 'sum'
        }).reset_index()
        
        avg_txn_count = region_summary['Transaction_Count'].mean()
        avg_txn_amount = region_summary['Transaction_Amount'].mean()

        low_engagement = region_summary[
            (region_summary['Transaction_Count'] < avg_txn_count) &
            (region_summary['Transaction_Amount'] < avg_txn_amount)
        ]

        st.write("### 📊 Low Engagement Regions Analysis")
        with st.expander("**Low Engagement Regions Table**"):       
            st.dataframe(low_engagement)

        with st.expander("**Low Engagement Regions Charts**"):
            fig5 = px.line(
                low_engagement, 
                x='State', 
                y="Transaction_Count", 
                title=f"Transaction Count by Low Engagement Region for the Year {selected_year} and  Quarter {selected_quarter}",
                color_discrete_sequence=["#17becf"], 
                markers=True,  
                height=500
            )
            st.plotly_chart(fig5)

            fig6 = px.line(
                low_engagement, 
                x='State', 
                y="Transaction_Amount", 
                title=f"Transaction Amount by Low Engagement Region for the Year {selected_year} and  Quarter {selected_quarter}",
                color_discrete_sequence=["#ff7f0e"], 
                markers=True,  
                height=500
            )
            st.plotly_chart(fig6)


    # Case Study 3

    if sb == "Case Study 3" :
        st.markdown("# User Registration Analysis")
        st.markdown("## Heat Map Analysis on Registered User by States")

        # Replacing the unmatched states with empty spaces

        top_us_df['State'] = top_us_df['State'].str.replace("-"," ").str.title()
        top_us_df['State'] = top_us_df['State'].str.replace("Andaman-&-Nicobar-Islands","Andaman & Nicobar")
        top_us_df['State'] = top_us_df['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
        top_us_df["State"] = top_us_df["State"].str.lower().str.strip()    

        # Loading geojson file        

        with open("E:\guvi\Project_2\Project_2\india_states.geojson", "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            feature["properties"]["ST_NM"] = feature["properties"]["ST_NM"].lower()

         # Select the year and Quarter for map

        col1, col2 = st.columns(2, gap = "medium")
        selected_year = col1.selectbox("Year", sorted(top_us_df["Year"].unique()))
        selected_quarter = col2.selectbox("Quarter", sorted(top_us_df["Quarter"].unique()))

        # Filter data based on selected Year and Quarter

        filtered_df = top_us_df[(top_us_df["Year"] == selected_year) & (top_us_df["Quarter"] == selected_quarter)]

        # Create Choropleth Map

        fig1 = go.Figure(data = go.Choropleth(
            geojson = geojson_data,
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = filtered_df['State'],
            z = filtered_df['Registered_Users'],  
            autocolorscale = False,
            colorscale = 'Portland',  
            marker_line_color = 'White',
            marker_line_width = 1.5,
            zmin = 0,
            zmax = 1000,

            colorbar = dict(
                title = {'text': "Registered_Users (in thousands)"},
                thickness = 15,
                len = 0.80,
                bgcolor = 'rgba(255,255,255,0.6)',
                xanchor = 'left',
                x = 0.01,
                yanchor = 'bottom',
                y = 0.10
            )
                
        ))

        fig1.update_geos(
            visible = False,
            projection = dict(
                type = 'conic conformal',
                parallels = [12.472944444, 35.172805555556],
                rotation = {'lat': 24, 'lon': 80}
            ),
            lonaxis = {'range': [68, 98]},
            lataxis = {'range': [6, 38]}
        )

        fig1.update_layout(
            title = dict(
                text=f"PhonePe Registered Users in Year {selected_year} and Quarter {selected_quarter} by State",
                xanchor = 'center',
                x = 0.5,
                yref = 'paper',
                yanchor = 'bottom',
                y = 1,
                pad = {'b': 10}
            ),
            margin = {'r': 0, 't': 30, 'l': 0, 'b': 0},
            height = 550,
            width = 550
        )
        st.subheader("📌 Choropleth Map")
        st.plotly_chart(fig1)

        # Top registered users state wise using bar chart

        st.write("### Top States With Registered Users")
        filtered_df = top_us_df[(top_us_df["Year"] == selected_year) & (top_us_df["Quarter"] == selected_quarter)]

        fig = px.bar(
            filtered_df, 
            x = 'State', 
            y = 'Registered_Users', 
            title = f"Top Performing States With Registered Users by Year {selected_year} and Quarter {selected_quarter}",
            color = 'State', 
            height = 500,
        )
        st.plotly_chart(fig)

        # Top registered users district wise using scatter chart

        st.write("### Top Districts With Registered Users")
        
        fig4 = px.scatter(
            filtered_df, 
            x='District', 
            y='Registered_Users', 
            title=f"Top Performing Districts With Registered Users by Year {selected_year} and Quarter {selected_quarter}",
            color='District', 
            size='Registered_Users',  
            height=500
        )

        st.plotly_chart(fig4)

        # Top registered users pincode wise using scatter chart

        st.write("### Top Pincodes With Registered Users")
        filtered_df = filtered_df.groupby('Pincode', as_index=False)['Registered_Users'].sum()
        filtered_df = filtered_df.sort_values(by='Registered_Users', ascending=False)

        fig = px.histogram(
            filtered_df.head(50),  # Limiting to top 50 pincodes for clarity
            x='Pincode', 
            y='Registered_Users', 
            title=f"Top Performing Pincodes With Registered Users by Year {selected_year} and Quarter {selected_quarter}",
            color='Pincode', 
            nbins=20,  # Adjust number of bins for better visibility
            histfunc='sum',
            height=600,
        )
        st.plotly_chart(fig)


    # Case Study 4

    if sb == "Case Study 4" :
        st.markdown("# Insurance Transactions Analysis")
        st.markdown("## Heat Map Analysis on Insurance Amount by States")

        # Replacing the unmatched states with empty spaces

        top_in_df['State'] = top_in_df['State'].str.replace("-"," ").str.title()
        top_in_df['State'] = top_in_df['State'].str.replace("Andaman-&-Nicobar-Islands","Andaman & Nicobar")
        top_in_df['State'] = top_in_df['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
        top_in_df["State"] = top_in_df["State"].str.lower().str.strip()    

        # Loading geojson file        

        with open("E:\guvi\Project_2\Project_2\india_states.geojson", "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            feature["properties"]["ST_NM"] = feature["properties"]["ST_NM"].lower()

         # Select the year and Quarter for map

        col1, col2 = st.columns(2, gap = "medium")
        selected_year = col1.selectbox("Year", sorted(top_us_df["Year"].unique()))
        selected_quarter = col2.selectbox("Quarter", sorted(top_us_df["Quarter"].unique()))

        # Filter data based on selected Year and Quarter

        filtered_df = top_in_df[(top_in_df["Year"] == selected_year) & (top_in_df["Quarter"] == selected_quarter)]

        # Create Choropleth Map

        fig1 = go.Figure(data = go.Choropleth(
            geojson = geojson_data,
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = filtered_df['State'],
            z = filtered_df['Insurance_Amount'] ,  
            autocolorscale = False,
            colorscale = 'earth',  
            marker_line_color = 'White',
            marker_line_width = 1.5,
            zmin = 0,
            zmax = 1000,

            colorbar = dict(
                title = {'text': "Insurance_Amount (in thousands)"},
                thickness = 15,
                len = 0.80,
                bgcolor = 'rgba(255,255,255,0.6)',
                xanchor = 'left',
                x = 0.01,
                yanchor = 'bottom',
                y = 0.10
            )
                
        ))

        fig1.update_geos(
            visible = False,
            projection = dict(
                type = 'conic conformal',
                parallels = [12.472944444, 35.172805555556],
                rotation = {'lat': 24, 'lon': 80}
            ),
            lonaxis = {'range': [68, 98]},
            lataxis = {'range': [6, 38]}
        )

        fig1.update_layout(
            title = dict(
                text=f"PhonePe Insurance Transaction Amount in Year {selected_year} and Quarter {selected_quarter} by State",
                xanchor = 'center',
                x = 0.5,
                yref = 'paper',
                yanchor = 'bottom',
                y = 1,
                pad = {'b': 10}
            ),
            margin = {'r': 0, 't': 30, 'l': 0, 'b': 0},
            height = 550,
            width = 550
        )
        st.subheader("📌 Choropleth Map")
        st.plotly_chart(fig1)

        # Top state wise insurance count using bar chart

        st.write("### Top States With Insurance Transaction Count")
        filtered_df = top_in_df[(top_in_df["Year"] == selected_year) & (top_in_df["Quarter"] == selected_quarter)]

        fig = px.bar(
            filtered_df, 
            x = 'State', 
            y = 'Insurance_Count', 
            title = f"Top Performing States With Insurance Transaction Count by Year {selected_year} and Quarter {selected_quarter}",
            color = 'State', 
            height = 500,
        )
        st.plotly_chart(fig)

        # Top insurance count district wise using scatter chart

        st.write("### Top Districts With Insurance_Count")
        fig4 = px.scatter(
            filtered_df, 
            x='District', 
            y='Insurance_Count', 
            title=f"Top Performing Districts Insurance Transaction Count by Year {selected_year} and Quarter {selected_quarter}",
            color='District', 
            size='Insurance_Count',  
            height=500
        )
        st.plotly_chart(fig4)

        # Top insurance count pincode wise using scatter chart

        st.write("### Top Pincodes With Insurance_Count")
        filtered_df = filtered_df.groupby('Pincode', as_index=False)['Insurance_Count'].sum()
        filtered_df = filtered_df.sort_values(by='Insurance_Count', ascending=False)

        fig = px.histogram(
            filtered_df.head(50), 
            x='Pincode', 
            y='Insurance_Count', 
            title=f"Top Performing Pincodes With Insurance Transaction Count by Year {selected_year} and Quarter {selected_quarter}",
            color='Pincode', 
            nbins=20, 
            histfunc='sum',
            height=600,
        )
        st.plotly_chart(fig)


    # Case Study 5

    if sb == "Case Study 5" :
        st.markdown("# Transaction Analysis for Market Expansion")
        st.markdown("## Map Transaction Analysis")

        # Replacing the unmatched states with empty spaces

        map_tr_df['State'] = map_tr_df['State'].str.replace("-"," ").str.title()
        map_tr_df['State'] = map_tr_df['State'].str.replace("Andaman-&-Nicobar-Islands","Andaman & Nicobar")
        map_tr_df['State'] = map_tr_df['State'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')
        map_tr_df["State"] = map_tr_df["State"].str.lower().str.strip()    

        # Loading geojson file        

        with open("E:\guvi\Project_2\Project_2\india_states.geojson", "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            feature["properties"]["ST_NM"] = feature["properties"]["ST_NM"].lower()

         # Select the year and Quarter for map

        col1, col2 = st.columns(2, gap = "medium")
        selected_year = col1.selectbox("Year", sorted(map_tr_df["Year"].unique()))
        selected_quarter = col2.selectbox("Quarter", sorted(map_tr_df["Quarter"].unique()))

        # Filter data based on selected Year and Quarter

        filtered_df = map_tr_df[(map_tr_df["Year"] == selected_year) & (map_tr_df["Quarter"] == selected_quarter)]

        # Create Choropleth Map

        fig1 = go.Figure(data = go.Choropleth(
            geojson = geojson_data,
            featureidkey = 'properties.ST_NM',
            locationmode = 'geojson-id',
            locations = filtered_df['State'],
            z = filtered_df['Transaction_Amount'] / 1e6,  
            autocolorscale = False,
            colorscale = 'armyrose',  
            marker_line_color = 'White',
            marker_line_width = 1.5,
            zmin = 0,
            zmax = 1000,

            colorbar = dict(
                title = {'text': "Transaction_Amount (in millions)"},
                thickness = 15,
                len = 0.80,
                bgcolor = 'rgba(255,255,255,0.6)',
                xanchor = 'left',
                x = 0.01,
                yanchor = 'bottom',
                y = 0.10
            )
                
        ))

        fig1.update_geos(
            visible = False,
            projection = dict(
                type = 'conic conformal',
                parallels = [12.472944444, 35.172805555556],
                rotation = {'lat': 24, 'lon': 80}
            ),
            lonaxis = {'range': [68, 98]},
            lataxis = {'range': [6, 38]}
        )

        fig1.update_layout(
            title = dict(
                text=f"PhonePe Transaction Amount in Year {selected_year} and Quarter {selected_quarter} by State",
                xanchor = 'center',
                x = 0.5,
                yref = 'paper',
                yanchor = 'bottom',
                y = 1,
                pad = {'b': 10}
            ),
            margin = {'r': 0, 't': 30, 'l': 0, 'b': 0},
            height = 550,
            width = 550
        )
        st.subheader("📌 Choropleth Map")
        st.plotly_chart(fig1)

        # Top states by transaction count and transaction amount using donut charts

        st.write("###  Top States By Transaction Count and Transaction Amount")
        filtered_df = agg_tr_df[(agg_tr_df["Year"] == selected_year) & (agg_tr_df["Quarter"] == selected_quarter)]
        summary_1 = filtered_df.groupby("State")["Transaction_Count"].sum().nlargest(10).reset_index()
        fig = px.pie(
            summary_1, 
            values = "Transaction_Count", 
            names = "State", 
            title = f"Transaction Count by State in {selected_year} & Q{selected_quarter}",
            hole = 0.4 
        )

        summary_2 = filtered_df.groupby("State")["Transaction_Amount"].sum().nlargest(10).reset_index()
        fig2 = px.pie(
            summary_2, 
            values = "Transaction_Amount", 
            names = "State", 
            title = f"Transaction Amount by State in {selected_year} & Q{selected_quarter}",
            hole = 0.4 
        )
        
        cola, colb = st.columns(2)
        with cola:
            st.plotly_chart(fig, use_container_width = True)
        with colb:
            st.plotly_chart(fig2, use_container_width = True)

        # Average transaction amount per state using bar chart

        st.write("### Average Transaction Amount Per State")
        avg_transaction = filtered_df.groupby("State")["Transaction_Amount"].mean().reset_index()

        fig = px.bar(
            avg_transaction, 
            x = 'State', 
            y = 'Transaction_Amount', 
            title = f"Average Transaction Amount Per State in {selected_year} & Q{selected_quarter}",
            color = 'State', 
            height = 500,
        )
        st.plotly_chart(fig)
        
        # Growth Trends by quarter

        st.write("### Transaction Growth Trends")

        filtered_df["Prev_Transaction"] = filtered_df.groupby("State")["Transaction_Amount"].shift(1)
        filtered_df["Growth_Percentage"] = ((filtered_df["Transaction_Amount"] - filtered_df["Prev_Transaction"]) / filtered_df["Prev_Transaction"]) * 100
        filtered_df.dropna(inplace=True)  

        fig1 = px.scatter(
            filtered_df, 
            x="Year",
            y="Transaction_Amount", 
            color="State", 
            title="Transaction Growth Over Years",
            size="Transaction_Amount",  # Optional: Adjust dot size based on transaction amount
            hover_data=["State", "Year", "Transaction_Amount"]  # Display details on hover
        )
        st.plotly_chart(fig1)

        fig2 = px.bar(
            filtered_df, 
            x="State",
            y="Growth_Percentage",
            color="State",
            title="Quarterly Growth Percentage by State"
        )
        st.plotly_chart(fig2)
