import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Function to connect to MongoDB and fetch data
def fetch_data_from_mongodb(option=None):
    client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
    db = client['NikitaDB']  # Replace with your database name
    collection = db['customers']  # Replace with your collection name
    data = pd.DataFrame(list(collection.find()))
    return data

# Set dark background for Streamlit app
st.markdown("""
    <style>
        body {
            background-color: #D3D3D3;  /* Dark background color */
            color: white;  /* White text */
        }
        
        .css-18e3th9 {
            background-color: #D3D3D3;  /* Dark sidebar */
            color: white;
        }
        
        .streamlit-expanderHeader {
            color: white;
        }
        
        .stText {
            color: white;
        }
        
        .stSelectbox, .stButton, .stSlider, .stRadio, .stCheckbox {
            background-color: #D3D3D3;  /* Dark background for controls */
            color: white;
        }

        .stApp {
            background-color: #D3D3D3;
        }

        .plotly-graph-div {
            background-color: #D3D3D3;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.title("MongoDB Chart Dashboard")

# Fetch data
data = fetch_data_from_mongodb()

# Ensure data is available
if not data.empty:
    # Section for Pie Chart
    st.header("Pie Chart")
    with st.expander("Configure Pie Chart"):
        # Dropdown for selecting column for the pie chart
        pie_column = st.selectbox("Select Column for Pie Chart", data.columns, key="pie_column_dropdown")
        
        # Dropdown for selecting the display metric (Count, Percentage, or both)
        display_metric = st.selectbox("Select Metric to Display", ["Count", "Percentage", "Count & Percentage"], key="metric_dropdown")
        
        if pie_column:
            # Create a DataFrame with count values
            count_data = data[pie_column].value_counts().reset_index()
            count_data.columns = [pie_column, 'Count']
            
            # Add percentage column
            count_data['Percentage'] = count_data['Count'] / count_data['Count'].sum() * 100
            
            # Prepare the labels
            if display_metric == "Count":
                count_data['Labels'] = count_data[pie_column] + ": " + count_data['Count'].astype(str)
                fig_pie = px.pie(count_data, names=pie_column, values='Count', title="Pie Chart")
                fig_pie.update_traces(textinfo='label+value')
            elif display_metric == "Percentage":
                count_data['Labels'] = count_data[pie_column] + ": " + count_data['Percentage'].round(2).astype(str) + "%"
                fig_pie = px.pie(count_data, names=pie_column, values='Percentage', title="Pie Chart")
                fig_pie.update_traces(textinfo='label+percent')
            elif display_metric == "Count & Percentage":
                count_data['Labels'] = count_data[pie_column] + ": " + count_data['Count'].astype(str) + " (" + count_data['Percentage'].round(2).astype(str) + "%)"
                fig_pie = px.pie(count_data, names=pie_column, values='Count', title="Pie Chart")
                fig_pie.update_traces(textinfo='label+value+percent')

            st.plotly_chart(fig_pie)

    # Section for Bar Chart
    st.header("Bar Chart")
    with st.expander("Configure Bar Chart"):
        x_axis = st.selectbox("Select X-axis Column", data.columns, key="bar_x_axis_dropdown")
        y_axis = st.selectbox("Select Y-axis Column", data.columns, key="bar_y_axis_dropdown")
        if x_axis and y_axis:
            fig_bar = px.bar(data, x=x_axis, y=y_axis, title="Bar Chart")
            st.plotly_chart(fig_bar)
else:
    st.error("No data available to display charts.")
