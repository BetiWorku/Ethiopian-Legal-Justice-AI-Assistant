# Developer Portfolio CLI Application

## 1. Project Description

The Developer Portfolio CLI Application is a Python Command Line Interface (CLI) application that displays developer profile information from a JSON configuration file and integrates with the GitHub Public REST API to retrieve and display GitHub user information.

The project demonstrates fundamental Python programming concepts, JSON file handling, REST API integration, error handling, and clean code organization using functions.

## 2. Features

- Read developer information from a JSON configuration file
- Display formatted developer portfolio information
- Consume GitHub Public REST API
- Display GitHub user information
- Convert API responses into JSON format
- Handle invalid GitHub usernames gracefully
- Handle API connection errors
- Follow clean coding practices using modular functions

## 3. Project Structure
AILegalAssistant/
│
├── README.md
├── app.py
├── requirements.txt
│
├── reports/              
├── data/
├── models/           
├── notebooks/
├── resourses
├── scripts/
├── tests
└── venv/                     # Python virtual environment
│.env
├── portfolio.py              # Main Python CLI application
├── profile.json              # Developer profile configuration file
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
                   
## 4. Technologies Used

- Python 3.13
- JSON
- REST API
- GitHub API
- Requests Library

## 5. Installation and Setup

### Create Virtual Environment

A virtual environment was created to isolate project dependencies.

python -m venv venv

### Activate Virtual Environment
venv\Scripts\activate

### Install Dependencies
pip install -r requirements.txt

The Python environment was successfully configured and all required dependencies were installed.

## 6. Configuration File

Developer information is stored in profile.json.

## 7. Application Functions

The application is organized into separate functions:

### read_profile()
- Reads developer information from the JSON file.

### display_profile()
- Displays formatted developer profile information.

### get_github_data()
- Sends a request to GitHub REST API and retrieves user data.

### display_github()
- Displays GitHub API response information.

### main()
- Controls the complete application workflow.

## 8. REST API Integration

This project uses the GitHub Public REST API.

API Endpoint:
https://api.github.com/users/{username}

The API provides public GitHub information:

- Username
- Public repositories
- Followers

No authentication token is required because only public GitHub data is accessed.

## 9. Running the Application

Run the application using:
python portfolio.py

## 10. Testing

The application was tested using different GitHub usernames.

Example:

Change profile.json:

"github_username": "octocat"
 Run:

python portfolio.py

The application successfully retrieves and displays information for different GitHub accounts.

## 11. Error Handling

The application handles:

- Missing profile JSON file
- Invalid JSON format
- Invalid GitHub username
- API connection problems
- Failed API requests

The program displays appropriate error messages instead of crashing.

## 12. Dependencies

The required Python package is listed in:
requirements.txt
Example:
requests

## 13. Author
<<<<<<< HEAD
    Betelhem Worku  
=======
    Betelhem Worku   based on this course listner stegn readme
>>>>>>> 05669aa (Reorganize project structure)
