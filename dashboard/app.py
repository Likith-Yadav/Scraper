import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

def load_data():
    """Load the latest data from all data files in the data directory"""
    data = []
    # Fix the path to look in the correct data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Try to load enriched data first
    enriched_data_path = os.path.join(data_dir, 'enriched_data.json')
    if os.path.exists(enriched_data_path):
        try:
            with open(enriched_data_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if content and isinstance(content, list):
                    data.extend(content)
        except json.JSONDecodeError:
            st.warning("Enriched data file is empty or invalid")
    
    # Load business leads
    business_leads_path = os.path.join(data_dir, 'business_leads.json')
    if os.path.exists(business_leads_path):
        try:
            with open(business_leads_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if content and isinstance(content, list):
                    data.extend(content)
        except json.JSONDecodeError:
            st.warning("Business leads file is empty or invalid")
    
    # Load all scrape result files
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.startswith('scrape_result_') and filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        if content:  # Add single result or extend list
                            if isinstance(content, list):
                                data.extend(content)
                            else:
                                data.append(content)
                except json.JSONDecodeError:
                    continue
    
    return data

def main():
    st.set_page_config(page_title="Lead Generation Dashboard", layout="wide")
    
    st.title("Lead Generation Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    data = load_data()
    
    with col1:
        st.metric("Total Leads", len(data))
    with col2:
        enriched_count = sum(1 for item in data if 'enriched_data' in item)
        st.metric("Enriched Leads", enriched_count)
    with col3:
        email_count = sum(len(item.get('emails', [])) for item in data)
        st.metric("Total Emails Found", email_count)
    with col4:
        # Safer timestamp handling
        timestamps = []
        for item in data:
            # Try different possible timestamp locations
            if 'enriched_data' in item and 'timestamp' in item['enriched_data']:
                timestamps.append(item['enriched_data']['timestamp'])
            elif 'timestamp' in item:
                timestamps.append(item['timestamp'])
            elif 'scrape_time' in item:
                timestamps.append(item['scrape_time'])
        
        if timestamps:
            latest_timestamp = max(timestamps)
            st.metric("Last Update", latest_timestamp)
        else:
            st.metric("Last Update", "No updates yet")
    
    # Data Table
    st.subheader("Latest Leads")
    if data:
        # Create a more readable DataFrame
        display_data = []
        for item in data:
            # Safely handle description
            description = ''
            desc_data = item.get('description', '')
            if isinstance(desc_data, list) and desc_data:
                description = desc_data[0]
            elif isinstance(desc_data, str):
                description = desc_data
            
            # Handle text content
            text_content = ', '.join(item.get('text_content', []))
            
            display_item = {
                'Title': item.get('title', ''),
                'URL': item.get('url', ''),
                'Emails': ', '.join(item.get('emails', [])),
                'Description': description,
                'Text Content': text_content
            }
            display_data.append(display_item)
        
        df = pd.DataFrame(display_data)
        st.dataframe(df)
    else:
        st.info("No data available yet. The scraper will populate this soon.")
    
    # Email List
    st.subheader("Found Emails")
    if data:
        email_data = []
        for item in data:
            for email in item.get('emails', []):
                email_data.append({
                    'Email': email,
                    'Source': item.get('title', ''),
                    'URL': item.get('url', '')
                })
        if email_data:
            email_df = pd.DataFrame(email_data)
            st.dataframe(email_df)
        else:
            st.info("No emails found yet.")
    
    # Filters and Search
    st.sidebar.title("Filters")
    if data:
        # Add search functionality
        search_term = st.sidebar.text_input("Search in titles and descriptions")
        if search_term:
            filtered_data = [
                item for item in data 
                if search_term.lower() in str(item.get('title', '')).lower() 
                or search_term.lower() in str(item.get('description', '')).lower()
            ]
            if filtered_data:
                st.subheader(f"Search Results for '{search_term}'")
                search_df = pd.DataFrame([{
                    'Title': item.get('title', ''),
                    'URL': item.get('url', ''),
                    'Emails': ', '.join(item.get('emails', [])),
                    'Text Content': ', '.join(item.get('text_content', []))
                } for item in filtered_data])
                st.dataframe(search_df)
            else:
                st.info("No matching results found.")

if __name__ == "__main__":
    main()
