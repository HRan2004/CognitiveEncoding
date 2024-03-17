import os
import pandas as pd

from models.gpt4 import call_gpt4
from models.qianwen import call_qwen


num = 20
source_file_path = './clean/all_data.xlsx'
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
如果无需修改就重复原文，如果有不断重复的文本可能是语音转换时的问题，请修正。
不要说缺少信息，无实意。不要输出任何解释无法处理的话，你只要尽力大胆猜测他是什么意思即可。


你的格式应该是这样的：
内容概述：xxxxxx

1. xxxxx
....
[SENTENCES_LENGTH]. xxxxx
'''


df = pd.read_excel(source_file_path, index_col=0)


def clean_sentences(lines, before):
  global user_prompt
  prompt = user_prompt.replace('[SENTENCES]', '\n'.join(lines))
  prompt = prompt.replace('[BEFORE]', before)
  prompt = prompt.replace('[SENTENCES_LENGTH]', str(len(lines)))
  print('\nPROMPT:')
  print(prompt, end='\n\n\n')
  print('RESULT:\n')
  result_text = call_gpt4(prompt)
  describe = ''
  infos = []
  results = []
  if '内容概述：' in result_text:
    describe = result_text.split(f'内容概述：')[1].split(f'\n')[0].strip()
  for i in range(1, len(lines) + 1):
    if f'\n{i}.' in result_text:
      result = result_text.split(f'\n{i}.')[1].split(f'\n')[0].strip()
      info = ''
      if result[0] == '(' or result[0] == ')':
        if result[-1] == '（' or result[-1] == '）':
          info = '[EXPLAIN] ' + result[1:-1]
          result = ''
      results.append(result)
      infos.append(info)
    else:
      results.append('')
      infos.append('[NOTFOUND]')
      print('Result format error')
  print('\n\n\n')
  return results, describe, infos


filename = ''
lines = []
ris = []


def do_current(ri):
  global lines, ris

  print('')
  before = ''
  for bi in range(10):
    bci = ri - bi - len(lines)
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
  # print('Before:', before)

  results, describe, infos = clean_sentences(lines, before)
  # results = ['[RESULT_TEXT]'] * len(lines)
  # describe = '[DESCRIBE_TEXT]'
  df.at[ris[0], 'describe'] = describe
  for i, result in enumerate(results):
    df.at[ris[i], 'clean'] = result
    df.at[ris[i], 'info'] = infos[i]
  try:
    df.to_excel(source_file_path)
  except Exception as e:
    print('Warning: Save failed.', e)

  print('')
  lines = []
  ris = []


for ri, row in df.iterrows():
  row_clean = str(row['clean'])
  if row_clean is not None and row_clean != 'nan' and len(row_clean) > 0:
    continue
  if filename != row['filename']:
    filename = row['filename']
    if len(lines) > 0:
      do_current(ri)
      print(f"File finished: {filename}\n")

  value = str(row['Value'])
  if len(value) > 0 and value != 'nan' and value != 'None':
    li = len(lines) + 1
    lines.append(str(li) + '. ' + value)
    ris.append(ri)
    print(f'Append {li} ({ri}):  {value}')
  else:
    df.at[ri, 'info'] = '[EMPTY]'
  if len(lines) >= num:
    do_current(ri)

