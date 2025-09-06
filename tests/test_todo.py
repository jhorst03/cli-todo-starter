import os, tempfile, unittest
from cli_todo import core

class TodoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["CLI_TODO_DB_DIR"] = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("CLI_TODO_DB_DIR", None)

    def test_add_and_list(self):
        t = core.add_task("Buy milk")
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Buy milk")

    def test_done_and_clear(self):
        t = core.add_task("Task A")
        ok = core.complete_task(t.id)
        self.assertTrue(ok)
        removed = core.clear_completed()
        self.assertEqual(removed, 1)

if __name__ == "__main__":
    unittest.main()
