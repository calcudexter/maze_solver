from PIL import Image
import numpy as np
import random
import cv2

img = Image.open("mazes/processed_maze.png")
maze = img.load()
dim = (3*img.size[0]//4, 3*img.size[1]//4)
video = cv2.VideoWriter('solving_process.avi', 0, 50, dim)
video.write(cv2.resize(np.asarray(img), dim, interpolation=cv2.INTER_AREA))

def locs(img):
    img = np.asarray(img)

    start = (255, 0, 0) # Red color states starting location
    end = (0, 0, 255) # Blue color states the ending location

    Ystart, Xstart = np.where(np.all(img==start, axis=2))
    Yend, Xend = np.where(np.all(img==end, axis=2))
    
    start_loc = (Xstart[0], Ystart[0])
    end_loc = [(Xend[i], Yend[i]) for i in range(len(Xend))]

    return start_loc, end_loc
    # return start_loc

def show(img):
    imgBig = img.resize((600, 600))
    imgBig.show()

def solve(start, end, img, maze):
    width, height = img.size
    
    solved = False
    curr = start
    array = np.asarray(img)

    path = []
    intersections = []
    ind = 0
    while not solved:
        poss = []
        neighbors = [(curr[0]-1, curr[1]),
                     (curr[0]+1, curr[1]),
                     (curr[0], curr[1]-1),
                     (curr[0], curr[1]+1)]

        for move in neighbors:
            if (move[0] >= width) or (move[0] < 0):
                continue
            if (move[1] >= height) or (move[1] < 0):
                continue
            # if end == move:
            if move in end:
                solved = True
            if ((maze[move]>=(200,200,200) or maze[move] == (0, 0, 255)) and move != start):
                # First comparison gets passed by red and white; second by blue
                poss.append(move)

        if len(poss) >= 2:
            if curr not in intersections:
                intersections.append(curr)

        if len(poss) == 0:
            # Executed at dead ends or path being backtracked
            intersections_rev = intersections[::-1]
            for i in intersections_rev:
                if i != curr:
                    curr = i
                    intersections.pop(intersections.index(i))

                    break
            path = path[:path.index(curr)]

        else:
            curr = random.choice(poss)
        
        path.append(curr)
        array[curr[1], curr[0]] = (0, 255, 0)
        if(ind%25 == 0):
            video.write(cv2.resize(array, dim, interpolation=cv2.INTER_AREA))

        img = Image.fromarray(array)
        maze = img.load()
        ind += 1
    j = 0
    print(len(path))
    for p in path:
        array[p[1], p[0]] = (255, 0, 0)
        if(j%25 == 0):
            video.write(cv2.resize(array, dim, interpolation=cv2.INTER_AREA))
        j += 1
    img = Image.fromarray(array)
    img.save('image1.png')

start, end = locs(img)
solve(start, end, img, maze)

cv2.destroyAllWindows()
video.release()