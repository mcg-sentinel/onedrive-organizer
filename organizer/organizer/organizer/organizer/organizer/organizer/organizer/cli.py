#!/usr/bin/env python3
import argparse
import json
import yaml
from auth import get_token
from scanner import Scanner
from deduplicator import Deduplicator
from renamer import Renamer


def main():
    parser = argparse.ArgumentParser(description="OneDrive Organizer CLI")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--apply", action="store_true", help="Apply changes (otherwise dry-run)")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    token = get_token()
    scanner = Scanner(token)
    files = list(scanner.scan())

    dedup = Deduplicator()
    duplicates = dedup.find_duplicates(files)

    renamer = Renamer(config)
    rename_suggestions = {f["id"]: renamer.suggest_name(f) for f in files}

    report = {
        "total_files": len(files),
        "duplicates": duplicates,
        "rename_suggestions": rename_suggestions,
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Report written to report.json")
    if args.apply:
        print("Apply mode not yet implemented – review report first.")


if __name__ == "__main__":
    main()
