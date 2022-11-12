import json

from tqdm import tqdm

zalo_file = 'static/dataset/zac2022_train_merged_final.json'
output_file = 'static/dataset/el/zalo_el_dataset.jsonl'
title_file = 'static/dataset/wikipedia_20220620_all_titles.txt'

with open(title_file, 'r') as f:
    entities = list(f)
    entities = [row.rstrip('\n') for row in entities]


fout = open(output_file, 'w')
count = 0
with open(zalo_file,'r') as f:
    all_dict = json.load(f)
    data = all_dict['data']

for item in tqdm(data, total=len(data)):
    if item['category'] != 'FULL_ANNOTATION':
        continue
    answer = item['answer']
    text = item['text']
    begin = item['short_candidate_start']
    short_candidate = item['short_candidate']
    if 'wiki' in answer:
        title = answer.replace('wiki/', '')
        title = title.replace('_', ' ')
        # print(title)
        #verify title
        if title in entities:
            # print(f'OK: {title}')
            json_data = {
                # 'label': item['text'],
                'label_title': title,
                'mention': short_candidate,
                'context_left': text[0: begin],
                'context_right': text[begin + len(short_candidate):]
            }
            count+=1
            json.dump(json_data, fout, ensure_ascii=False)
            fout.write('\n')
        else:
            print(f'ERROR: {title}')
            pass
        # input()

fout.close()
print(f'TOTAL: {count}')