
# Streamlit Multi-Page Project

This project uses Streamlit with a multi-page structure and API integration.

## Structure

- `src/app.py`: Main entry point for the Streamlit app
- `src/pages/`: Additional Streamlit pages (e.g., Home, Analytics)
- `src/api/`: API client logic
- `tests/`: Unit tests
- `requirements.txt`: Project dependencies

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the Streamlit app:
```bash
streamlit run src/app.py
```


## Running Tests
To run all tests:
```bash
python -m unittest discover -s tests
```

To run a specific test file:
```bash
python -m unittest tests/test_api.py
```

## Add dependencies
List them in `requirements.txt`.
