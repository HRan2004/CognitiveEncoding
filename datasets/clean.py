import os
import pandas as pd

from models.qianwen import call_qwen


user_prompt = '''
下面是一段公开课录音转换的文本，其中部分文本不正确，请你根据你的理解对其进行修改，使语句更加准确连贯，且符合场景。
注意，语音转换的文本会有大量的问题，请结合全部上下文，并改正。

[SENTENCES]

其中有老师说话的文本也有同学说话的文本，请你自行理解并区分。
请你先整体阅读一遍，并说出这堂课这部分大致在讲什么内容，然后开始修改文本。

原文按照10秒一段的方式换行分割，换行不影响语义和理解，在理解时请忽略。
然后请你输出给我的文本，按照原文的换行格式仍然每一行一一对应，并保留序号，这样我好找到你修改的部分。

注意你不需要根据语义去换行，请按照原文的文字在哪换行进行换行。
不要说缺少信息，无实意，或输出任何括号以及内部解释内容，你只要尽力大胆猜测即可。

你的格式应该是这样的：
内容概述：xxxxxx

1. xxxxx
....
20. xxxxx
'''


def clean_sentences(sentences):
  print(sentences, end='\n\n')
  result = call_qwen(user_prompt.replace('[SENTENCES]', sentences))
  return sentences


source_file_path = './clean/all_data.xlsx'
df = pd.read_excel(source_file_path)

filename = ''
lines = []

for index, row in df.iterrows():
  if filename != row['filename']:
    filename = row['filename']
  if filename != row['filename'] and len(lines) > 0:
    print(f"\nFile: {filename}")
    print(lines, end='\n')
    lines = []

  value = str(len(lines) + 1) + '. ' + str(row['Value'])
  if len(value) > 0 and value != 'nan':
    lines.append(value)
  if len(lines) >= 20:
    clean_sentences('\n'.join(lines))
    lines = []
    break

