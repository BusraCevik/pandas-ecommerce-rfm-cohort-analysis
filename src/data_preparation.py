import os
import pandas as pd


def prepare_data(input_path, output_path):
    """
    Loads raw transactional data, performs data cleaning and validation,
    and saves the cleaned dataset.
    """

    # -----------------------------
    # Load raw data
    # -----------------------------
    df = pd.read_csv(input_path)

    print("Initial shape:", df.shape)
    print("Missing values:")
    print(df.isnull().sum())

    # -----------------------------
    # Standardize column names
    # -----------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # -----------------------------
    # Fix data types
    # -----------------------------
    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

    # -----------------------------
    # Remove invalid rows
    # -----------------------------

    # Remove canceled invoices (InvoiceNo starts with 'C')
    is_canceled = df["invoiceno"].astype(str).str.startswith("C")
    df = df[is_canceled == False]

    # Remove missing customer IDs
    df = df.dropna(subset=["customerid"])

    # Remove negative or zero quantities
    df = df[df["quantity"] > 0]

    # Remove zero or negative prices
    df = df[df["unitprice"] > 0]

    # Drop duplicated rows if any
    df = df.drop_duplicates()

    # -----------------------------
    # Feature creation
    # -----------------------------
    df["total_price"] = df["quantity"] * df["unitprice"]

    # -----------------------------
    # Basic validation
    # -----------------------------
    assert (df["total_price"] > 0).all(), "Found non-positive total_price values."
    assert df["customerid"].isnull().sum() == 0, "Missing customerid detected."

    print("Cleaned shape:", df.shape)

    # -----------------------------
    # Save cleaned data
    # -----------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Processed data saved to:", output_path)

    return df
