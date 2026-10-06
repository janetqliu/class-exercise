import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Error: {col} missing from df")
            raise ValueError(f"Column must be in df")

    return df
