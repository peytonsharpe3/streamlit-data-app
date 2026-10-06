import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on October 6th, 2026")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas...
# (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())

# Using as_index=False here preserves the Category as a column.
st.bar_chart(
    df.groupby("Category", as_index=False).sum(),
    x="Category",
    y="Sales",
    color="#04f"
)

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set it as an index
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)

# Group sales by month
sales_by_month = (
    df.filter(items=["Sales"])
    .groupby(pd.Grouper(freq="M"))
    .sum()
)

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")


st.write("## Your additions")


# (1) Drop-down for Category
category_options = sorted(df["Category"].dropna().unique())

selected_category = st.selectbox(
    "Select a Category",
    options=category_options
)


# (2) Multi-select for Sub_Category within the selected Category
sub_category_options = sorted(
    df.loc[
        df["Category"] == selected_category,
        "Sub_Category"
    ]
    .dropna()
    .unique()
)

selected_sub_categories = st.multiselect(
    "Select Sub-Categories",
    options=sub_category_options,
    default=sub_category_options
)


# Filter the data using both selections
filtered_df = df[
    (df["Category"] == selected_category) &
    (df["Sub_Category"].isin(selected_sub_categories))
]


if selected_sub_categories:

    # (3) Line chart of sales for the selected Sub_Categories
    st.write("### Monthly Sales by Selected Sub-Category")

    selected_sales_by_month = (
        filtered_df
        .groupby(
            [
                pd.Grouper(freq="MS"),
                "Sub_Category"
            ]
        )["Sales"]
        .sum()
        .unstack(fill_value=0)
    )

    st.line_chart(selected_sales_by_month)


    # (4) Metrics for the selected items
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()

    selected_profit_margin = (
        total_profit / total_sales
    ) * 100


    # (5) Overall profit margin for the full dataset
    overall_profit_margin = (
        df["Profit"].sum() /
        df["Sales"].sum()
    ) * 100

    profit_margin_difference = (
        selected_profit_margin -
        overall_profit_margin
    )


    # Display the three metrics
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

    metric2.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

    metric3.metric(
        "Overall Profit Margin",
        f"{selected_profit_margin:.2f}%",
        delta=(
            f"{profit_margin_difference:+.2f} "
            "percentage points vs overall"
        )
    )

else:
    st.warning(
        "Select at least one Sub-Category to display the chart and metrics."
    )