import time

def timeLoop(double endTime):
    cdef float timeStart
    timeStart = time.clock()

    cdef float elapsed
    elapsed = 0

    cdef int loopCount
    loopCount = 0

    while elapsed < endTime:
            elapsed = time.clock() - timeStart
            loopCount += 1
            
    return loopCount