import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgb
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
<<<<<<< HEAD
import os
import json
import imageio

=======


# TODO:
#   1. Editable label name
#   2.
# save test in company commit
>>>>>>> 3940eb3eebd22043f3fbeefdaf3f9f0e03b6713f
class MainWindow():

    class DrawedLabel():
        def __init__(self, text):
            self.x1 = -1
            self.y1 = -1
            self.x2 = -1
            self.y2 = -1
            self.text = text
            self.cx1 = -1
            self.cy1 = -1
            self.cx2 = -1
            self.cy2 = -1

    def __init__(self, main):
        # Variables
        self.main = main
        self.supportImg = ['jpg', 'png', 'bmp']
        self.supportVdo = ['avi', 'mp4', 'wmv']

        self.files = []
        self.workLabelTxt = ''

        self.draws = []
        self.img = None
        self.imgtk= None
        self.vdo = None
        self.curImg = None
        self.fileType= None

        self.totalNumStr = tk.StringVar()
        self.mousePosStr = tk.StringVar()
        self.curLabelStr = tk.StringVar()
        self.pointStr1 = tk.StringVar()
        self.pointStr2 = tk.StringVar()

        # Initialize Frames
        self.initFrames()
        self.initButtonFrame()
        self.initLabelFrame()
        self.initImageFrame()
        self.initStatusFrame()

        main.mainloop()

    # Window Init
    def initFrames(self):
        self.buttonFrame = tk.LabelFrame(
            self.main,
            width=500,
            height=50
        )
        self.buttonFrame.pack(
            side=tk.TOP,
            fill=tk.X
        )

        self.labelFrame = tk.LabelFrame(
            self.main,
            width=30
        )
        self.labelFrame.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.imageFrame = tk.LabelFrame(
            self.main,
            bg='black',
            height=400
        )
        self.imageFrame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=tk.TRUE
        )

        self.statusFrame = tk.LabelFrame(
            self.labelFrame,
            height=30
        )
        self.statusFrame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
        )

    def initButtonFrame(self):
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

        self.folderBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Open Folder',
            width=10,
            height=3,
            command=self.openFolder
        )
        self.folderBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.saveBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Save Label',
            width=10,
            height=3,
            command=self.saveLabel
        )
        self.saveBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        self.preBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='<--',
            width=3,
            height=3,
            command=self.preImg
        )
        self.preBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        self.nxtBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='-->',
            width=3,
            height=3,
            command=self.nxtImg
        )
        self.nxtBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        self.jumpNum = tk.Entry(
            self.buttonFrame,
            width=10,
        )
        self.jumpNum.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        self.jumpGo = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Go',
            width=3,
            height=3,
            command=self.jumpFrame
        )
        self.jumpGo.pack(
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

    def initLabelFrame(self):
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
            height=10
        )
        self.labelBox.pack(
            side=tk.LEFT,
            fill=tk.BOTH
        )
        for i in range(0, 3):
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

        self.drawBtnFrame = tk.LabelFrame(
            self.labelFrame
        )
        self.drawBtnFrame.pack(
            side=tk.TOP,
            fill=tk.X
        )
        self.drawBtn = tk.Button(
            self.drawBtnFrame,
            text='Draw',
            command=self.drawLabel
        )
        self.drawBtn.pack(
            side=tk.LEFT,
            padx=15,
            pady=10
        )
        self.editBtn=tk.Button(
            self.drawBtnFrame,
            text='Edit',
            command=self.editLabel
        )
        self.delDrawBtn = tk.Button(
            self.drawBtnFrame,
            text='Delete',
            command=self.delDraw
        )
        self.delDrawBtn.pack(
            side=tk.LEFT,
            padx=15,
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
            height=10
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

    def initImageFrame(self):
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
        self.canvas.bind('<Configure>', self.canvasChange)
        self.c_width = self.canvas.winfo_width()
        self.c_height = self.canvas.winfo_height()

    def initStatusFrame(self):
        self.totalNumStr.set('Total: 0')
        self.mousePosStr.set('X: NULL Y: NULL')
        self.curLabelStr.set('Current Label: None')
        self.pointStr1.set('Point 1: NULL')
        self.pointStr2.set('Point 2: NULL')

        self.totalNum= tk.Message(
            self.statusFrame,
            textvariable=self.totalNumStr,
            width=150            
        )
        self.totalNum.pack(
            side=tk.TOP
        )
        self.mousePos = tk.Message(
            self.statusFrame,
            textvariable=self.mousePosStr,
            width=150
        )
        self.mousePos.pack(
            side=tk.TOP
        )
        self.curLabel = tk.Message(
            self.statusFrame,
            textvariable=self.curLabelStr,
            width=200
        )
        self.curLabel.pack(
            side=tk.TOP,
            padx=20
        )
        self.point1 = tk.Message(
            self.statusFrame,
            textvariable=self.pointStr1,
            width=150
        )
        self.point1.pack(
            side=tk.TOP,
            padx=10
        )
        self.point2 = tk.Message(
            self.statusFrame,
            textvariable=self.pointStr2,
            width=150
        )
        self.point2.pack(
            side=tk.TOP,
            padx=10
        )

    # Selection Listener
    def selectLabel(self, e):
        self.selectedNum = self.labelBox.curselection()
        self.selectedTxt = self.labelBox.get(self.selectedNum)

        self.workLabelNum = None
        self.workLabelTxt = ''
        self.curLabelStr.set('Current Label: None')
        self.pointStr1.set('Point 1: NULL')
        self.pointStr2.set('Point 2: NULL')

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

    # Button Event
    def openFile(self):
        self.resetAll()
        self.files = []
        self.filePath = fd.askopenfilename()
        if self.filePath != '':
            typeStr = self.filePath[-3:].lower()
            if typeStr in self.supportImg:
                self.curImg=0
                self.openImg(self.filePath)
                self.totalNumStr.set('Total: 1')
            elif typeStr in self.supportVdo:
                self.openVdo(self.filePath)
                self.totalNumStr.set('Total: '+str(self.vdo.get_length()))
            else:
                print('File type not support.')

    def openFolder(self):
        self.fileType=0
        folder = fd.askdirectory()
        for img in os.listdir(folder):
            if img[-3:] in self.supportImg:
                self.files.append(os.path.join(folder, img))
        self.totalNumStr.set('Total: '+str(len(self.files)))
        self.curImg = 0
        self.openImg(self.files[self.curImg])

    def resetAll(self):
        self.draws = []
        self.usedLabel.delete(0, tk.END)
        self.workLabelNum = None
        self.workLabelTxt = ''
        self.curLabelStr.set('Current Label: None')
        self.pointStr1.set('Point 1: NULL')
        self.pointStr2.set('Point 2: NULL')
        self.jumpNum.delete(0, tk.END)
        self.jumpNum.insert(0, str(self.curImg))

    def openImg(self, path):
        self.resetAll()
        self.filePath = path
        self.fileType = 0
        print(self.filePath)
        img = cv2.imread(self.filePath)
        b, g, r = cv2.split(img)
        img = cv2.merge((r, g, b))
        self.ratio = img.shape[1] / img.shape[0]
        self.i_width = img.shape[1]
        self.i_height = img.shape[0]
        self.img = Image.fromarray(img)
        self.resizeImage()
        self.canvas.create_image(
            self.c_width / 2, self.c_height / 2, image=self.imgtk)
        self.loadLabel()

    def openVdo(self, path):
        self.resetAll()
        self.filePath = path
        self.fileType = 1
        print(self.filePath)
        self.vdo = imageio.get_reader(self.filePath,  'ffmpeg')
        self.curImg = 0
        self.openFrame()

    def openFrame(self):
        self.resetAll()
        img = self.vdo.get_data(self.curImg)
        self.ratio = img.shape[1] / img.shape[0]
        self.i_width = img.shape[1]
        self.i_height = img.shape[0]
        self.img = Image.fromarray(img)
        self.resizeImage()
        self.canvas.create_image(
            self.c_width / 2, self.c_height / 2, image=self.imgtk)
        self.loadLabel()

    def loadLabel(self):
        if self.fileType == 0:
            path = self.filePath + '.json'
        else:
            path = os.path.join(self.filePath + '-labels',
                                str(self.curImg) + '.json')
        if os.path.exists(path):
            labelFile = open(path, 'r')
            try:
                data = json.load(labelFile)
            except Exception as error:
                print('Invalid JSON file. Ignore it.')
                return

            for label in data:
                tem = self.DrawedLabel(label)
                tem.x1 = data[label][0][0]
                tem.y1 = data[label][0][1]
                tem.x2 = data[label][1][0]
                tem.y2 = data[label][1][1]
                tem.cx1, tem.cy1 = self.restoreCoord(tem.x1, tem.y1)
                tem.cx2, tem.cy2 = self.restoreCoord(tem.x2, tem.y2)
                self.usedLabel.insert(tk.END, tem.text)
                self.usedLabel.selection_clear(0, tk.END)
                self.draws.append(tem)
        self.reDraw()

    def preImg(self):
        if self.fileType == 0:
            if len(self.files) > 0:
                if self.curImg != 0:
                    self.saveLabel()
                    self.curImg -= 1
                    self.openImg(self.files[self.curImg])
        else:
            if self.vdo != None:
                if self.curImg != 0:
                    self.saveLabel()
                    self.curImg -= 1
                    self.openFrame()

    def nxtImg(self):
        if self.fileType == 0:
            if len(self.files) > 0:
                if self.curImg < len(self.files) - 1:
                    self.saveLabel()
                    self.curImg += 1
                    self.openImg(self.files[self.curImg])
        else:
            if self.vdo != None:
                if self.curImg != self.vdo.get_length() - 1:
                    self.saveLabel()
                    self.curImg += 1
                    self.openFrame()

    def jumpFrame(self):
        if self.fileType!=None:
            if self.jumpNum.get()!='':
                self.curImg = int(self.jumpNum.get())
                self.saveLabel()
                if self.fileType==0:
                    self.openImg(self.filePath)
                else:
                    self.openFrame()

    def saveLabel(self):
        if self.filePath != None:
            savePath = ''
            if self.fileType == 0:
                savePath = self.filePath + '.json'
            else:
                path = self.filePath + '-labels'
                if not os.path.exists(path):
                    os.mkdir(path)
                savePath = os.path.join(path, str(self.curImg) + '.json')
            if len(self.draws) > 0:

                data = {}

                for box in self.draws:
                    if box.x1 >= 0 or box.x2 >= 0:
                        data[box.text] = []
                        data[box.text].append([box.x1, box.y1])
                        data[box.text].append([box.x2, box.y2])
                outFile = open(savePath, 'w')
                json.dump(data, outFile, indent=4)
                outFile.close()
                print('Label file saved:', savePath)
            elif os.path.exists(savePath):
                os.remove(savePath)

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

    def editLabel(self):
        return

    def delDraw(self):
        if self.workLabelNum != None:
            if msgb.askyesno('Warning', 'Are you sure to delete drawn label \"' + self.workLabelTxt + '\"?'):
                del self.draws[self.workLabelNum[0]]
                self.usedLabel.delete(self.workLabelNum[0])
                self.workLabelTxt = ''
                self.workLabelNum = None
                self.reDraw()

    # Mouse Event
    def showMouse(self, event):
        if self.img != None:
            x, y = self.rebuildCoord(event.x, event.y)
            if x >= 0 and y >= 0 and x < self.i_width and y < self.i_height:
                self.mousePosStr.set('X: ' + str(x) + ' Y: ' + str(y))

    def showPoint1(self, event):
        if self.workLabelNum and self.img != None:
            x, y = self.rebuildCoord(event.x, event.y)
            if x >= 0 and y >= 0 and x < self.i_width and y < self.i_height:
                self.pointStr1.set(
                    'Point 1: (' + str(x) + ',' + str(y) + ')')
                self.draws[self.workLabelNum[0]].x1 = x
                self.draws[self.workLabelNum[0]].y1 = y
                self.draws[self.workLabelNum[0]].cx1 = event.x
                self.draws[self.workLabelNum[0]].cy1 = event.y
                self.reDraw()
                print('Point 1: ', event.x, event.y)

    def showPoint2(self, event):
        if self.workLabelNum and self.img != None:
            x, y = self.rebuildCoord(event.x, event.y)
            if x >= 0 and y >= 0 and x < self.i_width and y < self.i_height:
                self.pointStr2.set(
                    'Point 2: (' + str(x) + ',' + str(y) + ')')
                self.draws[self.workLabelNum[0]].x2 = x
                self.draws[self.workLabelNum[0]].y2 = y
                self.draws[self.workLabelNum[0]].cx2 = event.x
                self.draws[self.workLabelNum[0]].cy2 = event.y
                self.reDraw()
                print('Point 2: ', event.x, event.y)

    ## Graphic Event ##
    def canvasChange(self, event):
        self.c_width = self.canvas.winfo_width()
        self.c_height = self.canvas.winfo_height()
        if self.img != None:
            self.resizeImage()
            self.resizeLabel()
            self.reDraw()

    def resizeImage(self):
        r_window = self.c_width / self.c_height
        tem = None
        if self.i_width > self.c_width or self.i_height > self.c_height:
            if r_window > self.ratio:
                tem = self.img.resize(
                    (int(self.ratio * self.c_height), int(self.c_height)), Image.ANTIALIAS)
            else:
                tem = self.img.resize((int(self.c_width), int(
                    self.c_width / self.ratio)), Image.ANTIALIAS)
        else:
            tem = self.img.resize(
                (self.i_width, self.i_height), Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(image=tem)

    def resizeLabel(self):
        for box in self.draws:
            box.cx1, box.cy1 = self.restoreCoord(box.x1, box.y1)
            box.cx2, box.cy2 = self.restoreCoord(box.x2, box.y2)

    def rebuildCoord(self, x, y):
        leftTop_x = int((self.c_width - self.imgtk.width()) / 2)
        leftTop_y = int((self.c_height - self.imgtk.height()) / 2)
        x -= leftTop_x
        y -= leftTop_y
        x = x / self.imgtk.width() * self.i_width
        y = y / self.imgtk.height() * self.i_height
        return int(x), int(y)

    def restoreCoord(self, x, y):
        x = x / self.i_width * self.imgtk.width()
        y = y / self.i_height * self.imgtk.height()
        leftTop_x = int((self.c_width - self.imgtk.width()) / 2)
        leftTop_y = int((self.c_height - self.imgtk.height()) / 2)
        x += leftTop_x
        y += leftTop_y
        return int(x), int(y)

    def reDraw(self):
        r = 7
        self.canvas.delete(tk.ALL)
        self.canvas.create_image(
            self.c_width / 2, self.c_height / 2, image=self.imgtk)
        if len(self.draws) > 0:
            for i in range(len(self.draws)):
                if self.workLabelNum and i == self.workLabelNum[0]:
                    color_in = 'red'
                    color_out = 'black'
                else:
                    color_in = 'grey'
                    color_out = '#999'

                x1 = self.draws[i].cx1
                y1 = self.draws[i].cy1
                x2 = self.draws[i].cx2
                y2 = self.draws[i].cy2
                if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                    self.canvas.create_line(
                        x1, y1, x1, y2, x2, y2, x2, y1, x1, y1, fill=color_in, width=2)
                if x1 >= 0 and y1 >= 0:
                    self.canvas.create_oval(
                        x1 - r, y1 - r, x1 + r, y1 + r, fill=color_in, outline=color_out, width=3)
                if x2 >= 0 and y2 >= 0:
                    self.canvas.create_oval(
                        x2 - r, y2 - r, x2 + r, y2 + r, fill=color_in, outline=color_out, width=3)


# Main
root = tk.Tk()
MainWindow(root)
root.mainloop()
