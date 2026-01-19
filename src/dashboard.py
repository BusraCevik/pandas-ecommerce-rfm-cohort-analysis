import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


# -----------------------------
# Color Theme
# -----------------------------
MAIN_COLOR = "#5FA8A8"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
BORDER_COLOR = "#000000"

HEATMAP_COLORSCALE = [
    [0.0, "#E6F2F2"],
    [0.3, "#9ED6D6"],
    [0.6, "#5FA8A8"],
    [1.0, "#3E7C7C"],
]


def build_rfm_dashboard(csv_dir: str, output_html_path: str):

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # -----------------------------
    # Load CSVs
    # -----------------------------
    segment_df = pd.read_csv(os.path.join(csv_dir, "segment_analysis.csv"))
    rfm_df = pd.read_csv(os.path.join(csv_dir, "rfm_analysis.csv"))
    retention_df = pd.read_csv(
        os.path.join(csv_dir, "retention_matrix.csv"),
        index_col=0
    )
    monthly_metrics_df = pd.read_csv(
        os.path.join(csv_dir, "monthly_metrics.csv")
    )

    # -----------------------------
    # Prepare datasets
    # -----------------------------
    rfm_score_dist = (
        rfm_df["RFM_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    rfm_score_dist.columns = ["rfm_score", "customer_count"]

    # -----------------------------
    # Build Figure
    # -----------------------------
    fig = go.Figure()

    # 0 — Revenue by Segment
    fig.add_trace(go.Bar(
        x=segment_df["segment"],
        y=segment_df["total_revenue"],
        name="Revenue by Segment",
        marker_color=MAIN_COLOR,
        visible=True
    ))

    # 1 — RFM Score Distribution
    fig.add_trace(go.Bar(
        x=rfm_score_dist["rfm_score"].astype(str),
        y=rfm_score_dist["customer_count"],
        name="RFM Score Distribution",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    # 2 — Monthly Revenue Trend
    fig.add_trace(go.Scatter(
        x=monthly_metrics_df["invoice_month"],
        y=monthly_metrics_df["total_revenue"],
        mode="lines+markers",
        name="Monthly Revenue Trend",
        line=dict(color=MAIN_COLOR, width=3),
        visible=False
    ))

    # 3 — Monthly Order Trend
    fig.add_trace(go.Scatter(
        x=monthly_metrics_df["invoice_month"],
        y=monthly_metrics_df["total_orders"],
        mode="lines+markers",
        name="Monthly Order Trend",
        line=dict(color=MAIN_COLOR, width=3),
        visible=False
    ))

    # 4 — Cohort Retention Heatmap (separate axis)
    fig.add_trace(go.Heatmap(
        z=retention_df.values,
        x=retention_df.columns.astype(str),
        y=retention_df.index.astype(str),
        colorscale=HEATMAP_COLORSCALE,
        colorbar=dict(title="Retention Rate"),
        name="Cohort Retention",
        visible=False,
        xaxis="x2",
        yaxis="y2"
    ))

    # -----------------------------
    # Base Layout
    # -----------------------------
    fig.update_layout(
        title=dict(text="Revenue by Customer Segment", x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_COLOR),
        margin=dict(t=80),
        yaxis=dict(
            title="Value",
            gridcolor=GRID_COLOR,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True,
            showticklabels=True
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True
        ),
        bargap=0.6,
    )

    # -----------------------------
    # Heatmap Dedicated Axes
    # -----------------------------
    fig.update_layout(
        xaxis2=dict(
            title="Cohort Index",
            type="category",
            overlaying="x",
            side="bottom",
            visible=False
        ),
        yaxis2=dict(
            title="Cohort Month",
            type="category",
            autorange="reversed",
            overlaying="y",
            side="left",
            visible=False,
            showticklabels=True
        )
    )

    plot_html = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs="cdn",
        div_id="rfmDashboard"
    )

    # -----------------------------
    # Write HTML
    # -----------------------------
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(f"""
<html>
<head>
<title>E-Commerce RFM & Cohort Dashboard</title>
</head>

<body style="background:#FAFEFE; font-family:Arial;">

<h1 style="color:{DARK_COLOR}; text-align:center;">
E-Commerce RFM & Cohort Analytics Dashboard
</h1>

<div style="text-align:center; margin-top:20px;">
<select id="metricSelect" style="
    padding:10px 16px;
    border-radius:10px;
    border:1px solid #BFDCDC;
    font-size:15px;
    color:{DARK_COLOR};
" onchange="updateChart()">
    <option value="0">Revenue by Segment</option>
    <option value="1">RFM Score Distribution</option>
    <option value="2">Monthly Revenue Trend</option>
    <option value="3">Monthly Order Trend</option>
    <option value="4">Cohort Retention Heatmap</option>
</select>
</div>

<div style="
    max-width: 1150px;
    margin: 25px auto;
    padding: 30px;
    border: 1px solid #E6F2F2;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    background-color: white;
">
{plot_html}
</div>

<script>
function updateChart() {{
    const val = document.getElementById("metricSelect").value;
    let visibility = [false, false, false, false, false];
    visibility[val] = true;

    let titles = [
        "Revenue by Customer Segment",
        "RFM Score Distribution",
        "Monthly Revenue Trend",
        "Monthly Order Trend",
        "Cohort Retention Heatmap"
    ];

    Plotly.restyle("rfmDashboard", "visible", visibility);
    Plotly.relayout("rfmDashboard", {{
        title: {{ text: titles[val], x: 0.5 }}
    }});

    if (val == 4) {{
        Plotly.relayout("rfmDashboard", {{
            "xaxis2.visible": true,
            "yaxis2.visible": true,
            "yaxis.showticklabels": false
        }});
    }} else {{
        Plotly.relayout("rfmDashboard", {{
            "xaxis2.visible": false,
            "yaxis2.visible": false,
            "yaxis.showticklabels": true
        }});
    }}
}}
</script>

</body>
</html>
""")

    print("Dashboard created at:", output_html_path)
