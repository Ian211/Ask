import pyttsx3.drivers
import pyttsx3.drivers.sapi5
import pyttsx3
import pyaudio
import keyboard
import wave
import threading
import datetime
import time
import random
import re


class Recorder():
    def __init__(self, chunk=1024, channels=2, rate=48000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self.recording, ())

    def recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False

    def save(self, filename):
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("saved.")

class Asker():
    def __init__(self):
        self.timeToAnswer=180
        self._count=0
        self._questions=[]
        self._types=[]
        self.round=0
        self.quesNo = 0
        self.quesNum = 0
        self.quesToAsk=''
        self._pat1 = re.compile(r'\d+、+')
        self._pat2 = re.compile(r'拓\d+:+')
        self.engine = pyttsx3.init()
        fileName=["题库/教育教学类.txt","题库/名言警句类.txt","题库/应急应变类.txt","题库/综合分析类.txt","题库/自我认知类.txt","题库/真题整理合集.txt"]
        for file in fileName:
            f=open(file,encoding="utf-8")
            tmp = self.AddQuestion(f)
            self._count += len(tmp)
            self._questions.append(tmp)
        self._types = [n for n in range(0, len(self._questions))]
        """ RATE"""
        config=open("config.txt")
        for line in config:
            if line.startswith("rate:"):
                rate=float(line[len("rate:"):])
                self.engine.setProperty('rate',rate)
            if line.startswith("timeToAnswer:"):
                self.timeToAnswer=float(line[len("timeToAnswer:"):])
        print("总题量：",self._count)
        print("当前语速为：", rate)
    def NewRound(self):
        self._round+=1
        random.shuffle(self._types)
    def NewQues(self):
        self.quesNo += 1
        ques_type = self._types[self.quesNo-1]
        ques_num = random.randint(0, len(self._questions[ques_type]) - 1)
        self.quesToAsk = self._questions[ques_type][ques_num]
    def ask(self):
        print('问题', self.quesNo, ":")
        self.engine.say(self.quesToAsk)
        self.engine.runAndWait()
    def AddQuestion(self,text):
        question = []
        for line in text:
            result1 = re.match(self._pat1,line)
            result2 =re.match(self._pat2,line)
            if result1 != None:
                question.append(line[result1.end():])
            elif result2 != None:
                question.append(line[result2.end():])
            else:
                continue
        return question

if __name__ == "__main__":
    interviewer=Asker()
    while True:
        interviewer.round+=1
        interviewer.quesNo=0
        interviewer.quesNum=0
        interviewer.quesToAsk=''
        menu=input("1.开始新一轮面试\t2.设置语速\t3.退出\n请输入数字选择相应功能：")
        if menu[0]==' ':
            menu=menu[1:]
        if menu=='1':
            rec=Recorder()
            rec.start()
            while interviewer.quesNo<3:
                interviewer.NewQues()
                interviewer.ask()
                menu2 = input("1.开始作答\t2.重复一次\t3.退出\n请输入数字选择相应功能：")
                if menu2[0]==' ':
                    menu2=menu2[1:]
                while menu2 == "2":
                    interviewer.ask()
                    menu2 = input("1.开始作答\t2.重复一次\t3.退出\n请输入数字选择相应功能：")
                if menu2 == '1':
                    print("开始计时，按空格结束回答：")
                    start_time = time.time()
                    while True:
                        used_time=time.time()-start_time
                        m,s=divmod(used_time,60)
                        if keyboard.is_pressed(' '):
                            print()
                            break
                        if used_time<=interviewer.timeToAnswer:
                            print("\r%02d:%02d"%(m,s),end="")
                        else:
                            print("\n时间到")
                            break
                elif menu2 == '3':
                    break
                else:
                    menu2 = input("请输入已有的选项数字：")
            rec.stop()
            t=time.localtime(time.time())
            saveName=("第%d轮.wav"%interviewer.round)
            rec.save(saveName)
            print()
        elif menu == '2':
            while True:
                NewRate = input("请输入语速：")
                if NewRate.isnumeric():
                    break
                else:
                    print("输入格式有误：请输入数字")
            file=open("config.txt",'w')
            file.write("rate:"+NewRate)
            interviewer.engine.setProperty('rate', float(NewRate))
        elif menu == '3':
            break
        else:
            menu = input("请输入已有的选项数字：")