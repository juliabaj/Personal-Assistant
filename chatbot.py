import json
from difflib import get_close_matches

#function for loading the json file
def load_json(file_path: str) -> dict:   #return contents of a json file as a dictionary | "str" is a "type hint"
    with open(file_path, 'r') as file:
        data: dict = json.load(file)     #"type hint" that data is supposed to be a dictionary (not important to the works of code, just for the programmer who read a code)
    return data

#function for saving the data even after closing it
def save_json(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)   #"indent=2" is for aesthetic purposes of the json file


def find_close_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)  #finding similar words in "questions" list to "user_questions" list, n is the amount of answers you want to receive and cutoff is a minimal similarity percentage = 60%, nothing below
    return matches[0] if matches else None #return first answer if there are any

def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:  #searching for all elements "q" that stores smaller dictionaries in a list under the key "questions" from a dict "knowledge_base"
        if q["question"].lower() == question.lower():
            return q["answer"]

# for example
# knowledge_base: dict = {
#     "questions": key,list: [
#         {"question": "What is Python?", "answer": "Python is a programming language."}: dict,
#         {"question": "How to install Python?", "answer": "You can install Python from python.org."}: dict
#     ]
# }

def chatbot():
    knowledge_base: dict = load_json('knowledge_base.json')

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            break

        closest_question: str | None = find_close_match(user_input, [q.get("question") for q in knowledge_base.get("questions", []) if "question" in q])

        if closest_question:
            answer: str = get_answer(closest_question, knowledge_base)
            print(f"Bot: {answer}")

        else:
            print('Bot: I don\'t know the answer to this question. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip:' )

        if new_answer.lower() != 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_json('knowledge_base.json', knowledge_base)

            print('Bot: Thank you! I learned a new response.')



if __name__ == '__main__':
    chatbot()
