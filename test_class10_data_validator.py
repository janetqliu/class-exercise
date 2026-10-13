import pandas as pd
import pytest

from class10_data_validator import validate_columns


@pytest.fixture
def sample_df():
    """Create a small DataFrame for testing."""
    return pd.DataFrame(
        {
            "title": ["Movie A", "Movie B"],
            "type": ["Movie", "Movie"],
            "release_year": [2020, 2021],
        }
    )


def test_validate_columns_with_valid_columns(sample_df):
    required = ["title", "type", "release_year"]

    df = validate_columns(sample_df, required)

    assert df.columns.tolist() == required


def test_validate_columns_with_missing_column(sample_df):

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_columns(sample_df, required_columns=["title", "rating"])