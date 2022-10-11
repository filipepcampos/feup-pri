import json
import sys

def process_json(transform_json):
     for line in sys.stdin:
        if(len(line) > 2):
            has_comma = line[-2] == ','
            j = json.loads(line[:-2] if has_comma else line[:-1])
            j = transform_json(j)
            if j:
                print(json.dumps(j) + ("," if has_comma else ""))
        else:
            print(line, end="")