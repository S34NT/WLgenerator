from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher('', a.lower(), b.lower()).ratio()