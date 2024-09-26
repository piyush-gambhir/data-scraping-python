# Data-Scraping-Python

This project is designed for scraping data from various websites. It uses Python, Selenium, and other web scraping libraries to automate the process of collecting and storing data from different sources.

## Project Structure

```plaintext
data-scraping-python/
│
├── helpers/
│   ├── csv/ 
│   │   ├── append.py            # Functionality to append data to CSV files
│   │   ├── read.py              # Functionality to read data from CSV files
│   │   └── write.py             # Functionality to write data to CSV files
│   ├── html/
│   │   ├── fetch_html.py        # Module to fetch raw HTML
│   │   └── parse_html.py        # Module to parse HTML content
│   ├── json/
│   │   ├── append.py            # Append new data to JSON files
│   │   ├── csv.py               # Functionality related to JSON and CSV conversion
│   │   ├── pandas_dataframe.py  # Manipulation using pandas dataframes
│   │   ├── print.py             # Utility for printing data
│   │   ├── read.py              # Read JSON data from files
│   │   └── write.py             # Write JSON data to files
│   ├── selenium/
│   │   └── webdriver.py         # Selenium WebDriver setup
│   ├── url/
│   │   ├── url.py               # URL construction utilities
│   │   └── __init__.py          # Package initializer for URL helpers
│   └── __init__.py              # Package initializer for helpers
│
├── scrapers/
│   ├── cars.com/                # Cars.com specific scraper
│   ├── amazon/                  # Amazon specific scraper (yet to implement)
│   ├── autotrader.com/          # Autotrader specific scraper (yet to implement)
│   ├── carfax/                  # Carfax specific scraper (yet to implement)
│   ├── cargurus/                # Cargurus specific scraper (yet to implement)
│   ├── carmax.com/              # Carmax specific scraper (yet to implement)
│   ├── google-maps/             # Google Maps scraper (yet to implement)
│   ├── youtube.com/             # Youtube specific scraper (yet to implement)
│   └── __init__.py              # Package initializer for scrapers
│
├── tests/                       # Test files (unit and integration tests)
│   ├── docker-compose.yml       # Docker Compose file for running in a containerized environment
│   └── Dockerfile               # Dockerfile for setting up a container environment
│
├── pyproject.toml               # Poetry configuration file
├── README.md                    # Project documentation (this file)
└── docker-compose.yml           # Docker Compose setup for deployment
```

## Prerequisites

Before running the project, ensure that the following are installed:

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Firefox (if you're using Selenium with the default Firefox driver)
- GeckoDriver for Selenium (Firefox WebDriver)

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd data-scraping-python
   ```

2. **Install dependencies using Poetry**:

   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:

   ```bash
   poetry shell
   ```

4. **Run any scraper**:

   For example, to run the `cars.com` scraper:

   ```bash
   poetry run python scrapers/cars.com/cars_com_listings.py
   ```

## Helper Modules

### `helpers/`
This folder contains utility functions that help with repetitive tasks such as CSV/JSON manipulation, HTML fetching and parsing, URL construction, and Selenium WebDriver setup.

- **csv**: Functions to read, write, and append data to CSV files.
- **html**: Contains functions to fetch and parse HTML content.
- **json**: Functions to read, write, and append JSON data. Additional utilities to work with pandas dataframes.
- **selenium**: Functions for setting up and managing Selenium WebDriver.
- **url**: URL construction utilities to dynamically create URLs based on parameters.

### Scraper Modules

Each folder inside `scrapers/` corresponds to a scraper for a particular website or data source. Currently, the main active scraper is for `cars.com`, but you can expand the project to include other scrapers (e.g., Amazon, Autotrader, Carfax).

- **cars.com**: The current implemented scraper collects vehicle listings from Cars.com.
- **Other scrapers**: These are placeholder folders for future implementations.

## How to Use

### Example: Cars.com Scraper

1. **Modify parameters** inside `cars_com_listings.py` to set search filters such as `zipcode`, `make`, `model`, and other parameters.
2. **Run the scraper** using Poetry:

   ```bash
   poetry run python scrapers/cars.com/cars_com_listings.py
   ```

3. **Data Output**:
   - JSON data is appended to `cars.com_listing_data.json`.
   - CSV data is appended to `cars.com_listing_data.csv`.

## Tests

Test cases can be placed inside the `tests/` folder. Currently, you can create unit tests to validate your helper functions and scrapers.

Run the tests using:

```bash
poetry run pytest tests/
```

## Docker Support

This project also includes Docker support for easy deployment. You can use the `Dockerfile` and `docker-compose.yml` files to containerize the application.

To build and run the Docker container:

```bash
docker-compose up --build
```

This will start the scraper in a containerized environment.

## Contributing

Feel free to submit issues or pull requests for additional scrapers or features. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
