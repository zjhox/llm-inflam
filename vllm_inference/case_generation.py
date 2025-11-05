
info_dict_demo = {
    'age': {
        'indicator_name': 'Age at recruitment',
        'indicator_name_cn': '年龄',
        'units': 'years',
        'units_cn': '岁',
        'category': 'basic information',
        'category_cn': '基本信息',
        'comment': '',
    },
}

category_list = [
    {
        'category_cn': '基本信息',
        'category': 'basic information',
        'field_dict': {
            'age': {
            'indicator_name': 'Age at recruitment',
            'indicator_name_cn': '年龄',
            'units': 'years',
            'units_cn': '岁',
            'comment': '',
            }
        }
    },
]


def generate_case(row, info_dict, cn=False):
    if cn:
        for field in info_dict:
            field_context = field['indicator_name_cn'] + ':' + row[field] + ' ' + field['units_cn']
