# Markov Chain Art Generator

Welcome to my Markov Chain Art Generation project! 
Video describing this project: https://www.youtube.com/watch?v=bNWjJtTdNg4

## Final Results

![](./final_1.jpg "(1.2)")
![](./final_2.png "(2.2)")
![](./final_3.png "(3.2)")
![](./final_4.png "(4.2)")
![](./final_5.png "(4.2)")

## Detailed Description

On a basic level, this program take an image of the user’s choice, and can create a few variations on a Markov Chain from which the user can choose to generate an pseudo-random output. To clarify, a Markov chain is a model for some sequential data that maps each state to all the possible states after. In my case, the means going through the image pixel by pixel and mapping the colors to all the possible colors that come after and how often they occur. The difference between the models in my project is how that data is taken and used. For the linear model, it is done from let to right and top to bottom like a book. For the neighbor model, pixels are mapped to all the valid pixels around them (up, right, left, down). Lastly, the order that is changeable signifies the length of the state stored in the model. So, an order of five means that the model stores tuples of five pixels as opposed to individually in an order one chain. 


This project uses pillow and tkinter, so please install pillow or it will not run(tkinter comes with all versions of python 3). To install pillow, go to the console and type “pip install pillow”. At this point, you should be ready to go!

To run the project, simply open it in a python interpreter with the the above already installed. Please ensure that any images you would like to use are in the same folder as MarkovArt.py. Also, any outside images may take up to a couple minutes to process the model if they are high resolution. Be patient, its worth the wait. Otherwise, a photo of a puppy and Warhol’s “Jackie O” have been provided for you to play around with. To start, simply run the program and enjoy!
