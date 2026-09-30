import CamUsage
import FindPencil
import numpy as np
from cv2 import imwrite
def Dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
#import MotorControl
UpOffset, C1UIndexOffset, C2UIndexOffset = 1.2, 29, 29
DownOffset, C1DIndexOffset, C2DIndexOffset = -3.6, -74, -74
def GetPositionFromCams(cam):
    # For Running:
    frames, timestamp = CamUsage.TakePhoto(cam)
    frame2, frame1 = frames[0], frames[1]

    #For Testing:
    #imwrite(f"SquareCalibration/C1_5-5.jpg", frame1)
    #imwrite(f"SquareCalibration/C2_5-5.jpg", frame2)
    # Setup values, must be calibrated.
    return (*GetPositionFromTwoPhotos(frame1, frame2), timestamp)

def GetPositionFromTwoPhotos(frame1, frame2):
    C1P1 = CamUsage.GetPencilPosIndex(frame1, C1UIndexOffset)
    C1P2 = CamUsage.GetPencilPosIndex(frame1, C1DIndexOffset)

    C2P1 = CamUsage.GetPencilPosIndex(frame2, C2UIndexOffset)
    C2P2 = CamUsage.GetPencilPosIndex(frame2, C2DIndexOffset)
    print(f"C1P1 = {C1P1}, C1P2 = {C1P2}, C2P1 = {C2P1}, C2P2 = {C2P2}")
    GroundPos, Direction = FindPencil.PencilPositionFromPixels_Plane(C1P1, C1P2, C2P1, C2P2, UpOffset, DownOffset)
    return GroundPos, Direction


# ENTRY POINT ====================================================================================================================================================

if(__name__ == "__main__"):
    cam = CamUsage.GetCamera()
    #m1 = MotorControl.MotorController(1, -1, -1, (-1, -1, -1), 0, -30, 100)
    #m2 = MotorControl.MotorController(2, -1, -1, (-1, -1, -1), 0, -100, 30)

    GroundPos, Direction, timestamp = GetPositionFromCams(cam)
""" Approx while loop structure:
LastGroundPos, LastDirection = GetPositionFromCams(cam)
myLinkage.MoveTo(LastGroundPos)
while(balancing_Pencil):
    NewGroundPos, NewDirection, timestamp = GetPositionFromCams(cam)
    Velocity = Whatever
    AngularVelocity = Whatever
    target = FindNextHeadPos(Velocity, AngularVelocity, NewGroundPos, NewDirection)
    myLinkage.MoveTo(target)
    curtime = datetime.now()
    if(curtime - timestamp > 0.015): continue
    sleep(0.015 - curtime + timestamp)
"""