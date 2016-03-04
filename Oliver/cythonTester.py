import cythonControl
import time

def timeLoop(endTime):
    timeStart = time.clock()
    elapsed = 0
    loopCount = 0

    while time.clock() - timeStart < endTime:
            loopCount += 1
            
    return loopCount



endTime = 1
cythonResult = cythonControl.timeLoop(endTime)
pythonResult = timeLoop(endTime)


print('Cython Result: {} Loops in {} seconds'.format(cythonResult, endTime))
print('Python Result: {} Loops in {} seconds'.format(pythonResult, endTime))

print('Speed Ratio: {} faster with Cython'.format(cythonResult/pythonResult))