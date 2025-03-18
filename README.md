# Footy Analytics Dashboard

A Streamlit dashboard for football analytics using Statsbomb's open data.

## Features
- Interactive filters for competitions, seasons, teams, players, and match events
- Dynamic visualizations based on filter selections
- Data validation and error handling
- Cached API responses for better performance
- Export functionality for visualizations
- Comprehensive logging for debugging

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/esanchezmex/StatsBomb_Viz_Streamlit.git
cd StatsBomb_Viz_Streamlit
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run src/app.py
```

## Development

### Running Tests
```bash
pytest tests/
```

### Project Structure
```
.
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── data/                  # Data handling modules
│   │   ├── loader.py         # Data loading functions
│   │   └── processor.py      # Data processing functions
│   ├── utils/                # Utility functions
│   │   ├── cache.py         # Caching utilities
│   │   ├── validation.py    # Data validation
│   │   └── visualization.py # Visualization functions
│   └── config.py             # Configuration settings
├── tests/                    # Test files
├── .gitignore
├── requirements.txt
└── README.md
```

## License
This project is licensed under the MIT License - see the LICENSE file for details. 
