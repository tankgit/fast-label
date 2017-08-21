import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgb
from PIL import Image, ImageTk
from matplotlib import pyplot as plt


# TODO:
#   1. Editable label name
#   2.

class MainWindow():

    class DrawedLabel():
        def __init__(self, text):
            self.x1 = -1
            self.y1 = -1
            self.x2 = -1
            self.y2 = -1
            self.text = text

    def __init__(self, main):
        self.main = main

        # framebox
        self.buttonFrame = tk.LabelFrame(
            main,
            width=500,
            height=50
        )
        self.buttonFrame.pack(
            side=tk.TOP,
            fill=tk.X
        )

        self.labelFrame = tk.LabelFrame(
            main,
            width=30
        )
        self.labelFrame.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.imageFrame = tk.LabelFrame(
            main,
            bg='black',
            height=400
        )
        self.imageFrame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=tk.TRUE
        )

        self.statusFrame = tk.LabelFrame(
            main,
            height=30
        )
        self.statusFrame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
        )

        # Buttons
        self.imgBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Open File',
            width=10,
            height=3,
            command=self.openFile
        )
        self.imgBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.infoBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Open Info',
            width=10,
            height=3,
            command=self.openInfo
        )
        self.infoBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.addLbBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Add',
            width=6,
            height=3,
            command=self.addLabel
        )
        self.addLbBtn.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        self.delLbBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Delete',
            width=6,
            height=3,
            command=self.delLabel
        )
        self.delLbBtn.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        # Lables box
        self.textLabel = tk.Text(
            self.labelFrame,
            height=5,
            width=32
        )
        self.textLabel.pack(
            side=tk.TOP,
            pady=2
        )

        self.allLabelFrame = tk.LabelFrame(
            self.labelFrame,
        )
        self.allLabelFrame.pack(
            side=tk.TOP,
        )
        self.labelBox = tk.Listbox(
            self.allLabelFrame,
            width=30,
            height=15
        )
        self.labelBox.pack(
            side=tk.LEFT,
            fill=tk.BOTH
        )
        for i in range(0, 30):
            self.labelBox.insert(tk.END, 'Label ' + str(i))

        self.scroll_1 = tk.Scrollbar(
            self.allLabelFrame,
            orient=tk.VERTICAL
        )
        self.scroll_1.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
        self.labelBox.config(yscrollcommand=self.scroll_1.set)
        self.scroll_1.config(command=self.labelBox.yview)

        self.selectedNum = None
        self.selectedTxt = ''
        self.labelBox.bind('<<ListboxSelect>>', self.selectLabel)

        self.drawBtn = tk.Button(
            self.labelFrame,
            text='Draw a Label',
            command=self.drawLabel
        )
        self.drawBtn.pack(
            side=tk.TOP,
            pady=10
        )

        self.usedLabelFrame = tk.LabelFrame(
            self.labelFrame,
        )
        self.usedLabelFrame.pack(
            side=tk.TOP,
        )

        self.usedLabel = tk.Listbox(
            self.usedLabelFrame,
            width=30,
            height=15
        )
        self.usedLabel.pack(
            side=tk.LEFT,
            fill=tk.BOTH
        )
        self.scroll_2 = tk.Scrollbar(
            self.usedLabelFrame,
            orient=tk.VERTICAL
        )
        self.scroll_2.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
        self.usedLabel.config(yscrollcommand=self.scroll_2.set)
        self.scroll_2.config(command=self.usedLabel.yview)

        self.workLabelNum = None
        self.workLabelTxt = ''
        self.usedLabel.bind('<<ListboxSelect>>', self.selectDraw)

        # image box
        self.draws = []

        self.canvas = tk.Canvas(
            self.imageFrame,
            bg='black',
        )
        self.canvas.pack(
            side=tk.TOP,
            expand=tk.YES,
            fill=tk.BOTH,
            padx=10,
            pady=10
        )
        self.canvas.bind('<Motion>', self.showMouse)
        self.canvas.bind('<Button 1>', self.showPoint1)
        self.canvas.bind('<Button 3>', self.showPoint2)
        self.canvas.bind('<Configure>',self.canvasChange)
        self.c_width=self.canvas.winfo_width()
        self.c_height=self.canvas.winfo_height()
        self.fileName=None
        self.imgtk=None
        # img=np.zeros((640,640,3),np.uint8)
        # img=Image.fromarray(img)
        # imgtk=ImageTk.PhotoImage(image=img)
        # self.container = tk.Label(
        #     self.canvas,
        #     bg='black',
        #     image=imgtk
        # )
        
        # self.container.pack(
        #     side=tk.TOP,
        #     expand=tk.YES,
        #     padx=10,
        #     pady=10
        # )
        # self.container.bind('<Motion>', self.showMouse)
        # self.container.bind('<Button 1>', self.showPoint1)
        # self.container.bind('<Button 3>', self.showPoint2)

        # Status box
        self.mousePosStr = tk.StringVar()
        self.curLabelStr = tk.StringVar()
        self.pointStr1 = tk.StringVar()
        self.pointStr2 = tk.StringVar()

        self.mousePosStr.set('X: NULL Y: NULL')
        self.curLabelStr.set('Current Label: None')
        self.pointStr1.set('Point 1: NULL')
        self.pointStr2.set('Point 2: NULL')

        self.mousePos = tk.Message(
            self.statusFrame,
            textvariable=self.mousePosStr,
            width=150
        )
        self.mousePos.pack(
            side=tk.LEFT
        )
        self.curLabel = tk.Message(
            self.statusFrame,
            textvariable=self.curLabelStr,
            width=200
        )
        self.curLabel.pack(
            side=tk.LEFT,
            padx=20
        )
        self.point1 = tk.Message(
            self.statusFrame,
            textvariable=self.pointStr1,
            width=150
        )
        self.point1.pack(
            side=tk.LEFT,
            padx=10
        )
        self.point2 = tk.Message(
            self.statusFrame,
            textvariable=self.pointStr2,
            width=150
        )
        self.point2.pack(
            side=tk.LEFT,
            padx=10
        )

        main.mainloop()

    def selectLabel(self, e):
        self.selectedNum = self.labelBox.curselection()
        self.selectedTxt = self.labelBox.get(self.selectedNum)

        self.workLabelNum = None
        self.workLabelTxt = ''
        self.reDraw()
        print('Select: ', self.selectedNum[0], self.selectedTxt)

    def selectDraw(self, e=None):
        self.workLabelNum = self.usedLabel.curselection()
        self.workLabelTxt = self.usedLabel.get(self.workLabelNum)

        a = self.draws[self.workLabelNum[0]]

        self.curLabelStr.set(
            'Current Label: ' + str(self.workLabelNum[0]) + '-' + a.text)
        self.pointStr1.set(
            'Point 1: (' + str(a.x1) + ',' + str(a.y1) + ')')
        self.pointStr2.set(
            'Point 2: (' + str(a.x2) + ',' + str(a.y2) + ')')

        self.selectedNum = None
        self.selectedTxt = ''
        self.reDraw()
        print('Working: ', self.workLabelNum[0], self.workLabelTxt)

    ## Button Functions ##
    def openFile(self):
        file = fd.LoadFileDialog(self.main)
        self.fileName = file.go()
        if self.fileName != '':
            print(self.fileName)
            img = cv2.imread(self.fileName)
            b, g, r = cv2.split(img)
            img = cv2.merge((r, g, b))
            img = Image.fromarray(img)
            self.imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(self.c_width/2,self.c_height/2,image=self.imgtk)
        self.main.mainloop()

    def openInfo(self):
        return

    def addLabel(self):
        input = (self.textLabel.get('1.0', tk.END)).split('\n')
        while '' in input:
            input.remove('')
        for label in input:
            self.labelBox.insert(tk.END, label)
        self.textLabel.delete('1.0', tk.END)
        return

    def delLabel(self):
        if self.selectedNum != None:
            if msgb.askyesno('Warning', 'Are you sure to delete label \"' + self.selectedTxt + '\"?'):
                self.labelBox.delete(self.selectedNum)
                self.selectedTxt = ''
                self.selectedNum = None

    def drawLabel(self):
        if self.selectedNum != None:
            self.usedLabel.insert(tk.END, self.selectedTxt)
            self.usedLabel.selection_clear(0, tk.END)
            self.usedLabel.select_set(tk.END)

            self.draws.append(self.DrawedLabel(self.selectedTxt))
            self.selectDraw()

    ## Mouse Event ##
    def showMouse(self, event):
        self.mousePosStr.set('X: ' + str(event.x) + ' Y: ' + str(event.y))

    def showPoint1(self, event):
        if self.workLabelNum:
            self.pointStr1.set(
                'Point 1: (' + str(event.x) + ',' + str(event.y) + ')')
            self.draws[self.workLabelNum[0]].x1 = event.x
            self.draws[self.workLabelNum[0]].y1 = event.y
            self.reDraw()
            print(event.x, event.y)

    def showPoint2(self, event):
        if self.workLabelNum:
            self.pointStr2.set(
                'Point 2: (' + str(event.x) + ',' + str(event.y) + ')')
            self.draws[self.workLabelNum[0]].x2 = event.x
            self.draws[self.workLabelNum[0]].y2 = event.y
            self.reDraw()
            print(event.x, event.y)

    ## Draw Canvas ##
    def canvasChange(self,event):
        self.c_width=self.canvas.winfo_width()
        self.c_height=self.canvas.winfo_height()
        self.reDraw()

    def reDraw(self):
        r = 7
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(self.c_width/2,self.c_height/2,image=self.imgtk)
        if len(self.draws)>0:
            for i in range(len(self.draws)):
                if self.workLabelNum and i == self.workLabelNum[0]:
                    color_in='red'
                    color_out='black'
                else:
                    color_in='grey'
                    color_out='#999'

                x1 = self.draws[i].x1
                y1 = self.draws[i].y1
                x2 = self.draws[i].x2
                y2 = self.draws[i].y2
                if x1>0 and y1>0 and x2>0 and y2>0:
                    self.canvas.create_line(x1,y1,x1,y2,x2,y2,x2,y1,x1,y1,fill=color_in,width=2)
                if x1>=0 and y1>=0:
                    self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill=color_in, outline=color_out, width=3)
                if x2>=0 and y2>=0:
                    self.canvas.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill=color_in, outline=color_out, width=3)


# Main
root = tk.Tk()
MainWindow(root)
root.mainloop()


# while(cap.isOpened()):
#     ret, frame = cap.read()
#     print(ret)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()
