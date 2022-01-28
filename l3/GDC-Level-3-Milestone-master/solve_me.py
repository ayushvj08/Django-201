from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):

        def check_dup_priority(key, val):

            if key not in self.current_items:
                self.current_items[key] = val

            else:
                check_dup_priority(key+1, self.current_items[key])
                self.current_items.pop(key)
                self.current_items[key] = val

        check_dup_priority(int(args[0]), args[1])

        self.write_current()
        print(f"Added task: \"{args[1]}\" with priority {args[0]}")

    def done(self, args):
        try:
            task = self.current_items.pop(int(args[0]))
            self.completed_items.append(task)
            self.write_current()
            self.write_completed()
            print("Marked item as done.")
        except KeyError:
            print(f"Error: no incomplete item with priority {args[0]} exists.")

    def delete(self, args):
        try:
            self.current_items.pop(int(args[0]))
            self.write_current()
            print(f"Deleted item with priority {args[0]}")
        except KeyError:
            print(
                f"Error: item with priority {args[0]} does not exist. Nothing deleted.")

    def ls(self):
        for index, item in enumerate(self.current_items.items()):
            print(f"{index+1}. {item[1]} [{item[0]}]")

    def report(self):
        print(f"Pending : {len(self.current_items)}")
        self.ls()
        print(f"\nCompleted : {len(self.completed_items)}")
        for index, task in enumerate(self.completed_items):
            print(f"{index+1}. {task.strip()}")

    def render_pending_tasks(self):
        pending = "<h1>Pending Tasks</h1>"
        for index, item in enumerate(self.current_items.items()):
            pending += f"<h3>{index+1}. {item[1]} [{item[0]}]</h3>"

        return ''.join(pending)

    def render_completed_tasks(self):
        self.read_completed()
        completed = "<h1>Completed Tasks</h1>"
        for index, item in enumerate(self.completed_items):
            completed += f"<h3>{index + 1}. {item}</h3>"
        return completed


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
