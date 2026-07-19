import json
import requests


def read_profile():
    try:
        with open("profile.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print("Profile file not found")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format")
        return None



def display_profile(profile):

    print("\n--- Developer Portfolio ---")
    print("Name:", profile["name"])
    print("Role:", profile["role"])
    print("Country:", profile["country"])

    print("Skills:")
    for skill in profile["skills"]:
        print("-", skill)



def get_github_data(username):

    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()

        else:
            print("Invalid GitHub username")
            return None

    except requests.exceptions.RequestException:
        print("API connection error")
        return None



def display_github(data):

    print("\n--- GitHub Information ---")
    print("Username:", data["login"])
    print("Repositories:", data["public_repos"])
    print("Followers:", data["followers"])



def main():

    profile = read_profile()

    if profile:

        display_profile(profile)

        github = get_github_data(
            profile["github_username"]
        )

        if github:
            display_github(github)



if __name__ == "__main__":
    main()