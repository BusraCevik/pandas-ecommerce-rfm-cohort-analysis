import pandas as pd
import os


def run_rfm_analysis(input_path, output_path):
    """
    Builds RFM scores and customer segments from customer-level feature dataset.
    Uses rank-based quantile scoring to avoid duplicated bin issues.
    """

    # -----------------------------
    # Load featured dataset
    # -----------------------------
    df = pd.read_csv(input_path)
    os.makedirs(output_path, exist_ok=True)

    # -----------------------------
    # Select RFM base columns
    # -----------------------------
    rfm_df = df[
        ["customer_id", "recency_days", "total_orders", "total_revenue"]
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
    # qcut sorts values from small → large.
    # I reverse labels because smaller recency means more recent (better).
    # -----------------------------
    rfm_df["R_score"] = pd.qcut(
        rfm_df["recency"],
        q=5,
        labels=[5, 4, 3, 2, 1],
    )

    # -----------------------------
    # Frequency score (higher frequency = better customer)
    #
    # I rank the values first to avoid duplicated quantile edges.
    # Rank spreads identical values into a continuous sequence,
    # making quantile binning stable on real-world skewed data (I tried
    # without using rank but it did not work out for this dataset).
    # -----------------------------
    rfm_df["frequency_rank"] = rfm_df["frequency"].rank(method="first")

    rfm_df["F_score"] = pd.qcut(
        rfm_df["frequency_rank"],
        q=5,
        labels=[1, 2, 3, 4, 5],
    )

    # -----------------------------
    # Monetary score (higher spending = better customer)
    #
    # Same rank-based strategy
    # -----------------------------
    rfm_df["monetary_rank"] = rfm_df["monetary"].rank(method="first")

    rfm_df["M_score"] = pd.qcut(
        rfm_df["monetary_rank"],
        q=5,
        labels=[1, 2, 3, 4, 5],
    )

    # -----------------------------
    # Combined RFM metrics
    # -----------------------------
    rfm_df["RFM_score"] = (
        rfm_df["R_score"].astype(int)
        + rfm_df["F_score"].astype(int)
        + rfm_df["M_score"].astype(int)
    )

    # String-based RFM code (e.g. "545")
    rfm_df["RFM_code"] = (
        rfm_df["R_score"].astype(str)
        + rfm_df["F_score"].astype(str)
        + rfm_df["M_score"].astype(str)
    )

    # -----------------------------
    # Segment initialization
    # -----------------------------
    rfm_df["segment"] = "Unclassified"

    # -----------------------------
    # Segment rules (ordered by priority)
    # -----------------------------
    champions_mask = (
        (rfm_df["R_score"] >= 4)
        & (rfm_df["F_score"] >= 3)
        & (rfm_df["M_score"] >= 3)
    )

    loyal_mask = (
        (rfm_df["F_score"] >= 4)
        & (rfm_df["M_score"] >= 3)
    )

    potential_mask = (
        (rfm_df["R_score"] >= 4)
        & (rfm_df["M_score"] >= 2)
    )

    at_risk_mask = (rfm_df["R_score"] == 2)
    lost_mask = (rfm_df["R_score"] == 1)

    # -----------------------------
    # Segment assignment
    # -----------------------------
    rfm_df.loc[champions_mask, "segment"] = "Champion"
    rfm_df.loc[loyal_mask, "segment"] = "Loyal"
    rfm_df.loc[potential_mask, "segment"] = "Potential"
    rfm_df.loc[at_risk_mask, "segment"] = "At Risk"
    rfm_df.loc[lost_mask, "segment"] = "Lost"

    print("Segment distribution:")
    print(rfm_df["segment"].value_counts())

    # -----------------------------
    # Save outputs
    # -----------------------------
    rfm_df.to_csv(
        os.path.join(output_path, "rfm_analysis.csv"),
        index=False
    )

    print("RFM analysis saved to:", output_path)

    segment_analysis_df = (
        rfm_df.groupby("segment")
        .agg(
            customer_count=("customer_id", "nunique"),
            total_revenue=("monetary", "sum"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        )
        .reset_index()
    )

    segment_analysis_df.to_csv(
        os.path.join(output_path, "segment_analysis.csv"),
        index=False
    )

    print("Segment analysis saved to:", output_path)
