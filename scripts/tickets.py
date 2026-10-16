import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preview local GitHub issue drafts; never publishes."
    )
    parser.add_argument("ticket", nargs="?")
    args = parser.parse_args()
    tickets = json.loads((ROOT / "tickets" / "index.json").read_text())
    if not args.ticket:
        for ticket in tickets:
            print(f"{ticket['id']:12} {ticket['title']} [{ticket['track']}]")
        return
    ticket = next((item for item in tickets if item["id"] == args.ticket), None)
    if ticket is None:
        parser.error(f"Unknown ticket: {args.ticket}")
    print(
        json.dumps(
            {
                "title": f"[{ticket['id']}] {ticket['title']}",
                "body": (ROOT / "tickets" / ticket["file"]).read_text(),
                "labels": ticket["labels"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
