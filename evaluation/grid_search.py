from sklearn.model_selection import ParameterGrid
import requests
from tqdm import tqdm

# Tasks 2
# tasks = [
#     ("query1", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=philosophy%0Aquotes.tags%3Aphilosophy~2%0Aquotes.text%3Aphilosophy"),
#     ("query2", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=-genres%3Aphilosophy%0Aquotes.tags%3Aphilosophy"),
#     ("query3", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=epic%20fantasy%0Aauthors%3A%22Stephen%20King%22%5E15%0Agenre1%3Afantasy%5E30%0Agenre2%3Afantasy%5E10%0Agenre3%3Afantasy%5E2"),
#     ("query4", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=genres%3Aspace%2Cnonfiction%0A-genres%3Afiction%0AauthorsCount%3A1%0ApageCount%3A%5B200%20TO%20*%5D%0Aquotes.text%3Aspace~3"),
# ]
tasks = [
    ("query1", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=philosophy%0Aquotes_en.text%3Aphilosophy%0Aquotes_en.tags%3Aphilosophy~2%0Adescription_en%3Aphilosophy"),
    ("query2", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=-genres%3Aphilosophy%0Aquotes_en.tags%3Aphilosophy"),
    ("query3", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=epic%20fantasy%0Adescription_en%3Aepic%20fantasy%0Aquotes_en.tags%3Aepic%20fantasy%0Aauthors%3A%22Stephen%20King%22%5E15%0Agenre1%3Afantasy%5E30%0Agenre2%3Afantasy%5E10%0Agenre3%3Afantasy%5E2"),
    ("query4", "http://127.0.0.1:8983/solr/goodreads/select?defType=edismax&indent=true&q.op=OR&q=space%20nonfiction%0A-genres%3Afiction%0AauthorsCount%3A1%0ApageCount%3A%5B200%20TO%20*%5D%0Aquotes_en.text%3Aspace"),
]

# &qf=title%5E2%20authors%5E1%20%20genre1%5E2%20genre2%5E2%20genre3%5E1.5%20wikipedia_description&rows=10"

MIN_VAL = 1
MAX_VAL = 5

# Tasks 2
# param_grid = {
#     "title": [i for i in range(1, 10)],
#     "authors": [i for i in range(MIN_VAL, MAX_VAL)],
#     "description": [i for i in range(MIN_VAL, MAX_VAL)],
#     "genre1": [i for i in range(MIN_VAL, MAX_VAL)],
#     # "genre2": [round(i, 1) for i in np.arange(0.1, 5.5, 0.5)],
#     # "genre3": [round(i, 1) for i in np.arange(0.1, 5.5, 0.5)],
#     "quotes.text": [i for i in range(MIN_VAL, MAX_VAL)],
#     "quotes.tags": [i for i in range(MIN_VAL, MAX_VAL)],
# }

param_grid = {
    "title": [i for i in range(MIN_VAL, MAX_VAL)],
    "authors": [i for i in range(MIN_VAL, MAX_VAL)],
    "genre1": [i for i in range(MIN_VAL, MAX_VAL)],
    "genre2": [i for i in range(MIN_VAL, MAX_VAL)],
    "genre3": [1, 2],
    "wikipedia_description": [i for i in range(MIN_VAL, MAX_VAL)],
}

def ap(results, relevant):
    """Average Precision"""
    precision_values = []
    for idx, doc in enumerate(results, start=1):
        if doc['title'] in relevant:
            precision_values.append(len([doc for doc in results[:idx] if doc['title'] in relevant]) / idx)
    if len(precision_values) > 0:
        return sum(precision_values) / len(precision_values)
    return 0

def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['title'] in relevant])/n

param_grid = ParameterGrid(param_grid)

p10_dict = {} # Keys: [parameter_index][query_name] = P@10
avp_dict = {}

with tqdm(total=len(param_grid)*len(tasks)) as pbar:
    for query_name, url in tasks:
        qrels_file = f"{query_name}/relevant.txt"

        # Read qrels to extract relevant documents
        relevant = list(map(lambda el: el.strip(), open(qrels_file).readlines()))
        
        task_ap_list = []
        for i, p in enumerate(param_grid):
            # qf = f"qf=title%5E{p['title']}%20authors%5E{p['authors']}%20description%5E{p['description']}%20genre1%5E{p['genre1']}%20genre2%5E2%20genre3%5E1.5%20quotes.text%5E{p['quotes.text']}%20quotes.tags%5E{p['quotes.tags']}&rows=10"
            qf = f"&qf=title%5E{p['title']}%20authors%5E{p['authors']}%20%20genre1%5E{p['genre1']}%20genre2%5E{p['genre2']}%20genre3%5E{p['genre3']}%20wikipedia_description%5E{p['wikipedia_description']}&rows=10"
            query_url = f"{url}&{qf}&fl=title"

            # Get query results from Solr instance
            results = requests.get(query_url).json()['response']['docs']
            
            p10_dict[i] = p10_dict.get(i, {})
            p10_dict[i][query_name] = (p10(results, relevant)
            avp_dict[i] = avp_dict.get(i, {})
            avp_dict[i][query_name] = ap(results, relevant)
            pbar.update(1)


max_p10 = 0
max_mAP = 0
best_params_index = -1
for i in range(len(param_grid)):
    mP10 = 0
    mAP = 0
    for query_name, _ in tasks:
        mP10 += p10_dict[i][query_name]
        mAP += avp_dict[i][query_name]
    mP10 /= len(tasks)
    mAP /= len(tasks)

    if mP10 > max_p10:
        max_p10 = mP10
        max_mAP = mAP
        best_params_index = i
    elif mP10 == max_p10:
        if mAP > max_mAP:
            max_p10 = mP10
            max_mAP = mAP
            best_params_index = i

print(param_grid[best_params_index], "ap", avp_dict[best_params_index], " p@10", p10_dict[best_params_index])

p = param_grid[best_params_index]
# qf = f"qf=title%5E{p['title']}%20authors%5E{p['authors']}%20description%5E{p['description']}%20genre1%5E{p['genre1']}%20genre2%5E2%20genre3%5E1.5%20quotes.text%5E{p['quotes.text']}%20quotes.tags%5E{p['quotes.tags']}&rows=10"
qf = f"&qf=title%5E{p['title']}%20authors%5E{p['authors']}%20%20genre1%5E{p['genre1']}%20genre2%5E{p['genre2']}%20genre3%5E{p['genre3']}%20wikipedia_description%5E{p['wikipedia_description']}&rows=10"
for query_name, url in tasks:
    print(f"{query_name},GridSearch,{url}&{qf}")