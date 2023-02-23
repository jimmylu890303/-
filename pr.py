from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from solveReCaptcha import solveRecaptcha
from cProfile import label
from inspect import Attribute
from tkinter import *

from matplotlib.pyplot import text
from setuptools import Command
import time
import pandas as pd

def deal(a,b,c,d,e,f):  

    options = Options()
    options.add_argument("--incognito") 
    options.add_argument("headless")
    browser = webdriver.Chrome(options=options)
    browser.get('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query')
    browser.implicitly_wait(3)
    #############################################################################
    userid = a
    start = b
    end = c
    n = d
    Date = e
    Train = f
    #############################################################################
    userid_input = browser.find_element_by_xpath('//*[@id="pid"]') #身分證字號
    start_input = browser.find_element_by_xpath('//*[@id="startStation"]') #起始站
    end_input = browser.find_element_by_xpath('//*[@id="endStation"]') #終點站
    numofticket = browser.find_element_by_xpath('//*[@id="normalQty"]') #訂票張數
    oneway = browser.find_element_by_xpath('//*[@id="queryForm"]/div[1]/div[1]/div[5]/div[2]/label[1]') #去程
    goback = browser.find_element_by_xpath('//*[@id="queryForm"]/div[1]/div[1]/div[5]/div[2]/label[2]') #來回
    date = browser.find_element_by_xpath('//*[@id="rideDate1"]') #日期
    train = browser.find_element_by_xpath('//*[@id="trainNoList1"]') #車次

    userid_input.send_keys(userid)
    start_input.send_keys(start)
    end_input.send_keys(end)
    numofticket.clear()
    numofticket.send_keys(n)
    date.clear()
    date.send_keys(Date)
    train.send_keys(Train)
    #############################################################################
    result = solveRecaptcha(
        "6LdHYnAcAAAAAI26IgbIFgC-gJr-zKcQqP1ineoz",
        "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
    )
    code = result['code']

    WebDriverWait(browser,10).until(
        EC.presence_of_element_located((By.ID,'g-recaptcha-response'))
    )

    browser.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = " + "'"+ code + "'"
    )
    #############################################################################
    btn = browser.find_element_by_xpath('//*[@id="queryForm"]/div[4]/input[2]')
    btn.click()
    #############################################################################
    browser.implicitly_wait(3)

    sreach_window=browser.current_window_handle

    cartlist_id = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/div/div/span')
    warn = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[1]/p[1]/strong')
    if warn.text == '訂票成功！':
        tdate = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/span[1]')
        tstarttime = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/span[2]')
        tfrom = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/span[3]')
        tendtime = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/span[5]')
        tto = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/span[6]')
        money = browser.find_element_by_xpath('/html/body/div[1]/form/div[2]/div[2]/table[1]/tbody/tr[2]/td[4]')
        
        return cartlist_id.text,tdate.text,tstarttime.text,tfrom.text,tendtime.text,tto.text,money.text

    else:
        return 0

def start():
    #將獲取輸入內容，並呼叫deal執行訂票
    result = deal(user_entry.get(),
        startstaion_entry.get(),
        endstaion_entry.get(),
        numoftic_entry.get(),
        date_entry.get(),
        train_entry.get())
    if len(result)!=1:
        tic_info_num.config(text=result[0])
        date_info_num.config(text=result[1])
        start_info_num.config(text=result[2]+" "+result[3])
        end_info_num.config(text=result[4]+" "+result[5])
        num_info_num.config(text=numoftic_entry.get())
        money_info_num.config(text=result[6])
        print(result)
    else:
        tic_info_num.config(text='訂票失敗!')

#GUI 介面
############################################################################
win = Tk()

#標題
win.title("TSA ticket")

#大小
win.geometry("800x400")
win.config(bg="skyblue")
win.resizable(0,0)
 
user = Label(text="身份證")
user.grid(row =0,column = 0,sticky='we',ipadx=30)
user_entry =Entry()
user_entry.grid(row =0,column = 1,sticky='ns')

startsation = Label(text="起點站")
startsation .grid(row =1,column = 0,sticky='we')
startstaion_entry =Entry()
startstaion_entry.grid(row =1,column = 1,sticky='ns')

endsation = Label(text="終點站")
endsation .grid(row =2,column = 0,sticky='we')
endstaion_entry =Entry()
endstaion_entry.grid(row =2,column = 1,sticky='ns')

numoftic = Label(text="訂票張數")
numoftic .grid(row =3,column = 0,sticky='we')
numoftic_entry =Entry()
numoftic_entry.grid(row =3,column = 1,sticky='ns')

date = Label(text="日期")
date .grid(row =4,column = 0,sticky='we')
date_entry =Entry()
date_entry.grid(row =4,column = 1,sticky='ns')


train = Label(text="車次")
train .grid(row =5,column = 0,sticky='we')
train_entry =Entry()
train_entry.grid(row =5,column = 1,sticky='ns')

ticket_btn = Button(text="訂票")
ticket_btn.grid(row=0,column=2,rowspan=3,columnspan=3,sticky='ns',ipadx=20)
ticket_btn.config(command=start) #按下按鈕即開始執行訂票功能
#空白組件
space = Label(text="",bg='skyblue')
space.grid(row=6,column=0,sticky='we')
space = Label(text="",bg='skyblue')
space.grid(row=6,column=1,sticky='ns')

space = Label(text="",bg='skyblue')
space.grid(row=7,column=0,sticky='we')
space = Label(text="",bg='skyblue')
space.grid(row=7,column=1,sticky='ns')

tic_info = Label(text="訂票代碼")
tic_info.grid(row=8,column=0,sticky='we')
tic_info_num = Label(text="123456")
tic_info_num.grid(row=8,column=1,sticky='we')

date_info = Label(text="乘車日期")
date_info.grid(row=9,column=0,sticky='we')
date_info_num = Label(text="2022/05/27")
date_info_num.grid(row=9,column=1,sticky='we')

start_info = Label(text="起點站")
start_info.grid(row=10,column=0,sticky='we')
start_info_num = Label(text="2022/05/27")
start_info_num.grid(row=10,column=1,sticky='we')

end_info = Label(text="終點站")
end_info.grid(row=11,column=0,sticky='we')
end_info_num = Label(text="2022/05/27")
end_info_num.grid(row=11,column=1,sticky='we')

num_info = Label(text="票數")
num_info.grid(row=12,column=0,sticky='we')
num_info_num = Label(text="2022/05/27")
num_info_num.grid(row=12,column=1,sticky='we')

money_info = Label(text="總金額")
money_info.grid(row=13,column=0,sticky='we')
money_info_num = Label(text="2022/05/27")
money_info_num.grid(row=13,column=1,sticky='we')


win.mainloop()