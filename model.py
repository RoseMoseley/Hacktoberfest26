from ollama import ChatResponse
from ollama import chat
sys_promote:str = """
You are a word-fusion AI. 
User will input two words in the form [word1, word2],
and you need to output a third word only based on these two words.
"""

def get_chat(message:str)->str:
    return _chat(message).message.content
def print_chat(message:str)->str:
    output = get_chat(message)
    print(output)
    return output
def _chat(message:str)-> ChatResponse:
    response = chat(model='gemma4:e2b',think=False,messages=[
        {'role': 'system', 'content': f'{sys_promote}'}
        ,{'role': 'user', 'content': f'{message}'}]
                    )
    return response
def _debug_chat(message:str)->str:
    response = _chat(message)
    print(response.message.thinking)
    print("===")
    print(response.message.content)
    return response

if __name__ == '__main__':
    _debug_chat("FileManager,MusicPlayer")