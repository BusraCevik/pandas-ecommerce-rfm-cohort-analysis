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

    # -----------------------------
    # Recency score (lower recency = better customer)
    #
    # R_score scale:
    #   5 → Most recent customers (purchased very recently)
    #   4 → Recent customers
    #   3 → Average recency
    #   2 → Inactive customers
    #   1 → Least recent customers (long time since last purchase)
    #
    # I reverse the labels because smaller recency values represent better customers.
    # -----------------------------

    rfm_df["R_score"] = pd.qcut(
        rfm_df["recency"],
        q=5,
        labels=[5, 4, 3, 2, 1],
    )

    print(rfm_df[["recency", "R_score"]].head(10))




