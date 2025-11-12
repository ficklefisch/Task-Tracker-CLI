import datetime, os, json
from colorama import Fore, Back, Style

class Task:
    string_end = ['end', 'exit', 'stop']
    line_len = os.get_terminal_size().columns
    task_len = (line_len // 10) + 10
    info_len = line_len - task_len - 60
    
    def __init__(self):
        self.tasks = []
        self.autosave = True
        self.autosave_hint = True
        
        f = open('tasks.json', 'r')
        try:
            self.tasks = json.load(f)
        except:
            pass
        f.close()
    
    def do_task(self, task, title = None, status = None):
        c = ''
        if title != None:
            task['title'] = title
        if status != None:
            if status.lower() not in ['schedule', 'inactive', 'active', 'done']:
                raise ValueError(f"Invalid status. (received {status})")
            else:
                task['status'] = status.lower()
        
        print("Would you like to add any additional information? (y or n): ")
        if input()[0].lower() == 'y':
            print(f"Type 'cancel' to cancel editing, or {self.string_end} to end input.")
            temp = ''
            c = input()
            while c.lower() not in self.string_end and c.lower() != 'cancel':
                temp += c + '\n'
                c = input()
            if c.lower() != 'cancel':
                task['info'] = temp[: -1 if '\n' in temp else None]
        elif 'info' not in task:
            task['info'] = ''
        task['modified'] = datetime.datetime.now().replace(microsecond = 0)
        return task, c
    
    def new(self, title, status):
        if title != None and status != None:
            task = {}
            task, _ = self.do_task(task, title, status)
            task['created'] = task['modified']
            self.tasks.append(task)
            print(f"\nCreated new task. (ID: {len(self.tasks)})")
            self.display(0)
            self.do_autosave()
        else:
            raise ValueError(f"Missing data: received task as {'None' if task == None else task} and status as {'None' if status == None else status}")
        
    def edit(self, id, title = None, status = None):
        c = ''
        task = self.tasks[id - 1]
        task, c = self.do_task(task, title, status)
        if (c == 'cancel' or c == '') and title == None and status == None:
            print(f"Cancelled editing task. (ID: {id})")
        else:
            print(f"Successfully edited task. (ID: {id})")
            self.tasks[id - 1] = task
            self.do_autosave()
            
    def do_autosave(self):
        if self.autosave:
            print("Autosaving...")
            if self.autosave_hint:
                print("(disable autosaving in Options.)")
                self.autosave_hint = not self.autosave_hint
            self.save()
    
    def save(self):
        f = open('tasks.json', 'w')
        json.dump(self.tasks, f, default = str)
        f.close()
    
    def get_color(self, task):
        color = ''
        if task['status'] == 'schedule':
            color = Fore.CYAN
        elif task['status'] == 'inactive':
            color = Fore.RED
        elif task['status'] == 'active':
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        return color
    
    def display_all(self):
        print(Back.WHITE + Fore.BLACK + f'{"ID ":<5}{"Task":<{self.task_len}}{"":<3}: {"Info":<{self.info_len}}{"Created":<25}{"Modified":<25}' + Style.RESET_ALL)
        for i in range(len(self.tasks)):
            self.display_short(i + 1)
    
    def display_short(self, id: int):
        task = self.tasks[id - 1]
        def shorten(txt, space):
            txt = txt[ : txt.find('\n') if '\n' in txt else None]
            return txt[ : space - 3] + ('...' if len(txt) > space else '')
        color = self.get_color(task)
        title = shorten(task['title'], self.task_len)
        info = shorten(task['info'], self.info_len)
        print(f"{str(id) + '.':<5}{color}{title:<{self.task_len}}{Style.RESET_ALL}{'':<3}: {info:<{self.info_len}}{str(task['created']):<25}{str(task['modified']):<25}")
        #for some reason adding Style.RESET_ALL into the task_len whateveryoucallit causes the console text to misalign with the header in display_all
        #NIGGER
        
    def display(self, id: int):
        task = self.tasks[id - 1]
        print("=" * self.line_len)
        print(f"{task['title']}")
        print(f"Status: {self.get_color(task)}{task['status']}{Style.RESET_ALL}")
        print(f"Last modified: {str(task['modified'])}")
        print(f"Date created: {str(task['created'])}")
        print("-" * self.line_len)
        print(f"{task['info']}")
        print("=" * self.line_len)
    
    def delete(self, id):
        if len(self.tasks) > 0:
            del self.tasks[id - 1]
            self.do_autosave()
        else:
            print("There are no tasks to delete.")