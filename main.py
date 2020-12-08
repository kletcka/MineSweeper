import field_gen
from tkinter import *
from tkinter import font
import keyboard
import json

file = {}
with open('settings.json', 'r', encoding='utf-8') as read_file:
    file = dict(json.load(read_file))

all_field = field_gen.gen()
stage = None
bombs_marked = 0
check_list = []
num_bombs = file['bombs']
glx = file['x']
if glx<10:
    glx = 10
gly = file['y']
if gly<10:
    gly = 10
def print_pressed_keys(e):
    global all_field, stage, bombs_marked, check_list, num_bombs, lbl1, lbl2, lbl3, btns, lbls, file, glx, gly
    if e.name == 'space' and e.event_type == 'up':
        all_field = field_gen.gen()
        stage = None
        bombs_marked = 0
        check_list = []
        num_bombs = file['bombs']
        lbl1 = Label(window, text=f'0', font='Bahnschrift 30', fg='#FF4040')
        lbl1.grid(column=6, row=1, columnspan=4)
        lbl1.after(1000, lambda: timer(lbl1))

        lbl2 = Label(window, text=str(num_bombs - bombs_marked), font='Bahnschrift 30', fg='#FF4040')
        lbl2.grid(column=0, row=1, columnspan=4)

        lbl3 = Label(window, text="😐", font='Bahnschrift 30')
        lbl3.grid(column=4, row=1, columnspan=2)


        for i in btns :
            i.destroy()

        
        for i in lbls:
            i.destroy()

        lbls = []
        for i in range(glx):
            for j in range(gly):
                txt = str(all_field[(i, j)]).replace('B', f'💣').replace('0', f' ')
                lbl = Label(window, text=f'{txt}' , font='Bahnschrift 10 bold', fg=colors[all_field[(i, j)]])
                lbl.pos = (i, j)
                lbls.append(lbl)
                lbl.grid(column=i, row=j+2)
        btns = []
        for i in range(glx):
            for j in range(gly):
                btn = Button(window, text=f'          \n')
                btn.pos = (i, j)
                btn.en = True
                btns.append(btn)
                btn.grid(column=i, row=j+2)

def green():
    global alst,  check_list
    alst = []
    trsc = list(check_list)
    counter = 0
    for j in check_list:
        for i in [(0, -1), (1, 0), (-1, 0), (0, 1)]:
            if j[0]+i[0] in range(glx) and j[1]+i[1] in range(gly) and ((j[0]+i[0], j[1]+i[1])) not in check_list: 
                if all_field[(j[0]+i[0], j[1]+i[1])] == 0:
                    trsc.append((j[0]+i[0], j[1]+i[1]))
                    alst.append((j[0]+i[0], j[1]+i[1]))
                    for n in btns:
                        if n.pos == (j[0]+i[0], j[1]+i[1]):
                            if n["text"] != "🚩":
                                n.grid_forget()
                                n.en = False
                    counter += 1
    check_list = list(trsc)
    if counter >= 1:
        green()


def dest(event):
    global inj, stage, bombs_marked, check_list
    if 'button' in str(vars(event)['widget']) :
        if stage == None:
            stage = True
        if all_field[event.widget.pos] != 'B':
            if event.widget["text"] == "🚩":
                bombs_marked -= 1
                lbl2["text"] = str(num_bombs - bombs_marked)

            if all_field[event.widget.pos] == 0:
                check_list.append(event.widget.pos)
                green()
                check_list = []
            event.widget.grid_forget()
            event.widget.en = False
            inj = 0
            for i in btns:
                if i.en == True:
                    inj+=1
            if inj == num_bombs:
                for i in btns:
                    i.grid_forget()
                stage = False
                lbl3 = Label(window, text="🙂", font='Bahnschrift 30')
                lbl3.grid(column=4, row=1, columnspan=2)

        else:
            for i in btns:
                i.grid_forget()
            stage = False
            lbl3 = Label(window, text="🙁", font='Bahnschrift 30')
            lbl3.grid(column=4, row=1, columnspan=2)
def change(event):
    global bombs_marked, stage
    if 'button' in str(vars(event)['widget']) :
        if stage == None:
            stage = True
        if  event.widget["text"] == "🚩":
            event.widget["text"] = '          \n'
            bombs_marked -= 1

        else:
            event.widget["text"] = "🚩"
            bombs_marked += 1
        lbl2["text"] = str(num_bombs - bombs_marked)

def timer(lbl):
    global stage
    
    try:
        if stage == True and int(lbl["text"])<=999:
            lbl["text"] = str(int(lbl["text"])+1)
        lbl.after(1000, lambda: timer(lbl))
    except Exception:
        pass


window = Tk()
window.title("Сапёр")
window.bind('<Button-1>', dest)
window.bind('<Button-3>', change)
lbl1 = Label(window, text=f'0', font='Bahnschrift 30', fg='#FF4040')
lbl1.grid(column=6, row=1, columnspan=4)
lbl1.after(1000, lambda: timer(lbl1))
keyboard.hook(print_pressed_keys)


lbl2 = Label(window, text=str(num_bombs - bombs_marked), font='Bahnschrift 30', fg='#FF4040')
lbl2.grid(column=0, row=1, columnspan=4)

lbl3 = Label(window, text="😐", font='Bahnschrift 30')
lbl3.grid(column=4, row=1, columnspan=2)

colors = {
    "B":'#000000',
    0:'#FFFFFF',
    1:'#3B5998',
    2:'#5DA130',
    3:'#E34234',
    4:'#191970',
    5:'#801818',
    6:'#45CEA2',
    7:'#9932CC',
    8:'#000000'
}

for i in range(glx):
    for j in range(gly):
        btn = Label(window, text=f'                  \n\n' , font='Bahnschrift 7', fg='#0F0')
        btn.grid(column=i, row=j+2)
lbls = []
for i in range(glx):
    for j in range(gly):
        txt = str(all_field[(i, j)]).replace('B', f'💣').replace('0', f' ')
        lbl = Label(window, text=f'{txt}' , font='Bahnschrift 10 bold', fg=colors[all_field[(i, j)]])
        lbl.pos = (i, j)
        lbls.append(lbl)
        lbl.grid(column=i, row=j+2)
btns = []
for i in range(glx):
    for j in range(gly):
        btn = Button(window, text=f'          \n')
        btn.pos = (i, j)
        btn.en = True
        btns.append(btn)
        btn.grid(column=i, row=j+2)

window.mainloop()