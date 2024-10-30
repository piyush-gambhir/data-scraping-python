
import ollama


def generate_streaming_response(model_name, message, stream=False):
    response = ollama.chat(model=model_name, messages=[
                           {'role': 'user', 'content': message}], stream=stream)
    if stream:
        for part in response:
            print(part['message']['content'], end='', flush=True)
    else:
        return response['message']['content']


def generate_response(model_name, prompt):
    response = ollama.generate(model=model_name, prompt=prompt)
    return response['response']
