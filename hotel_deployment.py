
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide",page_title="Hotel Booking EDA")

st.markdown("<h1 style='text-align: center;'>🏨 Hotel Booking Exploratory Data Analysis</h1>",unsafe_allow_html=True)

# LOAD DATA
df = pd.read_csv("cleaned booking.csv", index_col=0)

page = st.sidebar.radio("Page",["Data Overview", "Data Analysis", "Hotel General Report"])

if page == "Data Overview":

    st.title("Hotel Booking Dataset Overview")

    st.dataframe(df, use_container_width=True)

    st.markdown("""
    This dashboard analyzes hotel booking data to understand customer behavior,
    cancellation patterns, and booking trends.
    """)

    column_descriptions = {
        "hotel": "Type of hotel (City Hotel or Resort Hotel)",
        "is_canceled": "Whether the booking was canceled (1 = Yes, 0 = No)",
        "lead_time": "Days between booking and arrival",
        "arrival_date_year": "Arrival year",
        "arrival_date_month": "Arrival month",
        "arrival_date_week_number": "Arrival week number",
        "arrival_date_day_of_month": "Arrival day",
        "stays_in_weekend_nights": "Weekend nights stayed",
        "stays_in_week_nights": "Weekday nights stayed",
        "adults": "Number of adults",
        "children": "Number of children",
        "babies": "Number of babies",
        "meal": "Meal plan",
        "country": "Guest country",
        "market_segment": "Market segment",
        "distribution_channel": "Booking channel",
        "is_repeated_guest": "Repeated guest",
        "previous_cancellations": "Past cancellations",
        "previous_bookings_not_canceled": "Past completed bookings",
        "reserved_room_type": "Reserved room type",
        "assigned_room_type": "Assigned room type",
        "booking_changes": "Booking changes",
        "deposit_type": "Deposit type",
        "agent": "Agent ID",
        "company": "Company ID",
        "days_in_waiting_list": "Days in waiting list",
        "customer_type": "Customer type",
        "adr": "Average Daily Rate",
        "required_car_parking_spaces": "Parking spaces required",
        "total_of_special_requests": "Special requests",
        "reservation_status": "Reservation status",
        "reservation_status_date": "Status date"
    }

    desc_df = pd.DataFrame(
        column_descriptions.items(),
        columns=["Column Name", "Description"]
    )

    st.subheader("📋 Column Descriptions")
    st.dataframe(desc_df, use_container_width=True)

elif page == "Data Analysis":

    st.subheader("Overall Cancellation Rate")

    cancel_rate = round(df["is_canceled"].mean() * 100, 2)

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=cancel_rate,
            number={"suffix": "%"}
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Booking Distribution by Channel")

    channel_df = df["distribution_channel"].value_counts().reset_index()
    channel_df.columns = ["distribution_channel", "count"]

    st.plotly_chart(
        px.treemap(
            channel_df,
            path=["distribution_channel"],
            values="count"
        ),
        use_container_width=True
    )

    st.subheader("Average Revenue by Customer Type")

    revenue_df = (
        df.groupby("customer_type", as_index=False)["adr"]
        .mean()
        .round(2)
    )

    st.plotly_chart(
        px.bar(
            revenue_df,
            x="customer_type",
            y="adr",
            text_auto=True,
            labels={"adr": "Average ADR"}
        ),
        use_container_width=True
    )

    st.subheader("Monthly Booking Volume")

    month_df = df["arrival_date_month"].value_counts().reset_index()
    month_df.columns = ["month", "bookings"]

    st.plotly_chart(
        px.bar(
            month_df,
            x="month",
            y="bookings",
            text_auto=True
        ),
        use_container_width=True
    )

    st.subheader("Most Cancelled by market segment")

    most_canceled_segm = df.groupby('market_segment')['is_canceled'].mean().sort_values(ascending=False).round(2).reset_index()
    st.plotly_chart(px.bar(most_canceled_segm, y='market_segment',x = 'is_canceled',text_auto=True,title='Cancelation rate by market segment'))

    st.subheader("Correlations between numerical columns")

    num_col = (['is_canceled', 'lead_time',
       'arrival_date_week_number',
       'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children',
       'babies', 'is_repeated_guest', 'previous_cancellations',
       'previous_bookings_not_canceled', 'booking_changes', 'agent',
       'days_in_waiting_list', 'adr', 'required_car_parking_spaces',
       'total_of_special_requests'])
    corr = df[num_col].corr(numeric_only= True).round(2)
    st.plotly_chart(px.imshow(corr, text_auto= True, height= 800, width= 1000))



elif page == "Hotel General Report":

    st.subheader("Country-Based Booking Analysis")

    country_list = ["All Countries"] + sorted(
        df["country"].dropna().unique().tolist()
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        country_list
    )

    if selected_country == "All Countries":
        df_filtered = df.copy()
    else:
        df_filtered = df[df["country"] == selected_country]

    n = st.sidebar.slider(
        "Top N Countries",
        min_value=5,
        max_value=20,
        value=10
    )

    top_country_df = (
        df_filtered["country"]
        .value_counts()
        .head(n)
        .reset_index()
    )
    top_country_df.columns = ["country", "bookings"]

    st.plotly_chart(
        px.bar(
            top_country_df,
            x="bookings",
            y="country",
            orientation="h",
            text_auto=True,
            title=f"Top {n} Countries by Bookings"
        ),
        use_container_width=True
    )

    st.subheader("Filtered Data Preview")
    st.dataframe(df_filtered, use_container_width=True)
