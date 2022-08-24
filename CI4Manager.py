import os.path
import datetime
from tkinter import *
from tkinter.messagebox import *
from widget import *
from logger import *

#define
ORDER_LIMIT = 99
Day1 = 26
Day2 = 27
RENDERING_LIMIT = 12
PASS = "variable"

#predefine
PRICE = 200
ORDER_STOP_H = 15
ORDER_STOP_M = 20
PER = 12

#system
SlipNo = 1
Proceeds = 0
ProceAmounts = 0
RefNo = 1

#variable
ORDER_STOP = False
BUCKUP_STOP = False
Orders = [[0]*2]*(ORDER_LIMIT+1)
isDecide = False
NowOrder = 0
TotalAmount = 0
SetNo = 1
Order = 0
Wait = 0

#for reference
CalledList = []
CallPos = 0
Rest = False
delay = 500
colors = ('#000099', '#2222ff')
FLASH = False
ListNum = 0

#file
Data = open('System.log', 'a')
Data.write('Starting up on ')
datetimeStamp(Data)

Date = date.today()
DateStr.set(str(Date.year)+'年'+str(Date.month)+'月'+str(Date.day)+'日')

Day = datetime.today().day
if(Day == Day1):
	Log = open('DAY1.log', 'a')

	timeStamp(Data)
	Data.write('Day1.log opened\n')
elif(Day == Day2):
	Log = open('DAY2.log', 'a')

	timeStamp(Data)
	Data.write('Day2.log opened.\n')
else:
	Log = open('DEBUG.log', 'a')
	timeStamp(Data)
	Data.write('DEBUG.log opened.\n')

Log.write('Starting up on ')
datetimeStamp(Log)

if(os.path.exists('State.now')):
	timeStamp(Data)
	Data.write('Detected State.now file.\n')

	ans = askquestion('復元処理', '復元を実行しますか？')
	if(ans=='yes'):
		State = open('State.now', 'r')
		buff = State.readline()
		args = buff.split(',')
		SlipNo = int(args[0])
		Proceeds = int(args[1])
		ProceAmounts = int(args[2])
		RefNo = int(args[3])
		SetNo = RefNo
		
		NoStr = '整理番号：'+str(RefNo)
		NoLabel.set(NoStr)

		State.close()

def decideKey(event):
	decide()

def decide():
	global Box_amount, Order, SetNo, RefNo, TotalAmount, isDecide, FLASH

	timeStamp(Data)
	Data.write('<decied> button pushed.\n')

	if(Box_order.get().isdecimal()):
		if(Box_no.get().isdecimal()):
			SetNo = int(Box_no.get())
			if(SetNo>ORDER_LIMIT or SetNo<1):
				showinfo('整理番号エラー', '無効な整理番号です。\n1～99 の範囲で設定してください。')
				return

			if(RefNo!=SetNo):
				ask = askquestion('整理番号の変更', '整理番号が変更されています。\n現在：'+str(RefNo)+'\n変更しますか？')
				if(ask=='yes'):
					checkNo(True)
					RefNum.set('=> '+str(SetNo))
		else:
			if(checkNo(True)):
				RefNum.set('変更なし')
			else:
				RefNum.set('=> '+str(SetNo))


	if(Box_order.get().isdecimal() and int(Box_order.get())>0):
		isDecide = True
		payBtn.focus_set()
		Order = int(Box_order.get())
		TotalAmount = Order*PRICE

		Box_no.lower()
		Box_order.lower()
		OrderNum.set(Order)
		AmountNum.set(TotalAmount)
		Label_ref.lift()
		Label_order.lift()
		Label_ta.lift()
	else:
		return

	if(not FLASH):
		FLASH = True
		flash(payBtn, 0)

def checkNo(arg):
	global RefNo, SetNo

	if(arg):
		if(Orders[SetNo][1]!=0):
			showinfo('番号重複', 'すでに使われている番号です。\n空き番号に変更します')
			SetNo = 1
			while(True):
				if(Orders[SetNo][1]==0):
					return False
				else:
					SetNo += 1
					if(SetNo==ORDER_LIMIT+1):
						showwarn('受付不可', '個数管理エラー\n')
						RefNum.set('エラー')
						RESTRICTION(True)
						break
		else:
			return True
	else:
		if(Orders[SetNo][1]!=0):
			SetNo = 1
			while(True):
				if(Orders[SetNo][0]==0):
					return False
				else:
					SetNo += 1
					if(SetNo==ORDER_LIMIT+1):
						RESTRICTION(True)
						break
		else:
			return True

def payed():
	global SlipNo, RefNo, NowOrder, NoStr, Wait, Rest, FLASH, ListNum

	timeStamp(Data)
	Data.write('<payed> button pushed.\n')

	if(TotalAmount==0):
		return
	else:
		RefNo = SetNo
		if(entOrder()):
			NowOrder += 1
			StateNum.set(NowOrder)
			ListNum += 1
			if(NowOrder==ORDER_LIMIT):
				Rest = True
				RESTRICTION(True)

			x = '{0:0>2d}'.format(RefNo)
			List.insert(END, '整理番号：'+str(x)+'     注文数：'+str(Order))

			RefNo += 1
			if(RefNo==100):
				RefNo = 1

			checkNo(False)
			
			SlipNo += 1

			NoStr = '整理番号：'+str(RefNo)
			NoLabel.set(NoStr)
			Wait += Order
			Stay.set(Wait)
			clear()
			FLASH = False
		else:
			return

def entOrder():
	global Log, RefNo, Orders, Order, Proceeds, ProceAmounts

	timeStamp(Data)
	Data.write('<entOrder> button pushed.\n')

	if(Orders[RefNo][0]==0):
		Orders[RefNo] = [RefNo, Order]

		Proceeds += Orders[RefNo][1]*PRICE
		ProceAmounts += Orders[RefNo][1]

		timeStamp(Log)
		Log.write('Slip:'+str(SlipNo)+', No.'+str(RefNo)+', Amount:'+str(Order)+
				  ', Price:'+str(Orders[RefNo][1]*PRICE)+'\n')

		buff = timeStamp(None)
		AllOrderList.insert(END, buff+'伝票番号:'+str(SlipNo)+', 整理番号:'+str(RefNo)+
							', 個数:'+str(Order)+', 値段:'+str(Orders[RefNo][1]*PRICE)+'\n')

		return True
	else:
		showinfo('エラー', 'decide, entOrder')
		return False

def endOrder():
	global Wait, Proceeds, ProceAmounts, ListNum

	timeStamp(Data)
	Data.write('<endOrder> button pushed.\n')

	sel = []

	if(len(Call.curselection())==0):
		if(len(List.curselection())==0):
			return
		else:
			for index in List.curselection():
				sel.append(index)

			if(len(sel)==1):
				buff = List.get(sel[0])
				No = int(buff[5:7])

				Wait -= Orders[No][1]
				Stay.set(Wait)
				ListNum -= 1

				remOrder(No)
				List.delete(sel[0])
			else:
				for i in reversed(sel):
					buff = List.get(i)
					No = int(buff[5:7])

					Wait -= Orders[No][1]
					Stay.set(Wait)
					ListNum -= 1

					remOrder(No)
					List.delete(i)
	else:
		for index in Call.curselection():
			No = CalledList[index]

			remOrder(No)
			resetCall(index)
			Call.delete(index)

def callOrder():
	global List, Call, ListNum

	timeStamp(Data)
	Data.write('<callOrder> button pushed.\n')

	selListno = []
	callLen = len(List.curselection())

	if(CallPos==RENDERING_LIMIT):
		showinfo('表示限界', '呼び出し画面側に表示領域がありません。')
		return
	if(callLen==0):
		return
	if(CallPos+callLen>RENDERING_LIMIT):
		showinfo('表示限界', '呼び出し画面側に表示領域がありません。\n\n残り呼び出し可能数：'+str(RENDERING_LIMIT-CallPos))
		return

	for index in List.curselection():
		selListno.append(index)
		buff = List.get(index)
		Call.insert(END, buff)
		setCall(int(buff[5:7]))
		ListNum -= 1

	if(len(selListno)==1):
		List.delete(selListno)
	else:
		for i in reversed(selListno):
			List.delete(i)

def setCall(x):
	global CalledList, CallPos, InCall, InCallStr, Wait, ListNum

	CalledList.append(x)

	Wait -= Orders[x][1]
	Stay.set(Wait)

	x = '{0:0>2d}'.format(x)
	InCallStr[CallPos].set(str(x))
	InCall[CallPos].lift()
	CallPos += 1

def decallOrder():
	global List, Call, ListNum

	timeStamp(Data)
	Data.write('<decallOrder> button pushed.\n')

	if(len(Call.curselection())==0):
		return
	for index in Call.curselection():
		List.insert(END, Call.get(index))
		resetCall(index)
		Call.delete(index)
		ListNum += 1

def resetCall(x):
	global CalledList, CallPos, InCallStr, Wait, ListNum

	Wait += Orders[CalledList[x]][1]
	Stay.set(Wait)

	if(CallPos==1):
		InCall[x].lower()
	else:
		for i in range(CallPos-x-1):
			InCallStr[x+i].set(InCallStr[x+1+i].get())
		InCall[CallPos-1].lower()
	del CalledList[x]
	CallPos -= 1

def remOrder(no):
	global Orders, NowOrder

	Orders[no] = [0, 0]
	NowOrder -= 1
	StateNum.set(NowOrder)

	if(Rest):
		RESTRICTION(False)

def revOrder():
	global Proceeds, ProceAmounts

	timeStamp(Data)
	Data.write('<rev> button pushed.\n')

	ans = askquestion('返品確認', '返品処理しますか？')
	if(ans=='no'):
		timeStamp(Data)
		Data.write('revOrder cancelled.\n')
		
		return

	if(len(AllOrderList.curselection())==0):
		return
	else:
		for index in AllOrderList.curselection():
			revbuff = AllOrderList.get(index)
			revstrbuff = revbuff.split()

			revSNbuff = revstrbuff[2].split(':')
			revSN = int(revSNbuff[1])

			revRNbuff = revstrbuff[3].split(':')
			revRN = int(revRNbuff[1])

			revAbuff = revstrbuff[4].split(':')
			revA = int(revAbuff[1])

			AllOrderList.delete(index)

			Proceeds -= revA*PRICE
			ProceAmounts -= revA

			showinfo('返品完了', '注文一覧に残っている場合は完了してください。')

			timeStamp(Log)
			Log.write('Slip:'+str(revSN)+', No.'+str(revRN)+', Amount:-'+str(revA)+'\n')
			timeStamp(Data)
			Data.write('revOrder completed\n')

def upList():
	if(len(List.curselection())==0):
		return
	elif(len(List.curselection())>1):
		showinfo('非対応', '並べ替えは1件ずつとなります。')
		return

	index = []
	index = List.curselection()
	if(index[0]==0):
		return
	else:
		buff = List.get(index[0]-1)
		List.delete(index[0]-1)
		List.insert(index[0], buff)

def downList():
	if(len(List.curselection())==0):
		return
	elif(len(List.curselection())>1):
		showinfo('非対応', '並べ替えは1件ずつとなります。')
		return

	index = []
	index = List.curselection()
	buff = List.get(index[0]+1)
	if(len(buff)==0):
		return
	else:
		List.delete(index[0]+1)
		List.insert(index[0], buff)

def paramSet():
	global ORDER_STOP_H, ORDER_STOP_M, PER, PRICE
	check = True

	ans = askquestion('設定変更', 'パラメータを更新しますか？')
	if(ans=='yes'):
		if(Box_prm_endtime.get().isdecimal()):
			buff = Box_prm_endtime.get()
			if(int(buff)>=0 and int(buff)<=2359 and len(buff)>3 and len(buff)<5	):
				ORDER_STOP_H = int(buff[0:2])
				ORDER_STOP_M = int(buff[2:4])
				now_endtimeStr.set(buff[0:2]+':'+buff[2:4])
				RESTRICTION('OPEN')
			else:
				check = False
		else:
			check = False

		if(Box_prm_per.get().isdecimal() and int(Box_prm_per.get())>0):
			PER = int(Box_prm_per.get())
			now_perStr.set(PER)
		else:
			check = False

		if(Box_prm_price.get().isdecimal() and int(Box_prm_price.get())>0):
			PRICE = int(Box_prm_price.get())
			now_priceStr.set(PRICE)
		else:
			check = False

		if(len(Sentence.curselection())==0):
			pass
		else:
			buff = Sentence.get(Sentence.curselection())
			Label_checkStr.set(buff)
			Label_now_sentenceStr.set(buff)
	else:
		return

	Box_prm_endtime.delete(0, END)
	Box_prm_endtime.insert(END, str(ORDER_STOP_H)+str(ORDER_STOP_M))
	Box_prm_per.delete(0, END)
	Box_prm_per.insert(END, PER)
	Box_prm_price.delete(0, END)
	Box_prm_price.insert(END, PRICE)

	#x:1920, y:1080
	l = len(buff)
	sx = 960-(65*l/2)
	Label_check.place(x=sx, y=900)

	setBtn.config(state="disable", bg="#ff2222")
	checkBtn.config(state="active")

	if(check):
		showinfo('パラメータ更新', '設定値を更新しました。')
	else:
		showinfo('パラメータ無効', '無効な設定値です。')

def information():
	timeStamp(Data)
	Data.write('<info> button pushed.\n')

	Box_prm_endtime.focus_set()
	Box_prm_endtime.delete(0, END)
	Box_prm_endtime.insert(END, str(ORDER_STOP_H)+str(ORDER_STOP_M))
	Box_prm_per.delete(0, END)
	Box_prm_per.insert(END, PER)
	Box_prm_price.delete(0, END)
	Box_prm_price.insert(END, PRICE)

	over.lift()
	clocks.lift()

	now_endtimeStr.set(str(ORDER_STOP_H)+':'+str(ORDER_STOP_M))
	now_perStr.set(PER)
	now_priceStr.set(PRICE)

def backToMain():
	timeStamp(Data)
	Data.write('<backToMain> button pushed.\n')

	Box_order.focus_set()

	over.lower()

def clear():
	global SetNo, Order, TotalAmount, isDecide, FLASH

	if(isDecide):
		SetNo = RefNo
		Order = 0
		TotalAmount = 0

		Box_no.delete(0, END)
		Box_no.insert(END, '基本不要')
		Box_order.delete(0, END)

		Box_no.lift()
		Box_order.lift()
		Label_ref.lower()
		Label_order.lower()
		Label_ta.lower()
	else:
		Box_no.delete(0, END)
		Box_order.delete(0, END)
		Box_no.insert(END, '基本不要')

	isDecide = False
	FLASH = False
	payBtn.config(bg=colors[0])
	Box_order.focus_set()

def RESTRICTION(arg):
	global Rest, ORDER_STOP

	timeStamp(Data)

	if(arg==True):
		Data.write('Reached order limit.\n')
		Rest = True
		payBtnStr.set('受付不可')
		payBtn.config(state="disable", bg="#ff2222")

	elif(arg=='STOP'):
		Data.write('Time to stop order.\n')
		Rest = True
		ORDER_STOP = True
		payBtnStr.set('受付不可')
		payBtn.config(state="disable", bg="#ff2222")

	elif(arg=='OPEN'):
		Data.write('Released order stop(by time changed).\n')
		ORDER_STOP = False
		payBtnStr.set('精算')
		payBtn.config(state="active", bg="#000099")

	else:
		Data.write('Released order limit.\n')
		Rest = False
		payBtnStr.set('精算')
		payBtn.config(state="active", bg="#000099")

def FINISH():
	global BUCKUP_STOP

	timeStamp(Data)
	Data.write('<FINISH> button pushed.\n')

	ans = askquestion('確認', 'プログラムを終了しますか？')
	if(ans=='yes'):
		BACKUP_STOP = True

		dateStamp(Data)
		Data.write('tabulation result.\n')
		Data.write('Total amount : '+str(ProceAmounts)+'\n')
		Data.write('Total proceeds : '+str(Proceeds)+'\n')

		Data.write('Shutting down on ')
		datetimeStamp(Data)
		Data.close()

		Log.write('Shutting down on ')
		datetimeStamp(Log)
		Log.close()

		BUCKUP()
		os.remove('State.now')

		root.destroy()

def BUCKUP():
	State = open('State.now', 'w')
	State.write(str(SlipNo)+',')
	State.write(str(Proceeds)+',')
	State.write(str(ProceAmounts)+',')
	State.write(str(RefNo)+'\n')

	State.close()

	if(not BUCKUP_STOP):
		window.after(1000, BUCKUP)

def loop1s():
	Label_SlipStr.set('伝票番号 : '+str(SlipNo))
	Label_Slip.place(x=100, y=70)
	Label_PRICEStr.set('現在売値 : '+str(PRICE))
	Label_PRICE.place(x=100, y=120)
	Label_ProceedsStr.set('現在売上金額 : '+str(Proceeds))
	Label_Proceeds.place(x=100, y=170)
	Label_ProceAmountsStr.set('現在売上数 : '+str(ProceAmounts))
	Label_ProceAmounts.place(x=100, y=220)

	over.after(1000, loop1s)

def realtime():
	wn = int(Wait/PER)*5
	WaitNum.set(int(wn))

	for i in range(RENDERING_LIMIT):
		buff = List.get(i)
		if(len(buff)==0):
			InWaitStr[i].set('0')
			InWait[i].lower()
		else:
			if(i==RENDERING_LIMIT-1):
				n = ListNum-RENDERING_LIMIT+1
				InWaitStr[i].set('...他'+str(n)+'件')
				InWait[i].lift()
			else:
				x = int(buff[5:7])
				x = '{0:0>2d}'.format(x)
				InWaitStr[i].set(str(x))
				InWait[i].lift()

	window2.after(100, realtime)

def clock():
	Time = datetime.now()
	t = '{0:0>2d} {1:0>2d}'.format(Time.hour, Time.minute)
	Clock_disp.set(t)

	if(not ORDER_STOP):
		if(Time.hour>ORDER_STOP_H or (Time.hour==ORDER_STOP_H and Time.minute>ORDER_STOP_M)):
				RESTRICTION('STOP')
				showinfo('営業終了', '営業終了時刻を超過しています。\n受付を終了します。')

		if(Time.hour==ORDER_STOP_H and Time.minute==ORDER_STOP_M):
			RESTRICTION('STOP')
			showinfo('営業終了', '営業終了時刻10分前です。\n受付を終了します。')

	clocks.after(100, clock)

def passCheck():
	p = Box_pass.get()
	if(p==PASS):
		setBtn.config(state="active", bg="#2222ff")
		Box_pass.delete(0, END)
		checkBtn.config(state="disable")
	else:
		Box_pass.delete(0, END)

def flash(obj, index):
	if(FLASH):
		obj.config(bg=colors[index])
		window.after(delay, flash, obj, 1-index)

#widget using variable
decideBtn = Button(window, text='確定', command=decide, bg="#000099", fg="#ffffff", font=("", 20))
decideBtn.place(x=250, y=190, width=230, height=50)

clearBtn = Button(window, text='クリア', command=clear, bg="#000099", fg="#ffffff", font=("", 20))
clearBtn.place(x=10, y=190, width=230, height=50)

payBtnStr = StringVar()
payBtnStr.set('精算')
payBtn = Button(window, textvariable=payBtnStr, command=payed, bg="#000099", fg="#ffffff", font=("", 20))
payBtn.place(x=10, y=250, width=470, height=50)

upBtn = Button(window, text='↑', command=upList, bg="#000099", fg="#ffffff", font=("", 20))
upBtn.place(x=967, y=360, width=70, height=50)

downBtn = Button(window, text='↓', command=downList, bg="#000099", fg="#ffffff", font=("", 20))
downBtn.place(x=1047, y=360, width=70, height=50)

callBtn = Button(window, text='=====>\n呼出\n=====>', command=callOrder, bg="#000099", fg="#ffffff", font=("", 20))
callBtn.place(x=967, y=420, width=150, height=100)

endBtn = Button(window, text='===><===\n完了\n===><===', command=endOrder, bg="#000099", fg="#ffffff", font=("", 20))
endBtn.place(x=967, y=530, width=150, height=100)

decallBtn = Button(window, text='<=====\n呼出取消\n<=====', command=decallOrder, bg="#000099", fg="#ffffff", font=("", 20))
decallBtn.place(x=967, y=640, width=150, height=100)

sdBtn = Button(window, text='終了処理', command=FINISH, bg="#ff0000", fg="#ffffff", font=("", 20))
sdBtn.place(x=10, y=740, width=150, height=80)

infoBtn = Button(window, text='インフォメーション', command=information, bg="#000099", fg="#ffffff", font=("", 20))
infoBtn.place(x=180, y=740, width=300, height=80)

revBtn = Button(over, text='返品', command=revOrder, bg="#000099", fg="#ffffff", font=("", 20))
revBtn.place(x=630, y=765, width=200, height=60)

backBtn = Button(over, text='戻る', command=backToMain, bg="#000099", fg="#ffffff", font=("", 20))
backBtn.place(x=10, y=740, width=470, height=80)

setBtn = Button(over, text='適用', command=paramSet, font=("", 25), bg="#ff2222")
setBtn.place(x=1010, y=355, width=480, height=40)
setBtn.config(state="disable")

checkBtn = Button(over, text='認証', command=passCheck, font=("", 25))
checkBtn.place(x=1400, y=403, width=90, height=45)

#bind
Box_order.bind("<KeyPress-Return>", decideKey)

#begin
clock()
realtime()
loop1s()
BUCKUP()
root.mainloop()