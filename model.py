from ollama import chat
sys_promote:str = """
You are a word-fusion AI. 
User will input two words in the form [word1, word2],
and you need to output a third word only based on these two words.
"""

def get_chat(message:str):
    return _chat(message)
def print_chat(message:str)->str:
    output = _chat(message)
    print(output)
    return output
def _chat(message:str)->str:
    response = chat(model='gemma4:e2b',messages=[
        {'role': 'system', 'content': f'{sys_promote}'}
        ,{'role': 'user', 'content': f'{message}'}]
                    )
    return response.message.content
print_chat("fileManager,soundPlayer")