import json

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

# TODO: replace dummy call with the method to get the AI response
def merge_items(mergable1: str, mergable2: str) -> str:
    '''
    Provide 2 strings and it WILL merge them, it will first see if the merge is already known, if so it will just get the result, otherwise it will query the local model for what should be the output
    '''
    if mergable1 not in known_merges.keys():
        response = dummy_call(f"{mergable1}, {mergable2}")
        add_merge(mergable1, mergable2, response)
    if mergable2 not in known_merges[mergable1].keys():
        response = dummy_call(f"{mergable1}, {mergable2}")
        add_merge(mergable1, mergable2, response)
    return known_merges[mergable1][mergable2]

def add_merge(mergable1: str, mergable2:str, output:str) -> None:
    '''
    This will add the two items merge output to the known merge values for later lookup
    '''
    if mergable1 not in known_merges.keys():
        known_merges.update({mergable1:{}})
    known_merges[mergable1][mergable2] = output
    if mergable2 not in known_merges.keys():
        known_merges.update({mergable2:{}})
    known_merges[mergable2][mergable1] = output

def dummy_call(input: str) -> str:
    return ""

def save_merges_to_file(file_path: str) -> None:
    with open(file_path, "w") as file:
        json.dump(known_merges, file)

def load_merges_from_file(file_path: str) -> None:
    global known_merges
    with open(file_path, "r") as file:
        known_merges = json.load(file)