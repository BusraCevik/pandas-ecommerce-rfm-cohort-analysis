import os
import pandas as pd


def build_monthly_metrics(input_path: str, output_path: str):

    df = pd.read_csv(input_path)
    os.makedirs(output_path, exist_ok=True)

    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    # Normalize to calendar month
    df["invoice_month"] = (
        df["invoice_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_df = (
        df.groupby("invoice_month")
        .agg(
            total_revenue=("total_price", "sum"),
            total_orders=("invoice_no", "nunique"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values("invoice_month")
    )

    monthly_df.to_csv(
        os.path.join(output_path, "monthly_metrics.csv"),
        index=False
    )

    print("Monthly metrics saved to:", output_path)

    return monthly_df
