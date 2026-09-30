import math
unit = (1,0)
def Abs(p):
    return math.sqrt(p[0] * p[0] + p[1] * p[1])
def Dot(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]
def Dif(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])
def GetAngles(p, m, r):
    alpha = math.acos((Dot(Dif(m, p), unit)) / Abs(Dif(m, p)))
    if(p[1] < 0):
        alpha *= -1
    gamma = math.acos((2*r**2-Abs(Dif(m, p))**2)/(2*r**2))
    beta = (math.pi - gamma) / 2
    return (alpha-beta, alpha+beta)
def NewAngles(motorp1, motorp2, motorangles, targetpos, armlength):
    angles1 = GetAngles(targetpos, motorp1, armlength)
    angles2 = GetAngles(targetpos, motorp2, armlength)
    maxdist1 = max(abs((angles1[0]-motorangles[0]) % (2*math.pi)), abs((angles1[1]-motorangles[1]) % (2*math.pi)))
    maxdist2 = max(abs((angles2[0]-motorangles[0]) % (2*math.pi)), abs((angles2[1]-motorangles[1]) % (2*math.pi)))
    if(maxdist1 < maxdist2):
        return angles1
    else:
        return angles2


d = 0.2
r = 1.0

p = (1.5,1.0)
m1 = (0, 0)
m2 = (d, 0)
angles = NewAngles(m1, m2, (0,0), p, r)
print(angles)
print(Abs(Dif(p, (r*math.cos(angles[0]), r*math.sin(angles[0])))))
print(Abs(Dif(p, (r*math.cos(angles[1]), r*math.sin(angles[1])))))


