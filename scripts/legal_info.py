import requests
import json

with open("config.json","r") as file:
    config=json.load(file)

BASE_URL=config["courtlistener_api"]["base_url"]
SEARCH_URL=BASE_URL+config["courtlistener_api"]["endpoints"]["search_cases"]
COURTS_URL=BASE_URL+config["courtlistener_api"]["endpoints"]["courts"]

print("API:",SEARCH_URL)

LEGAL_KEYWORDS=[
    "copyright",
    "patent",
    "trademark",
    "criminal",
    "crime",
    "fraud",
    "contract",
    "agreement",
    "employment",
    "labor",
    "privacy",
    "tax",
    "immigration"
]


def validate_keyword(keyword):
    keyword=keyword.lower()

    for word in LEGAL_KEYWORDS:
        if word in keyword:
            return True

    return False


def search_cases_with_keyword(query):
    print("\n=== Search Legal Cases ===")
    print("Searching:",query)

    params={
        "q":query,
        "type":"o",
        "order_by":"dateFiled desc"
    }

    try:
        response=requests.get(
            SEARCH_URL,
            params=params,
            timeout=10
        )

        if response.status_code==200:
            data=response.json()
            results=data.get("results",[])

            if not results:
                print("No cases found.")
                return

            for i,case in enumerate(results[:5],start=1):
                print("\nCase",i)
                print("Name:",case.get("caseName"))
                print("Court:",case.get("court"))
                print("Date:",case.get("dateFiled"))
                print("URL:",case.get("absolute_url"))

        else:
            print("Error:",response.status_code)

    except requests.exceptions.ConnectionError:
        print("Internet connection error")

    except requests.exceptions.Timeout:
        print("Request timeout")


def legal_category_search():
    print("""
=== Legal Categories ===

1. Intellectual Property
2. Criminal Law
3. Contract Law
4. Employment Law
5. Search Custom Keyword
""")

    choice=input("Choose category: ")

    categories={
        "1":["copyright","patent","trademark"],
        "2":["criminal","crime","fraud"],
        "3":["contract","agreement"],
        "4":["employment","labor"]
    }

    if choice in categories:
        print("\nAvailable keywords:")

        for i,word in enumerate(categories[choice],start=1):
            print(f"{i}. {word}")

        keyword_choice=input("\nChoose keyword: ")

        try:
            keyword=categories[choice][int(keyword_choice)-1]

        except:
            print("Invalid keyword choice")
            return

    elif choice=="5":
        keyword=input("Enter legal keyword: ")

        if not validate_keyword(keyword):
            print("Please enter a valid legal keyword.")
            return

    else:
        print("Invalid category")
        return

    search_cases_with_keyword(keyword)


def list_courts():
    print("\n=== Courts List ===")

    try:
        response=requests.get(
            COURTS_URL,
            timeout=10
        )

        if response.status_code==200:
            data=response.json()
            courts=data.get("results",[])

            for i,court in enumerate(courts[:10],start=1):
                print("\nCourt",i)
                print("Name:",court.get("full_name"))
                print("Short Name:",court.get("short_name"))
                print("Jurisdiction:",court.get("jurisdiction"))

        else:
            print("Error:",response.status_code)

    except requests.exceptions.ConnectionError:
        print("Internet connection error")

    except requests.exceptions.Timeout:
        print("Request timeout")


def search_opinions():
    print("\n=== Search Court Opinions ===")

    keyword=input("Enter opinion keyword: ")

    if not validate_keyword(keyword):
        print("Please enter a valid legal keyword.")
        return

    params={
        "q":keyword,
        "type":"o",
        "order_by":"dateFiled desc"
    }

    try:
        response=requests.get(
            SEARCH_URL,
            params=params,
            timeout=10
        )

        if response.status_code==200:
            data=response.json()
            results=data.get("results",[])

            if not results:
                print("No opinions found.")
                return

            for i,opinion in enumerate(results[:5],start=1):
                print("\nOpinion",i)
                print("Case Name:",opinion.get("caseName"))
                print("Court:",opinion.get("court"))
                print("Date:",opinion.get("dateFiled"))
                print("URL:",opinion.get("absolute_url"))

        else:
            print("Error:",response.status_code)

    except requests.exceptions.ConnectionError:
        print("Internet connection error")

    except requests.exceptions.Timeout:
        print("Request timeout")


def main():
    while True:
        print("""
===== AI Legal Assistant =====

1. Search Legal Cases By Category
2. List Courts
3. Search Court Opinions
4. Exit
""")

        choice=input("Choice: ")

        if choice=="1":
            legal_category_search()

        elif choice=="2":
            list_courts()

        elif choice=="3":
            search_opinions()

        elif choice=="4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__=="__main__":
    main()