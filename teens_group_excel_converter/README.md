# Teens Group Excel Converter

A Python GUI for BSV staffs to convert CSV of registration based to children based (break up cell with multiple children record to independent row).

## Developer

> Uses python 3.12.9

Prerequisite:

- Have pyenv installed,

- Have `qt-base-dev` installed with `sudo apt install qt6-base-dev`.

```bash
# Install python version 3.12.9 and set as global
pyenv install 3.12.9 && pyenv global 3.12.9

# Create virtual environment named bsv
pyenv virtualenv bsv python=3.12.9

# Activate virtual environment
pyenv activate bsv
```

Install the dependencies.

```bash
cd ~/<PROJECT_ROOT_DIRECTORY>/teens_group_excel_converter

# App dependencies (pyqt6, pandas)
pip install -r requirements.txt

# Dev dependencies (pipreqs, pyinstaller)
pip install -r requirements.dev.txt
```

Run the program.

```bash
cd ~/<PROJECT_ROOT_DIRECTORY>/teens_group_excel_conveter/src
python app.py
```

Create standalone execution file.

```bash
cd ~/<PROJECT_ROOT_DIRECTORY>/teens_group_excel_conveter/src
pyinstaller -n <FILENAME> --noconsole --onefile app.py 
```
