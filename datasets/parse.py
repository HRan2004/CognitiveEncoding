import os
import pandas as pd

# 指定你的目录路径
directory_path = './source'

# 创建一个空的DataFrame用于存储所有数据
combined_df = pd.DataFrame()
combined_df['filename'] = None

# 遍历目录下的所有文件
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        print(file_path)
        try:
            df = pd.read_excel(file_path, usecols=['Key', 'Value', 'table', 'divergence'])
        except ValueError:
            df = pd.read_excel(file_path, usecols=['Key', 'Value', 'table'])
            df['divergence'] = None
        df['filename'] = filename
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# 输出合并后的数据到一个新的Excel文件
output_file_path = os.path.join('./clean/all_data.xlsx')
combined_df.to_excel(output_file_path)

print('Combined Finished:', output_file_path)

all_text = ''
for index, row in combined_df.iterrows():
    # print(index, row)
    text = f"{index}. {row['Value']} - Result: {row['table']}"
    if row['divergence'] is not None and len(str(row['divergence'])) > 0 and str(row['divergence']) != 'nan':
        text += f" - Divergence Explain: {row['divergence']}"
    all_text += text + '\n'
    print(text)

with open('./clean/all_text.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)
    f.close()
