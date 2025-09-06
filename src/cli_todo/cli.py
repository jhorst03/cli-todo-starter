import argparse, sys
from .core import add_task, list_tasks, complete_task, clear_completed

def main(argv=None):
    parser = argparse.ArgumentParser(prog="todo", description="Minimal CLI To-Do app")
    sub = parser.add_subparsers(dest="cmd", required=True)

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
        tasks = list_tasks()
        if not tasks:
            print("(no active tasks)")
            return 0
        for t in tasks:
            print(f"{t.id}. {t.description}")
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
