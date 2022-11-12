import json


def merge(file_list, output_file):
    data_total = []
    for file in file_list:
        with open(file, 'r') as f:
            full_data = json.load(f)
        data = full_data['data']
        data_total.extend(data)
    final_data = {'data': data_total}
    with open(output_file, 'w') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)


file_list = [
    'static/dataset/qa/dev-context-vi-question-vi.json',
    'static/dataset/qa/mailong25-dev.json',
    'static/dataset/qa/mailong25-train.json',
    'static/dataset/qa/test-context-vi-question-vi.json',
    'static/dataset/qa/xquad.vi.json',
    'static/dataset/qa/zac2022_qa.json'
]

merge(file_list,
      'static/dataset/qa/merged_all_dataset.json')
