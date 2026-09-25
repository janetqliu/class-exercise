import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def inspect_file(filepath_str):
    """Return basic information about an existing file."""

    file = Path(filepath_str)

    if not file.is_file():
        logger.error(f"Path is not valid.")
        raise FileNotFoundError("File not found.")

    else:
        return {"name": file, "extension": file.suffix}

def inspect_extension(file_info):
    """Confirm that the file uses a supported text extension."""
    supported_extension = ".txt"

    if file_info["extension"] != supported_extension:
        logger.error("Unsupported format.")
        raise ValueError(f"File extension not supported: {file_info["extension"]}")

    else:
        return file_info