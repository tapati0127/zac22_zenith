from datetime import datetime
from typing import List

days = ['%-d', '%d']
months = ['%-m', '%m']
years = ['%Y', '%y', '%-y']
delimiters = ['', '/', '-', '.']
prefix = ['ngày', 'tháng', 'năm', '']
date_types = ['DAY', 'MONTH', 'YEAR']


def get_day_rule():
    rules = []
    for delimiter in delimiters:
        for day in days:
            for month in months:
                for year in years:
                    if delimiter == '':
                        _format = f'ngày {day} tháng {month} năm {year}'
                        rules.append((_format, 'DAY'))
                        _format = f'{day} tháng {month} năm {year}'
                        rules.append((_format, 'DAY'))
                        _format = f'ngày {day} tháng {month}, năm {year}'
                        rules.append((_format, 'DAY'))
                        _format = f'{day} tháng {month}, năm {year}'
                        rules.append((_format, 'DAY'))
                        _format = f'{day} tháng {month}, {year}'
                        rules.append((_format, 'DAY'))
                    else:
                        _format = f'ngày {day}{delimiter}{month}{delimiter}{year}'
                        rules.append((_format, 'DAY'))
                        _format = f'{day}{delimiter}{month}{delimiter}{year}'
                        rules.append((_format, 'DAY'))
    return rules


def get_month_rule():
    rules = []
    for delimiter in delimiters:
        for month in months:
            for year in years:
                if delimiter == '':
                    _format = f'tháng {month} năm {year}'
                    rules.append((_format, 'MONTH'))
                    _format = f'{month} năm {year}'
                    rules.append((_format, 'MONTH'))
                else:
                    _format = f'tháng {month}{delimiter}{year}'
                    rules.append((_format, 'MONTH'))
                    _format = f'{month}{delimiter}{year}'
                    rules.append((_format, 'MONTH'))
    return rules


def get_year_rule():
    rules = []
    for year in years:
        _format = f'năm {year}'
        rules.append((_format, 'YEAR'))
    return rules


RULES = get_day_rule()
RULES.extend(get_month_rule())
RULES.extend(get_year_rule())


def is_int(string: str):
    try:
        int(string)
        return True
    except:
        return False


def find_first_int(string_list: str):
    for i, item in enumerate(string_list):
        if is_int(item):
            return i
    return None


def find_last_int(string_list: str):
    res = None
    for i, item in enumerate(string_list):
        if is_int(item):
            res = i
    return res


def clear_redundancy(string: str):
    if 'ngày' in string:
        start = string.find('ngày')
        string = string[start:]
    start = find_first_int(string)
    end = find_last_int(string)
    if (start is not None) and (end is not None) \
            and (end != start) and (not string.startswith('năm')):
        return string[start:end + 1]
    else:
        return string


def filter_result(result, result_type):
    if result_type == 'DAY':
        return result.strftime('ngày %-d tháng %-m năm %Y')
    elif result_type == 'MONTH':
        return result.strftime('tháng %-m năm %Y')
    elif result_type == 'YEAR':
        return result.strftime('năm %Y')
    return None


def parse(string: str):
    string = string.lower()
    string = clear_redundancy(string)
    for rule, date_type in RULES:
        try:
            result = datetime.strptime(string, rule)
            result_type = date_type
            return filter_result(result, result_type)
        except:
            pass
    else:
        return None


print(parse('22:29 UTC ngày 31/5/2009'))
