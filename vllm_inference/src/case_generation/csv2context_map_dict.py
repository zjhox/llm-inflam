import pandas as pd

def generate_category_list(category_df: pd.DataFrame):
    """
    从 category_df 中读取数据，生成 category_list，格式如下：
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
    """
    category_list = []
    for _, row in category_df.iterrows():
        category_list.append({
            'id': row['category_index'],
            'name_cn': row['category_cn'],
            'name': row['category'],
            'field_list': [],
        })
    return category_list


def generate_units_dict(units_df: pd.DataFrame):
    """
    从 units_df 中读取数据，生成 units_dict，格式如下：
    units_dict = {
        1: ('', ''),
        100001: ('years', '岁'),
        100002: ('months', '月'),
        100003: ('days', '天'),
    }
    """
    units_dict = {}
    for _, row in units_df.iterrows():
        # todo: 中文单位待补充
        # 定义实例单位设置为空
        unit_name = row['unit_name'] if not str(row['unit_name']).startswith('Defined-instances') else ''
        units_dict[row['unit_index']] = (unit_name, unit_name)
    # 约定NA的id为0，手动设置NA为空
    units_dict[0] = ('', '')
    return units_dict


def generate_csv2context_map_dict(xlsx_path):
    """
    从 xlsx_path 中读取数据，生成指标到上下文的映射字典或列表，包括category_list,units_dict
    """
    df = pd.read_excel(xlsx_path, sheet_name=['category', 'units'])
    category_list  = generate_category_list(df['category'])
    units_dict = generate_units_dict(df['units'])
    return category_list, units_dict