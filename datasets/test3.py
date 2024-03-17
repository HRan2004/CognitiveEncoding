from models.gpt4 import call_gpt4

prompt = '''
我将会给你一段初中学校公开课的录音转换后的文本节选，我需要分析课堂每一部分师生在做什么，帮我严格按照下方类型描述，判断这段文本属于哪一类。

类型一共有四大类，十小类。
### 第一大类 被动：
接受: 学生被动接受学习内容，不做其他事情。
1.只是听或看，并不做笔记或回应。 
2.学生根据老师的简单指令，作出相应动作，如翻书等。

### 第二大类 主动：
记忆: 任何学生在记忆知识的行为。
1.学生在发言或讨论中引用先前知识 
2.学生独立进行记忆活动，如接下来几分钟，同学记一下课文/内容等 
3.学生听写或默写 
4.学生记笔记
5.学生集体跟着老师一起记忆当前课程知识点，如老师说上句，集体回答下句 
6.学生参与复习活动，如开小火车/快问快答等，回顾课文、单词、公式等

应用: 学生能够将所学知识应用到实际问题中，举例使用。
1.学生做对需要应用所学知识解决实际问题的练习题 
2.学生正确回答需要应用所学知识解决实际问题的教师提问 
3.学生在发言或讨论中将所学知识应用到实际问题中，可以举出具体的例子
（注意其中的应用是指应用到实际生活中，应用于回答问题并不符合）

### 第三大类 建构：
提问: 学生分解当前学习内容，理解各部分知识点，提出疑问。
1.学生向同学或者老师发出与所学知识相关提问（注意必须是学生向老师的提问，老师的提问或反问都不算）

阐述: 学生将不同的知识元素、技能或观点整合在一起，综合解决问题，提出自己的见解。
1.学生在发言或讨论中出现成段判断性描述，如XXX是正确的/错误的 
2.学生在发言或讨论中出现成段逻辑性描述，如XXX导致XXX，是因为XXXX，例如XXXX等 
3.学生在发言或讨论中出现总结性话语，如我认为XXXX是XXX”等 4.学生进行黑板板书讲解题目。 
（注意 必须是学生在阐述）
（注意 在这3种以外学生的发言一律不符合阐述，可能更倾向于记忆讨论或反对中的一项）

创造: 学生对创新性内容表现出兴趣或探究欲望，尝试不同的方法策略，进行批判性思考，能够做出贡献或产出作品。
1.学生对创新性内容展示出探索欲，如主动举手提出想法。 
2.学生尝试不同的方法策略，学生在发言或讨论全新观点或新的解决方案。 
3.学生产出思维导图、知识树等成果，并包含创新性内容。

### 第四大类 交互：
支持: 学生赞同他人观点。
1.在同学或老师发表观点后，有明确的“我同意ta的观点”、“我赞同”、“我部分赞同”等表示赞同的语句 
2.对同学的观点进行补充

反对: 学生不赞同他人观点。
1.在同学或老师发表观点后，有明确的“我不同意他的观点”、“我不赞同”等表示反对的语句

讨论: 学生之间的讨论互动。
1.老师要求学生之间进行课堂讨论、小组实验等场景下，学生之间的相互讨论
（注意必须是学生之间的讨论，不是师生之间，师生问答更有可能是老师在引导学生记忆知识点）

### 其他：
无内容：没有任何有效内容


以下是文本：
老师：我们看到，老师收集了同学们做的很多模型，因为我们第一单元是潜望镜模型，第二单元的地球内部结构模型，第三单元的日晷模型，那么现在我们第四单元关于健康生活的这个板块还空缺着，等着我们一起来填补。
老师：今天，老师就邀请我们同学们一起来设计并完成我们的身体运动的模型。
老师：在课前，我们进行了举哑铃的体验活动。
 

分类时类型的主体一定是学生，如果是老师在说话，那可以猜测学生可能在听讲，即接受类型。
每一小类中，比如后面都有序号标注好的列出了所有该小类的情况，必须严格符合其中的某一项情况，才可以判断他属于该类型。

第一步，先整体概述这一段内容讲了什么。
第二步，说出最有可能符合上面的哪个一个类型 中的哪一个例子。注意，你要完整带序号的说出他符合其中的哪一项。
第三步，是否还有其他相似的类型可能，同样说出符合哪个例子。如果有，则继续判断最终应该是哪一类，如果没有则直接跳过。
第四步，说出这么分类的理由。
第五步，说出最终结果。



格式举例，请按照下方例子的格式进行回答，包括在何处换行。在需要替换的地方请自行替换文本。

内容概述：这段文本xxxxx

内容概述：xxxx
符合例子：n.xxxx
其他有可能的例子（本行可选）：n.xxx。对比之下xxxx
分类理由：xxxx
最终结果：xxx（例如 建构-创造）
'''

result = call_gpt4(prompt)