#Build LLM Brain
import os
from groq import Groq
from dotenv import load_dotenv
from logic import search_faq,get_recommendation 

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a junior banking assistant.
You can answer basic banking questions and ask follow-up questions.
If a user asks about loan or account types, ask for income, age, purpose, etc.
Do not give incorrect information. If unsure, ask for clarification.
""" 

def ask_llm(message):
        response=client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                        "role":"system","content":SYSTEM_PROMPT},
                        {"role":"user","content":message}
                ]
        )
        return response.choices[0].message.content

def bot_response(text):
        #try FAQ first
        faq_ans=search_faq(text)
        if faq_ans:
                return faq_ans
        
        #try recommnedation
        rec=get_recommendation(text)
        if rec:
                return rec 
        
        #fallback to llm
        return ask_llm(text)
