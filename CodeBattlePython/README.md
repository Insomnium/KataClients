## Prerequisites:

```pip install -e .```


## Usage:

Run client form command line:
```
kataclient
```

Client support comand line parametrs
```
Usage: kataclient [OPTIONS]

Options:
  --address TEXT  Server address.
  --name TEXT     Player name.
  --auth TEXT     Auth code.
  --description / --no-description
                                  View only task description and close
  --help          Show this message and exit.
```

You can view only task description with parameter '--description'.
In this case client show current task description and close.


## Add new solvers:

In file `kataclient.CodeBattlePythonSolvers.py` add
function with one argument and name 'level_<level>' where `<level>` is kata level.

Then run script again. Clien will find solver for requested level.
