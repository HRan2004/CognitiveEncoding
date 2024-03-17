from models.gpt4 import call_gpt4

prompt = '''
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
老师：好，上课了，有什么问题吗？请坐。
老师：在我们永中一小，这个学期开展了“小小模型科学家”的一个活动。
老师：我们看到，老师收集了同学们做的很多模型，因为我们第一单元是潜望镜模型，第二单元的地球内部结构模型，第三单元的日晷模型，那么现在我们第四单元关于健康生活的这个板块还空缺着，等着我们一起来填补。
老师：今天，老师就邀请我们同学们一起来设计并完成我们的身体运动的模型。
老师：在课前，我们进行了举哑铃的体验活动。
老师：这是同学们在举哑铃过程中自己的一些发现和收获。
老师：我请这几个同学来说一说你们有什么收获。好，请第一位同学。
学生：(学生说的话1，未录制清晰)
老师：哦，你认为骨骼和肌肉参与了我们的运动，是吗？并且提到了骨骼有支撑的作用。
学生：(学生说的话2，未录制清晰)
老师：这位同学好像有一点点不一样的看法。是关节哦，还有关节也参与了我们的运动。
老师：好，这位同学，老师说你的发现很有意思。谢谢。
老师：好，接下来，作为新任和科学的探索，肌肉没有参加？你还提到了肌肉用于发力，肌肉用于发力，这个关节可以活动，是吗？好，请坐。
老师：老师做了一个简单的统计，发现同学们对于运动中骨骼、肌肉和关节都有参与的认识比较到位。但是对于他们在运动过程中分别起到什么样的作用呢，有一些不统一的意见。到底谁说的是正确的呢，我们等会儿继续来研究。
老师：那么我们再来回顾一下刚才的活动，我们的肌肉在活动中有没有发生变化，是怎么变的？你来说说看。
学生：我在举哑铃的时候，


请你按课堂各环节帮我进行分段，随后我自己会判断类型。
有时候可能所有语句都属于一段，如果类型类似就分做一段就可以。有时候可能只有两三句，这都很正常，放心按照类型分即可。分出多少段都有可能，合理即可。
例如一整个师生问答环节，一整个仅老师讲课环节，一整个学生交流环节，一整个朗读背诵环节，都应该算做一段。
同时例如学生突然发表了一句支持或反对意见，有一句提问等，符合上述某个特别的分类，他也应当单独作为一段。
分段时，请直接输出每一段全部的原文，相当于只是在原文上增加了开头的序号。


严格按照以下格式回答我：
内容概述：（整体概括这段讲了什么）

1.xxxx
xxxx
xxxx

2.xxxx
xxxx
xxxx

......
'''

result = call_gpt4(prompt)