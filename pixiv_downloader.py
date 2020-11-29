import tkinter
from tkinter import Widget
import tkinter.ttk as ttk
import requests
import json
import os

try:
    os.makedirs("pixiv_downloads")
except Exception as e:
    pass

gui=tkinter.Tk()
gui.title("Pixiv downloader")
gui.geometry("590x150")
gui.resizable(False, False)

def download():
    try:
        global p_num
        p_num.set(0)
        progressbar.update()
        num=0
        num2=0
        if url.get()=="":
            txt.config(text="url이나 아이디를 입력해주세요!")
            return
        if name.get()=="":
            txt.config(text="피일 이름을 제대로 입력해주세요!")
            return
        try:
            urls=url.get().split("/")
        except Exception as e:
            urls=[url.get()]
        txt.config(text="다운로드중...")
        try:
            os.mkdir("pixiv_downloads\\"+name.get())
        except Exception as e:
            txt.config(text="파일명이 이미 있습니다.")
            return
        urls.reverse()
        try:
            urls=urls[0].split("?")[0]
        except Exception as e:
            urls=urls[0]
        urls=json.loads(requests.get("https://apis.hunhee.tk/api1/pixiv/illust.json?id="+urls+"&beautify=true", verify=False).text)["illust"]["image_urls"]
        for i in urls:
            photo=open("pixiv_downloads\\"+name.get()+"\\"+name.get()+"_"+str(num)+".jpg", "wb")
            photo.write(requests.get(i["original"], verify=False, headers={"Referer":"https://www.pixiv.net/"}).content)
            photo.close()
            num=num+1
            num2=num2+100/len(urls)
            p_num.set(num2)
            progressbar.update()
        txt.config(text=os.getcwd()+"\\pixiv_downloads\\"+name.get()+"풀더에 다운로드 완료!")
    except Exception as e:
        txt.config(text="다운로드 실패...")
        print(e)

def cleaner():
    url.delete(0,len(url.get()))
    name.delete(0,len(name.get()))

def openfolder():
    os.startfile(os.path.realpath(os.getcwd()+"\\pixiv_downloads"))

txt=tkinter.Label(gui, text="다운로드 버튼을 눌러주세요!")

url=tkinter.Entry(gui, width=100)
urtext=tkinter.Label(gui, text="url or id")
name=tkinter.Entry(gui, width=100)
natext=tkinter.Label(gui, text="name")

btn1=tkinter.Button(gui, text="다운로드", padx=5, pady=5, command=download)
btn2=tkinter.Button(gui, text="글자삭제", padx=11, pady=5, command=cleaner)
btn3=tkinter.Button(gui, text="다운풀더 열기", padx=0, pady=5, command=openfolder)
p_num=tkinter.DoubleVar()
progressbar=ttk.Progressbar(gui, maximum=100, length=350, variable=p_num)

txt.pack(side="bottom")
urtext.pack(), url.pack(pady=1)
natext.pack(), name.pack(pady=1)
progressbar.pack(side="left"), btn1.pack(side="right"), btn2.pack(side="right"), btn3.pack(side="right")

gui.mainloop()