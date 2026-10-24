from ollama import ChatResponse
from ollama import chat
sys_promote:str = """
You are a creative word-fusion AI.

Given two words [word1, word2], invent a single new word that combines
their meaning, sound, spelling, symbolism, or cultural associations.

Prioritize originality and memorability over literal combinations.

Output exactly one invented word and nothing else.

If absolutely no meaningful connection can be found, output [unrelated].
"""
print("Loading model...")
chat(model='gemma4:e2b')
print("model loaded")
def get_chat(message:str)->str:
    '''
    :param message: the words you send to AI
    :return: The response returns by AI
    '''
    return str(_chat(message).message.content)
def print_chat(message:str)->str:
    '''
        :param message: the words you send to AI
        :return: The messages returns by AI
        simular with get_chat(), but print the response to console
    '''
    output = get_chat(message)
    print(output)
    return output
def _chat(message:str)-> ChatResponse:
    response = chat(model='gemma4:e2b',think=False,options={
    "temperature": 2,
    },messages=[
        {'role': 'system', 'content': f'{sys_promote}'}
        ,{'role': 'user', 'content': f'{message}'}]
                    )
    return response
def _debug_chat(message:str)->ChatResponse:
    response = _chat(message)
    print(response.message.thinking)
    print("===")
    print(response.message.content)
    return response

if __name__ == '__main__':
    user_input = input('Enter a word: ')
    while user_input != 'exit' and user_input != '':
        _debug_chat(user_input)
        user_input = input('Enter words: ')