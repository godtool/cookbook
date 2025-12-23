import json
import re

from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("LiquidAI/LFM2-1.2B", torch_dtype="bfloat16", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("LiquidAI/LFM2-1.2B")

def get_flight_status(id: str):
    """Get flight status for an ID.

    Args:
        id: The ID to get flight status for.
    """
    return {"status": "interrupted"}

def get_weather(location: str):
    """Get current weather for a location.

    Args:
        location: The location to get weather for.
    """
    # Mock weather data
    return {
        "location": location,
        "temperature": 72,
        "unit": "fahrenheit",
        "conditions": "partly cloudy",
        "humidity": 65,
        "wind_speed": 8
    }

def ask_model(messages: list[dict]) -> str:
    """
    Given message history and a set of available tool, generate text completion

    Args:
        messages: history of previous messages

    Return:
        str: model response, possibly containing a tool that needs to be called
    """
    inputs = tokenizer.apply_chat_template(messages, tools=[get_flight_status, get_weather], add_generation_prompt=True, return_dict=True, return_tensors="pt")
    outputs = model.generate(**inputs.to(model.device), max_new_tokens=256)
    response = tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=False)
    return response, messages

user_prompts = [
    "Get status for flight 123",
    "What is the weather like in San Francisco?",
    "How much money do I have in my savings account?"
]

for i, prompt in enumerate(user_prompts, 1):
    print(f"\n{'='*80}")
    print(f"Test Case {i}/{len(user_prompts)}")
    print(f"{'='*80}")
    print(f"User: {prompt}")
    print(f"{'-'*80}")

    messages = [{"role": "user", "content": prompt}]

    # generate a text completion with the model
    response, messages = ask_model(messages)

    # parse model respons


    print(f"Model Response:")
    print(response)
    print(f"{'='*80}")

exit()

def parse_tool_call(response_text: str) -> str:
    """Extracts the tool call JSON from the response text."""
    match = re.search(r'<\|tool_call_start\|>(.*?)<\|tool_call_end\|>', response)
    if not match:
        return []

    tool_call_str = match.group(1).strip()
    # Remove surrounding brackets: [get_status(id="123")] -> get_status(id="123")
    tool_call_str = tool_call_str.strip('[]')
    
    # Parse function name and arguments
    # Format: function_name(arg1="val1", arg2="val2")
    func_match = re.match(r'(\w+)\((.*)\)', tool_call_str)
    if not func_match:
        return []

    func_name = func_match.group(1)
    args_str = func_match.group(2)

    # Parse arguments (simple key="value" format)
    args = {}
    for arg in re.findall(r'(\w+)="([^"]*)"', args_str):
        args[arg[0]] = arg[1]

    return [{
        "type": "function",
        "function": {
            "name": func_name,
            "arguments": json.dumps(args)
        }
    }]
       
print("Extracted tool calls: ", extract_tool_call(response))

