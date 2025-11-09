import pandas as pd
import yaml

if __name__ == '__main__':
    df = pd.read_csv('patient_info_dict.csv')
    field_dict = {}
    for i in range(len(df)):
        row = df.iloc[i]
        print(row)
        field_temp = row[1]
            
        field_dict[field_temp] = {
            'field_id': int(row[0]) if not row[0] == '—' else None,
            'indicator_name': str(row[1]),
            'units': str(row[2]),
        }
    # 将field_dict写入yml文件,且保留原顺序
    with open('temp.yml', 'w') as f:
        yaml.dump(field_dict, f, default_flow_style=False, allow_unicode=True)
