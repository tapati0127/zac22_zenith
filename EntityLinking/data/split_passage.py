import json
from uuid import uuid4

from tqdm import tqdm
from underthesea import sent_tokenize


def write(fout, json_data):
    json.dump(json_data, fout, ensure_ascii=False)
    fout.write('\n')


def get_data(_id, title, subdoc):
    unique_id = str(uuid4())
    item = {
        'doc_id': _id,
        'title': title,
        'text': ' '.join(subdoc),
        'id': unique_id
    }
    return item


def rm_dup(item):
    text: str = item['text']
    item['text'] = text.replace(item['title'], '', 1)
    return item


read_file = r'static/dataset/wikipedia_20220620_cleaned.jsonl'
write_file_passages = r'static/dataset/retrieval/splitted_wikipedia_20220620_cleaned.jsonl'
write_file_entities = r'static/dataset/el/entities.jsonl'
write_file_entity_dict = r'static/dataset/el/entity_dict.json'
fout_passages = open(write_file_passages, 'w')
fout_entities = open(write_file_entities, 'w')
fout_entity_dict = open(write_file_entity_dict, 'w')

count = 0
with open(read_file, 'r') as f:
    for line in f:
        count += 1

last_title = ''
entity_dict = {}
with open(read_file, 'r') as f:
    for line in tqdm(f, total=count):
        data = json.loads(line)
        _id = data.get('id', 0)
        title = data.get('title', '')
        try:
            title_float = float(title)
            if title_float is not None:
                continue
        except:
            pass
        text = data.get('text', '')
        sents = sent_tokenize(text)
        count_char = 0
        subdoc = []

        for sent in sents:
            if count_char < 500:
                subdoc.append(sent)
                count_char += len(sent)
            else:
                item = get_data(_id, title, subdoc)
                write(fout_passages, item)
                if title != last_title:
                    item = rm_dup(item)
                    entity_dict[title] = item
                    write(fout_entities, item)
                    last_title = title
                count_char = 0
                subdoc = []

        if len(subdoc) > 0:
            item = get_data(_id, title, subdoc)
            write(fout_passages, item)
            if title != last_title:
                item = rm_dup(item)
                entity_dict[title] = item
                write(fout_entities, item)
                last_title = title

# fout_passages.close()
fout_entities.close()
json.dump(entity_dict, fout_entity_dict, ensure_ascii=False, indent=2)
fout_entity_dict.close()
