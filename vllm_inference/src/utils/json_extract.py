import json

def extract_json(str):
    """
    从一个字符串中提取json对象
    :param str: 输入的字符串
    :return: 提取到的json对象

    demo str: "1、[基本信息]\n年龄: 61 years\n性别: Male \n2、[体格与肥胖指标]\n身高: 168.0 cm\n体重: 73.3 Kg\n体质指数（BMI）: 25.9708 Kg/m2\n", "model_generated_aging_prediction": ["```json\n{\n    \"推理过程\": \"根据提供的信息，我们可以从多个角度评估整体炎症水平和器官特异性炎症水平。首先，BMI、腰围、腰臀比、体脂百分比等指标提示个体存在肥胖，肥胖是慢性炎症的促进因素。血压、心率、血常规、血液生化检查等信息显示了心血管、血液系统和代谢系统的健康状况，其中CRP水平升高提示炎症状态。饮食与营养摄入、生活方式、睡眠特征等信息反映了个体的生活习惯对炎症水平的影响。最后，感染血清学检查结果和器官功能与影像指标提供了器官特异性炎症的线索。综合考虑，整体炎症水平较高，大脑、心血管、肝脏、肺炎、肾脏、骨骼肌肉和代谢系统均存在不同程度的炎症。具体数值需要根据上述信息进行综合评估。\",\n    \"整体炎症水平\": 75,\n    \"大脑炎症水平\": 50,\n    \"心血管炎症水平\": 65,\n    \"肝脏炎症水平\": 60,\n    \"肺炎症水平\": 45,\n    \"肾脏炎症水平\": 55,\n    \"骨骼肌肉炎症水平\": 55,\n    \"代谢系统炎症水平\": 70\n}\n```
    根据其中 “```json” 和 “```” 提取json对象

    """
    try : 
        start = str.find("```json") + len("```json")
        end = str.find("```", start)
        json_str = str[start:end]
        return json.loads(json_str)
    except Exception as e:
        # print(f"Error extracting JSON: {str}\n {json_str}， {e}")
        return None

if __name__ == "__main__":

    file_path = 'data/cache_file/mydata1019_cn_0_50000_qwen7I.jsonl'
    output_path = 'data/cache_file/mydata1019_cn_0_50000_qwen7I_extracted'
    selected_field = 'model_generated_aging_prediction'

    import pandas as pd
    import tqdm

    result_metric = []
    result_process = []
    total_lines = sum(1 for _ in open(file_path, "r", encoding="utf-8"))
    with open(file_path, "r", encoding="utf-8") as infile:
        for line in tqdm.tqdm(infile):
            data = json.loads(line)
            if selected_field in data:
                json_obj = extract_json(data[selected_field][0])
                if json_obj is None:
                    continue
                eid = data['eid']
                result_metric.append({
                    'eid': eid,
                    '整体炎症水平': json_obj['整体炎症水平'],
                    '大脑炎症水平': json_obj['大脑炎症水平'],
                    '心血管炎症水平': json_obj['心血管炎症水平'],
                    '肝脏炎症水平': json_obj['肝脏炎症水平'],
                    '肺炎症水平': json_obj['肺炎症水平'],
                    '肾脏炎症水平': json_obj['肾脏炎症水平'],
                    '骨骼肌肉炎症水平': json_obj['骨骼肌肉炎症水平'],
                    '代谢系统炎症水平': json_obj['代谢系统炎症水平'],
                })
                result_process.append({
                    'eid': eid,
                    '推理过程': json_obj['推理过程']
                })
    print(f"Extracted {len(result_metric)/total_lines*100:.2f}% records with metrics.")
    df_metric = pd.DataFrame(result_metric)
    df_metric.to_csv(output_path + '_metric.csv', index=False)
    df_metric.to_excel(output_path + '_metric.xlsx', index=False)
    df_process = pd.DataFrame(result_process)
    df_process.to_csv(output_path + '_process.csv', index=False)
    df_process.to_excel(output_path + '_process.xlsx', index=False)
