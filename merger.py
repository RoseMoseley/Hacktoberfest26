import json
#from model import get_chat

# This is a nested dictionary
# mergable_name: merges
# mergable_name: output
# when a new merge is added, we need to add both cases
known_merges = {
    "1": {
        "1": "2",
        "2": "3"
    },
    "2": {
        "1": "3",
        "2": "4"
    }
}

known_items = ["1", "2"]

def get_chat(input):
    return "test"

def merge_items(mergable1: str, mergable2: str) -> str:
    '''
    Provide 2 strings and it WILL merge them, it will first see if the merge is already known, if so it will just get the result, otherwise it will query the local model for what should be the output
    '''
    if mergable1 not in known_merges.keys():
        response = get_chat(f"{mergable1}, {mergable2}")
        add_merge(mergable1, mergable2, response)
    if mergable2 not in known_merges[mergable1].keys():
        response = get_chat(f"{mergable1}, {mergable2}")
        add_merge(mergable1, mergable2, response)
    return known_merges[mergable1][mergable2]

def add_merge(mergable1: str, mergable2:str, output:str) -> None:
    '''
    This will add the two items merge output to the known merge values for later lookup, this also adds the output to the known items
    '''
    if mergable1 not in known_merges.keys():
        known_merges.update({mergable1:{}})
    known_merges[mergable1][mergable2] = output
    if mergable2 not in known_merges.keys():
        known_merges.update({mergable2:{}})

    known_items.append(output)

    known_merges[mergable2][mergable1] = output

def save_merges_to_file(file_path: str) -> None:
    global known_merges, known_items
    with open(file_path, "w") as file:
        json.dump({"merges": known_merges, "known_items": known_items}, file)

def load_merges_from_file(file_path: str) -> None:
    global known_merges, known_items
    with open(file_path, "r") as file:
        data = json.load(file)
        known_merges = data["merges"]
        known_items = data["known_items"]