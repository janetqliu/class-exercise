import logging
import pandas as pd
import re


logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug(f"Shape: {df.shape}")
    print(f"Shape: {df.shape}")
    print(f"Preview: {df.head(5)}")
    print(f"Columns: {df.columns}")
    print(f"Data types: {df.dtypes}")

    
def remove_duplicates(df):
    """Remove exact duplicate rows."""
    logger.debug(f"Rows before: {len(df)}")
    df = df.drop_duplicates()
    logger.debug(f"Rows after dropping duplicates: {len(df)}")
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    logger.debug(f"Rows before: {len(df)}")
    df = df.dropna()
    logger.debug(f"Rows after dropping missing values: {len(df)}")
    return df

def clean_text(value):
    """Normalize one text value."""
    value = value.strip()
    value = value.lower()
    value = re.sub(r"\s+", " ",value)
    return value

def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    if column not in df.columns:
        logger.error(f"Column does not exist: {column}")
        raise ValueError(f"Column must be one of following: {df.columns}")
    else:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr

        before = len(df)
        df = df[(df[column] <= upper) & (df[column] >= lower)]
        after = len(df)

        logger.debug(f"Bounds: ({lower}, {upper}) | Rows removed: {before - after}")
    return df