# route-calc
CU Boulder DTSC 5501 Group Project #3: Find the shortest route in a city

## Roles & Responsibilities
# TODO
Written and maintained by Group 1:
- **Wesley Allen**:
- **Chushmitha Battula**:
- **Stephanie Bie**:
- **Glen Vadakkoott**:

## Install

```bash
git clone git@github.com:stephaniebie/route-calc.git
```

Create and enter a virtual environment (Windows):

```bash
python -m venv venv
source venv/Scripts/activate
```

Once in the environment, install the package:

```bash
cd route-calc
pip install .
```

### For Developers

Install the package in editable mode:

```bash
pip install -e .[dev]
```

Install a kernel for use with Jupyter notebooks:

```bash
python -m ipykernel install --user --name=route_calc
```

Optionally, run `black .` prior to pushing to ensure uniform formatting.

## Testing

Use the following command to run the unit tests:

```bash
pytest tests
```
