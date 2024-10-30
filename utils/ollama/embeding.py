import ollama


def embed_text(model_name, input_text):
    return ollama.embed(model=model_name, input=input_text)


def embed_text_batch(model_name, input_texts):
    return ollama.embed(model=model_name, input=input_texts)
