# Currency Converter CLI

A simple command-line tool for converting between currencies using live exchange rates from [exchangerate-api.com](https://www.exchangerate-api.com/).

---

## Requirements

- Python 3.10 or newer
- A free API key from [exchangerate-api.com](https://www.exchangerate-api.com/)

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create a virtual environment

A virtual environment keeps the project's dependencies isolated from the rest of your system.

**Windows:**
```bash
py -m venv venv
source venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You will see `(venv)` at the start of your terminal prompt when the environment is active.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### First run — provide your API key

On the first run you need to supply your API key with `--key`. It will be saved to a `.env` file so you do not have to type it again.

```bash
py currency_converter.py --key YOUR_API_KEY USD EUR 100
```

### Subsequent runs — key is read from .env automatically

```bash
py currency_converter.py USD EUR 100
```

**Output:**
```
  100.0 USD = 92.34 EUR
  Exchange rate: 1 USD = 0.9234 EUR
```

### Save a new API key without converting

```bash
py currency_converter.py --key YOUR_NEW_API_KEY
```

---

## Examples

| Command | Description |
|---|---|
| `py currency_converter.py USD EUR 50` | Convert 50 US dollars to euros |
| `py currency_converter.py GBP DKK 200` | Convert 200 British pounds to Danish kroner |
| `py currency_converter.py --key ABC123 JPY USD 1000` | Save key and convert 1000 yen to dollars |

---

## Deactivating the virtual environment

When you are done, deactivate the virtual environment with:

```bash
deactivate
```

---

## Notes

- The `.env` file contains your API key and is **not committed to Git** (listed in `.gitignore`).  
  Never share this file publicly.
- The free tier of exchangerate-api.com allows 1 500 requests per month.
