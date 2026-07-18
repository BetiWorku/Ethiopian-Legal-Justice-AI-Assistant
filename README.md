# Developer Portfolio CLI Application - Task 3

## 1. Project Description

This project is a Python command-line application that reads developer profile information from a JSON file and fetches public GitHub profile data from the GitHub REST API. It demonstrates core Python concepts such as file handling, API integration, error handling, and modular function design.

## 2. Features

- Read developer information from a JSON configuration file
- Display formatted developer portfolio information
- Retrieve public GitHub user information
- Convert API responses into JSON-friendly data
- Handle invalid GitHub usernames and API errors gracefully
- Follow clean coding practices using separate functions

## 3. Project Structure

```text
AILegalAssistant/
├── README.md
├── app.py
├── portfolio.py
├── profile.json
├── requirements.txt
├── data/
├── models/
├── notebooks/
├── reports/
├── resourses/
├── scripts/
└── tests/
```

## 4. Technologies Used

- Python 3.13
- JSON
- Requests
- GitHub REST API

## 5. Installation and Setup

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configuration File

Developer information is stored in `profile.json`.

## 7. Application Functions

The application is organized into separate functions:

- `read_profile()` - reads developer information from the JSON file
- `display_profile()` - displays formatted developer profile information
- `get_github_data()` - sends a request to the GitHub API and retrieves user data
- `display_github()` - displays GitHub API response information
- `main()` - controls the complete application workflow

## 8. REST API Integration

This project uses the GitHub Public REST API.

API endpoint:

```text
https://api.github.com/users/{username}
```

The API provides public GitHub information such as:

- Username
- Public repositories
- Followers

## 9. Running the Application

Run the application using:

```bash
python portfolio.py
```

## 10. Testing

You can test the application by updating `profile.json` with a GitHub username such as `octocat` and then running the script again.

## 11. Error Handling

The application handles:

- Missing profile JSON files
- Invalid JSON format
- Invalid GitHub usernames
- API connection errors
- Failed API requests

## 12. Dependencies

The required package is listed in `requirements.txt`:

- requests

## 13. Author

Betelhem Worku
