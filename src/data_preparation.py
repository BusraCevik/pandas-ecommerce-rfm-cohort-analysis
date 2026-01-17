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

    RENAME_MAP = {
        "customerid": "customer_id",
        "invoiceno": "invoice_no",
        "unitprice": "unit_price",
        "stockcode": "stock_code",
        "invoicedate": "invoice_date",
    }

    df = df.rename(columns=RENAME_MAP)

    # -----------------------------
    # Fix data types
    # -----------------------------
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["invoice_date"] = df["invoice_date"].dt.normalize()
    df = df.dropna(subset=["invoice_date"])

    # -----------------------------
    # Remove invalid rows
    # -----------------------------

    # Remove canceled invoices (InvoiceNo starts with 'C')
    is_canceled = df["invoice_no"].astype(str).str.startswith("C")
    df = df[is_canceled == False]

    # Remove missing customer IDs
    df = df.dropna(subset=["customer_id"])

    # Remove negative or zero quantities
    df = df[df["quantity"] > 0]

    # Remove zero or negative prices
    df = df[df["unit_price"] > 0]

    # Drop duplicated rows if any
    df = df.drop_duplicates()

    # -----------------------------
    # Feature creation
    # -----------------------------
    df["total_price"] = df["quantity"] * df["unit_price"]

    # -----------------------------
    # Basic validation
    # -----------------------------
    assert (df["total_price"] > 0).all(), "Found non-positive total_price values."
    assert df["customer_id"].isnull().sum() == 0, "Missing customer_id detected."

    print("Cleaned shape:", df.shape)

    # -----------------------------
    # Save cleaned data
    # -----------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Processed data saved to:", output_path)

    return df
