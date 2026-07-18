# AI Legal Assistant CLI Application

## 1. Project Description

The AI Legal Assistant CLI Application is a Python Command Line Interface (CLI) application that interacts with the CourtListener REST API to search legal cases, list courts, and search court opinions. The application also reads API configuration from a JSON file and validates legal keywords before searching.

The project demonstrates fundamental Python programming concepts, JSON configuration handling, REST API integration, error handling, and clean code organization using functions.

## 2. Features

- Read API configuration from a JSON file
- Search legal cases by legal category
- Search legal cases using custom legal keywords
- Display court information
- Search court opinions
- Validate legal keywords before searching
- Consume CourtListener Public REST API
- Handle connection and timeout errors
- Follow clean coding practices using modular functions

## 3. Project Structure
AILegalAssistant/
│
├── README.md
├── legal_info.py
├── config.json
├── requirements.txt
├── reports/
├── data/
├── models/
├── notebooks/
├── resources/
├── scripts/
├── tests/
└── venv/

## 4. Technologies Used

- Python 3.13
- JSON
- REST API
- CourtListener API
- Requests Library

## 5. Installation and Setup

### Create Virtual Environment

A virtual environment was created to isolate project dependencies.
python -m venv venv

### Activate Virtual Environment

venv\Scripts\activate

### Install Dependencies
pip install -r requirements.txt


## 6. Configuration File

The API configuration is stored in `config.json`.

Example:

```json
{
  "courtlistener_api": {
    "base_url": "https://www.courtlistener.com/api/rest/v4",
    "endpoints": {
      "search_cases": "/search/",
      "courts": "/courts/"
    }
  }
}
## 7. Application Functions

The application is organized into separate functions.

### `validate_keyword()`

- Validates whether the entered keyword is a supported legal keyword.

### `search_cases_with_keyword()`

- Searches legal cases using the CourtListener Search API.

### `legal_category_search()`

- Displays legal categories and predefined legal keywords.

### `list_courts()`

- Retrieves and displays court information from the CourtListener API.

### `search_opinions()`

- Searches court opinions using valid legal keywords.

### `main()`

- Controls the complete application workflow.

## 8. REST API Integration

This project uses the CourtListener Public REST API.

Base URL
https://www.courtlistener.com/api/rest/v4
```

Endpoints

Search Cases

```
/search/
```

List Courts

```
/courts/
```

The application retrieves public legal information including:

- Case Name
- Court Name
- Filing Date
- Opinion URL
- Court Information

No authentication token is required because only public CourtListener endpoints are used.

## 9. Running the Application

Run the application using:
python legal_info.py

## 11. Testing

The application was tested using multiple legal keywords.

Example keywords:

- copyright
- patent
- trademark
- criminal
- fraud
- contract
- employment
- labor
- tax
- immigration

The application successfully retrieves legal cases, courts, and opinions from the CourtListener API.

## 12. Error Handling

The application handles:

- Invalid legal keywords
- Invalid menu selections
- API connection errors
- Request timeout errors
- Empty search results
- Failed API requests

## 13. Author

**Betelhem Worku**