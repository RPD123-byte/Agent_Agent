"""
create a tool-creator assistant using the assistant creation API
"""

import json
import os
from jsonschema import Draft7Validator
import jsonschema

from creator_config import AssistantConfig as CreatorConfig
from utils import chat as chat_loop

from openai import OpenAI
client = OpenAI(api_key="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") # be sure to set your OPENAI_API_KEY environment variable



def is_valid_json_schema(schema):
    try:
        Draft7Validator.check_schema(schema)  # Draft7 is a commonly used version, but you can choose the appropriate draft for your needs
        return True
    except jsonschema.exceptions.SchemaError as err:
        print("JSON Schema Validation Error:", err)
        return False

    
def validate_tool_schema(tool_name):
    tool_json_path = f'tools/{tool_name}.json'
    with open(tool_json_path, 'r') as f:
        tool_details = json.load(f)

    # Assuming the schema is stored under 'parameters' in the tool JSON
    tool_schema = tool_details.get('parameters')
    if tool_schema and is_valid_json_schema(tool_schema):
        print(f"JSON Schema for tool {tool_name} is valid.")
    else:
        print(f"JSON Schema for tool {tool_name} is invalid.")

def create_tool_creator(assistant_details):
    # create the assistant
    tool_creator = client.beta.assistants.create(**assistant_details["build_params"])

    print(f"Created assistant to create tools: {tool_creator.id}\n\n" + 90*"-" + "\n\n", flush=True)

    # save the assistant info to a json file
    info_to_export = {
        "assistant_id": tool_creator.id,
        "assistant_details": assistant_details,
    }

    os.makedirs('assistants', exist_ok=True)
    with open('assistants/tool_creator.json', 'w') as f:
        json.dump(info_to_export, f, indent=4)

    return tool_creator

def talk_to_tool_creator(assistant_details):
    """
    talk to the assistant to create tools
    """

    # check if json file exists
    try:
        os.makedirs('assistants', exist_ok=True)
        with open('assistants/tool_creator.json') as f:
            create_new = input(f'Assistant details found in tool_creator.json. Create a new assistant? [y/N]')
            if create_new == 'y':
                raise Exception("User wants a new assistant")
            assistant_from_json = json.load(f)
            tool_creator = client.beta.assistants.retrieve(assistant_from_json['assistant_id'])
            print(f"Loaded assistant details from tool_creator.json\n\n" + 90*"-" + "\n\n", flush=True)
            print(f'Assistant {tool_creator.id}:\n')
            assistant_details = assistant_from_json["assistant_details"]
    except:
        tool_creator = create_tool_creator(assistant_details)

    # load the functions into the execution environment
    functions = assistant_details["functions"]
    for func in functions:
        # define the function in this execution environment
        exec(functions[func], globals())
    
        # add the function to the assistant details
        functions.update({func: eval(func)})

    # Create thread
    thread = client.beta.threads.create()

    chat_loop(client, thread, tool_creator, functions)


def main():
    # create the tool creator assistant and chat to create your tools
    creator_details = CreatorConfig().assistant_details
    talk_to_tool_creator(creator_details)

if __name__ == '__main__':
    main()