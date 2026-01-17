import os
from src.data_preparation import prepare_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
SRC_DIR = os.path.join(BASE_DIR, 'src')

RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', 'dataset.csv')
CLEAN_DATA_PATH = os.path.join(DATA_DIR, 'clean', 'cleaned.csv')
FEATURED_DATA_PATH = os.path.join(DATA_DIR, 'featured', 'featured.csv')

TABLES_PATH = os.path.join(OUTPUT_DIR, 'tables')
FIGURES_PATH = os.path.join(OUTPUT_DIR, 'figures')
DASHBOARD_HTML_PATH = os.path.join(DOCS_DIR, 'dashboard.html')


def main():
    prepare_data(RAW_DATA_PATH, CLEAN_DATA_PATH)


if __name__ == '__main__':
    main()