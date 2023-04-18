---
weight: 1
title: "uDO API"
---

# API

## Execution
<!-- TODO: Explain execution -->

## Task
```py
class Task:
    name : str # The name of the task, defaults to the constructor's name
    description : str # Will be shown on the 'udo help' message
    deps : list[str | Task] # List of files, directories, or other task
                            # constructors this task depends on 
    outs : list[str] # List of files or directories this task creates
    clean : bool = True # Should outs be removed on 'udo clean'
    capture = -1 | 0 | 1 # Capture stderr and stdout (-1), only stdout (0),
                         # or nothing (1)
    actions : list[str | callable] # List of bash commands or python functions
                                   # to be executed
    subtasks : list[dict | callable] # List of subtasks
```
Tasks (and subtasks) may be functions that return a dictionary with it's attributes, or the dictionary itself (see [examples](https://github.com/GalileoCap/udo-src/tree/main/examples)).
