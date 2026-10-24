import merger
import random
def get_goal(option_size:int,recursive_count:int,all_words:list[str])->tuple[list,list,str]:#merger.known_items):
    '''
    get the goal,required items, step to goal and the goal tuple
    :param option_size: the size of the options
    :param recursive_count: number of recursions to get the goal
    :param all_words: the list of all words
    :return: tuple(list of required items, list of step to goal,goal)
    '''
    items:list[str] = []
    used_items:list[str] = []
    for i in range(option_size):
        items.append(random.choice(all_words))
    used_items.extend(items)
    print(f"Goal:",end=" ")
    current_item = items[0]
    new_item = ""
    for i in range(recursive_count):
        new_item = merger.merge_items(current_item,random.choice(used_items))
        current_item = new_item
        used_items.append(current_item)
    print(f"items:{items}\ngoal:{current_item}\n====")
    return items,current_item
if __name__ == "__main__":
    lines = []
    with open("common-words.txt", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    get_goal(4,7,lines)
