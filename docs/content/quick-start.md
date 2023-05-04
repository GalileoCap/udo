---
weight: 1
title: "Quick Start"
---

# Quick Start

## Install
Download binary from the [releases](https://github.com/GalileoCap/udo-src/releases/latest).  

## Create a basic task
In `udo.py`
```py
UDOConfig = {
  'version': '1.3.0',
}

FPATH = '/tmp/test.touch'

def TaskTouch():
  return {
    'description': 'Creates the file',

    'outs': [FPATH], # This task creates these files

    'actions': [
      f'echo "Ahoy there!" > {FPATH}',
    ],
  }
```

## Execute it
```bash
udo
```
### Try to execute it again...
And see that it won't happen because the results were cached

### Remove the outputs
```bash
udo clean
```

## Use the output in other tasks
```py
def TaskMessage():
  return {
    'description': 'Prints the file',

    'deps': [FPATH], # This task depends on these files
    'capture': 1, # Show stdout

    'actions': [
        f'cat {FPATH}',
    ],
  }
```
```bash
udo # Will execute them in order: Touch -> Message
```
