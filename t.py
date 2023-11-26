from tkinter import *
from tkinter import colorchooser
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("NoodleDoodle")
root.geometry("1100x600")
# Declare canvas as a global variable
canvas = None

# logo
img = PhotoImage(file='pap.png')
root.iconphoto(False, img)

# -------------- variables --------------------

# stroke size options
brush_options = [5, 10, 15,]
pencil_options = [0.5, 1, 1.5]
eraser_options = [3, 20, 25, 30]

stroke_size = IntVar() 
stroke_size.set(1)

stroke_color = StringVar()
stroke_color.set("black")

# variables for pencil
prevPoint = [0, 0]
currentPoint = [0, 0]

# variable for text
textValue = StringVar()

#canvas
canvas = None

canvas_actions = []
current_action_index = -1
# --------------------- functions -------------------------

def usePencil():
    global canvas
    stroke_color.set("black")
    canvas["cursor"] = "pencil"
    sizeList['menu'].delete(0, 'end')  
    for size in pencil_options:
        sizeList['menu'].add_command(label=str(size), command=lambda s=size: stroke_size.set(s))
    stroke_size.set(0.5)

def useBrush():
    global canvas
    stroke_color.set("black")
    canvas["cursor"] = "arrow"
    sizeList['menu'].delete(0, 'end')  
    for size in brush_options:
        sizeList['menu'].add_command(label=str(size), command=lambda s=size: stroke_size.set(s))
    stroke_size.set(5) 

def useEraser():
    global canvas  
    stroke_color.set("white")
    canvas["cursor"] = "dotbox"
    sizeList['menu'].delete(0, 'end')  
    for size in eraser_options:
        sizeList['menu'].add_command(label=str(size), command=lambda s=size: stroke_size.set(s))
    stroke_size.set(3)

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

    if prevPoint != [0, 0]:
        canvas.create_line(prevPoint[0], prevPoint[1], currentPoint[0], currentPoint[1],fill=stroke_color.get(), width=stroke_size.get())

    prevPoint = currentPoint

    if event.type == "5":
        prevPoint = [0, 0]

def clearImage():
    global current_action_index
    if current_action_index < len(canvas_actions):
        canvas.delete("all")
        for action in canvas_actions[:current_action_index + 1]:
            if action["type"] == "line":
                canvas.create_line(action["points"], fill=action["fill"], width=action["width"])
            elif action["type"] == "polygon":
                canvas.create_polygon(action["points"], fill=action["fill"], outline=action["outline"], width=action["width"])
        current_action_index == 1


def save_canvas_action():
    global current_action_index
    current_action_index += 1
    canvas_data = {
        "points": canvas.find_all(),
        "fill": stroke_color.get(),
        "outline": stroke_color.get(),
        "width": stroke_size.get(),
    }
    canvas_actions.append(canvas_data)

def saveImage():
    try:
        fileLocation = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPG files", ".jpg")])
        if fileLocation:
            x = root.winfo_rootx() + canvas.winfo_x()
            y = root.winfo_rooty() + canvas.winfo_y() + 100
            x1 = x + canvas.winfo_width() + 300
            y1 = y + canvas.winfo_height() + 100 
            img = ImageGrab.grab(bbox=(x, y, x1, y1))
            img.save(fileLocation)
            showImage = messagebox.askyesno("NoodleDoodle", "Do you want to open the saved image?")
            if showImage:
                import os
                os.startfile(fileLocation)  
    except Exception as e:
        messagebox.showinfo("NoodleDoodle", "Error occurred")

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

strokeSize = Label(sizeFrame, text="Size", width=10,)
strokeSize.grid(row=0, column=0)


# colorBoxFrame

colorBoxFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidt=3)
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

#option menu

sizeList = OptionMenu(sizeFrame, stroke_size, *pencil_options)
sizeList.grid(row=1, column=0)

sizeLabel = Label(sizeFrame, text="Size", width=10)
sizeLabel.grid(row=2, column=0)

# saveImageFrame

saveImageFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
saveImageFrame.grid(row=0, column=4)

save = Button(saveImageFrame, text="Save", bg="white", width=10, command=saveImage)
save.grid(row=0, column=0)


# clearbutton frame

clearImageFrame = Frame(frame1, height=100, width=100, relief=SUNKEN, borderwidth=3)
clearImageFrame.grid(row=0, column=5)

clear = Button(clearImageFrame, text="Clear Artwork", bg="white", width=10, command=clearImage)
clear.grid(row=0, column=0)

# Frame - 2 - Canvas

frame2 = Frame(root, height=500, width=1100, bg="yellow")
frame2.grid(row=1, column=0)

# Create the canvas globally
canvas = Canvas(frame2, height=500, width=1100, bg="white")
canvas.grid(row=0, column=0)

#Bind
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)

root.resizable(False, False)
root.mainloop()
