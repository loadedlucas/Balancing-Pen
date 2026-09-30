import cv2
import numpy as np
from datetime import datetime

camera = cv2.VideoCapture(0)
print("Camera initialised")

width = 320
height = 240

camera.set(3, width)
camera.set(4, height)

return_value, image = camera.read() # First image takes longer
cv2.imwrite("identifyPencil.png", image)
exit()
t = datetime.now()

samplesize = 5 # Must be odd
Center = height//2

lines = np.array(image[Center-samplesize//2:Center+samplesize//2], dtype=int)
print(len(lines))
line = np.zeros(width, dtype=int)
for j in range(width):
    for i in range(len(lines)):
        line[j] += sum(lines[i][j]) 
    line [j] /= samplesize
print(line)
inPencil = False
PencilPositions = []
PositionWeights = []
threshold = 0.2 * max(line)
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
Position = PencilPositions[np.argmax(PositionWeights)]
print(PencilPositions)
print(Position)
print(f"Time Required: {datetime.now()-t}")
for pos in PencilPositions:
    for i in range(height):
        for j in range(5):
            image[i, (int(pos) + j) % width] = [255,0,0]
            if(np.abs(height - Center) < 5):
                image[i, (int(pos) + j) % width] = [0,0,0]
cv2.imwrite("identifyPencil.png", image)
        
        
        
        
        
        
        
