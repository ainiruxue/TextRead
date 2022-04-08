from talkcontext import talk

T1 = talk()
content = T1.opencontent("F:\个人\相关文档\smalltalk\保护我方组长.txt")
engine = T1.talkInit()
T1.talkContent(engine, content)