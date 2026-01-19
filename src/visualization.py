import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap



# -----------------------------
# Theme
# -----------------------------
THEME = {
    "primary": "#5FA8A8",
    "light": "#9ED6D6",
    "dark": "#3E7C7C",
    "grid": "#E6F2F2",
    "accent": "#F2B6C6",

}
HEATMAP_CMAP = LinearSegmentedColormap.from_list(
    "theme_heatmap",
    [
        "#E6F2F2",   # light background tone
        "#9ED6D6",   # light turquoise
        "#5FA8A8",   # primary
        "#3E7C7C"
    ]
)


FIG_SIZE = (8, 5)


# -----------------------------
# Shared Plot Helpers
# -----------------------------
def _save_bar_plot(df, x_col, y_col, title, x_label, y_label, save_path):

    plt.figure(figsize=FIG_SIZE)

    # Use numeric positions for bars
    bars = plt.bar(
        range(len(df)),
        df[y_col],
        color=THEME["primary"],
        edgecolor=THEME["dark"],
        width=0.5
    )

    # Manually set x tick labels
    x_values = df[x_col].astype(str)

    plt.xticks(
        ticks=range(len(x_values)),
        labels=x_values,
        rotation=0
    )

    plt.title(title, color=THEME["dark"])
    plt.xlabel(x_label, color=THEME["dark"])
    plt.ylabel(y_label, color=THEME["dark"])

    plt.grid(axis="y", color=THEME["grid"])

    plt.xticks(color=THEME["dark"])
    plt.yticks(color=THEME["dark"])

    for bar in bars:
        height = bar.get_height()
        x_center = bar.get_x() + bar.get_width() / 2

        plt.text(
            x_center,
            height,
            f"{height:,.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()



def _save_line_plot(df, x_col, y_col, title, x_label, y_label, save_path):

    plt.figure(figsize=FIG_SIZE)

    plt.plot(
        df[x_col],
        df[y_col],
        marker="o",
        linewidth=2,
        color=THEME["primary"]
    )

    plt.title(title, color=THEME["dark"])
    plt.xlabel(x_label, color=THEME["dark"])
    plt.ylabel(y_label, color=THEME["dark"])

    plt.grid(color=THEME["grid"])

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def _save_heatmap(matrix_df, title, save_path):

    plt.figure(figsize=(10, 6))

    plt.imshow(
        matrix_df,
        aspect="auto",
        cmap=HEATMAP_CMAP
    )

    plt.title(title, color=THEME["dark"])
    plt.xlabel("Cohort Index", color=THEME["dark"])
    plt.ylabel("Cohort Month", color=THEME["dark"])

    plt.colorbar()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


# -----------------------------
# Individual Plot Functions
# -----------------------------
def _plot_revenue_by_segment(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "segment_analysis.csv"))

    _save_bar_plot(
        df=df,
        x_col="segment",
        y_col="total_revenue",
        title="Revenue Contribution by Customer Segment",
        x_label="Customer Segment",
        y_label="Total Revenue",
        save_path=os.path.join(fig_dir, "revenue_by_segment.png")
    )


def _plot_rfm_score_distribution(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "rfm_analysis.csv"))

    counts = (
        df["RFM_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    counts.columns = ["rfm_score", "customer_count"]

    _save_bar_plot(
        df=counts,
        x_col="rfm_score",
        y_col="customer_count",
        title="RFM Score Distribution",
        x_label="RFM Score",
        y_label="Number of Customers",
        save_path=os.path.join(fig_dir, "rfm_score_distribution.png")
    )


def _plot_cohort_retention_heatmap(csv_dir, fig_dir):

    retention_matrix_df = pd.read_csv(
        os.path.join(csv_dir, "retention_matrix.csv"),
        index_col=0
    )

    _save_heatmap(
        matrix_df=retention_matrix_df,
        title="Customer Retention Cohort Heatmap",
        save_path=os.path.join(fig_dir, "cohort_retention_heatmap.png")
    )


def _plot_monthly_revenue_trend(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "monthly_metrics.csv"))

    _save_line_plot(
        df=df,
        x_col="invoice_month",
        y_col="total_revenue",
        title="Monthly Revenue Trend",
        x_label="Month",
        y_label="Total Revenue",
        save_path=os.path.join(fig_dir, "monthly_revenue_trend.png")
    )


def _plot_monthly_order_trend(csv_dir, fig_dir):

    df = pd.read_csv(os.path.join(csv_dir, "monthly_metrics.csv"))

    _save_line_plot(
        df=df,
        x_col="invoice_month",
        y_col="total_orders",
        title="Monthly Order Volume Trend",
        x_label="Month",
        y_label="Total Orders",
        save_path=os.path.join(fig_dir, "monthly_order_trend.png")
    )


# -----------------------------
# Public Runner
# -----------------------------
def generate_visualizations(csv_dir, fig_dir):

    os.makedirs(fig_dir, exist_ok=True)

    _plot_revenue_by_segment(csv_dir, fig_dir)
    _plot_rfm_score_distribution(csv_dir, fig_dir)
    _plot_cohort_retention_heatmap(csv_dir, fig_dir)
    _plot_monthly_revenue_trend(csv_dir, fig_dir)
    _plot_monthly_order_trend(csv_dir, fig_dir)

    print("Visualization files created in:", fig_dir)
