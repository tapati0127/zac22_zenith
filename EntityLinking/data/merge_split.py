import json

from sklearn.model_selection import train_test_split

merge_files = [
    'static/dataset/el/wiki_el_dataset.jsonl',
    'static/dataset/el/zalo_el_dataset.jsonl'
]

train_file = 'static/dataset/el/train_el_dataset.jsonl'
test_file = 'static/dataset/el/test_el_dataset.jsonl'
total = []
for file in merge_files:
    with open(file, 'r') as f:
        for line in f:
            total.append(json.loads(line))

train, test = train_test_split(total, train_size=0.9, shuffle=True)


def write(dataset, filename):
    fout = open(filename, 'w')
    for item in dataset:
        fout.write(json.dumps(item, ensure_ascii=False))
        fout.write('\n')
    fout.close()


write(train, train_file)
write(test, test_file)
