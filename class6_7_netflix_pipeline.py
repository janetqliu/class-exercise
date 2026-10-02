import argparse
import logging
import sys
from pathlib import Path
import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    path = Path(args.input)

    try:
        df = pd.read_csv(path)
        logger.info(f"File loaded successfully: {path}")
        logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
        original = df.copy()

    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    show_overview(df)
    logger.info("Displayed DataFrame overview.")
    

    before = len(df)
    df = remove_duplicates(df)
    logger.info(f"Duplicate rows removed: {before - len(df)}")

    before2 = len(df)
    df = drop_missing_rows(df)
    logger.info(f"Missing value rows removed: {before2 - len(df)}")

    try:
        before = len(df)
        df = remove_iqr_outliers(df,"runtime_minutes",1.5)
        logger.info(f"Removed {before - len(df)} outliers from column")
    except ValueError as e:
        logger.info(f"Invalid column entered")
        sys.exit(1)
        
    df['title'] = df['title'].apply(clean_text)
    logger.info("Cleaned title column")
    df['type'] = df['type'].apply(clean_text)
    logger.info("Cleaned type column")
    df['country'] = df['country'].apply(clean_text)
    logger.info("Cleaned country column")

    report = {
        'rows_before': len(original),
        'rows_after': len(df),
        'rows_removed': len(original) - len(df),
        'columns': df.columns
    }
    logger.info(f"Rows before: {report['rows_before']} | Rows after: {report['rows_after']} | Rows removed: {report['rows_removed']} \nColumns: {report['columns']}")


if __name__ == "__main__":
    main()
