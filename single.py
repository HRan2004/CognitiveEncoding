import openai
from http import HTTPStatus
import httpx
from dashscope import Generation


system_prompt = '''
你是一个逻辑能力语言理解能力各方面都很强的助手。
'''

user_prompt = f'''
我将会给你一段初中学校公开课的录音截取后转换后的文本，我需要对课程的每一部分在干什么做一个记录。
最后会需要请你帮忙判断一段文本属于哪一类型。


类型一共有10种。
接受: 学习者被动接受学习内容，不做其他事情。 比如 1.学习者盯着黑板/PPT/老师等（非发呆），只是听或看，并不做笔记或回应。 2.学习者根据老师的简单指令，作出相应动作，如翻书到XX面等
记忆: 任何学生在记忆知识的行为。 比如 "1.学习者记笔记 2.学习者独立进行记忆活动，如“接下来几分钟，同学记一下课文/内容等” 3.学习者听写或默写 4.学习者在发言或讨论中引用先前知识 5.学习者集体跟着老师一起记忆当前课程知识点，如老师说上句，集体回答下句 6.学习者参与复习活动，如开小火车/快问快答等，回顾课文、单词、公式等" 
应用: 学习者能够将所学知识应用到实际问题中，举例使用。 比如 "1.学习者做对需要应用所学知识解决实际问题的练习题 2.学习者正确回答需要应用所学知识解决实际问题的教师提问。 3.学习者在发言或讨论中将所学知识应用到实际问题中，可以举出具体的例子"
提问: 学习者分解当前学习内容，理解各部分知识点，提出疑问。 比如 1.学习者向同学或者老师发出与所学知识相关提问，包括一般疑问句和特殊疑问句
阐述: 学习者将不同的知识元素、技能或观点整合在一起，综合解决问题，提出自己的见解。 比如 "1.学习者在发言或讨论中出现成段判断性描述，如“XXX是正确的/错误的” 2.学习者在发言或讨论中出现成段逻辑性描述，如“XXX导致XXX，是因为XXXX，例如XXXX”等 3.学习者在发言或讨论中出现总结性话语，如“我认为XXXX是XXX”等 4.学习者进行黑板板书讲解题目" 
创造: 学习者对创新性内容表现出兴趣或探究欲望，尝试不同的方法策略，进行批判性思考，能够做出贡献或产出作品。 比如 "1.学习者对创新性内容展示出探索欲，如主动举手提出想法。 2.学习者尝试不同的方法策略，学习者在发言或讨论全新观点或新的解决方案。 3.学习者产出思维导图、知识树等成果，并包含创新性内容。" 
支持: 学习者赞同他人观点。 比如 "1.在同学或老师发表观点后，有“我同意ta的观点”、“我赞同”、“我部分赞同”等表示赞同的语句 2.对同学的观点进行补充"
反对: 学习者不赞同他人观点。 比如 1.在同学或老师发表观点后，有“我不同意ta的观点”、“我不赞同”等表示反对的语句
讨论: 学习者之间的讨论互动。 比如 1.课堂讨论、小组实验等场景下，学生之间相互讨论
无内容：没有任何有效内容


下面是已经标注好的准确数据，注意其中的分歧点，在判断摸棱两可的情况时会有很大帮助。
请你在回答时先进行参考与对比，最后再给出结果。
[DATA]

历史文本信息: (文本在转换时可能有问题，你可以适当修复句子)
[HISTORY]
我需要你判断的句子是:
[TEXT]


请你现在上方标注好的数据中寻找类似的话术，如果有，说出他的编号内容以及结果。
然后请注意历史文本信息，由于每一条信息只有10s时间但场景中师生的行为状态不会频繁发生改变。所以大概率本次的结果会与上次相同，请注意到明确的行为变更后，再给出与之前历史中不同的结果。
然后说出其中的文本分别来自于谁说的话，他们在讨论什么内容，做出详细的思考和解释，最后给出你的答案。
注意请必须在你的回答的最后，重复你的最终答案。
'''


client = openai.OpenAI(
    base_url="https://api.xty.app/v1",
    api_key='sk-n41nAj6WDDMgJgkS7a9eDc6dDd2f4930A0F7388b4cC44f31',
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

with open('./datasets/clean/all_text.txt', encoding='utf-8') as f:
    all_text = f.read()
    if len(all_text) > 20000:
        all_text = all_text[:20000]
    user_prompt = user_prompt.replace('[DATA]', all_text)
    f.close()


def call_model(text='', history=''):
    messages = [{'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt.replace('[TEXT]', text)}]

    responses = Generation.call(
        'qwen-plus',
        messages=messages,
        result_format='message',  # set the result to be "message" format.
        stream=True,
        incremental_output=True  # get streaming output incrementally
    )
    full_content = ''  # with incrementally we need to merge output.
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            content = response.output.choices[0]['message']['content']
            full_content += content
            print(content, end='')
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
    if len(full_content) == 0:
        full_content = 'ERROR'
    return full_content



