import six
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgb
from PIL import Image, ImageTk
import os
import json
import imageio

PROJECT_NAME = 'Fast Label'
VERSION = '1.0'


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
        self.supportVdo = ['avi', 'mp4', 'wmv', 'mkv']

        self.filePath = None

        self.files = []
        self.workLabelTxt = ''

        self.draws = []
        self.img = None
        self.imgtk = None
        self.vdo = None
        self.curImg = None
        self.fileType = None

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

        self.keyBinding()
        self.mode = 0

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
        self.fileBtn = tk.Button(
            self.buttonFrame,
            anchor=tk.CENTER,
            text='Open File',
            width=10,
            height=3,
            command=self.openFile
        )
        self.fileBtn.pack(
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

        self.info = tk.Button(
            self.buttonFrame,
            width=5,
            height=3,
            text='Help',
            command=self.showInfo
        )
        self.info.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

    def initLabelFrame(self):
        self.labelBtnFrame = tk.LabelFrame(
            self.labelFrame
        )
        self.labelBtnFrame.pack(
            side=tk.TOP,
            fill=tk.X
        )

        self.addLbBtn = tk.Button(
            self.labelBtnFrame,
            anchor=tk.CENTER,
            text='Add',
            command=self.addLabel
        )
        self.addLbBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.delLbBtn = tk.Button(
            self.labelBtnFrame,
            anchor=tk.CENTER,
            text='Delete',
            command=self.delLabel
        )
        self.delLbBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

        self.allLabelFrame = tk.LabelFrame(
            self.labelFrame,
        )
        self.allLabelFrame.pack(
            side=tk.TOP,
        )
        self.labelBoxNum = tk.Listbox(
            self.allLabelFrame,
            width=4,
            height=10,
        )
        self.labelBoxNum.pack(
            side=tk.LEFT,
        )
        self.labelBox = tk.Listbox(
            self.allLabelFrame,
            width=26,
            height=10,

        )
        self.labelBox.pack(
            side=tk.LEFT,
            fill=tk.BOTH
        )
        for i in range(0, 3):
            self.labelBox.insert(tk.END, 'Label ' + str(i + 1))
            self.labelBoxNum.insert(tk.END, i + 1)

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
            padx=10,
            pady=10
        )
        self.editBtn = tk.Button(
            self.drawBtnFrame,
            text='Edit',
            command=self.editLabel
        )
        self.editBtn.pack(
            side=tk.LEFT,
        )
        self.delDrawBtn = tk.Button(
            self.drawBtnFrame,
            text='Delete',
            command=self.delDraw
        )
        self.delDrawBtn.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        self.usedLabelFrame = tk.LabelFrame(
            self.labelFrame,
        )
        self.usedLabelFrame.pack(
            side=tk.TOP,
        )

        self.usedLabelNum = tk.Listbox(
            self.usedLabelFrame,
            width=4,
            height=10,
        )
        self.usedLabelNum.pack(
            side=tk.LEFT,
        )
        self.usedLabel = tk.Listbox(
            self.usedLabelFrame,
            width=26,
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

        self.totalNum = tk.Message(
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

    # Hotkey Binding
    def keyBinding(self):
        self.main.bind('<Control-f>', self.openFile)
        self.main.bind('<a>', self.preImg)
        self.main.bind('<d>', self.nxtImg)
        self.main.bind('<s>', self.saveLabel)
        self.main.bind('<q>', self.drawMode)
        self.main.bind('<w>', self.selectMode)
        self.main.bind('<e>', self.editLabel)
        self.main.bind('<space>', self.key2draw)

    def drawMode(self, event=None):
        if self.mode == 0:
            self.cmd = tk.Entry(
                self.labelFrame,
                width=10
            )
            self.cmd.pack(
                side=tk.TOP,
                fill=tk.X
            )
            self.mode = 1
        self.cmd.focus()

    def selectMode(self, event=None):
        if self.mode == 0:
            self.cmd = tk.Entry(
                self.labelFrame,
                width=10
            )
            self.cmd.pack(
                side=tk.TOP,
                fill=tk.X
            )
            self.mode = 2
        self.cmd.focus()

    def key2draw(self, event=None):
        if self.mode == 1:
            self.mode = 0
            try:
                self.selectedNum = (int(self.cmd.get()) - 1,)
                if self.selectedNum[0] < self.labelBox.size():
                    self.selectedTxt = self.labelBox.get(self.selectedNum[0])
                    self.drawLabel()
            except Exception as error:
                pass
        elif self.mode == 2:
            self.mode = 0
            try:
                self.workLabelNum = (int(self.cmd.get()) - 1,)
                self.usedLabel.selection_clear(0, tk.END)
                self.usedLabel.select_set(self.workLabelNum[0])
                self.selectDraw()
            except Exception as error:
                pass
        self.cmd.pack_forget()

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
            'Current Label: ' + str(self.workLabelNum[0] + 1) + '-' + a.text)
        self.pointStr1.set(
            'Point 1: (' + str(a.x1) + ',' + str(a.y1) + ')')
        self.pointStr2.set(
            'Point 2: (' + str(a.x2) + ',' + str(a.y2) + ')')

        self.selectedNum = None
        self.selectedTxt = ''
        self.reDraw()
        print('Working: ', self.workLabelNum[0], self.workLabelTxt)

    # Button Event
    # Menu Button
    def openFile(self, event=None):
        self.files = []
        self.filePath = ()
        self.filePath = fd.askopenfilename()
        if self.filePath != ():
            typeStr = self.filePath[-3:].lower()
            if typeStr in self.supportImg:
                self.curImg = 0
                self.openImg(self.filePath)
                self.totalNumStr.set('Total: 1')
            elif typeStr in self.supportVdo:
                self.openVdo(self.filePath)
                self.totalNumStr.set('Total: ' + str(self.vdo.get_length()))
            else:
                print('File type not support.')

    def openFolder(self):
        self.fileType = 0
        folder = fd.askdirectory()
        if folder != '' and folder != ():
            for img in os.listdir(folder):
                if img[-3:] in self.supportImg:
                    self.files.append(os.path.join(folder, img))
            self.totalNumStr.set('Total: ' + str(len(self.files)))
            self.curImg = 0
            self.openImg(self.files[self.curImg])

    def resetAll(self):
        self.draws = []
        self.usedLabel.delete(0, tk.END)
        self.usedLabelNum.delete(0, tk.END)
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
        img = imageio.imread(self.filePath)
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
                self.usedLabelNum.insert(tk.END, self.usedLabel.size())
                self.usedLabel.selection_clear(0, tk.END)
                self.draws.append(tem)
        self.reDraw()

    def preImg(self, event=None):
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

    def nxtImg(self, event=None):
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
        if self.fileType != None:
            if self.jumpNum.get() != '':
                self.saveLabel()
                try:
                    self.curImg = int(self.jumpNum.get())
                    if self.fileType == 0:
                        self.openImg(self.filePath)
                    else:
                        self.openFrame()
                except Exception as error:
                    print(
                        'Error: The input must be a number between 0 to (video length) or (image amount)')

    def saveLabel(self, event=None):
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

    # Label Button
    def addLabel(self):
        self.addWindow = tk.Tk()
        self.addWindow.title('Add Labels')

        self.addWindow.bind('<Control-Return>', self.addYes)
        self.addWindow.bind('<Escape>', self.addNo)

        self.textLabel = tk.Text(
            self.addWindow,
            height=5,
            width=32
        )
        self.textLabel.pack(
            side=tk.TOP,
            pady=4,
            padx=4,
            fill=tk.X
        )
        self.textLabel.focus()
        yes = tk.Button(
            self.addWindow,
            width=5,
            height=3,
            text='Add',
            command=self.addYes
        )
        yes.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )
        no = tk.Button(
            self.addWindow,
            width=5,
            height=3,
            text='Cancel',
            command=self.addNo
        )
        no.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )

    def addYes(self, event=None):
        input = (self.textLabel.get('1.0', tk.END)).split('\n')
        while '' in input:
            input.remove('')
        for label in input:
            if label not in self.labelBox.get(0, tk.END):
                self.labelBox.insert(tk.END, label)
                self.labelBoxNum.insert(tk.END, self.labelBox.size())
        self.textLabel.delete('1.0', tk.END)
        self.addWindow.destroy()

    def addNo(self, event=None):
        self.addWindow.destroy()

    def delLabel(self):
        if self.selectedNum != None:
            if msgb.askyesno('Warning', 'Are you sure to delete label \"' + self.selectedTxt + '\"?'):
                self.labelBox.delete(self.selectedNum)
                self.labelBoxNum.delete(tk.END)
                self.selectedTxt = ''
                self.selectedNum = None

    def drawLabel(self):
        if self.selectedNum != None:
            if self.selectedTxt not in self.usedLabel.get(0, tk.END):
                self.usedLabel.insert(tk.END, self.selectedTxt)
                self.usedLabelNum.insert(tk.END, self.usedLabel.size())
                print('Add: ', self.selectedTxt)
                self.usedLabel.selection_clear(0, tk.END)
                self.usedLabel.select_set(tk.END)

                self.draws.append(self.DrawedLabel(self.selectedTxt))
                self.selectDraw()
            else:
                print('Add faild: ', self.selectedTxt, ' already exists')

    def editLabel(self, event=None):
        if self.workLabelNum != None:
            self.rename = tk.Tk()
            self.rename.title('Edit Label')

            self.rename.bind('<Return>', self.editYes)
            self.rename.bind('<Escape>', self.editNo)

            self.renameBox = tk.Entry(
                self.rename,
                width=20,
            )
            self.renameBox.pack(
                side=tk.LEFT,
                padx=10,
                pady=10
            )
            self.renameBox.insert(0, self.workLabelTxt)
            self.renameBox.focus()
            yes = tk.Button(
                self.rename,
                width=5,
                height=3,
                text='Change',
                command=self.editYes
            )
            yes.pack(
                side=tk.LEFT,
                padx=10,
                pady=10
            )
            no = tk.Button(
                self.rename,
                width=5,
                height=3,
                text='Cancel',
                command=self.editNo
            )
            no.pack(
                side=tk.LEFT,
                padx=10,
                pady=10
            )

    def editYes(self, event=None):
        txt = self.renameBox.get()
        if txt not in self.usedLabel.get(0, tk.END):
            self.draws[self.workLabelNum[0]].text = txt
            self.workLabelNumTxt = txt
            self.usedLabel.delete(self.workLabelNum[0])
            self.usedLabel.insert(self.workLabelNum[0], txt)
            self.rename.destroy()
        elif txt == self.workLabelTxt:
            print('Nothing changed')
            self.editNo()
        else:
            errMsg = tk.Message(
                self.rename,
                text='Label name already exists'
            )
            errMsg.pack(
                side=tk.BOTTOM,
                padx=5,
                pady=5,
                fill=tk.X
            )

    def editNo(self, event=None):
        self.rename.destroy()

    def delDraw(self, event=None):
        if self.workLabelNum != None:
            if msgb.askyesno('Warning', 'Are you sure to delete drawn label \"' + self.workLabelTxt + '\"?'):
                del self.draws[self.workLabelNum[0]]
                self.usedLabel.delete(self.workLabelNum[0])
                self.usedLabelNum.delete(tk.END)
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

    # Graphic Event
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

    # Other
    def showInfo(self):
        self.info = tk.Tk()
        self.info.title('Help')
        msg = tk.Message(
            self.info,
            text='Fast Label - 1.0\n\r\n\r' +
            'Fast Label is an open source tool build by Derek Liu.\n\r\n\r' +
            '- Support media type:\n\r' +
            '\t*.jpg *.png *.bmp\n\r' +
            '\t*.mp4 *.avi *.wmv *.mkv\n\r' +
            '- Project page:\n\r' +
            '\thttps://github.com/tankgit/fast-label\n\r' +
            '- Email: derektanko@gmail.com\n\r'
            '- GPL-3.0\n\r',
            width=500
        )
        msg.pack(
            side=tk.LEFT,
            fill=tk.X,
            padx=15,
            pady=15,
            expand=tk.YES
        )

# Main


root = tk.Tk()
root.title(PROJECT_NAME + ' - ' + VERSION)
MainWindow(root)
root.mainloop()
