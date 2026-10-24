# Word Fusion
This is a fun game that requires you to merge words together to make a final target word.
This game uses a gemma 4:e2b model to run

## How To Play
When opening the game you will be give 4 word on the right and a goal word in the bottom left
Click on the words to start dragging them and click again to release them.
Drag words on top of each other to merge them into new words.
Drop a word in the bar on the right hand side to remove it, or click the clear button to remove all words.
Every new word you discover will be added to the list of words you have, so don't worry about losing newly made words!

## Setup
Install Ollama and the gemma4:e2b model
Run the code below to your terminal(if you have ollama installed)
```
> ollama run gemma4:e2b
```
Python is required and make sure to install the following packages required
```
pip install ollama
pip install pygame
```
To install the ollama python package and use
```
python main.py
```
To run the game

