from math import *
import CamUsage
import numpy as np
np.set_printoptions(precision=2, suppress=True, legacy="1.13")
UNIT = (1, 0)
def Abs(p):
    return sqrt(p[0] * p[0] + p[1] * p[1])
def Dot(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]
def Dif(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])
def Z_Rotation_Matrix(theta):
    c, s = cos(theta), sin(theta)
    return np.matrix([[c, s, 0], [-s, c, 0], [0, 0, 1]])
def Y_to_Z():
    return np.matrix([[0,0,1],[1,0,0],[0,1,0]])
def X_to_Z():
    return np.matrix([[0,1,0],[0,0,1],[1,0,0]])

# Takes pixel coordinates of points where the pencil was detected and returns a position & orientation of the pencil in real world space (ideally).

CALIBRATION_VALS = [16.5, 37, 57.5, 78, 98.5, 119, 139.5, 160, 180.5, 201, 221.5, 242, 262.5, 283, 303.5] # Pixel indices at which a 1cm horizontal shift occurs at 13.5cm depth. 
# Units: cm, degrees. Can be changed at will. 
CAMERA1POS = (7.5, -13.5, 20) #APPROX VALUES
CAMERA1ANGLE = 0 # Relative rotation along Z axis

CAMERA2POS = (-13.5, 7.5, 20)
CAMERA2ZANGLE = 1.8 #Relative Rotation along Z axis

HORIZONTALFOV = 63
VERTFOV = 49.5

PLATFORMHEIGHT = 0
# First and last indices are ~limits of camera FOV
# Center index is 0cm offset (aka straight ahead). 
def HorizontalFromPixel(pixindex):
    i = 0
    if(pixindex > max(CALIBRATION_VALS)): return 7.5
    if(pixindex < min(CALIBRATION_VALS)): return -7.5
    while(pixindex > CALIBRATION_VALS[i]):
        i += 1
    CalibrationDict = {}
    for q, val in enumerate(CALIBRATION_VALS):
        CalibrationDict[val] = q - len(CALIBRATION_VALS) // 2
    l = CALIBRATION_VALS[i-1]
    r = CALIBRATION_VALS[i]
    pixelvalue = (1- ((pixindex-l)/(r-l))) * CalibrationDict[l] + (1 - ((r-pixindex)/(r-l))) * CalibrationDict[r] # LERP
    return pixelvalue

def UnitVecFromPixelCoords(x, y): # Camera pointing in local space towards +y
    MinX = -tan(HORIZONTALFOV / 2 * np.pi / 180)
    MaxX = tan(HORIZONTALFOV / 2 * np.pi / 180)
    MinZ = -tan(VERTFOV / 2 * np.pi / 180)
    MaxZ = tan(VERTFOV / 2 * np.pi / 180)
    W = CamUsage.width
    H = CamUsage.height
    XRatio = x / W
    ZRatio = y / H
    vec = np.array([MinX * (1-XRatio) + MaxX * XRatio, 1, MinZ * (1-ZRatio) + MaxZ * ZRatio])
    vec /= np.linalg.norm(vec)
    return vec

def PlaneFromTwoVectors(p, v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    n = np.cross(v1, v2)
    n /= np.linalg.norm(n)
    return (np.array(p), n)

def PlanePlaneIntersection(plane1, plane2):
    p1, n1 = (plane1[0], plane1[1])
    p2, n2 = (plane2[0], plane2[1])
    v = np.cross(n1, n2)
    c1 = (np.dot(n1, p1) - np.dot(n2, p2) * np.dot(n1, n2)) / (1 - np.pow(np.dot(n1, n2), 2))
    c2 = (np.dot(n2, p2) - np.dot(n1, p1) * np.dot(n1, n2)) / (1 - np.pow(np.dot(n1, n2), 2))
    return (c1*n1 + c2*n2, v)

def PencilPositionFromVectors_Plane(c1v1, c1v2, c2v1, c2v2):
    Plane1 = PlaneFromTwoVectors(CAMERA1POS, c1v1, c1v2)
    Plane2 = PlaneFromTwoVectors(CAMERA2POS, c2v1, c2v2)
    print(f"P1: {Plane1}")
    print(f"P2: {Plane2}")
    PencilLine = PlanePlaneIntersection(Plane1, Plane2)
    print(f"PencilLine: {PencilLine}")
    PencilHeadPosition = np.subtract(PencilLine[0], ((PencilLine[0][2]-PLATFORMHEIGHT)/PencilLine[1][2]) * PencilLine[1])
    PencilHeadPosition = (PencilHeadPosition[0], PencilHeadPosition[1]) # z should be zero
    print(f"PencilHead: {PencilHeadPosition}")
    return(PencilHeadPosition, PencilLine)
def LocalToWorldSpace(v, Transform):
    NotImplementedError
def GetUnitVectorsFromPixels(cam1pix1, cam1pix2, cam2pix1, cam2pix2, UpOffset, DownOffset):
    c1v1 = np.array([HorizontalFromPixel(cam1pix1), 13.5, UpOffset])
    c1v2 = np.array([HorizontalFromPixel(cam1pix2), 13.5, DownOffset])
    c2v1= np.array([13.5, -HorizontalFromPixel(cam2pix1), UpOffset])
    c2v2 = np.array([13.5, -HorizontalFromPixel(cam2pix2), DownOffset])
    return c1v1, c1v2, c2v1, c2v2

def PencilPositionFromPixels_Plane(cam1pix1, cam1pix2, cam2pix1, cam2pix2, UpOffset, DownOffset):
    c1v1, c1v2, c2v1, c2v2 = GetUnitVectorsFromPixels(cam1pix1, cam1pix2, cam2pix1, cam2pix2, UpOffset, DownOffset)
    print(f"1a: {c1v1}, 1b: {c1v2}, 2a: {c2v1}, 2b: {c2v2}")
    return PencilPositionFromVectors_Plane(c1v1, c1v2, c2v1, c2v2)

if(__name__=="__main__"):
    print(PencilPositionFromVectors_Plane((30, 15), (30, -15), (-30, 15), (-30, -15)))