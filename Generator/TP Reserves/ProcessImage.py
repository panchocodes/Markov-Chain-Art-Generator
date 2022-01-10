import os
from PIL import Image
from PIL import ImageEnhance
import random
import pyprind
import sys


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

    def generateOutput(self, width, height):
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
        finalImg = listOfColorsToImage(output, width, height)
        return finalImg

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
        image = Image.new('RGB', canvas, (100,100,100,0))
        pixel_data = image.load()

        y = -1
        for pixel in range(l):
            r, g, b = lst[pixel].split('_')
            x = pixel % width
            #each new row add to y
            if x == 0:
                y = y+1
            pixel_data[x, y] = (int(r), int(g), int(b))
        return image
'''
pup = imageToListOfColors(img)
a = None
a = LinearMarkov(1,pup)
print(type(a))

pup = imageToListOfColors(img)
a = LinearMarkov(1,pup)
b= a.generateOutput(600,600)
b.show()

pup = imageToListOfColors(img)
a = LinearMarkov(1,pup)
b= a.generateOutput(600,600)
b.show()



#pup2 = image_to_colorlst(img2)
a = LinearMarkov(1,pup)
b= a.generateOutput(500,500)
b.show()
b= a.generateOutput(1000,1000)
b.show()
b= a.generateOutput(1000,1000)
b.show()
b= a.generateOutput(1000,1000)
b.show()
b= a.generateOutput(1000,1000)
b.show()
print("len of img: "+ str(len(pup)))

mod =  make_higher_order_markov_model(2, pup)
short = generate_higher_random_sentence(250000, mod)
pap = str_to_image(short, 500, 500)
pap.show()

short = generate_higher_random_sentence(250000, mod)
pap = str_to_image(short, 500, 500)
pap.show()
short = generate_higher_random_sentence(250000, mod)
pap = str_to_image(short, 500, 500)
pap.show()

mod2 = make_markov_model(pup)
short2 = generate_random_sentence(4096000, mod2)
pap2 = str_to_image(short2, 2560, 1600)
pap2.show()
bar = pyprind.ProgBar(len(data)-order, stream = sys.stdout)
'''
