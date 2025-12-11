import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_settings_env():
    """
    Ensure we are always in a test environment to avoid touching real production
    settings.
    """
    with patch.dict(os.environ, {"APP_ENV": "test", "DEBUG": "true"}):
        yield
