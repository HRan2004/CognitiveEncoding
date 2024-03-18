from models.gpt4 import call_gpt4
import pandas as pd

num = 20
source_file_path = './clean/all_data.xlsx'
user_prompt = '''
我将会给你一段初中学校公开课的录音转换后的文本，我需要你帮我区分这些话分别是谁说的。
我最终需要用这个数据去分析课堂每一环节在做什么，所以数据一定要准确。

下面是文本：
[DATA]

请你先对该段文本内容进行概述，后面的回答里注意理解上下文后，再做出回答。
在每一个人硕的话前加老师或学生 冒号空格，然后是他说的话。一句一行。
其中可能会有学生说的话，也可能会有老师说的话，甚至有可能混合起来。
完整按顺序判断完所有文本，不要有遗漏。

录音有的话可能会只录到一部分，你可以频繁的去切分他们说的话。
有时候学生的音频很有可能没有录制到，如果你发现了，应该有学生说话的地方，却没有。可以输出一行 学生：（学生说的话，未录制清晰）
课堂中大部分都是老师在说话，多注意，很多情况是老师在反问或者肯定同学的回答，而不是同学在说话。
如果有时候文本很乱，可能是多个人同时讲话，可以结合上下文判断，如果是多个学生讨论，可以输出一行 学生：（学生们说的话，无法录制清晰）


请你严格按照以下格式回答

内容概述：xxxxxxx

学生：xxxx
老师：xxxx
老师：xxxx
学生：xxxx
老师：xxxx
......
'''

user_prompt_paragraph = '''
我将会给你一段初中学校公开课的录音转换后的文本，我想要分析出课堂的每个时间段学生正在做什么，我需要你帮我按课堂不同环节进行分段。

类型一共有五大类，十小类。
### 第一大类 被动：
接受: 学生被动接受学习内容，不做其他事情。 比如：
1.只是听或看，并不做笔记或回应。 
2.学生根据老师的简单指令，作出相应动作，如翻书等。

### 第二大类 主动：
记忆: 任何学生在记忆知识的行为。 比如 
1.学生在发言或讨论中引用先前知识 
2.学生独立进行记忆活动，如接下来几分钟，同学记一下课文/内容等 
3.学生听写或默写 
4.学生记笔记
5.学生集体跟着老师一起记忆当前课程知识点，如老师说上句，集体回答下句 
6.学生参与复习活动，如开小火车/快问快答等，回顾课文、单词、公式等

应用: 学生能够将所学知识应用到实际问题中，举例使用。 比如 
1.学生做对需要应用所学知识解决实际问题的练习题 
2.学生正确回答需要应用所学知识解决实际问题的教师提问 
3.学生在发言或讨论中将所学知识应用到实际问题中，可以举出具体的例子

### 第三大类 建构：
提问: 学生分解当前学习内容，理解各部分知识点，提出疑问。 比如 
1.学生向同学或者老师发出与所学知识相关提问（注意必须是学生向老师的提问，老师的提问或反问都不算）

阐述: 学生将不同的知识元素、技能或观点整合在一起，综合解决问题，提出自己的见解。 比如 
1.学生在发言或讨论中出现成段判断性描述，如XXX是正确的/错误的 
2.学生在发言或讨论中出现成段逻辑性描述，如XXX导致XXX，是因为XXXX，例如XXXX等 
3.学生在发言或讨论中出现总结性话语，如我认为XXXX是XXX”等 4.学生进行黑板板书讲解题目。 

创造: 学生对创新性内容表现出兴趣或探究欲望，尝试不同的方法策略，进行批判性思考，能够做出贡献或产出作品。 比如 
1.学生对创新性内容展示出探索欲，如主动举手提出想法。 
2.学生尝试不同的方法策略，学生在发言或讨论全新观点或新的解决方案。 
3.学生产出思维导图、知识树等成果，并包含创新性内容。

### 第四大类 交互：
支持: 学生赞同他人观点。 比如 
1.在同学或老师发表观点后，有明确的“我同意ta的观点”、“我赞同”、“我部分赞同”等表示赞同的语句 
2.对同学的观点进行补充

反对: 学生不赞同他人观点。 比如 
1.在同学或老师发表观点后，有明确的“我不同意他的观点”、“我不赞同”等表示反对的语句

讨论: 学生之间的讨论互动。 比如 
1.老师要求学生之间进行课堂讨论、小组实验等场景下，学生之间的相互讨论

### 第五大类 其他：
无内容：没有任何有效内容


以下是文本：
[DATA]


请你按课堂各环节帮我进行分段，随后我自己会判断类型。
有时候可能所有语句都属于一段，如果类型类似就分做一段就可以。有时候可能只有两三句，这都很正常，放心按照类型分即可。分出多少段都有可能，合理即可。
例如一整个师生问答环节，一整个仅老师讲课环节，一整个学生交流环节，一整个朗读背诵环节，都应该算做一段。
同时例如学生突然发表了一句支持或反对意见，有一句提问等，符合上述某个特别的分类，他也应当单独作为一段。
分段时，请先输出分段序号，及当前段落的课堂环节的小的概括标题，小标题要具体的概括在讨论什么内容，是什么样形式的环节。
然后在下一行输出该段全部的原文。注意不要遗漏原文中的任何语句，分段之间应该是紧密连接的。


严格按照以下格式回答我：
内容概述：（整体概括这段讲了什么）

1. （小标题）
xxxx
xxxx
xxxx

2. （小标题）
xxxx
xxxx
xxxx

......
'''

user_prompt_position = '''
我将会给你两段文本，一段带序号的完整文本，和一段从中抽出的节选文本（节选文本可能略有变动），你要告诉我节选文本的第一个字，开始于完整文本的哪里，回答我序号。

完整文本：
[ALL_TEXT]

节选文本：
[DATA]


请你严格按照以下格式回答我。

节选文本的开头最早出现于完整文本的 [n] xxxx 中。

（其中 [n] xxx 对应了完整文本中符合的那行的序号及内容）
'''


df = pd.read_excel(source_file_path, index_col=0)

rows = list(df.iterrows())


def call_with_print(prompt):
  print('Prompt:', end='\n\n')
  print(prompt, end='\n\n')
  print('Result:', end='\n\n')
  result = call_gpt4(prompt)
  print('\n\n\n')
  return result


progress = 0
while True:
  lines = []
  for i in range(num):
    ri = progress + i
    line = df.at[ri, 'clean']
    lines.append(line)
    print(f'Append {len(lines)} ({ri}):  {line}')

  result = call_with_print(user_prompt.replace('[DATA]', ' '.join(lines)))
  result_lines = []
  for result_line in result.split('\n'):
    if result_line[:3] == '老师：' or result_line[:3] == '学生：':
      result_lines.append(result_line)
  print('Result line number:', len(result_lines))

  result_lines_text = '\n'.join(result_lines)
  result = call_with_print(user_prompt_paragraph.replace('[DATA]', result_lines_text))

  paragraphs = []
  paragraph_now = 1
  in_paragraph = False
  for pi, line in enumerate(result.split('\n')):
    if line.startswith(str(paragraph_now) + '. '):
      paragraph_now += 1
      in_paragraph = True
      paragraphs.append([])
    elif len(line.strip()) == 0:
      in_paragraph = False
    elif in_paragraph:
      paragraphs[-1].append(line)
  paragraphs_text = []
  for paragraphs_lines in paragraphs:
    paragraphs_text.append('\n'.join(paragraphs_lines))
  print('Paragraphs:\n\n' + '\n\n'.join(paragraphs_text) + '\n\n')

  all_text = ''
  for li, line in enumerate(lines):
    all_text += f'[{li + 1}] {line}\n'
  print(all_text)

  for paragraph in paragraphs_text:
    prompt = user_prompt_position.replace('[ALL_TEXT]', all_text)
    prompt = prompt.replace('[DATA]', paragraph)
    while True:
      result = call_with_print(prompt)
      if '[' in result and ']' in result:
        text = result.split('[')[1].split(']')[0]
        if len(text) > 0 and 0 < int(text) < num + 1:
          if paragraph == paragraphs_text[-1]:
            progress += int(text) - 1
            print('Set progress to:', progress, end='\n\n\n')
          else:
            print('Position result:', text, end='\n\n\n')
            df.at[progress + int(text) - 1, 'paragraph'] = paragraph
          break
  break

