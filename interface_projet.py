import tkinter as tk
from tkinter import *
import PIL.Image
import PIL.ImageOps
import io
import tensorflow as tf
import cv2
import numpy as np
#from tensorflow.keras.models import load_model
import tensorflow as tf 
import time
lastx, lasty = 0, 0

arabic_alph = []
for i in range(0,36):
    #print(chr(1575+i), i)
    arabic_alph.append(chr(1575+i))

arabic_alph.remove('ة')
arabic_alph.remove('ؼ')
arabic_alph.remove('ؽ')
arabic_alph.remove('ؾ')
arabic_alph.remove('ؿ')
arabic_alph.remove('ـ')
arabic_alph.remove('ى')
arabic_alph.remove('ػ')


def xy(event):
    "Takes the coordinates of the mouse when you click the mouse"
    global lastx, lasty
    lastx, lasty = event.x, event.y
 
 
def addLine(event):
    """Creates a line when you drag the mouse
    from the point where you clicked the mouse to where the mouse is now"""
    global lastx, lasty
    canvas.create_oval((lastx, lasty, event.x, event.y), fill="black", outline="black",width='13')

    # this makes the new starting point of the drawing
    lastx, lasty = event.x, event.y
    panel5.configure(state=NORMAL)
def pred_digit():
    global no,no1
    model = tf.keras.models.load_model('arabic_recognition2.model')

    """
    x=root.winfo_rootx()+canvas.winfo_x()
    y=root.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    im = ImageGrab.grab((x, y, x1, y1))
    
    im = im.crop((55, 30, 250, 200))    
    im = im.resize((32, 32))
    img_array = np.array(im)"""

    ps = canvas.postscript(colormode = 'color')
    # use PIL to convert to PNG
    im1 = PIL.Image.open(io.BytesIO(ps.encode('utf-8')))
    img = im1.resize((32,32))
    
    #convert rgb to grayscale
    img = PIL.ImageOps.invert(img).convert('L')
    img.save("geeks.jpg")
    img_array = np.array(img)
    
    #reshaping to support our model input and normalizing
    img_array = np.where(img_array > 100, 255, 0)
    img_array=img_array.reshape([-1, 32, 32, 1])
     


    res1 = model.predict(img_array/255.0)
    print(len(res1[0]))
    """
    if max(res1)>max(res2):
    	acc = max(res1)
    	pred =  np.argmax(res1)
    else :
        """    
    acc = max(res1[0])*100
    pred =  np.argmax(res1) 
    
    no = tk.Label(root, text='Predicted Letter is: '+str(arabic_alph[pred]), width=34, height=1,
                  fg="white", bg="midnightblue",
                  font=('times', 16, ' bold '))
    no.place(x=460, y=380)
    txt = 'Prediction Accuracy is: {:.2f}'.format(acc)
    no1 = tk.Label(root, text=txt, width=34, height=1,
                   fg="white", bg="green",
                   font=('times', 16, ' bold '))
    no1.place(x=460, y=415)


def clear_digit():
	#panel5.configure(state=DISABLED)
    canvas.delete("all")
    try:
        no.destroy()
        no1.destroy()
    except:
        pass

root = tk.Tk()
root.geometry("1000x500")
lbl = Label(root, text="Handwriting Pad", font=("Arial Bold", 30))

lbl.grid(column=125, row=2)
lbl.place(x=40,y=60)



"""
canvas = tk.Canvas(root)
canvas.grid(column=250, row=100, sticky=(tk.N, tk.W, tk.E, tk.S))
canvas.configure(bg='black')
"""
canvas = tk.Canvas(root, width=405, height=280, cursor="pencil", highlightbackground="midnightblue")

canvas.grid(row=0, column=0, pady=2, sticky=W,)
canvas.place(x=460,y=90)
#canvas.configure(bg='black')
canvas.update()

canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
panel5 = Button(root,text = 'Predict',state=DISABLED,command = pred_digit,width = 15,borderwidth=0,bg = 'midnightblue',fg = 'white',font = ('times',18,'bold'))
panel5.place(x=60, y=305)

panel6 = Button(root,text = 'Clear',width = 15,borderwidth=0,command = clear_digit,bg ='red',fg = 'white',font = ('times',18,'bold'))
panel6.place(x=60, y=355)
#root.bind("<Control-s>", save)
root.update()
root.mainloop()