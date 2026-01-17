import pandas as pd
import os

def build_customer_features(input_path, output_path):

    df = pd.read_csv(input_path)

    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    customer_df = (
        df.groupby("customer_id")
        .agg(
            first_purchase_date=("invoice_date", "min"),
            last_purchase_date=("invoice_date", "max"),
            total_orders=("invoice_no",  "nunique"),
            total_revenue=("total_price", "sum"),
            total_quantity=("quantity", "sum")
        )
        .reset_index()
    )

    reference_date = df["invoice_date"].max() + pd.Timedelta(days=1)

    customer_df["recency_days"] =(
        reference_date - customer_df["last_purchase_date"]
    ).dt.days

    customer_df["lifetime_days"] = (
        customer_df["last_purchase_date"] - customer_df["first_purchase_date"]
    ).dt.days

    customer_df["avg_order_value"] = (
        customer_df["total_revenue"]/customer_df["total_orders"]
    )

    customer_df["first_purchase_month"] = (
        customer_df["first_purchase_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    customer_df["last_purchase_month"] = (
        customer_df["last_purchase_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    lifetime_months = customer_df["lifetime_days"] / 30
    lifetime_months = lifetime_months.clip(lower=1)

    customer_df["orders_per_month"]=(
        customer_df["total_orders"]/lifetime_months
    )

    customer_df["avg_items_per_order"] = (
            customer_df["total_quantity"] / customer_df["total_orders"]
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    customer_df.to_csv(output_path, index=False)


    print("Featured dataset saved successfully.")

    return customer_df