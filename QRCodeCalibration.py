import sympy as sy
import scipy
import numpy as np
from FindPencil import *

C1V = np.array([0, 8.8, 18.5, 1]) # replace with measured values
C1W = np.array([0, 11.2, 26.5, 1])
C1R = np.array([0, 6.4, 26.5, 1])


def GetUnitVectorsFromPixels(p1, p2, p3): 
    v = UnitVecFromPixelCoords(p1[0], p1[1])
    w = UnitVecFromPixelCoords(p2[0], p2[1])
    r = UnitVecFromPixelCoords(p3[0], p3[1])
    
    return v, w, r

def FindLengths_Scipy(v, w, r):
    l1 = np.linalg.norm(C1V - C1W)
    l2 = np.linalg.norm(C1R - C1W)
    
    def equations(variables):
        a, b, c = variables
        
        eq1 = np.dot((a*v) - (b*w), (c*r) - (b*w)) - np.cos(np.radians(73.3)) * l1 * l2
        eq2 = np.linalg.norm(a*v - b*w) - l1
        eq3 = np.linalg.norm(c*r - b*w) - l2
        
        return [eq1, eq2, eq3]
    
    solution = scipy.optimize.root(equations, [13.68, 14.13, 13.68])
    print(solution)
    return solution.x

def FindLengths(v, w, r):
    a, b, c = sy.symbols('a, b, c')
    vsy = sy.Matrix(v)
    wsy = sy.Matrix(w)
    rsy = sy.Matrix(r)
    eq1 = sy.Eq((a*vsy - b*wsy).dot(c*rsy - b*wsy), (sy.cos(73.3 * sy.pi / 180) * (C1V - C1W).norm() * (C1V - C1R).norm()).evalf()) # p2p1 are at a 73.3° angle to p2p3 in world space
    eq2 = sy.Eq((a * vsy - b * wsy).dot((a * vsy - b * wsy)), (C1V - C1W).norm().evalf() * (C1V - C1W).norm().evalf())
    eq3 = sy.Eq((c * rsy - b * wsy).dot((c * rsy - b * wsy)), (C1V - C1R).norm().evalf() * (C1V - C1R).norm().evalf())
    sol = sy.nsolve([eq1, eq2, eq3], [a, b, c], [10, 10, 10])
    print(sol)
    return np.array([sol[0], sol[1], sol[2]])
    
def GetQRPointsLocal(p1, p2, p3):
    v,w,r = GetUnitVectorsFromPixels(p1,p2,p3)
    a,b,c = FindLengths_Scipy(v,w,r)
    return [a * v, b * w, c * r]

def GetLocalToGlobalTransform(LV, LW, LR):
    v_h = np.array([*LV, 1])
    w_h = np.array([*LW, 1])
    r_h = np.array([*LR, 1])
    def equations(variables):
        phi, theta, psi, x,y,z = variables
        R = scipy.spatial.transform.Rotation.from_euler("xyz", [phi, theta, psi])
        A = np.eye(4)
        A[:3, :3] = R.as_matrix()
        A[:3, 3] = np.array([x, y, z])
        eq1 = np.linalg.norm(np.matmul(A, v_h) - C1V)
        eq2 = np.linalg.norm(np.matmul(A, w_h) - C1W)
        eq3 = np.linalg.norm(np.matmul(A, r_h) - C1R)
        return [eq1, eq2, eq3, 0, 0, 0]

    sol = scipy.optimize.root(equations, [0, 0, 0, 0, 0, 0])
    phi,theta,psi,x,y,z = sol.x

    R = scipy.spatial.transform.Rotation.from_euler("xyz", [phi, theta, psi])
    A = np.eye(4)
    A[:3, :3] = R.as_matrix()
    A[:3, 3] = np.array([x, y, z])
    return A

if(__name__ == "__main__"):
    #print(GetLocalToGlobalTransform([-9, 10, 0], [-7.5, 10, 0], [-7.5, 10, -1.5]))
    myframe = CamUsage.ReadImage("QRCalibrationImages/163454.png")
    #CamUsage.WriteImage(myframe, "QRCalibrationImages")
    points2D = CamUsage.FindQRPoints(myframe, 0.8, bounds=(70, 0, 270, 230))
    print(f"Points2D: \n {points2D}")
    print(GetUnitVectorsFromPixels(*points2D))
    #points3D = GetQRPointsLocal(*points2D)
    points3D = [np.array([0, 13.5, -4]), np.array([2.4, 13.5, 4]), np.array([-2.4, 13.5, 4])]
    print(f"Points: \n {points3D}")
    Transform = GetLocalToGlobalTransform(*points3D)
    print(f"Transform: \n {Transform}")
    print(f"CameraPos: \n {np.matmul(Transform, np.array([0, 0, 0, 1]))}")
    print(f"CameraViewDir: \n {np.matmul(Transform[:3, :3], np.array([0, 1, 0]))}")
    

