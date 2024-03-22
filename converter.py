import pandas as pd
import os

def remove_lrm(text):
    # 替换文本中的U+200E字符为空字符串
    return text.replace('\u200e', '')

def process_excel_file(filename):
    # 读取excel文件
    df = pd.read_excel(filename, header=None)  # 不使用列名
    # 获取文件名作为导演信息
    director = os.path.splitext(os.path.basename(filename))[0]
    # 处理excel文件，将内容转成词典格式
    movies_dict = {}
    for index, row in df.iterrows():
        if not pd.isna(row[0]) and not pd.isna(row[1]):
            # 移除演员表中的左至右标记
            actors = remove_lrm(row[1]).split('/')
            # 将信息添加到词典里
            movies_dict[row[0]] = {'director': director, 'actors': actors}
    return movies_dict

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('{\n')
        for key, value in data.items():
            f.write(f"  '{key}': ")
            f.write("{")
            f.write(f"'director': '{value['director']}', ")
            f.write(f"'actors': {value['actors']}")
            f.write("},\n")
        f.write('}\n')

movies_dict = process_excel_file('杜琪峰.xlsx')
save_to_file(movies_dict, 'movies-per-杜琪峰.py')
