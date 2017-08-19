import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image,ImageTk
from matplotlib import pyplot as plt

class MainWindow():


    def __init__(self,main):
        self.main=main
        self.fileBtn=tk.Button(
            main,
            anchor=tk.CENTER,
            text='Open File',
            width=10,
            height=3,
            command=self.openFile
        )
        self.fileBtn.pack(
            side='top',
            padx=10,
            pady=10
        )

        self.labels=[]
        self.v=tk.IntVar()
        btn1=tk.Radiobutton(
            main,
            text='Default',
            variable=v
            value=1
        )
        btn2=tk.Radiobutton(
            main,
            text='Default',
            variable=v
            value=1
        )
        btn1.pack(anchor=tk.W)
        btn2.pack(anchor=tk.W)
        self.labels.append(tk.Radiobutton(main,))

        img=np.zeros((640,640,3),np.uint8)
        img=Image.fromarray(img)
        imgtk=ImageTk.PhotoImage(image=img)

        self.container=tk.Label(main,image=imgtk)
        self.container.pack(
            side='bottom',
            padx=10,
            pady=20
        )
        main.mainloop()


    def openFile(self):
        file=fd.LoadFileDialog(self.main)
        fileName=file.go()
        if fileName!='':
            print(fileName)
            img=cv2.imread(fileName)
            b,g,r = cv2.split(img)
            img = cv2.merge((r,g,b))
            img=Image.fromarray(img)
            imgtk=ImageTk.PhotoImage(image=img)
            self.container.config(image=imgtk)   
        self.main.mainloop()

    

root=tk.Tk()
MainWindow(root)
root.mainloop()






# while(cap.isOpened()):
#     ret, frame = cap.read()
#     print(ret)
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()