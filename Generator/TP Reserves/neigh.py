from PIL import Image
import numpy as np
import pyprind
import random
import os
import pygame
from collections import defaultdict, Counter


class MarkovChain(object):
    def __init__(self, bucket_size=10):
        self.weights = defaultdict(Counter)
        self.bucket_size = bucket_size

    def normalize(self, pixel):
        return pixel // self.bucket_size

    def denormalize(self, pixel):
        return pixel * self.bucket_size

    def get_neighbours(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def train(self, img):
        """
        Train on the input PIL image
        :param img:
        :return:
        """
        width, height = img.size
        img = np.array(img)[:, :, :3]
        for x in range(height):
            for y in range(width):
                # get the left, right, top, bottom neighbour pixels
                pix = tuple(self.normalize(img[x, y]))

                for neighbour in self.get_neighbours(x, y):
                    try:
                        self.weights[pix][tuple(self.normalize(img[neighbour]))] += 1
                    except IndexError:
                        continue

    def generate(self, width=512, height=512):
        import cv2
        fourcc = cv2.VideoWriter_fourcc(*'MP4v')
        writer = cv2.VideoWriter('markov_img.mp4', fourcc, 24, (width, height))
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        pygame.init()

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Markov Image')
        screen.fill((0, 0, 0))

        initial_state = random.choice(list(self.weights.keys()))

        img = Image.new('RGB', (width, height), 'white')
        img = np.array(img)
        img_out = np.array(img.copy())

        # start filling out the image
        # start at a random point on the image, set the neighbours and then move into a random, unchecked neighbour,
        # only filling in unmarked pixels
        initial_position = (np.random.randint(0, width), np.random.randint(0, height))
        print(img[initial_position])
        img[initial_position] = initial_state
        print(img[initial_position])
        stack = [initial_position]
        coloured = set()
        i = 0

        # input()
        while stack:
            x, y = stack.pop()
            if (x, y) in coloured:
                continue
            else:
                coloured.add((x, y))
            try:
                cpixel = img[x, y]
                print(cpixel)
                node = self.weights[tuple(cpixel)]  # a counter of neighbours
                img_out[x, y] = self.denormalize(cpixel)
                i += 1
                screen.set_at((x, y), img_out[x, y])
                if i % 128 == 0:
                    pygame.display.flip()
                    # writer.write(cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR))
                    pass
            except IndexError:
                continue

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

            keys = list(node.keys())
            neighbours = self.get_neighbours(x, y)
            counts = np.array(list(node.values()), dtype=np.float32)
            key_idxs = np.arange(len(keys))
            ps = counts / counts.sum()
            np.random.shuffle(neighbours)
            for neighbour in neighbours:
                try:
                    col_idx = np.random.choice(key_idxs, p=ps)
                    if neighbour not in coloured:
                            img[neighbour] = keys[col_idx]
                except IndexError:
                    pass
                except ValueError:
                    continue
                if 0 <= neighbour[0] < width and 0 <= neighbour[1] < height:
                    stack.append(neighbour)
        writer.release()
        return Image.fromarray(img_out)


if __name__ == "__main__":
    import sys

    chain = MarkovChain(bucket_size=16)
    fnames = ['jackieo.jpg']
    print(fnames)
    for fname in fnames:
        im = Image.open(fname)
        # im.show()
        print("Training " + fname)
        chain.train(im)
    # print chain.weights
    print("\nGenerating")
    chain.generate().show()
