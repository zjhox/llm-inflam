import logging
import colorlog

def set_logger(logger, log_file_path="log.txt"):
    # 创建彩色日志格式
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        }
    )
    # 配置日志记录,默认输出到控制台(设置彩色输出)，还有文件log.txt
    haldler_console = logging.StreamHandler()
    haldler_console.setFormatter(formatter)
    haldler_file = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    haldler_file.setFormatter(formatter)
    logger.addHandler(haldler_console)
    logger.addHandler(haldler_file)
    logger.setLevel(logging.DEBUG)
