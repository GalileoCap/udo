---
weight: 1
title: "uDO API"
---

# API

## Task
Tasks are either dictionaries or functions that return a dictionary, with the following attributes.  
They must follow the naming scheme of "TaskX" where "X" is the name of the task.
```py
class Task:
    name : str # The name of the task, defaults to the constructor's name
    description : str # Will be shown on the default 'udo help' message
    deps : list[str | Task] # List of files, directories, or other task
                            # constructors this task depends on 
    outs : list[str] # List of files or directories this task creates
    clean : bool | callable = True # Should outs be removed on 'udo clean'
    skipRun : bool | callable = False # Should the task be skipped
    capture = -1 | 0 | 1 # Capture stderr and stdout (-1), only stdout (0),
                         # or nothing (1)
    actions : list[str | callable] # List of bash commands or python functions
                                   # to be executed
    subtasks : list[Task] # List of subtasks
```

Example:
```py
def TaskExample():
    return {
        'description': 'This is the main task',
        'deps': [], # It doesn't depend on anything
        'outs': ['build', 'build/test'],

        'actions': [
            'mkdir -p build',
            'echo "Ahoy there!" > build/test',
        ],
    }
```

### deps
A list of files that have to exist or other tasks that should be executed before this task can be executed.  
Example:
```py
    'deps': ['build', TaskExample],
```

### outs
A list of files that will be created by this task.  
This is checked, so it will cause an error if any of these doesn't exist after it's execution.

### clean
If True, all files in outs will be deleted on `udo clean`.  
If False, `udo clean` will skip this task.
If it's a function, then `udo clean` will execute it instead of deleting outs.

### skipRun
If True, this task won't be executed.  
If False, this task will be executed normally (see [Execution](#execution)).  
If it's a function, then instead of checking the cache this function will determine if the task is run by returning True or False.  

## Execution
When you execute **uDO**, the program loads all the described tasks and then executes them in such an order that all dependencies are met.  
It also caches the files described in each task's deps and outs, so that tasks will be skipped if both:
* The dependencies haven't changed
* The outputs still exists

<!-- TODO: Graph -->
<!-- TODO: TaskGraph design -->

## Config
Some of the arguments can be also saved in the `udo.py` file under a dictionary:
```py
UDOConfig = {
  'version': (1, 3, 0), # Used to check compatibility
  'cache': './.udo.db',
  'prefix': 'Task',
}
```
**WARNING:** Don't use this variable or it's name for anything else.

