import os
import pandas as pd

from models.gpt4 import call_gpt4
from models.qianwen import call_qwen


num = 20
user_prompt = '''
下面是一段公开课录音转换的文本，其中部分文本不正确，请你根据你的理解对其进行修改，使语句更加准确连贯，且符合场景。
注意，语音转换的文本会有大量的问题，请结合全部上下文，并改正。

这是前文，仅供你参考。
[BEFORE]

下方是我需要你处理的文本。
[SENTENCES]

其中有老师说话的文本也有同学说话的文本，请你自行理解并区分。
请你先整体阅读一遍，并说出这堂课这部分大致在讲什么内容，然后开始修改文本。

原文按照10秒一段的方式换行分割，换行不影响语义和理解，在理解时请忽略。
然后请你输出给我的文本，按照原文的换行格式仍然每一行一一对应，并保留序号，这样我好找到你修改的部分。

注意你不需要根据语义去换行，请按照原文的文字在哪换行进行换行。
不要说缺少信息，无实意，或输出任何括号以及内部解释内容，你只要尽力大胆猜测即可，但必须和原文有关，不能全自己编。

你的格式应该是这样的：
内容概述：xxxxxx

1. xxxxx
....
20. xxxxx
'''


source_file_path = './clean/all_data.xlsx'
df = pd.read_excel(source_file_path)
df = df.assign(clean=lambda x: x['clean'] if 'clean' in x.columns else '')


def clean_sentences(sentences, before):
  global user_prompt
  prompt = user_prompt.replace('[SENTENCES]', sentences)
  prompt = prompt.replace('[BEFORE]', before)
  print(user_prompt, end='\n\n\n')
  result_text = call_gpt4(prompt)
  results = []
  for i in range(1, num + 1):
    if f'\n{i}.' in result_text:
      result = result_text.split(f'\n{i}.')[1].split(f'\n')[0].strip()
      results.append(result)
    else:
      results.append('')
      print('Result format error')
  print('\n\n\n')
  return results


filename = ''
lines = []


def do_current(ri):
  global lines
  print('')
  before = ''
  for bi in range(10):
    bci = ri - bi - num
    if bci < 0:
      if len(before) == 0:
        before = '(无上文，开始上课)'
      else:
        before = '(开始上课)' + before
      break
    before_clean = str(df.at[bci, 'clean'])
    if before_clean is not None and before_clean != 'nan' and len(before_clean) > 0:
      before = before_clean + before
    else:
      print(f'Before text {bci} not found.')
  if len(before) == 0:
    print('Warning: Before text not found.')
    before = '(暂无前文参考内容)'
  print('Before:', before)

  results = clean_sentences('\n'.join(lines), before)
  # results = ['empty'] * num
  results_length = len(results)
  for i, result in enumerate(results):
    df.at[ri - results_length + i + 1, 'clean'] = result
  try:
    df.to_excel(source_file_path)
  except Exception as e:
    print('Warning: Save failed.', e)
  print('')
  lines = []


for ri, row in df.iterrows():
  row_clean = str(row['clean'])
  if row_clean is not None and row_clean != 'nan' and len(row_clean) > 0:
    continue
  if filename != row['filename']:
    filename = row['filename']
    if len(lines) > 0:
      do_current(ri)
      print(f"File finished: {filename}\n")

  value = str(len(lines) + 1) + '. ' + str(row['Value'])
  if len(value) > 0 and value != 'nan':
    lines.append(value)
    print(f'Get {ri}:   {value}')
  if len(lines) >= num:
    do_current(ri)

