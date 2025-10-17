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

    p_reopen = sub.add_parser("reopen", help="Reopen a completed task by id")
    p_reopen.add_argument("id", type=int)

    p_edit = sub.add_parser("edit", help="Edit a task's description by id")
    p_edit.add_argument("id", type=int, help="Task id")
    p_edit.add_argument("description", help="New task description")

    p_search = sub.add_parser("search", help="Search tasks by keyword")
    p_search.add_argument("keyword", help="Keyword to search for")

    p_stats = sub.add_parser("stats", help="Show totals and completion rate")
    p_stats.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

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
    
    if args.cmd == "reopen":
        from .core import reopen_task, list_tasks
        ok = reopen_task(args.id)
        if ok:
            print(f"[reopened] {args.id}")
            return 0
        else:
            # either not found or already active
            # check if it exists but is active to tailor the message (optional)
            tasks_all = list_tasks(include_completed=True)
            if any(t.id == args.id for t in tasks_all):
                print(f"Error: task {args.id} is already active.", file=sys.stderr)
            else:
                print(f"Error: no task with id {args.id} found.", file=sys.stderr)
            return 1
        
    if args.cmd == "edit":
        from .core import edit_task
        ok = edit_task(args.id, args.description)
        if ok:
            print(f"[edited] {args.id}: {args.description}")
            return 0
        else:
            print(f"Error: no task with id {args.id} found.", file=sys.stderr)
            return 1
        
    if args.cmd == "search":
        from .core import search_tasks
        results = search_tasks(args.keyword)
        if not results:
            print("No results found.")
            return 0
        for t in results:
            status = "✓" if t.completed else " "
            print(f"{t.id}. [{status}] {t.description}")
        return 0
    
    if args.cmd == "stats":
        from .core import compute_stats
        s = compute_stats()
        if args.format == "json":
            import json
            print(json.dumps(s, indent=2))
            return 0
        print(f"Total: {s['total']}")
        print(f"Active: {s['active']}")
        print(f"Completed: {s['completed']}")
        print(f"Completion rate: {s['completion_rate']}")
        return 0

        
    if args.cmd == "clear":
        removed = clear_completed()
        print(f"[cleared] {removed} completed task(s)")
        return 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
