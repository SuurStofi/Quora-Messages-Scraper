import json
import sys
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as Soup


def fetch_answers(my_url):
    req = requests.get(my_url)

    page_soup = Soup(req.content, "html.parser")
    ld_json_scripts = page_soup.findAll("script", {"type": "application/ld+json"})

    if not ld_json_scripts:
        print("No LD JSON scripts found on the page.")
        return

    main_box = ld_json_scripts[0].text

    data = json.loads(main_box)
    answers = []
    try:
        answers += [x["text"] for x in data["mainEntity"]["acceptedAnswer"]]
    except:
        pass
    answers += [x["text"] for x in data["mainEntity"]["suggestedAnswer"]]
    for i in range(len(answers)):
        print(f"\n\n\n\n Answers #{i + 1}\n\n")
        print(answers[i])

    if "-txt" in sys.argv:
        save_answers_to_folder(answers, "txt")

    if "-json" in sys.argv:
        save_answers_to_folder(answers, "json")


def save_answers_to_folder(answers, file_format):
    folder_name = "answers"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    current_time = datetime.now().strftime('%H%M_%Y%m%d')
    file_name = f"{current_time}.{file_format}"
    file_path = os.path.join(folder_name, file_name)

    try:
        with open(file_path, "a+", newline="", encoding="UTF-8") as f:
            if file_format == "txt":
                for answer in answers:
                    f.write(answer)
                    f.write("\n\n\n\n\n\n")
            elif file_format == "json":
                answers_json = {i + 1: answers[i] for i in range(len(answers))}
                json.dump(answers_json, f)
    except IOError:
        print("IO Error")


def get_user_input():
    while True:
        user_input = input("Please enter the URL: ")
        if user_input.strip(): 
            return user_input.strip()


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            url = get_user_input()
        else:
            url = sys.argv[1]
        fetch_answers(url)
    except requests.exceptions.MissingSchema:
        print("Invalid URL provided")
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
