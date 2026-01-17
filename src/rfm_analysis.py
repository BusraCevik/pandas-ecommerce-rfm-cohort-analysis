import pandas as pd
import os

def run_rfm_analysis(input_path, output_path):

    df = pd.read_csv(input_path)


    rfm_df = df[
        ["customer_id", "recency_days", "total_orders","total_revenue"]
    ].copy()

    rfm_df = rfm_df.rename(
        columns={
            "recency_days": "recency",
            "total_orders": "frequency",
            "total_revenue": "monetary",

        }
    )

    print("RFM base shape:", rfm_df.shape)
    print(rfm_df.head())




