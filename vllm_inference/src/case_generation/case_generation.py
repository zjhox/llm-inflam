

def get_field_dict(dict_file_path, units_dict, category_list):
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
    # 丢弃field_name为空的行
    df = df.dropna(subset=['field_name'])
    for _, row in df.iterrows():
        field_id,indicator_name,indicator_name_cn,field_name,units_id,category_id = row['field id'],row['indicator name'],row['indicator_name_cn'],row['field_name'],row['unit_id'],row['category_id']
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

def generate_case_json_list(csv_path, category_list, field_dict,cn=False,output_file_path=None):
    """
    从 csv_path 中读取数据，根据 category_list 和 field_dict 生成样本, 每个样本为一个 json 字符串列表，格式如下：
    {"eid": 1, "input": "[Basic information]\nAge: 56 years old\nGender: female\n......"]}
    其中 input 部分根据 cn 参数决定使用中文还是英文字段名称
    如果 output_file_path 不为 None，则将结果保存到指定文件中，每行一个 json 字符串，逐行写入
    """
    import pandas as pd
    import tqdm
    import json

    if output_file_path is not None:
        f = open(output_file_path, 'w', encoding='utf-8')
    case_josnl = []
    df = pd.read_csv(csv_path)
    for _, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        eid = row['eid']
        input = ''
        try: 
            for category in category_list:
                category_name = category['name_cn'] if cn else category['name']
                input += f' {category['id']}、[{category_name}]\n'
                for field_name in category['field_list']:
                    field_info = field_dict[field_name]
                    indicator_name = field_info['indicator_name_cn'] if cn else field_info['indicator_name']
                    units = field_info['units_cn'] if cn else field_info['units']
                    input += f'{indicator_name}: {row[field_name]} {units}\n' if pd.notna(row[field_name]) else f'{indicator_name}: NA\n'
            if output_file_path is not None:
                f.write(json.dumps({
                    'eid': eid,
                    'input': input,
                }, ensure_ascii=False) + '\n')
            else:
                case_josnl.append({
                    'eid': eid,
                    'input': input,
                })
        except Exception as e:
            print(f'Error processing eid {eid}: {e}')
            print('category:', category, 'field_name:', field_name)
            continue
    return case_josnl