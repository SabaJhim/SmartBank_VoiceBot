import json

def load_faq():
        with open('data/faq.json','r') as f:
                return json.load(f)

FAQ=load_faq()

def search_faq(user_input):
        for item in FAQ:
                if any(word.lower() in item["question"].lower() for word in user_input.split()):
                        return item["answer"]
        return None

def get_recommendation(info):
        if "student" in info.lower():
                return "A student savings account with low minimum balance is suitable."
        if "business" in info.lower():
                return "A business current account is suitable because it allows unlimited transactions."
        if "loan" in info.lower() and "salary" in info.lower():
                return "You may qualify for a personal loan if your salary is consistent and above the bank threshold."
        return "Can you provide a bit more detail about your income or purpose?"