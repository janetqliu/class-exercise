import logging

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