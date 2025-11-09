import os
# import pandas as pd 

# 从jsonl文件中读取数据，其中每一行是一个json对象
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(eval(line.strip()))
    return data


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Test Sample Builder")
    parser.add_argument('--data_file', default='data/cache_file/health_info-main_analysis-result-example-zjh.jsonl', help='Path to the input data file')
    parser.add_argument('--index', default=0, type=list or int, help='Indices of recently edited files')
    return parser.parse_args()

def main():
    args = parse_args()
    data_file = args.data_file
    index = args.index
    data = read_jsonl(data_file)
    
    if isinstance(index, int):
        index = [index]
    for i in index:
        print(f"Index: {i}")
        print(data[i])
        # 将 input 字段的内容分割打印
        if "input" in data[i]:
            print("input:")
            print(data[i]["input"])
        
        # 将model_generated_aging_prediction字段的内容按行分割打印
        if "model_generated_aging_prediction" in data[i]:
            print("model_generated_aging_prediction:")
            for line in data[i]["model_generated_aging_prediction"]:
                print(line)
        print("\n")

if __name__ == "__main__":
    main()