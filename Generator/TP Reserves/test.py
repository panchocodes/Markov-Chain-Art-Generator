from tkinter import *
from PIL import Image, ImageTk
import os
import math
import random
import sys
import time
import threading
from queue import Queue 
from threading import Thread

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def rgbString(red, green, blue):
    #from: https://www.cs.cmu.edu/~112/notes/notes-graphics.html
    return "#%02x%02x%02x" % (red, green, blue)

################################################################

def init(data):
    data.mode = "start"
    data.image = None
    data.timerCounter = 0
    data.gray = rgbString(50, 50, 50)
    data.lgray = rgbString(210, 210, 210)
    data.imageName = "load1.png"
    data.displayStr, data.displayStr2, data.displayStr3= "", "", ""
    data.inputString=""
    data.printWarning, data.printWarning2 = False, False
    data.fill1, data.fill2, data.fill3 = data.gray, data.gray, data.gray
    data.order = 1
    data.inputNum = 0
    data.desiredOutput = ""
    data.chain = None
    data.outImage = None
    data.coverY=0
    data.loadingScreen=False
    
def mousePressed(event, data):
    if (data.mode == "start"): startMousePressed(event, data)
    elif (data.mode == "input"):   inputMousePressed(event, data)
    elif (data.mode == "input2"):   input2MousePressed(event, data)
    elif (data.mode == "input3"):   input3MousePressed(event, data)
    elif (data.mode == "loading"):       loadingMousePressed(event, data)
    elif (data.mode == "output"):   outputMousePressed(event, data)
    elif (data.mode == "final"):   finalMousePressed(event, data)
def keyPressed(event, data):
    if (data.mode == "start"): startKeyPressed(event, data)
    elif (data.mode == "input"):   inputKeyPressed(event, data)
    elif (data.mode == "input2"):   input2KeyPressed(event, data)
    elif (data.mode == "input3"):   input3KeyPressed(event, data)
    elif (data.mode == "loading"):       loadingKeyPressed(event, data)
    elif (data.mode == "output"):   outputKeyPressed(event, data)
    elif (data.mode == "final"):   finalKeyPressed(event, data)
def timerFired(data):
    if (data.mode == "start"): startTimerFired(data)
    elif (data.mode == "input"):   inputTimerFired(data)
    elif (data.mode == "input2"):   input2TimerFired(data)
    elif (data.mode == "input3"):   input3TimerFired(data)
    elif (data.mode == "loading"):       loadingTimerFired(data)
    elif (data.mode == "output"):   outputTimerFired(data)
    elif (data.mode == "final"):   finalTimerFired(data)
def redrawAll(canvas, data):
    if (data.mode == "start"): startRedrawAll(canvas, data)
    elif (data.mode == "input"):   inputRedrawAll(canvas, data)
    elif (data.mode == "input2"):   input2RedrawAll(canvas, data)
    elif (data.mode == "input3"):   input3RedrawAll(canvas, data)
    elif (data.mode == "loading"):  loadingRedrawAll(canvas, data)
    elif (data.mode == "output"):   outputRedrawAll(canvas, data)
    elif (data.mode == "final"):   finalRedrawAll(canvas, data)
    
################################################################

def startMousePressed(event, data):
    pass
def startKeyPressed(event, data):
    if event.keysym:
        data.mode = "input"
def startTimerFired(data):
    data.timerCounter+=1
    if data.timerCounter % 3 == 0:
        data.imageName="load1.png"
    if data.timerCounter % 3 == 1:
        data.imageName="load2.png"
    if data.timerCounter % 3 == 2:
        data.imageName="load3.png"
def startRedrawAll(canvas, data):  
    image = Image.open(data.imageName)
    image = image.resize((data.width, data.height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image)
    data.image = tkImage
    canvas.create_image(0, 0, image=tkImage, anchor="nw")
    canvas.create_text(data.width/2, data.height/2-20,
                       text="Markov Art Generator", font="Arial 36 bold", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2+20,
                       text="Press any key to start.", font="Arial 26", fill = data.lgray)

################################################################

def inputMousePressed(event, data):
    pass
def inputKeyPressed(event, data):
    if event.keysym == "BackSpace":
        data.inputString = data.inputString[:-1]
    elif event.keysym == "period":
        data.inputString += "."
    elif len(event.keysym)==1:
        if len(data.inputString)<=17:
            data.inputString+=event.keysym
        else:
            data.printWarning = False
            data.printWarning2 = True

    elif event.keysym == "Return":
        if (os.path.exists(data.inputString) and (data.inputString.endswith(".jpg") or \
            data.inputString.endswith(".png"))):
            data.mode="input2"
        else:
            data.printWarning2 = False
            data.printWarning=True
    else:
        data.printWarning=True
def inputTimerFired(data):
    data.timerCounter+=1
    if data.timerCounter % 3 == 0:
        data.imageName="load1.png"
    if data.timerCounter % 3 == 1:
        data.imageName="load2.png"
    if data.timerCounter % 3 == 2:
        data.imageName="load3.png"
    if data.timerCounter % 8 < 4:
        data.displayStr = data.inputString + "|"
    else:
        data.displayStr = data.inputString
def inputRedrawAll(canvas, data):
    image = Image.open(data.imageName)
    image = image.resize((data.width, data.height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image)
    data.image = tkImage
    canvas.create_image(0, 0, image=tkImage, anchor="nw")
    canvas.create_rectangle(data.width/2-135, data.height/2-17,data.width/2+135, 
        data.height/2+17,fill=data.gray, width=0)
    canvas.create_text(data.width/2, data.height/2-35,
        text="Type a filename:", font="Arial 26", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2,
            text=data.displayStr, font="Arial 26", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2+35,
        text="Press enter to submit.", font="Arial 26", fill = data.lgray) 
    if data.printWarning:
        canvas.create_text(data.width/2, data.height/2+75,
            text="File path must be alphanumeric and valid.", font="Arial 26", fill = "red")
    elif data.printWarning2:  
        canvas.create_text(data.width/2, data.height/2+75,
            text="File path too long.", font="Arial 26", fill = "red")
    #take input for image and type of chain
    #check image size
    #valid input
    #scale?
    #do chain
    #store model for later
    #ready button

################################################################

def input2MousePressed(event, data):
    mouseLoc = (event.x, event.y)
    c1Loc = (data.width/4, data.height/2-90)
    c2Loc = (data.width/4, data.height/2)
    c3Loc = (data.width/4, data.height/2+90)
    bigR = 12
    if distance(mouseLoc, c1Loc) <= bigR:
        data.fill1 = data.lgray
        data.fill2 = data.gray
        data.fill3 = data.gray
    if distance(mouseLoc, c2Loc) <= bigR:
        data.fill1 = data.gray
        data.fill2 = data.lgray
        data.fill3 = data.gray
    if distance(mouseLoc, c3Loc) <= bigR:
        data.fill1 = data.gray
        data.fill2 = data.gray
        data.fill3 = data.lgray
def input2KeyPressed(event, data):
    if data.fill2==data.lgray:
        if event.keysym == "BackSpace":
            data.inputNum = data.inputNum//10
        elif len(event.keysym)==1 and event.keysym.isdigit():
            data.inputNum=data.inputNum*10+int(event.keysym)
        elif event.keysym == "Return":
            data.order=data.inputNum
            data.inputNum=0
            data.mode="input3"
            data.fill1, data.fill2, data.fill3 = "black", "black", "black"
    elif data.fill1==data.gray or data.fill3==data.gray:
        if event.keysym == "Return":
            data.mode="input3"
            data.fill1, data.fill2, data.fill3 = "black", "black", "black"
def input2TimerFired(data):
    data.timerCounter+=1
    if data.timerCounter % 3 == 0:
        data.imageName="load1.png"
    if data.timerCounter % 3 == 1:
        data.imageName="load2.png"
    if data.timerCounter % 3 == 2:
        data.imageName="load3.png"
    if data.timerCounter % 8 < 4:
        if data.inputNum != 0:
            data.displayStr3 = str(data.inputNum) + "|"
        else:
            data.displayStr3 = "|"
    else:
        if data.inputNum != 0:
            data.displayStr3 = str(data.inputNum)
        else:
            data.displayStr3= ""
def input2RedrawAll(canvas, data):
    image = Image.open(data.imageName)
    image = image.resize((data.width, data.height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image)
    data.image = tkImage
    canvas.create_image(0, 0, image=tkImage, anchor="nw")
    canvas.create_text(data.width/2, data.height/2-130,
        text="Click and choose a model:", font="Arial 36", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2+130,
        text="Press enter to continue to output size selection.", font="Arial 22", fill = data.lgray)
    canvas.create_rectangle(data.width/2-170, data.height/2-110, 
        data.width/2+170, data.height/2+110, fill = data.gray)
    cx,cy1 = data.width/4, data.height/2-90
    cy2 = data.height/2
    cy3 = data.height/2+90
    bigR=12
    littleR=10
    canvas.create_text(cx+20, cy1,
    text="Order 1 Linear Markov", font="Arial 26", fill = data.lgray, anchor="w")
    canvas.create_oval(cx-bigR,cy1-bigR,cx+bigR,cy1+bigR,fill=data.lgray)
    canvas.create_oval(cx-littleR,cy1-littleR,cx+littleR,cy1+littleR,fill=data.fill1)
    if data.fill1 == data.lgray:
        data.order = 1
        data.desiredOutput = "linear"

    canvas.create_text(cx+20, cy2,
        text="Order n Linear Markov", font="Arial 26", fill = data.lgray, anchor="w")
    canvas.create_oval(cx-bigR,cy2-bigR,cx+bigR,cy2+bigR,fill=data.lgray)
    canvas.create_oval(cx-littleR,cy2-littleR,cx+littleR,cy2+littleR,fill=data.fill2)

    if data.fill2 == data.lgray:
        canvas.create_text(data.width/2+30, data.height/2+30,
            text="Type an order:", font="Arial 26", fill = data.lgray, anchor="e")
        canvas.create_text(data.width/2+30, data.height/2+30,
            text=data.displayStr3, font="Arial 26", fill = data.lgray, anchor="w")
        data.desiredOutput = "linear"
        
    canvas.create_text(cx+20, cy3,
        text="Neighbor Markov", font="Arial 26", fill = data.lgray, anchor="w")
    canvas.create_oval(cx-bigR,cy3-bigR,cx+bigR,cy3+bigR,fill=data.lgray)
    canvas.create_oval(cx-littleR,cy3-littleR,cx+littleR,cy3+littleR,fill=data.fill3)

    if data.fill3 == data.lgray:
        data.desiredOutput = "neighbor"

################################################################

def input3MousePressed(event, data):
    mouseLoc = (event.x, event.y)
    c1Loc = (data.width/4, data.height/2-30)
    c2Loc = (data.width/4, data.height/2+30)
    bigR = 12
    if distance(mouseLoc, c1Loc) <= bigR:
        data.fill1 = data.lgray
        data.fill2 = data.gray
    if distance(mouseLoc, c2Loc) <= bigR:
        data.fill1 = data.gray
        data.fill2 = data.lgray
def input3KeyPressed(event, data):
    if data.fill1==data.lgray:
        if event.keysym == "BackSpace":
            data.inputNum = data.inputNum//10
        elif len(event.keysym)==1 and event.keysym.isdigit():
            data.inputNum=data.inputNum*10+int(event.keysym)
        elif event.keysym == "Return":
            data.outWidth=data.inputNum
            data.outHeight=data.inputNum
            tb_click(data, canvas)
            data.loadingScreen = True
    elif data.fill2==data.gray:
        if event.keysym == "Return":
            data.outWidth=1920
            data.outHeight=1080
            tb_click(data, canvas)
            data.loadingScreen = True
def input3TimerFired(data):
    data.timerCounter+=1
    if data.timerCounter % 3 == 0:
        data.imageName="load1.png"
    if data.timerCounter % 3 == 1:
        data.imageName="load2.png"
    if data.timerCounter % 3 == 2:
        data.imageName="load3.png"
    if data.timerCounter % 9 == 0:
        if data.inputNum != 0:
            data.displayStr2 = str(data.inputNum) + "|"
        else:
            data.displayStr2 = "|"
    if data.timerCounter % 9 == 5:
        if data.inputNum != 0:
            data.displayStr2 = str(data.inputNum)
        else:
            data.displayStr2 = ""
def input3RedrawAll(canvas, data):
    image = Image.open(data.imageName)
    image = image.resize((data.width, data.height), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image)
    data.image = tkImage
    canvas.create_image(0, 0, image=tkImage, anchor="nw")    
    cx1,cy1 = data.width/4, data.height/2-30
    cx2,cy2 = data.width/4, data.height/2+30
    #10 = desired margin

    canvas.create_text(data.width/2, data.height/2-85,
        text="Select output dimensions:", font="Arial 36", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2+80,
        text="Press enter to begin output.", font="Arial 30", fill = data.lgray)
    canvas.create_rectangle(data.width/2-210, data.height/2-65, 
        data.width/2+210, data.height/2+65, fill = data.gray)

    bigR=12
    littleR=10
    canvas.create_text(data.width/4+20, cy1,
    text="Square Output", font="Arial 26", fill = data.lgray, anchor="w")
    canvas.create_oval(cx1-bigR,cy1-bigR,cx1+bigR,cy1+bigR,fill=data.lgray)
    canvas.create_oval(cx1-littleR,cy1-littleR,cx1+littleR,cy1+littleR,fill=data.fill1)
    if data.fill1 == data.lgray:
        canvas.create_text(data.width/2+30, data.height/2,
            text="Type a width:", font="Arial 26", fill = data.lgray, anchor="e")
        canvas.create_text(data.width/2+30, data.height/2,
            text=data.displayStr2, font="Arial 26", fill = data.lgray, anchor="w")

    canvas.create_text(data.width/2+130, cy2,
        text="Desktop Background", font="Arial 26", fill = data.lgray, anchor="e")
    canvas.create_text(data.width/2+130, cy2,
        text="(1920x1080)", font="Arial 12", fill = data.lgray, anchor="w")
    canvas.create_oval(cx2-bigR,cy2-bigR,cx2+bigR,cy2+bigR,fill=data.lgray)
    canvas.create_oval(cx2-littleR,cy2-littleR,cx2+littleR,cy2+littleR,fill=data.fill2)
    if data.loadingScreen:
        canvas.create_rectangle(0, 0, data.width, data.height,fill="black", width=0)
        canvas.create_text(data.width/2, data.height/2,
    text="Modeling...", font="Arial 26", fill = data.lgray)

################################################################

    def tb_click(data, canvas):
        data.queue = Queue()
        ThreadedTask(data.queue).start()
        canvas.after(100, process_queue(data, canvas))

    def process_queue(data, canvas):
        try:
            msg = data.queue.get(0)
        except Queue.Empty:
            process_queue(data)
            canvas.after(100, process_queue(data, canvas))

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self, data):
        if data.desiredOutput == "linear":
            img = Image.open(data.inputString)
            colors = imageToListOfColors(img)
            data.chain = LinearMarkov(data.order,colors)
            queueTup = data.chain.generateOutput(data, data.outWidth, data.outHeight)
            #saves a tuple of the info of the queue(output, w, h)
            colors = queueTup[0]
            w , h = queueTup[1], queueTup[2]
            data.outImage = listOfColorsToImage(colors, w, h)
            data.outImage.save('out.png')
            self.queue.put(outImage)
        if data.desiredOutput == "neighbor":
            img = Image.open(data.inputString)
            w, h = img.size
            colors = imageToListOfColors(img)
            data.chain = NeighborMarkov(w, data.order, colors)
            queueTup = data.chain.generateOutput(data, data.outWidth, data.outHeight)
            #saves a tuple of the info of the queue(output, w, h)
            colors = queueTup[0]
            w , h = queueTup[1], queueTup[2]
            data.outImage = listOfColorsToImage(colors, w, h)
            data.outImage.save('out.png')
            self.queue.put(outImage)

################################################################

def outputMousePressed(event, data):
    pass
def outputKeyPressed(event, data):
    pass
def outputTimerFired(data):
    data.coverY+=4
def outputRedrawAll(canvas, data):
    if data.desiredOutput == "linear":
        image = Image.open('out.png')
        image = image.resize((data.width, data.height), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(image)
        data.outImage = tkImage
        canvas.create_image(0, 0, image=tkImage, anchor="nw")
        if(data.coverY<data.height):
            canvas.create_rectangle(0, data.coverY, data.width, data.height, fill="black")
        else:
            data.mode="final"
    if data.desiredOutput == "neighbor":
        data.mode="final"

################################################################

def finalMousePressed(event, data):
    pass
def finalKeyPressed(event, data):
    if event.keysym == "r":
        data.mode="input"
    if event.keysym == "g":
        data.chain.generateOutput(data, data.outWidth, data.outHeight)
        data.queueTup = data.queue.get(block=False)
        colors = queueTup[0]
        w , h = queueTup[1], queueTup[2]
        data.outImage = listOfColorsToImage(colors, w, h)
        data.outImage.save('out.png')
        data.mode = "output"
    if event.keysym == "o":
        image = Image.open('out.png')
        image.show()
    if event.keysym == "e":
        sys.exit()
def finalTimerFired(data):
    pass
def finalRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height,fill="black", width=0)
    canvas.create_text(data.width/2, data.height/8,
        text="Your output has been saved as 'out.png' in the folder with this program.", font="Arial 14", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/4,
        text="Press 'o' to open your output in another window.", font="Arial 14", fill = data.gray)
    canvas.create_text(data.width/2, data.height*3/8,
        text="Press 'r' to go back and change the model, output size, or input image.", font="Arial 14", fill = data.lgray)
    canvas.create_text(data.width/2, data.height/2,
        text="Press 'g' to generate a new output from the current model.", font="Arial 14", fill = data.lgray)
    canvas.create_text(data.width/2, data.height*7/8,
        text="Press 'e' to quit.", font="Arial 14", fill = data.lgray)
################################################################

def run(width=300, height=300):
    #https://www.cs.cmu.edu/~112/notes/notes-animations.html
    #copied from MVC barebones
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

class FrequencyTable(dict):
    def __init__(self):
        super(FrequencyTable, self).__init__()
        self.keyCount = 0  
        self.valueCount = 0  

    def update(self, lst):
        # i chose to do this because counting totals for the entries and such
        #is a hell of a lot cheaper here than looping through in randomColor
        for item in lst:
            if item not in self:               
                self.keyCount += 1
            self[item] = 1 + self.get(item,0)
            self.valueCount += 1

    def randomColor(self):
        #https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability
        #effectively copied and modified this code
        randomIndex = random.randint(0, self.valueCount-1)
        total = 0
        for key, value in self.items():
            total += value
            #once past randomIndex we stop and return
            if(randomIndex < total):
                return key

class LinearMarkov():
    #i didnt base my code on these but i did look at them so im citing them
    #to clarify, I designed the algorithms and wrote all the code for the models
    #https://en.wikipedia.org/wiki/Markov_model
    #https://hackernoon.com/from-what-is-a-markov-model-to-here-is-how-markov-models-work-1ac5f4629b71
    def __init__(self, order=1, colors=None):
        if order < 1 or not isinstance(order, int):
            #so it doesnt break
            order=1
        self.order = order
        self.markov_model = dict()
        if colors:
            self.addToModel(colors)

    def addToModel(self, data):
        print('modeling...')
        if self.order == 1:
            for i in range(0, len(data)-1):
                if data[i] in self.markov_model:
                    self.markov_model[data[i]].update([data[i+1]])
                else:
                    self.markov_model[data[i]] = FrequencyTable()
                    self.markov_model[data[i]].update([data[i+1]])

        if self.order > 1:
            for i in range(len(data)-self.order):
                window = tuple(data[i: i+self.order])
                if window in self.markov_model:
                    self.markov_model[window].update([tuple(data[i+1: i+self.order+1])])
                else:
                    self.markov_model[window] = FrequencyTable()
                    self.markov_model[window].update([tuple(data[i+1: i+self.order+1])])

            last = tuple(data[len(data)-self.order:len(data)])
            #this maps the last tuple to the first so it completes the chain
            self.markov_model[last] = FrequencyTable()
            self.markov_model[last].update([tuple(data[0:self.order])])

    def generateOutput(self, data, width, height):
        print('generating...')
        output = []
        #l is the iterations for the final image
        l = width*height
        #returns a 'random' output form the current model based on order
        if self.order == 1:
            currKey = random.choice(list(self.markov_model.keys()))
            output = [currKey]
            for i in range(l):
                currTable = self.markov_model[currKey]
                randomCol= currTable.randomColor()
                currKey = randomCol
                output.append(currKey)

        if self.order > 1:
            currKey = random.choice(list(self.markov_model.keys()))
            output = list(currKey)
            for i in range(l):
                currTable = self.markov_model[currKey]
                randomCol = currTable.randomColor()
                currKey = randomCol
                output.append(randomCol[self.order-1])
        ret = tuple([output, width, height])
        return ret

class NeighborMarkov():
    def __init__(self, width, order=1, colors=None):
        if order < 1 or not isinstance(order, int):
            #so it doesnt break
            order=1
        self.order = order
        self.markov_model = dict()
        self.width = width
        if colors:
            self.addToModel(colors)
    def getNeighbors(self, colors, i):
        neighbors = [i-self.width, i-1, i+1, i+self.width]
        validNeighbors = []
        for neighbor in neighbors:
            try:
                validNeighbors.append(colors[neighbor]) 
            except IndexError:
                continue
        return validNeighbors
        
    def addToModel(self, colors):
        for i in range(len(colors)-1):
            if colors[i] in self.markov_model:
                self.markov_model[colors[i]].update(self.getNeighbors(colors,i))
            else:
                self.markov_model[colors[i]] = FrequencyTable()
                self.markov_model[colors[i]].update(self.getNeighbors(colors,i))

    def generateOutput(self, data ,w, h):
        #generation algorithm(not the code) taken from below link and modified:
        #https://jonnoftw.github.io/2017/01/18/markov-chain-image-generation
        l=w*h
        output = [None] * l
        donePixels=set()
        currKey = random.choice(list(self.markov_model.keys()))
        currPos = random.randint(0, l-1)
        output[currPos] = currKey
        stack = [currPos]
        while stack:
            currPos = stack.pop()
            if currPos in donePixels:
                continue
            else:
                donePixels.add(currPos)
            try:
                pixel = output[currPos]
                currTable = self.markov_model[pixel]
                output[currPos] = pixel
            except IndexError:
                    continue
            keys = list(currTable.keys())
            neighbours = [currPos-w, currPos-1, currPos+w,currPos+1]
            
            random.shuffle(neighbours)
            for neighbour in neighbours:
                try:
                    rand = self.markov_model[pixel].randomColor()
                    if neighbour not in donePixels:
                            output[neighbour] = rand
                except IndexError:
                    pass
                stack.append(neighbour)
        ret = tuple(output, w, h)
        return ret

def imageToListOfColors(image):
    #https://stackoverflow.com/questions/11064786/get-pixels-rgb-using-pil
    #referenced API and above link
    print('converting...')
    rgbImage = image.convert('RGB')
    colors = []
    height, width = rgbImage.size[1], rgbImage.size[0]
    print(str(width) + "by" + str(height))
    for y in range(0, height):
        for x in range(0, width):
            r, g, b = rgbImage.getpixel((x, y))
            pixelColor = "%s_%s_%s"%(r,g,b)
            colors.append(pixelColor)

    return colors

def listOfColorsToImage(lst, width, height):
        #referenced API
        canvas = (width, height)
        l = width * height
        #from Pillow API
        img = Image.new('RGB', canvas, (100,100,100,0))
        pixels = img.load()

        y = -1
        for pixel in range(l):
            r, g, b = lst[pixel].split('_')
            x = pixel % width
            #each new row add to y
            if x == 0:
                y = y+1
            pixels[x, y] = (int(r), int(g), int(b))
        return img

run(500, 500)