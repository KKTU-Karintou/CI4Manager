from tkinter import *

WIN_SIZE = "1440x810"
WIN_W = 1920
WIN_H = 1080

#main
root = Tk()
root.title("CI4会計マネージャー ver1.4.0")
root.geometry(WIN_SIZE)
window = Frame(root, width=WIN_W, height=WIN_H)
window.place(x=0, y=0)
over = Frame(root, width=WIN_W, height=WIN_H)
over.place(x=0, y=0)
over.lower()
clocks = Frame(root, width=490, height=330)
clocks.place(x=0, y=400)

window2 = Toplevel()
window2.title("")
window2.geometry(WIN_SIZE)

### 画面1 ###
#キャンバス：注文
area1 = Canvas(window, width=480, height=350)
area1.place(x=5, y=5)

#整理番号
NoLabel = StringVar()
NoStr = '整理番号：'+str(1)
NoLabel.set(NoStr)
Label_no = Label(window, textvariable=NoLabel, font=("", 30))
Label_no.place(x=25, y=10, width=230, height=40)
Box_no = Entry(window, font=("", 30))
Box_no.place(x=270, y=10, width=160, height=40)
Box_no.insert(END, "基本不要")
RefNum = StringVar()
RefNum.set('変更なし')
Label_ref = Label(window, textvariable=RefNum, font=("", 30))
Label_ref.place(x=270, y=10, width=160, height=40)
Label_ref.lower()

#フライドポテト
Label1 = Label(window, text='フライドポテト', font=("", 30))
Label1.place(x=25, y=60, width=230, height=40)
Box_order = Entry(window, font=("", 30))
Box_order.place(x=270, y=60, width=160, height=40)
Box_order.focus_set()
OrderNum = IntVar()
OrderNum.set(0)
Label_order = Label(window, textvariable=OrderNum, font=("", 30))
Label_order.place(x=270, y=60, width=160, height=40)
Label_order.lower()

#合計金額
area1.create_line(5, 110, 480, 110)
area1.create_text(260, 145, text="合計金額　　　　　　　　円", font=(", 30"))
AmountNum = IntVar()
AmountNum.set(0)
Label_ta = Label(window, textvariable=AmountNum, font=("", 30))
Label_ta.place(x=270, y=128, width=160, height=45)

#ラベル：注文状態
BStateLabel = Label(window, text="注文件数：", font=("", 25))
BStateLabel.place(x=10, y=305)
StateNum = IntVar()
StateNum.set(0)
StateLabel = Label(window, textvariable=StateNum, font=("", 25))
StateLabel.place(x=165, y=305)

#待ち時間
BWaitLabel = Label(window, text="待ち時間：約      分", font=("", 25))
BWaitLabel.place(x=200, y=305)
WaitNum = IntVar()
WaitNum.set(0)
WaitLabel = Label(window, textvariable=WaitNum, font=("", 25))
WaitLabel.place(x=390, y=305)

#リスト：注文一覧
Label_list = Label(window, text='注文一覧', font=("", 25))
Label_list.place(x=660, y=10)
ListArray = ()
ListStr = StringVar(value=ListArray)
List = Listbox(window, listvariable=ListStr, font=("", 25))
List.place(x=500, y=50, width=440, height=760)
List.configure(selectmode="multiple")

Label_change = Label(window, text='注文並替え用', font=("", 20))
Label_change.place(x=962, y=320, width=160, height=40)

#リスト：呼び出し一覧
Label_call = Label(window, text='呼び出し一覧', font=("", 20))
Label_call.place(x=1250, y=330)
CallArray = ()
CallStr = StringVar(value=CallArray)
Call = Listbox(window, listvariable=CallStr, font=("", 20), bg="#ffff66")
Call.place(x=1140, y=360, width=370, height=445)

#キャンバス：注文個数
area2 = Canvas(window, width=500, height=300)
area2.place(x=950, y=10)
area2.create_text(280, 60, text="発注数", font=(", 80"))
Stay = IntVar()
Stay.set(0)
Label_s = Label(window, textvariable=Stay, font=("", 140), fg="#ff2222")
Label_s.place(x=1050, y=150, width=360, height=150)

#時計
Clock_disp = StringVar()
Clock_disp.set('00 00')
Label_clock = Label(clocks, textvariable=Clock_disp, font=("", 125))
Label_clock.place(x=0, y=50, width=470, height=150)
Label_sep = Label(clocks, text=':', font=("", 150))
Label_sep.place(x=215, y=5)
DateStr = StringVar()
Label_date = Label(clocks, textvariable=DateStr, width=13, height=1, font=("", 50))
Label_date.place(x=15, y=220)

### 画面2 ###
#キャンバス：呼び出し
#x:1535->3055, y:0->800
Label_wait1 = Label(window2, text='お待ち番号　　　', fg="#ffffff", bg="#333333", font=("", 70))
Label_wait1.place(x=30, y=20, width=700)
Label_wait2 = Label(window2, text='お呼出中の番号', fg="#ffffff", bg="#005500", font=("", 70))
Label_wait2.place(x=745, y=20, width=700)
Label_checkStr = StringVar()
Label_checkStr.set('お手元の整理券番号をご参照ください')
Label_check = Label(window2, textvariable=Label_checkStr, font=("", 60))
Label_check.place(x=350, y=900)

InWaitStr = []
InWait = []
InCallStr = []
InCall = []
#inwait
for i in range(12):
	InWaitStr.append(StringVar())
	InWaitStr[i].set(22)
	if(i==11):
		InWait.append(Label(window2, textvariable=InWaitStr[i], font=("", 65)))
	else:
		InWait.append(Label(window2, textvariable=InWaitStr[i], font=("", 100)))

bx = 160
by = 140
for i in range(2):
	for j in range(6):
		InWait[i*6+j].place(x=bx, y=by)
		by += 120
	bx += 275
	by = 140
InWait[11].place(x=450, y=765)

#incall
for i in range(12):
	InCallStr.append(StringVar())
	InCallStr[i].set(22)
	InCall.append(Label(window2, textvariable=InCallStr[i], font=("", 100)))

bx = 810
by = 140
for i in range(2):
	for j in range(6):
		InCall[i*6+j].place(x=bx, y=by)
		by += 120
	bx += 275
	by = 140

area3 = Canvas(window2, width=WIN_W, height=WIN_H)
area3.place(x=0, y=0)

#返品処理
#注文履歴リスト
AllOrderLabel = Label(over, text='注文履歴', font=("", 15))
AllOrderLabel.place(x=690, y=10)
AllOrderArray = ()
AllOrderStr = StringVar(value=AllOrderArray)
AllOrderList = Listbox(over, listvariable=AllOrderStr, font=("", 15), bg="#ffffff", fg="#000000")
AllOrderList.place(x=500, y=35, width=460, height=720)

#パラメータ設定
Label_endtime = Label(over, text='終了時刻(HHMM):', font=("", 25))
Label_endtime.place(x=1010, y=20, width=270, height=40)
Box_prm_endtime = Entry(over, font=("", 25))
Box_prm_endtime.place(x=1290, y=20, width=100, height=40)
now_endtimeStr = StringVar()
Label_now_endtime = Label(over, textvariable=now_endtimeStr, font=("", 25))
Label_now_endtime.place(x=1400, y=20, width=90, height=40)
Label_per = Label(over, text='単位時間調理数:', font=("", 25))
Label_per.place(x=1003, y=70, width=270, height=40)
Box_prm_per = Entry(over, font=("", 25))
Box_prm_per.place(x=1290, y=70, width=100, height=40)
now_perStr = IntVar()
Label_now_per = Label(over, textvariable=now_perStr, font=("", 25))
Label_now_per.place(x=1400, y=70, width=90, height=40)
Label_price = Label(over, text='販売価格:', font=("", 25))
Label_price.place(x=1015, y=120)
Box_prm_price = Entry(over, font=("", 25))
Box_prm_price.place(x=1290, y=120, width=100, height=40)
now_priceStr = IntVar()
now_priceStr.set(0)
Label_now_price = Label(over, textvariable=now_priceStr, font=("", 25))
Label_now_price.place(x=1415, y=120)

Label_now_sentenceStr = StringVar()
Label_now_sentenceStr.set('お手元の整理券番号をご参照ください')
Label_now_sentence = Label(over, textvariable=Label_now_sentenceStr, font=("", 20))
Label_now_sentence.place(x=1010, y=165)
SentenceArray = ()
SentenceStr = StringVar(value=SentenceArray)
Sentence = Listbox(over, listvariable=SentenceStr, font=("", 20), bg="#22ff22")
Sentence.place(x=1010, y=200, width=480, height=145)
Sentence.insert(END, 'お手元の整理券番号をご参照ください')
Sentence.insert(END, '受付終了は午後3時20分となります')
Sentence.insert(END, '本日の受付は終了しました')

Label_pass = Label(over, text='パスワード :', font=("", 25))
Label_pass.place(x=1010, y=410)
Box_pass = Entry(over, font=("", 25))
Box_pass.place(x=1200, y=410, width=180, height=40)

#情報
Cv_info = Canvas(over, width=400, height=300, bg="#22ff22")
Cv_info.place(x=45, y=10)
Label_info = Label(over, text='ステータス(5秒毎に更新)', font=("", 25), bg="#22ff22")
Label_info.place(x=75, y=20)
Label_SlipStr = StringVar()
Label_Slip = Label(over, textvariable=Label_SlipStr, font=("", 25), bg="#22ff22")
Label_PRICEStr = StringVar()
Label_PRICE = Label(over, textvariable=Label_PRICEStr, font=("", 25), bg="#22ff22")
Label_ProceedsStr = StringVar()
Label_Proceeds = Label(over, textvariable=Label_ProceedsStr, font=("", 25), bg="#22ff22")
Label_ProceAmountsStr = StringVar()
Label_ProceAmounts = Label(over, textvariable=Label_ProceAmountsStr, font=("", 25), bg="#22ff22")

#lift
Label_wait1.lift()
Label_wait2.lift()
Label_check.lift()