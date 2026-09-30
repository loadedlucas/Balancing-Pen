import cv2
from copy import deepcopy
import numpy as np
from datetime import datetime
from pseyepy import Camera

# Initialize PS3 Eye camera
width = 320
height = 240
samplesize = 5 # Must be odd
Center = height//2
THRESHOLD = 0.3

def GetCamera():
    return Camera(fps=60, resolution=Camera.RES_SMALL)
def TakePhoto(cam):
    return cam.read()
def WriteImage(frame, location):
    x = cv2.imwrite(location + f"/{datetime.now().strftime("%H%M%S")}.png", frame)
    return x
def ReadImage(filepath):
    return cv2.imread(filepath)
def FindQRPoints(frame, threshold, bounds=[0, 0, width, height]):
    myframe = np.array(deepcopy(frame), dtype = np.float32)
    myframe = np.array([[myframe[y][x][0] + myframe[y][x][1] + myframe[y][x][2] for x in range(width)] for y in range(height)], dtype=np.float32)
    myframe /= np.max(myframe)
    for x in range(width):
        for y in range(height):
            if(x < bounds[0] or x >= bounds[2] or y < bounds[1] or y >= bounds [3]):
                myframe[y][x] = 1
    DotCenters = {0:[0, 0]}
    minvalue = 0
    for y in range(height):
        for x in range(width):
            foundpoints = []
            FloodFill(myframe, x, y, foundpoints, threshold)
            Value = len(foundpoints)
            if(Value < minvalue or Value == 0):
                continue
            else:
                foundpoints = np.array(foundpoints)
                Center = np.average(foundpoints, axis=0)
                if(len(DotCenters) > 2): DotCenters.pop(minvalue)
                minvalue = min(DotCenters.keys())
                DotCenters[Value] = Center
    return list(DotCenters.values())

def FloodFill(frame, x, y, foundpoints, threshold):
    if frame[y][x] < threshold:
        foundpoints.append([x,y])
        frame[y][x] = 1
        if(x+1 < width):
            FloodFill(frame, x+1, y, foundpoints, threshold)
        if(y+1 < height):
            FloodFill(frame, x, y+1, foundpoints, threshold)
        if(x-1 >= 0):
            FloodFill(frame, x-1, y, foundpoints, threshold)
    return
def GetPencilPosIndex(frame, VertPixOffset):
    localCenter = Center + VertPixOffset
    lines = np.array(frame[localCenter-samplesize//2:localCenter+samplesize//2], dtype=int)
    print(len(lines))
    line = np.zeros(width, dtype=int)
    for j in range(width):
        for i in range(len(lines)):
            line[j] += sum(lines[i][j]) 
        line[j] /= samplesize
    print(line)
    inPencil = False
    PencilPositions = []
    PositionWeights = []
    threshold = THRESHOLD * max(line) # Arbitrary (TODO)
    CurrentPencilWidth = 0
    for i in range(width):
        if(line[i] > threshold):
            if(inPencil):
                inPencil = False
                PencilPositions[-1] /= CurrentPencilWidth
                PositionWeights.append(CurrentPencilWidth)
                CurrentPencilWidth = 0
        if(line[i] <= threshold):
            if(not inPencil):
                inPencil = True
                PencilPositions.append(i)
            else:
                PencilPositions[-1] += i
                if(i == width-1):
                    PencilPositions[-1] /= CurrentPencilWidth
                    PositionWeights.append(CurrentPencilWidth)
            CurrentPencilWidth += 1
    if(len(PencilPositions) == 0):
        print("No Pencil Detected")
        time = datetime.now()
        cv2.imwrite("PencilNotFound.jpg", frame)
        return width // 2
    Position = PencilPositions[np.argmax(PositionWeights)]
    return width - Position # BECAUSE CAMERAS ARE UPSIDE DOWN WE REVERSE THE INDEX TO RETURN TO CORRECT INDEX I THINK (TODO)