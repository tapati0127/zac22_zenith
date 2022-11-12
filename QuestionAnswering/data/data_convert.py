import json


def zalo_data_to_squid2(input_file, output_file):
    with open(input_file, 'r') as f:
        full_data = json.load(f)
    feature_list = []
    data = full_data['data']
    for item in data:
        _id = item['id']
        question = item['question']
        title = item['title']
        answers = []

        context = item['text']
        is_long_answer = item['is_long_answer']
        category = item['category']  # FULL_ANNOTATION,PARTIAL_ANNOTATION,FALSE_LONG_ANSWER
        if not is_long_answer:
            is_impossible = True
            plausible_answers = []
            temp = {
                'title': title,
                'paragraphs': [
                    {
                        'context': context,
                        'qas': [
                            {
                                'answers': answers,
                                'id': _id,
                                'question': question,
                                'is_impossible': is_impossible,
                                'plausible_answers': plausible_answers
                            }
                        ]
                    }
                ]
            }
            feature_list.append(temp)
        else:
            if category == 'FULL_ANNOTATION':
                start = item['short_candidate_start']
                text = item['short_candidate']
                temp = {
                    'title': title,
                    'paragraphs': [
                        {
                            'context': context,
                            'qas': [
                                {
                                    'answers': [
                                        {
                                            "answer_start": start,
                                            "text": text
                                        }
                                    ],
                                    'id': _id,
                                    'question': question,
                                    'is_impossible': False,
                                    'plausible_answers': []
                                }
                            ]
                        }
                    ]
                }
                feature_list.append(temp)
    final_data = {'data': feature_list}
    with open(output_file, 'w') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)


zalo_data_to_squid2('/home/tapati/Zenith_QA_System/static/dataset/qa/zac2022_train_merged_final.json',
                    '/home/tapati/Zenith_QA_System/static/dataset/qa/zac2022_qa.json')
