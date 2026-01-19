import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly as plt

MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
PINK_COLOR = "#F2B6C6"

FIG_SIZE = (8, 5)

def _save_bar_plot(df, x_col, y_col, title, x_label, y_label, save_path):
def _save_heatmap(matrix_df, title, save_path):
def _plot_revenue_by_segment(csv_dir, fig_dir):
def _plot_rfm_score_distribution(csv_dir, fig_dir):
def _plot_cohort_retention_heatmap(csv_dir, fig_dir):




def generate_visualizations(csv_dir, fig_dir):
    _plot_revenue_by_segment(csv_dir, fig_dir)
    _plot_rfm_score_distribution(csv_dir, fig_dir)
    _plot_cohort_retention_heatmap(csv_dir, fig_dir)
