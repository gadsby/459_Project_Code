import numpy as np
import scipy

#tunable
numberOfTargets = 10000

torqueList = #read torques from csv(?) file into size:<num_targs,2> array

#break torques into vectors of torques for each motor

for i in torqueList.shape(1):
    torqueVec1[i] = torqueList(i,1)
    torqueVec2[i] = torqueList(i,2)

x = np.linspace(0,fallTime,torqueList.shape(1))

# interpolate torque profile with splines

func1 = scipy.interpolate.interp1d(x,torqueVec1,kind='cubic')
func2 = scipy.interpolate.interp1d(x,torqueVec2,kind='cubic')

# access torques somewhere on the spline profile at whatever sampling rate we desire

for k in numberOfTargets:
    target1[k] = func1(k*resolution)
    target2[k] = func2(k*resolution)

def targets(k):
    return [target1[k],target2[k]]