# Python babel utility functions
Utility functions for working with python babel. Currently it provides functionality for:
* Exporting existing translations to spreadsheet file
* Updating existing translations from spreadsheet file

## Installing
Install with pip:

`pip install git+https://git@github.com/Vlsarro/python-babel-utils.git`

## Examples

Exporting existing translations to spreadsheet file:
```python
from pybabel_utils.spreadsheets import PoFilesSpreadsheetExporter

PoFilesSpreadsheetExporter.run('some/path/input_folder', 'some/path/output_file')
```

Updating existing translations from spreadsheet file:
```python
from pybabel_utils.spreadsheets import PoFilesSpreadsheetUpdater


# assign this to None if you want to update translations inplace
output_folder = 'some/path/output_folder'

PoFilesSpreadsheetUpdater.run('some/path/input_spreadsheet.xlsx', 'some/path/input_folder', output_folder)
```
