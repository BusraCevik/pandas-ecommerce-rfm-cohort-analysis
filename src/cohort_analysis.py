import os
import pandas as pd


def run_cohort_analysis(input_path, output_path):

    # Load cleaned transactional dataset
    df = pd.read_csv(input_path)
    os.makedirs(output_path, exist_ok=True)

    # Ensure datetime consistency
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    print("Initial shape:", df.shape)

    # Map each transaction to its calendar month
    df["invoice_month"] = (
        df["invoice_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # First purchase month per customer (cohort anchor)
    df["cohort_month"] = (
        df.groupby("customer_id")["invoice_month"]
        .transform("min")
    )

    # Calculate month difference between invoice and cohort
    year_diff = df["invoice_month"].dt.year - df["cohort_month"].dt.year
    month_diff = df["invoice_month"].dt.month - df["cohort_month"].dt.month
    total_month_diff = (year_diff * 12) + month_diff

    # Cohort index starts from 1 (cohort month = 1)
    df["cohort_index"] = total_month_diff + 1

    # Count unique active customers per cohort and month index
    cohort_counts_df = (
        df.groupby(["cohort_month", "cohort_index"])
        .agg(
            active_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values("cohort_index")
    )

    # Save long-format cohort counts
    cohort_counts_df.to_csv(
        os.path.join(output_path, "cohort_counts.csv"),
        index=False
    )

    # Pivot into retention matrix (wide format)
    cohort_matrix_df = cohort_counts_df.pivot(
        index="cohort_month",
        columns="cohort_index",
        values="active_customers"
    )

    print("Cohort matrix preview:")
    print(cohort_matrix_df.head())

    # Save cohort matrix
    cohort_matrix_df.to_csv(
        os.path.join(output_path, "cohort_matrix.csv")
    )


    print("Sample cohort mapping:")
    print(
        df[["customer_id", "invoice_month", "cohort_month", "cohort_index"]]
        .head(10)
    )




    retention_matrix_df = cohort_matrix_df.divide(
        cohort_matrix_df.iloc[:, 0],
        axis=0
    )

    print("Retention matrix preview:")
    print(retention_matrix_df.head())

    retention_matrix_df.to_csv(
        os.path.join(output_path, "retention_matrix.csv")
    )
