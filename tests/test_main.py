from takeoff.core.config import settings
from takeoff.main import main


def test_config_loader():
    """Test that settings are loaded correctly."""
    # Since we mocked env in conftest, these should match
    assert settings.APP_ENV == "test" or settings.APP_ENV == "development"
    # depends on when config was imported
    assert settings.APP_NAME == "Takeoff"

def test_main_execution(capsys):
    """Test the main entry point runs without error."""
    exit_code = main()
    assert exit_code == 0

    captured = capsys.readouterr()
    # In test env, we expect structlog to print to stdout
    assert "Starting up application" in captured.out
    assert "app_name=Takeoff" in captured.out
