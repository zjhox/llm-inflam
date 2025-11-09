
def keep_first_n_lines(file_path, n=50001):
    """
    保留文件前n行，删除其余内容
    :param file_path: 文本文件路径（相对/绝对路径）
    :param n: 需保留的行数（默认50000行）
    """
    # 临时文件路径（避免直接覆盖原文件导致数据丢失）
    temp_file_path = file_path + ".tmp"
    
    try:
        # 读取原文件前n行，写入临时文件
        with open(file_path, "r", encoding="utf-8") as infile, \
             open(temp_file_path, "w", encoding="utf-8") as outfile:
            
            for line_num, line in enumerate(infile, 1):
                outfile.write(line)
                # 达到目标行数后停止读取
                if line_num >= n:
                    break
        
        
        print(f"成功保留前{n}行，文件已保存：{temp_file_path}")
    
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}")
    except Exception as e:
        # 若出错，删除临时文件避免残留
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print(f"错误：处理文件时发生异常 - {str(e)}")

# -------------------------- 配置区域 --------------------------
# 替换为你的文本文件路径（例如："data.txt" 或 "C:/docs/input.txt"）
TARGET_FILE = "data/source_data/mydata1019_cn.jsonl"
# 需保留的行数（默认50000行，可根据需求修改）
KEEP_LINES = 50001
# --------------------------------------------------------------

# 执行脚本
if __name__ == "__main__":
    keep_first_n_lines(TARGET_FILE, KEEP_LINES)