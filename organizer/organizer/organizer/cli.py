import json
import yaml
import typer
from rich import print
from .auth import get_token
from .scanner import Scanner
from .deduplicator import Deduplicator
from .renamer import Renamer

app = typer.Typer(help="OneDrive Organizer CLI")


@app.command()
def scan(
    config: str = "config.yaml",
    apply: bool = typer.Option(False, help="Apply changes (otherwise dry-run)"),
):
    """Scan OneDrive, detect duplicates, suggest renames, optionally apply."""
    with open(config) as f:
        cfg = yaml.safe_load(f)

    token = get_token()
    scanner = Scanner(token)
    files = list(scanner.scan())

    dedup = Deduplicator()
    duplicates = dedup.find_duplicates(files)

    renamer = Renamer(cfg)
    rename_suggestions = {f["id"]: renamer.suggest_name(f) for f in files}

    report = {
        "total_files": len(files),
        "duplicates": duplicates,
        "rename_suggestions": rename_suggestions,
    }

    with open("report.json", "w") as fh:
        json.dump(report, fh, indent=2)

    print("[green]Report written to report.json[/green]")
    if apply:
        print("[yellow]Apply mode not yet implemented – review report first.[/yellow]")


if __name__ == "__main__":
    app()
