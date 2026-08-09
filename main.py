import argparse

from termcolor import cprint

from utils.utils import fetch_data, fetch_table, parse_int, add_data, get_keys
from models.user import User
from models.task import Task
from models.project import Project

TYPES = ["user","project","task"]

#get full table
def get_table(args):
    table = fetch_table(table=args.table)
    if not table:
        return
    for row in table:
        cprint(row,"green")

#get entry from table
def get_entry(args):
    entry = fetch_data(table=args.table, lookup_key=args.key, lookup_value=parse_int(args.value))
    if not entry:
        cprint(f"Entry '{args.value}' not found in table '{args.table}'","red")
        return
    cprint(entry.__dict__,"green")

#add entry to table
def create_entry(args):
    if args.force:
        entry = {"name":args.name}
    else:
        match args.type:
            case "user":
                entry = User(args.name).__dict__
            case "task":
                entry = Task(args.name).__dict__
            case "project":
                if not args.date:
                    cprint("date is required for project","red")
                    return
                entry = Project(args.name,args.date).__dict__
            case _:
                cprint("type must be one of [user,task,project]","red")
                return
    if entry:
        add_data(args.type+"s",entry)

#add task to user
def assign_task(args):
    keys = get_keys(args)
    task = fetch_data(table=Task.TABLE,lookup_key=keys["task_key"], lookup_value=parse_int(args.task))
    user = fetch_data(table=User.TABLE,lookup_key=keys["user_key"],lookup_value=parse_int(args.user))
    project = fetch_data(table=Project.TABLE,lookup_key=keys["project_key"],lookup_value=parse_int(args.project))
    if task and user and project:
        project.assign_task(task,user)

#remove task from user
def unassign_task(args):
    keys = get_keys(args)
    task = fetch_data(table=Task.TABLE,lookup_key=keys["task_key"], lookup_value=parse_int(args.task))
    user = fetch_data(table=User.TABLE,lookup_key=keys["user_key"],lookup_value=parse_int(args.user))
    if task and user:
        user.remove_task(task)

#add project to user
def assign_project(args):
    keys = get_keys(args)
    project = fetch_data(table=Project.TABLE,lookup_key=keys["project_key"],lookup_value=parse_int(args.project))
    user = fetch_data(table=User.TABLE,lookup_key=keys["user_key"],lookup_value=parse_int(args.user))
    project.add_user(user)

#remove project from user
def unassign_project(args):
    keys = get_keys(args)
    project = fetch_data(table=Project.TABLE,lookup_key=keys["project_key"],lookup_value=parse_int(args.project))
    user = fetch_data(table=User.TABLE,lookup_key=keys["user_key"],lookup_value=parse_int(args.user))
    project.remove_user(user)

#add task to project
def add_task(args):
    keys = get_keys(args)
    task = fetch_data(table=Task.TABLE,lookup_key=keys["task_key"],lookup_value=parse_int(args.task))
    project = fetch_data(table=Project.TABLE,lookup_key=keys["project_key"],lookup_value=parse_int(args.project))
    if project and task:
        project.add_task(task)

#remove task from project
def remove_task(args):
    keys = get_keys(args)
    task = fetch_data(table=Task.TABLE,lookup_key=keys["task_key"],lookup_value=parse_int(args.task))
    project = fetch_data(table=Project.TABLE,lookup_key=keys["project_key"],lookup_value=parse_int(args.project))
    if project and task:
        project.remove_task_task(task)

#remove entry from table
def delete_entry(args):
    #check if table is valid. add cases if new tables are added
    match args.type:
        case "user":
            table = User.TABLE
            key = "_name"
        case "task":
            table = Task.TABLE
            key = "title"
        case "project":
            table = Project.TABLE
            key = "name"
        case _:
            cprint("type must be one of [user,task,project]","red")
            return
    if args.id:
        key = "id"
    entry = fetch_data(table=table,lookup_key=key,lookup_value=parse_int(args.entry))
    entry.delete()

#set project or task to complete
def complete(args):
    if not args.p and not args.t:
        cprint("Must use either '-p' or '-t'","red")
        return
    if args.p:
        table = Project.TABLE
        key = "name"
    else:
        table = Task.TABLE
        key = "title"
    if args.id:
        key = "id"
    entry = fetch_data(table=table, lookup_key=key, lookup_value=parse_int(args.entry))
    if entry:
        if args.p:
            entry.complete_project()
        else:
            entry.complete_task()
#get tasks assigned to user
def get_user_tasks(args):
    if args.id:
        key = "id"
    else:
        key = "_name"
    user = fetch_data(table=User.TABLE, lookup_key=key, lookup_value=parse_int(args.user))
    user.get_assigned_tasks()

#get projects assigned to user
def get_user_projects(args):
    if args.id:
        key = "id"
    else:
        key = "_name"
    user = fetch_data(table=User.TABLE,lookup_key=key, lookup_value=parse_int(args.user))
    user.get_assigned_projects()

def main():
    parser = argparse.ArgumentParser(description = "Project Manager CLI")
    subparser = parser.add_subparsers()

    #table
    get_table_parser = subparser.add_parser("table", help="Get Table")
    get_table_parser.add_argument("table",help="Name of table")
    get_table_parser.set_defaults(func=get_table)

    #entry
    get_entry_parser = subparser.add_parser("entry", help="Get Entry from Table")
    get_entry_parser.add_argument("table",help="Name of table")
    get_entry_parser.add_argument("value",help="Value to search for")
    get_entry_parser.add_argument("key",help="Column to search in. Defaults to 'id'", default="id", nargs="?")
    get_entry_parser.set_defaults(func=get_entry)

    #add-entry
    create_entry_parser = subparser.add_parser("add-entry", help="Add Entry to Table")
    create_entry_parser.add_argument("type", help="Type of Entry. Must be one of [user,task,project]")
    create_entry_parser.add_argument("name", help="Name of the Entry")
    create_entry_parser.add_argument("date", help="Due date for Project. Only needed if type is 'project'", nargs="?")
    #-force option is just meant to showcase that add_data creates a new table if one doesn't exist
    create_entry_parser.add_argument("-force",help="Override type restriction. Entry will only be accessible through 'entry' command", action="store_true")
    create_entry_parser.set_defaults(func=create_entry)

    #assign_task
    assign_task_parser = subparser.add_parser("assign-task",help="Assign Task to User")
    assign_task_parser.add_argument("task",help="Task Name or ID")
    assign_task_parser.add_argument("user",help="User Name or ID")
    assign_task_parser.add_argument("project",help="Project name or ID")
    assign_task_parser.add_argument("-tid",help="Use if arg 'task' is ID", action="store_true")
    assign_task_parser.add_argument("-uid",help="Use if arg 'user' is ID", action="store_true")
    assign_task_parser.add_argument("-pid",help="Use if arg 'project' is ID", action="store_true")
    assign_task_parser.set_defaults(func=assign_task)

    #add_task
    add_task_parser = subparser.add_parser("add-task",help="Add Task to Project")
    add_task_parser.add_argument("task",help="Task Name of ID")
    add_task_parser.add_argument("project",help="Project name or ID")
    add_task_parser.add_argument("-tid",help="Use if arg 'task' is ID", action="store_true")
    add_task_parser.add_argument("-pid",help="Use if arg 'project' is ID", action="store_true")
    add_task_parser.set_defaults(func=add_task)

    #assign_project
    assign_project_parser = subparser.add_parser("assign-project",help="Assign User to Project")
    assign_project_parser.add_argument("user",help="User Name or ID")
    assign_project_parser.add_argument("project",help="Project name or ID")
    assign_project_parser.add_argument("-uid",help="Use if arg 'user' is ID", action="store_true")
    assign_project_parser.add_argument("-pid",help="Use if arg 'project' is ID", action="store_true")
    assign_project_parser.set_defaults(func=assign_project)

    #delete_entry
    delete_entry_parser = subparser.add_parser("delete-entry",help="Delete entry by Name or ID")
    delete_entry_parser.add_argument("type",help="Type of Entry. Must be one of [user,task,project]")
    delete_entry_parser.add_argument("entry",help="Entry Name or ID")
    delete_entry_parser.add_argument("-id",help="Use if arg 'entry' is ID", action="store_true")
    delete_entry_parser.set_defaults(func=delete_entry)

    #complete
    complete_parser = subparser.add_parser("complete",help="Complete Project or Task")
    complete_parser.add_argument("entry",help="Name or ID of the Project/Task")
    complete_parser.add_argument("-p",help="Use for Project", action="store_true")
    complete_parser.add_argument("-t",help="Use for Task", action="store_true")
    complete_parser.add_argument("-id",help="Use if 'entry' is ID",action="store_true")
    complete_parser.set_defaults(func=complete)

    #get_user_tasks
    get_user_tasks_parser = subparser.add_parser("user-tasks",help="Get Task details for User")
    get_user_tasks_parser.add_argument("user",help="User Name or ID")
    get_user_tasks_parser.add_argument("-id",help="Use if arg 'user' is ID", action="store_true")
    get_user_tasks_parser.set_defaults(func=get_user_tasks)

    #get_user_projects
    get_user_projects_parser = subparser.add_parser("user-projects",help="Get Project details for User")
    get_user_projects_parser.add_argument("user",help="User Name or ID")
    get_user_projects_parser.add_argument("-id",help="Use if arg 'user' is ID", action="store_true")
    get_user_projects_parser.set_defaults(func=get_user_projects)

    args = parser.parse_args()

    if hasattr(args,"func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
