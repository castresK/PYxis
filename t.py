from tkinter import *
from tkinter import colorchooser
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("NoodleDoodle")
root.geometry("1100x600")

# -------------- variables --------------------

# stroke size options
options = [1, 2, 3, 4, 5, 10, 15, 20]

stroke_size = IntVar()
stroke_size.set(1)

stroke_color = StringVar()
stroke_color.set("black")


# variables for pencil
prevPoint = [0, 0]
currentPoint = [0, 0]

# variable for text
textValue = StringVar()

# --------------------- functions -------------------------

def usePencil():
    stroke_color.set("black")
    canvas["cursor"] = "pencil"

def useBrush():
    stroke_color.set("black")
    canvas["cursor"] = "boat"

def useEraser():
    stroke_color.set("white")
    canvas["cursor"] = "dotbox"

def selectColor():
    selectedColor = colorchooser.askcolor("blue", title="Select Color")
    if selectedColor[1] is None:
        stroke_color.set("black")
    else:
        stroke_color.set(selectedColor[1])

def paint(event):
    global prevPoint
    global currentPoint
    x = event.x
    y = event.y
    currentPoint = [x, y]
    # canvas.create_oval(x , y , x +5 , y + 5 , fill="black")

    if prevPoint != [0, 0]:
        canvas.create_polygon(prevPoint[0], prevPoint[1], currentPoint[0], currentPoint[1],
                               fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())

    prevPoint = currentPoint

    if event.type == "5":
        prevPoint = [0, 0]

def paintRight(event):
    x = event.x
    y = event.y
    canvas.create_arc(x, y, x + stroke_size.get(), y + stroke_size.get(),
                       fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())

def redoImage():
    fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
    x = root.winfo_rootx()
    y = root.winfo_rooty() - 50
    # Add code to redo the image

def undoImage():
    # Add code to undo the image
    pass

def saveImage():
    try:
        fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
        x = root.winfo_rootx()
        y = root.winfo_rooty() + 100
        img = ImageGrab.grab(bbox=(x, y, x + 1100, y + 500))
        img.save(fileLocation)
        showImage = messagebox.askyesno("NoodleDoodle", "Do you want to open image?")
        if showImage:
            img.show()

    except Exception as e:
        messagebox.showinfo("NoodleDoodle: ", "Error occurred")

def writeText(event):
    canvas.create_text(event.x, event.y, text=textValue.get())

# ------------------- User Interface -------------------

# Frame - 1 : Tools

frame1 = Frame(root, height=100, width=1100)
frame1.grid(row=0, column=0, sticky=NW)

# toolsFrame

toolsFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
toolsFrame.grid(row=0, column=0)

toolsLabel = Label(toolsFrame, text="Tools", width=10)
toolsLabel.grid(row=1, column=0)
pencil = Button(toolsFrame, text="Pencil", width=10, command=usePencil)
pencil.grid(row=2, column=0)
brush = Button(toolsFrame, text="Brush", width=10, command=useBrush)
brush.grid(row=3, column=0)
eraser = Button(toolsFrame, text="Eraser", width=10, command=useEraser)
eraser.grid(row=4, column=0)

# sizeFrame

sizeFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
sizeFrame.grid(row=0, column=1)

defaultButton = Button(sizeFrame, text="Default", width=10, command=usePencil)
defaultButton.grid(row=0, column=0)
sizeList = OptionMenu(sizeFrame, stroke_size, *options)
sizeList.grid(row=1, column=0)
sizeLabel = Label(sizeFrame, text="Size", width=10)
sizeLabel.grid(row=2, column=0)

# colorBoxFrame

colorBoxFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
colorBoxFrame.grid(row=0, column=2)

colorBoxButton = Button(colorBoxFrame, text="Select Color", width=10, command=selectColor)
colorBoxButton.grid(row=0, column=0)

# colorsFrame

colorsFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
colorsFrame.grid(row=0, column=3)

redButton = Button(colorsFrame, text="Red", bg="red", width=10, command=lambda: stroke_color.set("red"))
redButton.grid(row=0, column=0)
greenButton = Button(colorsFrame, text="Green", bg="green", width=10, command=lambda: stroke_color.set("green"))
greenButton.grid(row=1, column=0)
blueButton = Button(colorsFrame, text="Blue", bg="blue", width=10, command=lambda: stroke_color.set("blue"))
blueButton.grid(row=2, column=0)
yellowButton = Button(colorsFrame, text="Yellow", bg="yellow", width=10, command=lambda: stroke_color.set("yellow"))
yellowButton.grid(row=0, column=1)
orangeButton = Button(colorsFrame, text="Orange", bg="orange", width=10, command=lambda: stroke_color.set("orange"))
orangeButton.grid(row=1, column=1)
purpleButton = Button(colorsFrame, text="Purple", bg="purple", width=10, command=lambda: stroke_color.set("purple"))
purpleButton.grid(row=2, column=1)

# saveImageFrame

saveImageFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
saveImageFrame.grid(row=0, column=4)

save = Button(saveImageFrame, text="Save", bg="white", width=10, command=saveImage)
save.grid(row=0, column=0)
redo = Button(saveImageFrame, text="Redo", bg="white", width=10, command=redoImage)
redo.grid(row=1, column=0)
undo = Button(saveImageFrame, text="Undo", bg="white", width=10, command=undoImage)
undo.grid(row=2, column=0)
addlayer = Button(saveImageFrame, text="Layers", bg="white", width=10, )
addlayer.grid(row=3, column=0)


# Frame - 2 - Canvas

frame2 = Frame(root, height=500, width=1100, bg="yellow")
frame2.grid(row=1, column=0)

canvas = Canvas(frame2, height=500, width=1100, bg="white")
canvas.grid(row=0, column=0)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)
canvas.bind("<B3-Motion>", paintRight)
canvas.bind("<Button-2>", writeText)

root.resizable(False, False)
root.mainloop()
