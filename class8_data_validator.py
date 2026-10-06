import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    missing = [col for col in require_columns if col not in df.columns]
    if missing:
        logger.error(f"{len(missing)} Columns missing")
        raise ValueError(f"Df must have all required columns")
        
    for col in missing:
        logger.error(f"Missing column: {col}")

    return df
