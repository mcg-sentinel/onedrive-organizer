from typer.testing import CliRunner
from organizer.cli import app

def test_scan_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "OneDrive Organizer CLI" in result.output
