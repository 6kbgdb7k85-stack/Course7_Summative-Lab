import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


def test_get_table_prints_rows(monkeypatch, capsys):
    rows = [{"id": 1, "name": "Alpha"}]
    monkeypatch.setattr(main, "fetch_table", lambda table: rows)

    main.get_table(SimpleNamespace(table="projects"))

    captured = capsys.readouterr().out
    assert "Alpha" in captured


def test_get_entry_prints_found_entry(monkeypatch, capsys):
    fake_entry = SimpleNamespace(id=1, name="Alpha")
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: fake_entry)
    monkeypatch.setattr(main, "parse_int", lambda value: 1)

    main.get_entry(SimpleNamespace(table="projects", key="id", value="1"))

    captured = capsys.readouterr().out
    assert "Alpha" in captured


def test_create_entry_for_project_saves_project(monkeypatch):
    saved = {}
    monkeypatch.setattr(main, "add_data", lambda table, entry: saved.setdefault("payload", {"table": table, "entry": entry}))

    args = SimpleNamespace(force=False, type="project", name="Demo Project", date="09/01/2026")
    main.create_entry(args)

    assert saved["payload"]["table"] == "projects"
    assert saved["payload"]["entry"]["name"] == "Demo Project"
    assert saved["payload"]["entry"]["_due_date"] == "09/01/2026"


def test_assign_task_calls_project_assign_task(monkeypatch):
    calls = []

    fake_task = SimpleNamespace(id=7, title="Fix bug")
    fake_user = SimpleNamespace(id=9, name="Alice")

    class FakeProject:
        TABLE = "projects"

        def __init__(self):
            self.id = 3
            self.name = "Demo"

        def assign_task(self, task, user):
            calls.append((task.title, user.name))

    fake_project = FakeProject()
    monkeypatch.setattr(main, "get_keys", lambda args: {"task_key": "title", "user_key": "_name", "project_key": "name"})
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: {
        main.Task.TABLE: fake_task,
        main.User.TABLE: fake_user,
        main.Project.TABLE: fake_project,
    }.get(table))

    args = SimpleNamespace(task="Fix bug", user="Alice", project="Demo")
    main.assign_task(args)

    assert calls == [("Fix bug", "Alice")]


def test_complete_project_marks_entry_complete(monkeypatch):
    fake_project = SimpleNamespace(id=3, name="Demo", completed=False)

    def complete_project():
        fake_project.completed = True

    fake_project.complete_project = complete_project
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: fake_project)

    args = SimpleNamespace(p=True, t=False, id=False, entry="Demo")
    main.complete(args)

    assert fake_project.completed is True


def test_delete_entry_uses_id_lookup_when_flag_is_set(monkeypatch):
    calls = {}

    class FakeUser:
        TABLE = "users"

        def __init__(self):
            self.id = 12
            self.name = "Alice"

        def delete(self):
            calls["deleted"] = True

    fake_user = FakeUser()
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: fake_user)

    args = SimpleNamespace(type="user", entry="12", id=True)
    main.delete_entry(args)

    assert calls["deleted"] is True


def test_get_user_tasks_calls_users_assigned_tasks(monkeypatch):
    calls = []

    class FakeUser:
        TABLE = "users"

        def __init__(self):
            self.id = 9
            self._name = "Alice"

        def get_assigned_tasks(self):
            calls.append(self._name)

    fake_user = FakeUser()
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: fake_user)

    args = SimpleNamespace(user="Alice", id=False)
    main.get_user_tasks(args)

    assert calls == ["Alice"]

def test_get_user_tasks_calls_users_assigned_projects(monkeypatch):
    calls = []

    class FakeUser:
        TABLE = "users"

        def __init__(self):
            self.id = 9
            self._name = "Alice"

        def get_assigned_projects(self):
            calls.append(self._name)

    fake_user = FakeUser()
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: fake_user)

    args = SimpleNamespace(user="Alice", id=False)
    main.get_user_projects(args)

    assert calls == ["Alice"]


def test_unassign_task_calls_user_remove_task(monkeypatch):
    calls = []

    fake_task = SimpleNamespace(id=7, title="Fix bug")
    fake_user = SimpleNamespace(id=9, name="Alice")

    class FakeUser:
        TABLE = "users"

        def __init__(self):
            self.id = 9
            self._name = "Alice"

        def remove_task(self, task):
            calls.append((task.title, self._name))

    fake_user = FakeUser()
    monkeypatch.setattr(main, "get_keys", lambda args: {"task_key": "title", "user_key": "_name"})
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: {
        main.Task.TABLE: fake_task,
        main.User.TABLE: fake_user,
    }.get(table))

    args = SimpleNamespace(task="Fix bug", user="Alice")
    main.unassign_task(args)

    assert calls == [("Fix bug", "Alice")]


def test_unassign_project_calls_project_remove_user(monkeypatch):
    calls = []

    fake_project = SimpleNamespace(id=3, name="Demo")
    fake_user = SimpleNamespace(id=9, name="Alice")

    class FakeProject:
        TABLE = "projects"

        def __init__(self):
            self.id = 3
            self.name = "Demo"

        def remove_user(self, user):
            calls.append((user.name, self.name))

    fake_project = FakeProject()
    monkeypatch.setattr(main, "get_keys", lambda args: {"project_key": "name", "user_key": "_name"})
    monkeypatch.setattr(main, "fetch_data", lambda table, lookup_key, lookup_value: {
        main.Project.TABLE: fake_project,
        main.User.TABLE: fake_user,
    }.get(table))

    args = SimpleNamespace(user="Alice", project="Demo")
    main.unassign_project(args)

    assert calls == [("Alice", "Demo")]


def test_main_dispatches_to_selected_command(monkeypatch):
    calls = []
    monkeypatch.setattr(sys, "argv", ["main.py", "entry", "projects", "1", "id"])
    monkeypatch.setattr(main, "get_entry", lambda args: calls.append((args.table, args.value, args.key)))

    main.main()

    assert calls == [("projects", "1", "id")]
