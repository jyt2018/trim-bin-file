# 程序功能说明：
# 该程序用于从文件的开头或结尾移除指定数量的字节，并将处理后的内容保存到一个新文件中。
# 可以通过命令行参数指定要修剪的文件、要移除的字节数、修剪的位置（开头或结尾）以及输出文件的路径。

import os
from pathlib import Path
from tempfile import gettempdir
from argparse import ArgumentParser


# 默认输出文件的名称
DEFAULT_OUTPUT_FILE_NAME = "trimmed_file"
# 默认输出文件的路径，为系统临时目录与默认文件名的组合
DEFAULT_OUTPUT_FILE_PATH = Path(gettempdir()) / DEFAULT_OUTPUT_FILE_NAME

# 定义修剪位置的常量
class TrimOptions:
    END = "end"    
    START = "start"

# 创建命令行参数解析器
def create_parser():
    _parser = ArgumentParser(description="Remove given number of bytes from "
                                         "the start or end of a file.")
    _parser.add_argument("input_file", type=Path, action="store", 
                         help="Full path to the file to trim.")
    _parser.add_argument("bytes", type=int, action="store", 
                         help="Number of bytes to trim.")
    _parser.add_argument("side", choices=["start", "end"], 
                         help="Whether to trim from the start.")
    _parser.add_argument("-d", "--destination-file", type=Path, action="store", 
                         default=DEFAULT_OUTPUT_FILE_PATH,
                         help="Path to the output file. Defaults to a temporary file.")
    return _parser

# 计算要读取的字节数
def get_bytes_to_read(path, bytes):
    try:
        file_size = os.path.getsize(path)
        if bytes > file_size:
            raise ValueError(f"The number of bytes to trim ({bytes}) is larger than the file size ({file_size}).")
        return file_size - bytes
    except FileNotFoundError:
        print(f"Error: The input file {path} was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# 主函数
def main():
    args = create_parser().parse_args()
    bytes_to_read = get_bytes_to_read(args.input_file, args.bytes)
    
    if bytes_to_read is None:
        return
    
    try:
        with open(args.input_file, 'rb') as infile:
            if args.side == TrimOptions.START:
                infile.seek(bytes_to_read)
                data = infile.read()
            elif args.side == TrimOptions.END:
                data = infile.read()[:bytes_to_read]
        
        with open(args.destination_file, "wb") as outfile:
            outfile.write(data)
        print(f"File trimmed successfully. Output saved to {args.destination_file}.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == '__main__':
    main()