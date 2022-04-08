import pyttsx3
import time
import yaml
import os


class talk():

    def __init__(self):
        """ 加载配置文件 """
        yaml_f = open("talkconfig.yaml", encoding="utf-8")
        self.config = yaml.load(yaml_f, Loader=yaml.FullLoader)

    def opencontent(self, name):
        """ 打开文本 """
        try:

            path = self.config["contentpath"] + name
            f = open(path, mode="r", encoding="utf-8")
            try:
                content = f.read()
                return content, len(content)
            finally:
                f.close()
        except Exception as e:
            return e

    def recordpoint(self, content, tmpcontnt_file):
        """ 处理文本-读取上次阅读记录 """
        try:
            path = tmpcontnt_file + "recordpoint.txt"
            f1 = open(path, mode="r", encoding="utf-8")
            tmprecordcontent = f1.read()
            f2 = open(tmprecordcontent, mode="r", encoding="utf-8")
            try:
                tmpcontent = f2.read()[-12:-1:]
                record_index = content.find(tmpcontent)
                if record_index == -1:
                    return False
                else:
                    return content[record_index:], record_index
            finally:
                f2.close()
                f1.close()
        except Exception as e:
            return e

    def talkInit(self):
        """ 初始化 """
        engine = pyttsx3.init()
        # 设置朗读速度
        engine.setProperty('rate', 165)
        # 设置发音大小，范围为0.0-1.0
        engine.setProperty('volume', 1.0)
        return engine

    def talkwith(self, engine, content):
        """ 朗读内容 """
        engine.say(content)
        engine.runAndWait()

    def talkcontent(self, name=None, content=None, engine=None, ):
        """ 朗读字符串内容 使用系统文字转语音 """
        # 初始化
        engine = self.talkInit()

        # 打开文本
        content, content_len = self.opencontent(name)

        # 判断历史记录的文件夹是否存在，不存在创建,定义变量为临时文件路径
        dirs = self.config["tmpcontnt_path"] + name[:-4:] + "\\"
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        global tmpcontnt_file
        tmpcontnt_file = self.config["tmpcontnt_path"] + name[:-4:] + "\\"

        # 如果历史记录存在，则从历史记录开始
        if self.recordpoint(content, tmpcontnt_file):
            content, history_index = self.recordpoint(content, tmpcontnt_file)

        # 打印阅读进度
        print("{0:0.2f}%".format((history_index / content_len) * 100))

        # 记录本次已读部分文件
        tmprecordcontent = tmpcontnt_file + time.strftime("%Y%m%d%H%M%S") + ".txt"
        recordpoint = open(tmpcontnt_file+"recordpoint.txt", mode="w", encoding="utf-8")
        recordpoint.write(tmprecordcontent)
        recordpoint.close()

        f = open(tmprecordcontent, mode="a", encoding='utf-8')
        try:
            # 如果字符串过长 通过句号分隔 循环读取
            if len(content) > 20:
                con_list = content.split('。')
                for item in con_list:
                    f.write(item+"\t")
                    f.flush()
                    self.talkwith(engine, item)
                    time.sleep(0.3)
            else:
                f.write(content + "\t")
                f.flush()
                self.talkwith(engine, content)
                time.sleep(0.3)
        except Exception as e:
            return e
        finally:
            f.close()
            self.talkstop(engine)

    def talkstop(self, engine):
        """ 停止当前讲话并清除命令队列 """
        engine.stop()


if __name__ == '__main__':
    T1 = talk()
    T1.talkcontent(name="神壕从宕机开始.txt")
    # T1.talkcontent(name="吞噬星空之签到成神.txt")
    # T1.talkStop()


