from litellm import completion
from sys import argv
import os
import re
from datetime import  date, datetime
import subprocess
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL_NAME = os.getenv('LLM_MODEL')
USER_NAME = os.getenv('USER_NAME')
AI_NAME = os.getenv('AI_NAME')
PRINTED_REPLY_HEAD = os.getenv('REPLY_HEAD')
LLM_PROMPT_FILENANME = os.getenv('PROMPT_FILENANME')
LLM_API_BASE = os.getenv('API_BASE')
LLM_API_KEY= os.getenv('API_KEY')
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE'))
LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS'))

os.environ["OPENAI_API_KEY"] = LLM_API_KEY
os.environ["OPENAI_API_BASE"] = LLM_API_BASE

KNOWLEDGE =  [
               f"Today's date: {date.today()}.",
               f"Time is {datetime.now().strftime('%H:%M')}.",
               f"User's name: {USER_NAME}.",
               f"AI assistant name: {AI_NAME}."
             ]
knowledge_str = "Knowledge: " + '\n'.join(KNOWLEDGE)


dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, LLM_PROMPT_FILENANME)
f = open(file_path, "r")

SYSTEM_PROMPT = f.read() + knowledge_str
f.close()

user_input = ""

if len(argv) > 1:
    for i in range(1,len(argv)):
        user_input = user_input + " " + argv[i]
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        exit(0)
else:
    user_input = input(f"{USER_NAME}: ")

messages =  [
                { "content": SYSTEM_PROMPT ,"role": "system"},
                { "content": user_input ,"role": "user"},
            ]

while True:
    response = completion(
        model=LLM_MODEL_NAME, 
        messages=messages, 
        stream=True,
        temperature=LLM_TEMPERATURE
    )
    print(f"{AI_NAME}: ", sep=" ", end='')
    for part in response:
        if re.search( "#EXIT" , response.response_uptil_now.strip().capitalize()):
            part = re.sub("#EXIT", "", part)
        print(part.choices[0].delta.content or "", sep=" ", end='')
    print()   
    llm_response= { "content": response.response_uptil_now ,"role": "system"}   
    messages.append(llm_response)        

    # If it's Command
    if re.search( "#\s*`.*?`" , response.response_uptil_now.strip().lower()):
        command = re.search( "#\s*`.*`"  , response.response_uptil_now.strip()).group()
        command = re.search( "`.*`"  , response.response_uptil_now.strip()).group()[1:-1]
        if re.search( "#\s*ASK_USER"  , response.response_uptil_now.strip()):
            print("Execute Command: " + command + "\n")
            do_proceed = input("Proceed with command?  y/n: ")
            # TODO fix if no character
            if do_proceed.strip().lower()[0] != 'y' :
                continue
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = process.communicate()
        if err != "":
            print("Execution Error:\n" + err + "\n")
        if out != "":
            print("Execution Results:\n" + out + "\n")
        exec_results = { "content": f"Execution result: {out}" ,"role": "system"}   
        messages.append(exec_results)


    if re.search( "#\s*exit" , response.response_uptil_now.strip().lower()):
        print()
        exit(0)

    user_input = input(PRINTED_REPLY_HEAD)
    message = { "content": user_input ,"role": "user"}
    messages.append(message)
    
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print()
        exit(0)