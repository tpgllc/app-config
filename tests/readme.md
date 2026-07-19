# TESTING

## NOTES

### from cmd line

Testing of the config module and `configparms_ext` now uses `pytest` with
temporary module fixtures. The tests no longer copy `config.py` or
`configparms_ext.py` into `tests/src`.

1. cd to the tests directory
2. `uv run pytest -o addopts=''`

All tests should pass

### in vs code

The tests work in VS Code when run with the project `src` directory on
`PYTHONPATH`.

```
{
    "name": "Python: Current File",
    "type": "debugpy",
    "request": "launch",
    "program": "${file}",
    "env": {"PYTHONPATH": "${workspaceFolder}/src"},
    "console": "integratedTerminal",
    "justMyCode": true
    },
```
