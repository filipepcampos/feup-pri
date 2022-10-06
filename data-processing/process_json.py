import json
import sys

def process_json(transform_json):
     for line in sys.stdin:
        try:
            j = json.loads(line[:-2])
            j = transform_json(j)
            if j:
                print(json.dumps(j) + ",")
        except json.JSONDecodeError:
            print(line, end="")