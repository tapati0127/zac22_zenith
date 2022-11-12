import json
import random

import requests
from tqdm import tqdm

num = 100000
end_point = 'https://www.wikidata.org/w/api.php?action=wbgetentities&sites=viwiki&titles={' \
            'titles}&languages=vi&props=aliases|labels&format=json'
title_file = 'static/dataset/wikipedia_20220620_all_titles.txt'
alias_file = 'static/dataset/el/aliases.jsonl'

alias_dict = {}
with open(alias_file, 'r') as f:
    for json_text in f:
        alias_dict.update(json.loads(json_text))

fout = open(alias_file, 'a')

with open(title_file, 'r') as f:
    entities = f.readlines()
    random.shuffle(entities)
    entities = entities[:num]
entitiess = [entities[50 * i:50 * i + 50] for i in range(int(num / 50))]
aliases_dict = {}

for entity in tqdm(entitiess, total=len(entitiess)):
    try:
        aliases = []
        _end_point = end_point.replace('{titles}', '|'.join(entity))
        res = requests.get(_end_point, timeout=4)
        if res.status_code == 200:
            res = res.json()
            level = res['entities']
            if level is not None:
                for k, v in level.items():
                    if 'Q' in k:
                        label = level[k].get('labels', {}).get('vi', {}).get('value')
                        if label:
                            if label not in alias_dict:
                                _aliases = level[k].get("aliases", {})
                                _aliases = _aliases.get('vi', [])
                                aliases = [_aliase.get('value', '') for _aliase in _aliases]
                                if len(aliases) > 0:
                                    json.dump({label: aliases}, fout, ensure_ascii=False)
                                    fout.write('\n')
        else:
            print(f'ERROR: {entity}')
    except Exception as e:
        print(f'except: {e}')
fout.close()
# with open('static/dataset/el/aliases.json', 'w') as f:
#     json.dump(aliases_dict, f, indent=2, ensure_ascii=False)
