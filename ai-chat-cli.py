from litellm import completion
from sys import argv
import os
import re
from datetime import  date, datetime
import subprocess
from dotenv import load_dotenv
import json

load_dotenv()

LLM_MODEL_NAME = os.getenv('LLM_MODEL')
USER_NAME = os.getenv('USER_NAME')
AI_NAME = os.getenv('AI_NAME')
PRINTED_REPLY_HEAD = os.getenv('REPLY_HEAD')
CONFIG_FILENANME = os.getenv('CONFIG_FILENANME')
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
file_path = os.path.join(dir_path, CONFIG_FILENANME)
f = open(file_path, "r")
config_raw_data = f.read()
f.close()

class Prompt():
    def __init__(self, name, prompt, info,  description=None, shortcuts=None ):
        self.name = name
        self.prompt = prompt
        self.info = info
        self.description = description
        self.shortcuts = shortcuts if shortcuts else []
        

class Config:
    def __init__(self, prompts_data, save):
        # self.prompts = [Prompt(**prompt) for prompt in prompts_data]
        self.prompts = {prompt['name']: Prompt(**prompt) for prompt in prompts_data}
        self.save = save
        self.shortcuts_to_prompt = self._build_shortcuts_dict()

    def _build_shortcuts_dict(self):
        shortcuts_dict = {}
        for prompt in self.prompts.values():
            for shortcut in prompt.shortcuts:
                shortcuts_dict[shortcut] = prompt
        return shortcuts_dict

parsed_json = json.loads(config_raw_data)

config = Config(parsed_json['prompts'], parsed_json['save'])

SYSTEM_PROMPT = config.prompts['default'].prompt

user_input = ""

def custom_prompt_resolver(test_if_shortcut):
    if test_if_shortcut in config.shortcuts_to_prompt:
            return config.prompts[test_if_shortcut].prompt
    return None


SYSTEM_PROMPT = config.prompts["default"].prompt
if len(argv) > 1:
    is_default = True
    custom_prompt = custom_prompt_resolver(argv[1])
    if custom_prompt:
        SYSTEM_PROMPT = custom_prompt
        is_default = False
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        exit(0)

    user_input_start = 1
    if is_default != True:
        user_input_start = 2

    for i in range(user_input_start, len(argv)):
        user_input = user_input + " " + argv[i]
else:
    user_input = input(f"{USER_NAME}: ")

messages =  [
                { "content": SYSTEM_PROMPT ,"role": "system"},
                { "content": user_input ,"role": "user"},
            ]

def execute_command(response, command):
    if re.search( "#\s*ASK_USER"  , response.response_uptil_now.strip()):
        print("Execute Command: " + command + "\n")
        do_proceed = input("Proceed with command?  y/n: ")
        # TODO fix if no character
        if do_proceed.strip().lower()[0] != 'y' :
            return -1
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out, err = process.communicate()
    if err != "":
        print("Execution Error:\n" + err + "\n")
        exec_results = { "content": f"Execution result: error: {err}" ,"role": "system"}   
    elif out != "":
        print("Execution Results:\n" + out + "\n")
        exec_results = { "content": f"Execution result: {out}" ,"role": "system"}   
    else:
        exec_results = { "content": f"Execution result: null output" ,"role": "system"}   
    messages.append(exec_results)
    return 0

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
        if execute_command(response, command) != 0:
            continue
    # If it's bash quotes
    if re.search( "```(.*\n*)*```" , response.response_uptil_now.strip().lower()):
        pass

    if re.search( "#\s*exit" , response.response_uptil_now.strip().lower()):
        print()
        exit(0)

    user_input = input(PRINTED_REPLY_HEAD)
    message = { "content": user_input ,"role": "user"}
    messages.append(message)
    
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print()
        exit(0)
