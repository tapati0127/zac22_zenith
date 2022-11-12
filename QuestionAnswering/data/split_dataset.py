import json

from sklearn.model_selection import train_test_split


def split(file, train_file, test_file):
    with open(file, 'r') as f:
        data = json.load(f)
    train, test = train_test_split(data['data'], test_size=0.1, random_state=42)
    with open(train_file, 'w') as f:
        json.dump({'data': train}, f, indent=2, ensure_ascii=False)

    with open(test_file, 'w') as f:
        json.dump({'data': test}, f, indent=2, ensure_ascii=False)


split('/home/tapati/Zenith_QA_System/static/dataset/qa/merged_all_dataset.json',
      '/home/tapati/Zenith_QA_System/static/dataset/qa/merged_train_dataset.json',
      '/home/tapati/Zenith_QA_System/static/dataset/qa/merged_test_dataset.json')
