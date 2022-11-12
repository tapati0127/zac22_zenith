import json
import random
from collections import Counter
from underthesea import chunk

from tqdm import tqdm

alias_file = 'static/dataset/el/aliases.jsonl'

alias_dict = {}
with open(alias_file, 'r') as f:
    for json_text in f:
        alias_dict.update(json.loads(json_text))


def write(fout, json_data):
    json.dump(json_data, fout, ensure_ascii=False)
    fout.write('\n')


def search_chunk(title: str, text: str):
    if len(title) <= 3:
        return None
    chunk_list: list = chunk(text)
    chunk_list.reverse()
    new_title = None
    for item, noun, _ in chunk(text):
        if title.lower() in item.lower():
            new_title: str = item
            break
    if new_title:
        begin = text.lower().find(new_title.lower())
        return begin, new_title
    return None


def search(title: str, text: str):
    title_lower = title.lower()
    text_lower = text.lower()
    if len(title) <= 3:
        return None
    start = random.randint(int(len(title) / 5), int(2 * len(title) / 3))
    begin_title = None
    aliases = alias_dict.get(title, [])
    random.shuffle(aliases)
    for alias in aliases:
        alias_lower = alias.lower()
        if alias_lower in text_lower[start:]:
            begin_title = text_lower.find(title_lower, start), alias, text
            alias_dict[title].remove(alias)
            break
    if begin_title is None and len(aliases) >= 1:
        new_title = aliases[0]
        if title_lower in text_lower[start:]:
            begin = text_lower.find(title_lower, start)
            end = begin + len(title)
            new_text = text[0:begin] + new_title + text[end:]
            begin_title = begin, new_title, new_text
            alias_dict[title].remove(new_title)

    if begin_title is None:
        if title_lower in text_lower[start:]:
            begin_title = text_lower.find(title_lower, start), title, text
    return begin_title


# read_file_entity_dict = r'static/dataset/el/entity_dict.json'
read_file_passages = r'static/dataset/retrieval/splitted_wikipedia_20220620_cleaned.jsonl'
write_file_el = r'static/dataset/el/wiki_el_dataset.jsonl'

fout = open(write_file_el, 'w')

# with open(read_file_entity_dict, 'r') as f:
#     entity_dict = json.load(f)

count = 0
with open(read_file_passages, 'r') as f:
    for line in f:
        count += 1

last_title = ''
counter = Counter()
with open(read_file_passages, 'r') as f:
    for line in tqdm(f, total=count):
        data = json.loads(line)

        _id = data.get('doc_id', 0)
        title = data.get('title', '')
        text = data.get('text', '')
        unique_id = data.get('id', '')

        if last_title != title:
            last_title = title
            continue
        if counter.get(title, 0) >= 2 + len(alias_dict.get(title, [])):
            continue
        res = search(title, text)
        if res:
            begin, new_title, text = res
            # item = entity_dict[_id]
            json_data = {
                # 'label': item['text'],
                'label_title': title,
                'mention': new_title,
                'context_left': text[0: begin],
                'context_right': text[begin + len(new_title):]
            }
            write(fout, json_data)
            counter[title] += 1
        last_title = title
