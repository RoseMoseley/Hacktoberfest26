from ollama import ChatResponse
from ollama import chat
sys_promote:str = """
You are a creative word-fusion AI.

Given two words [word1, word2], give another word that is linked to both words.
for example: [blue,yellow] should give [green]

Prioritize giving real words that link well to the input words.

Output exactly one word and nothing else.

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
    return str(_chat(message).message.content).lower()
def print_chat(message:str)->str:
    '''
    simular with get_chat(), but print the response to console
        :param message: the words you send to AI
        :return: The messages returns by AI
    '''
    output = get_chat(message)
    print(output)
    return output
def _chat(message:str)-> ChatResponse:
    response = chat(model='gemma4:e2b',think=False,options={
    "temperature": 1.8,
    "top_k": 80,
    "top_p": 0.95
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