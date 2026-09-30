import Control
import numpy as np
from scipy.optimize import least_squares
import sympy as sy
import CamUsage
from matplotlib import pyplot
from cv2 import imwrite
from cv2 import imread

def CheckPosError(frame1, frame2, x, y):
    expectedPos = (3 * x, 3 * y)
    CalculatedPos, Line = Control.GetPositionFromTwoPhotos(frame1, frame2)
    return np.array([CalculatedPos[0] - expectedPos[0], CalculatedPos[1] - expectedPos[1]])
def CheckDirError(frame1, frame2, x, y):
     CalculatedPos, Line = Control.GetPositionFromTwoPhotos(frame1, frame2)
     expectedDir = Line[1]
     return 1-abs(np.dot(np.array(Line[1]), np.array(expectedDir)))
def CheckCam_2DAngles(frame1, frame2, x, y, isCam1):
    C1P1 = CamUsage.GetPencilPosIndex(frame1, Control.C1UIndexOffset)
    C1P2 = CamUsage.GetPencilPosIndex(frame1, Control.C1DIndexOffset)
    C2P1 = CamUsage.GetPencilPosIndex(frame2, Control.C2UIndexOffset)
    C2P2 = CamUsage.GetPencilPosIndex(frame2, Control.C2DIndexOffset)
    C1DX = C1P2 - C1P1
    C2DX = C2P2 - C2P1
    C1DY = Control.C1DIndexOffset - Control.C1UIndexOffset
    C2DY = Control.C2DIndexOffset - Control.C2UIndexOffset
    if isCam1: return np.atan(C1DX / C1DY) 
    else: return np.atan(C2DX / C2DY)
def CheckCam1_2DAngles(frame1, frame2, x, y):
    return CheckCam_2DAngles(frame1, frame2, x, y, True) * 180 / np.pi
def CheckCam2_2DAngles(frame1, frame2, x, y):
    return CheckCam_2DAngles(frame1, frame2, x, y, False) * 180 / np.pi
def ForAllFrames(Func):
    Data = []
    for x in range(6):
        Data.append([])
        for y in range(6):
            frame1 = imread(f"SquareCalibration/C1_{x}-{y}.jpg")
            frame2 = imread(f"SquareCalibration/C2_{x}-{y}.jpg")
            Data[x].append(Func(frame1, frame2, x,y))
    return np.array(Data)

PosErrors = ForAllFrames(CheckPosError)
DirErrors = ForAllFrames(CheckDirError)
C1Angles = ForAllFrames(CheckCam1_2DAngles)
C2Angles = ForAllFrames(CheckCam2_2DAngles)

CalculatedPos = [np.array([3 * x + PosErrors[x][y][0], 3 * y + PosErrors[x][y][1]]) for x in range(6) for y in range(6)]
ExpectedPos = [np.array([3 * x, 3 * y]) for x in range(6) for y in range(6)]

def ErrorFromTransform(params):
    alpha, k, dx, dy = params
    MyMatrix = sy.Matrix([[k * np.cos(alpha), k * np.sin(alpha), 0], [k * -np.sin(alpha), k * np.cos(alpha), 0], [dx, dy, 1]])
    errors = np.zeros(36)
    for i, cpos in enumerate(CalculatedPos):
        if(i == 0): continue
        transformedcpos = MyMatrix * sy.Matrix([cpos[0], cpos[1], 1])
        Offset = sy.Matrix([transformedcpos[0] - ExpectedPos[i][0], transformedcpos[1] - ExpectedPos[i][1]])
        errors[i] = Offset.norm()
    return errors

sol = least_squares(ErrorFromTransform, [0, 1, 0, 0])
alpha, k, dx, dy = sy.symbols('alpha, k, dx, dy', real=True)
MyMatrix = sy.Matrix([[k * sy.cos(alpha), k * sy.sin(alpha), 0], [k * -sy.sin(alpha), k * sy.cos(alpha), 0], [dx, dy, 1]])
MyMatrix = MyMatrix.subs(dict(zip([alpha, k, dx, dy], sol.x))).evalf()
TransformedPositions = []
for pos in CalculatedPos:
    newpos = MyMatrix * sy.Matrix([pos[0], pos[1], 1])
    TransformedPositions.append(np.array([newpos[0], newpos[1]]))
TransformedPositions = np.array(TransformedPositions)
print(sol.x)

a = [3 * x for x in range(6) for y in range(6)] + [3 * x + PosErrors[x][y][0] for x in range(6) for y in range(6)] + [TransformedPositions[x][0] for x in range(36)]
b = [3 * y for x in range(6) for y in range(6)] + [3 * y + PosErrors[x][y][1] for x in range(6) for y in range(6)] + [TransformedPositions[x][1] for x in range(36)]
XCoords =  np.array(a)
YCoords = np.array(b)

data = {'a': XCoords, 'b': YCoords}
pyplot.scatter('a', 'b', c=[1 for _ in range(36)] + [0 for _ in range(36)] + [0.5 for _ in range(36)],data=data)
pyplot.show()
#pyplot.scatter(XCoords, YCoords, )
#pyplot.show()

print(np.average(C1Angles))
print(np.average(C2Angles))

print(PosErrors)
print(np.sum(PosErrors) / 36)
print(np.sum([[np.linalg.norm(PosErrors[x][y]) for x in range(6)] for y in range(6)]) / 36)
