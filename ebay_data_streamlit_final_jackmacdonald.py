import pandas as pd
import streamlit as st
import plotly.express as px

## terminal command
# python -m streamlit run ebay_data_streamlit_final_jackmacdonald.py

# Streamlit Page Configuration
st.set_page_config(page_title="Ebay Data Dashboard", layout="wide")

# Load Data
df = pd.read_csv('ebay_df.csv')

# Function to clean and process the Price column
def clean_price(price):
    price = price.replace('$', '')
    if '-' in price:
        try:
            low, high = map(float, price.split('-'))
            return (low + high) / 2
        except ValueError:
            return None
    try:
        return float(price)
    except ValueError:
        return None

# Apply the cleaning function to the Price column
df['Price'] = df['Price'].apply(clean_price)
df.dropna(subset=['Price'], inplace=True)

# Dashboard Header
st.title("Ebay Data Dashboard")
st.write("---")

# Create Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Full Data", "Filter by Brand", "Filter by Type", "Filter by Price", "Visualizations"])

# Tab 1: Full Data
with tab1:
    st.header("Ebay CSV Data")
    st.dataframe(df, use_container_width=True, height=400)
    st.write("---")

# Tab 2: Filter by Brand
with tab2:
    st.subheader("Computers filtered by Brand")
    brand_options = df['Brand'].unique()
    brand_selection = st.multiselect('Select Brand(s):', options=brand_options, default=["Dell"])
    filtered_df_brand = df[df['Brand'].isin(brand_selection)]
    st.dataframe(filtered_df_brand)
    st.write("---")

# Tab 3: Filter by Type
with tab3:
    st.subheader("Computers filtered by Type")
    type_options = df['Type'].unique()
    type_selection = st.multiselect('Select Type(s):', options=type_options, default=type_options)
    filtered_df_type = df[df['Type'].isin(type_selection)]
    st.write("Filtered Dataframe:")
    st.dataframe(filtered_df_type)
    st.write("---")

# Tab 4: Filter by Price
with tab4:
    st.subheader("Computers filtered by Price")
    min_price, max_price = int(df['Price'].min()), int(df['Price'].max())
    price_range = st.slider("Select a price range:", min_price, max_price, (min_price, max_price))
    filtered_df_price = df[(df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1])]
    st.write("Filtered Dataframe:")
    st.dataframe(filtered_df_price)
    st.write("---")

# Tab 5: Visualizations
with tab5:
    # Visualization: Average Price by Brand
    st.subheader("Average Price by Brand")
    price_by_brand = df.groupby('Brand')['Price'].mean().reset_index()
    st.bar_chart(data=price_by_brand, x='Brand', y='Price')
    st.write("""
    ### Brand-Price Analysis
    Key Insights:
            
    - MSI stands out as the brand with the highest average price, reflecting its focus on premium and high-performance products, likely targeting gamers and professionals requiring powerful hardware.
            
    - Panasonic follows closely, also positioned in the high-price segment, which could indicate a focus on specialized or niche markets, such as rugged laptops or industry-specific solutions.
            
    - Brands like ASUS, LG, and GPD maintain mid-range average prices, suggesting a balance between affordability and quality, appealing to a broader customer base.
            
    - Dell, Toshiba, and Acer operate in the lower price range, highlighting their competitive pricing strategies to capture value-conscious customers.
            
    - Lenovo T440 and Microsoft appear to target niche or specialized markets, as reflected by their below-average pricing compared to high-end brands like MSI and Panasonic.
    """)
    st.write("---")

    # Visualization: Brand vs Condition vs Price (Bubble Chart)
    st.subheader("Brand vs Condition vs Price (Bubble Chart)")
    bubble_chart_fig = px.scatter(
        df, x='Brand', y='Condition', size='Price', color='Brand',
        title="Brand vs Condition with Price as Bubble Size",
        labels={'Brand': 'Brand', 'Condition': 'Condition', 'Price': 'Price ($)'}
    )
    st.plotly_chart(bubble_chart_fig)
    st.write("""
    ### Brand-Price-Condition Analysis
    Key Insights:
            
    Brand Performance Across Conditions:

    - MSI and Panasonic dominate the "Certified" and "Excellent" conditions with larger bubble sizes, indicating higher average prices for these conditions.
    - Dell, HP, and Lenovo appear in almost every condition category, reflecting their diverse product offerings across both new and used markets. However, their price bubbles are smaller, especially in lower conditions like "Used" and "Good", indicating competitive pricing.
    - Chuwi, CHUWI, and Acer focus heavily on "New" and "Very Good" conditions but show smaller bubble sizes, suggesting their products target budget-conscious consumers.

    Price Variance by Condition:

    - Products in "Certified" and "Excellent" conditions command higher prices across almost all brands, emphasizing that customers are willing to pay a premium for quality assurance.
    - "For Parts" and "Not Available" conditions show limited representation, with smaller bubbles, highlighting that these categories likely represent older or less desirable inventory.

    Brand Representation:

    - Apple and some premium brands like MSI and Panasonic are notably absent in lower conditions like "For Parts", aligning with their high-end positioning.
    - Brands like Toshiba and Gateway are primarily concentrated in mid-range conditions ("Good" and "Used"), suggesting an emphasis on affordability.

    """)
    st.write("---")

    # Visualization: Average Price by Condition for Selected Type
    selected_type = st.selectbox('Select a Product Type:', options=df['Type'].unique(), index=0)
    filtered_df_type_specific = df[df['Type'] == selected_type]
    bar_chart_fig = px.bar(
        filtered_df_type_specific.groupby('Condition')['Price'].mean().reset_index(),
        x='Condition', y='Price',
        title=f"Average Price by Condition for {selected_type}",
        labels={'Condition': 'Product Condition', 'Price': 'Average Price ($)'},
        color='Condition'
    )
    st.subheader(f"Average Price by Condition by Laptop Type")
    st.plotly_chart(bar_chart_fig)