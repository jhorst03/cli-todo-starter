import argparse, sys
from .core import add_task, list_tasks, complete_task, clear_completed

def main(argv=None):
    parser = argparse.ArgumentParser(prog="todo", description="Minimal CLI To-Do app")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Show active and completed")
    p_list.add_argument("--completed", action="store_true", help="Show only completed")
    p_list.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")

    p_add = sub.add_parser("add")
    p_add.add_argument("description")

    sub.add_parser("list")
    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)
    sub.add_parser("clear")

    args = parser.parse_args(argv)

    if args.cmd == "add":
        t = add_task(args.description)
        print(f"[added] {t.id}: {t.description}")
        return 0
    if args.cmd == "list":
        include_completed = args.all
        only_completed = args.completed

        # mutually exclusive guard (optional, but nice)
        if include_completed and only_completed:
            print("Error: use either --all or --completed, not both.", file=sys.stderr)
            return 1

        tasks = list_tasks(include_completed=include_completed, only_completed=only_completed)

        if args.format == "json":
            import json
            # Convert dataclasses to dicts safely if needed
            # tasks may be dataclass objects in your version; handle both cases
            try:
                from dataclasses import asdict
                payload = [asdict(t) for t in tasks]
            except Exception:
                payload = [t.__dict__ if hasattr(t, "__dict__") else t for t in tasks]
            print(json.dumps(payload, indent=2))
            return 0

        # text output (default)
        if not tasks:
            print("(no tasks)")
            return 0

        for t in tasks:
            status = "✓" if t.completed else " "
            print(f"{t.id}. [{status}] {t.description}")
        return 0

    if args.cmd == "done":
        ok = complete_task(args.id)
        if ok:
            print(f"[done] {args.id}")
        else:
            print(f"Error: No task with id {args.id} found.", file=sys.stderr)
        return 1
    if args.cmd == "clear":
        removed = clear_completed()
        print(f"[cleared] {removed} completed task(s)")
        return 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
