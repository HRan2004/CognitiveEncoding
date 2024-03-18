
result = '''
内容概述：课程开始与引入，学生发现分享，讨论身体运动的生理机制

1. 开场与课程介绍
老师：好，上课了，有什么问题吗？ 请坐。
老师：在我们永中一小，这个学期 开展了“小小模型科学家”的一个活动。我们看到，老师收集了同学们做的很多模型，因为我们第一单元 是潜望镜模型，第二单元的地球内部结构模型，第三单元的日晷模型，那么现在 我们第四单元关于健康生活的这个板块还空缺着，等着我们一起来填补。今天，老师就 邀请我们同学们一起来设计并完成我们的身体运动的模型。在课前， 我们进行了举哑铃的体验活动。

2. 学生发现分享
老师：这是同学们在举哑铃过程中自己的一些 发现和收获。我请这几个同学来说一说你们有什么收获。好，请第一位同学。
学生：（学生说的话，未录制清晰）
老师：哦，你认为骨骼和肌肉参与了我们 的运动，是吗？并且提到了骨骼有支撑的作用。
学生：（学生说的话，未录制清晰）
老师：这位同学好像有一点点不一样的看法。 是关节哦，还有关节也参与了我们的运动。
学生：（学生说的话，未录制清晰）
老师：好，这位同学，老师说你的发现 很有意思。
学生：谢谢。
学生：（学生说的话，未录制清晰）
老师：作为新任和科学的探索，肌肉没有参加？你还提到了肌肉用于发力， 肌肉用于发力，这个关节可以活动，是吗？好，请坐。

3. 讨论运动生理机制
老师：老师做了一个简单的统计，发现同学们对于运动中骨骼、肌肉和关节都有参与的认识 比较到位。但是对于他们在运动过程中分别起到什么样的作用呢，有一些 不统一的意见。到底谁说的是正确的呢，我们等会儿继续来研究。
老师：那么我们再来回顾一下刚才的活动，我们的肌肉 在活动中有没有发生变化，是怎么变的？你来说说看。
学生：（学生说的话，未录制清晰）

总结语句xxxx
'''

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
