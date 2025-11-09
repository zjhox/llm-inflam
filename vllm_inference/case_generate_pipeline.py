import argparse
import colorlog 
import logging
import os
from src.utils.logger import set_logger
from src.case_generation.case_generation import get_field_dict, generate_case_json_list
from src.case_generation.csv2context_map_dict import generate_csv2context_map_dict
import json

def set_argparser():
    parser = argparse.ArgumentParser(description='Case Generation Pipeline')
    parser.add_argument('--dict_file_path', type=str, default='data/meta/dict.xlsx', help='Path to the dictionary file (csv or xlsx)')
    parser.add_argument('--data_file_path', type=str, default='data/ukb_initial/mydata1019_1107_mini.csv', help='Path to the data file (csv)')
    parser.add_argument('--cn', action='store_true', help='Whether to use Chinese field names')
    parser.add_argument('--output_file_path', type=str, default='data/source_data/mydata1019_mini.jsonl', help='Path to the output file (csv)')
    parser.add_argument('--lined', action='store_true', help='Whether to use line-by-line data')
    args = parser.parse_args()
    return args

def main():
    args = set_argparser()
    logger = colorlog.getLogger('case_generate_pipeline logger')
    set_logger(logger, log_file_path="log.txt")

    logger.info("Starting case generation pipeline...")
    logger.info('args: %s', args)

    # 生成 category_list 和 units_dict
    category_list, units_dict = generate_csv2context_map_dict(args.dict_file_path)
    logger.info('category_list[:2]: %s', category_list[:2])
    logger.info('units_dict[:3]: %s', list(units_dict.items())[:3])
    # 生成 field_dict
    field_dict, category_list = get_field_dict(args.dict_file_path, units_dict, category_list)
    logger.info('field_dict keys[:3]: %s', list(field_dict.keys())[:3])
    if args.lined:
        logger.info('Using line-by-line data processing mode.')
        generate_case_json_list(args.data_file_path, category_list, field_dict, args.cn, args.output_file_path)
        logger.info('case_json_list saved to %s', args.output_file_path)
    else:
        logger.info('Using standard data processing mode.')
        # 生成 case_json_list
        case_json_list = generate_case_json_list(args.data_file_path, category_list, field_dict, args.cn)
        logger.info('case_json_list[:1]: %s', case_json_list[:1])
        # 保存 case_json_list 到 args.output_file_path
        with open(args.output_file_path, 'w', encoding='utf-8') as f:
            for case_json in case_json_list:
                f.write(json.dumps(case_json, ensure_ascii=False) + '\n')
        logger.info('case_json_list saved to %s', args.output_file_path)

    logger.info("case_generate_pipeline completed successfully.")


if __name__ == "__main__":
    main()