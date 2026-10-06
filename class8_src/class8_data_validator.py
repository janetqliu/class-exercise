import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error(f"{len(missing)} Column(s) missing")
        
        for col in missing:
            logger.error(f"Missing column: {col}")

        raise ValueError(f"Df must have all required columns")
    else:
        logger.info("All required columns present")
        
    return df
