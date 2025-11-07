
field_dict_demo = {
    'age': {
        'indicator_name': 'Age at recruitment',
        'indicator_name_cn': '年龄',
        'units': 'years',
        'units_cn': '岁',
        'comment': '',
    },
}

category_list  = [
    {
        'id': '1',
        'name_cn': '基本信息',
        'name': 'basic information',
        'field_list': [],
    },
    {
        'id': '2',
        'name_cn': '社会经济因素',
        'name': 'socioeconomic factors',
        'field_list': [],
    },
    {
        'id': '3',
        'name_cn': '健康因素',
        'name': 'health factors',
        'field_list': [],
    },
]

units_dict = {
    '1': ('no units', '无单位'),
    '100001': ('years', '岁'),
    '100002': ('months', '月'),
    '100003': ('days', '天'),
}


def get_field_dict(dict_file_path):
    """
    从 dict_file_path 中获取指标信息字典; csv or xlsx 格式如下：
    field_id,indicator_name,indicator_name_cn,field_name,units_id,category_id

    构建 field_dict 和 category_list，格式如下：

    field_dict = {
        'age': {
            'field_id': '1',
            'indicator_name': 'Age at recruitment',
            'indicator_name_cn': '年龄',
            'units': 'years',
            'units_cn': '岁',
            'comment': '',
        },
    }

    category_list  = [
        {
            'id': '1',
            'name_cn': '基本信息',
            'name': 'basic information',
            'field_list': ['age', ......],
        },
        ......
    ]

    """
    import pandas as pd
    
    if dict_file_path.endswith('.csv'):
        df = pd.read_csv(dict_file_path)
    elif dict_file_path.endswith('.xlsx'):
        df = pd.read_excel(dict_file_path, sheet_name='dict')
    else:
        raise ValueError('dict_file_path must be csv or xlsx file')
    
    field_dict = {}
    for _, row in df.iterrows():
        field_id,indicator_name,indicator_name_cn,field_name,units_id,category_id = row
        field_dict[field_name] = {
            'field_id': field_id,
            'indicator_name': indicator_name,
            'indicator_name_cn': indicator_name_cn,
            'units': units_dict[units_id][0],
            'units_cn': units_dict[units_id][1],
            'comment': '',
        }
        for category in category_list:
            if category['id'] == category_id:
                category['field_list'].append(field_name)
                break
    return field_dict, category_list

def generate_case_json_list(csv_path, category_list, field_dict,cn=False):
    """
    从 csv_path 中读取数据，根据 category_list 和 field_dict 生成样本, 每个样本为一个 json 字符串列表，格式如下：
    {"eid": 1, "input": "[Basic information]\nAge: 56 years old\nGender: female\n......"]}

    """
    case_josnl = []
    import pandas as pd
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        eid = row['eid']
        input = ''
        for category in category_list:
            category_name = category['name_cn'] if cn else category['name']
            input += f'[{category_name}]\n'
            for field_name in category['field_list']:
                field_info = field_dict[field_name]
                indicator_name = field_info['indicator_name_cn'] if cn else field_info['indicator_name']
                units = field_info['units_cn'] if cn else field_info['units']
                input += f'{indicator_name}: {row[field_name]} {units}\n'
        case_josnl.append({
            'eid': eid,
            'input': input,
        })
    return case_josnl