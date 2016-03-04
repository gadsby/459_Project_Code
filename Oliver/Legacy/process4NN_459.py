# DATA GATHERING LIBRARY

def processFile (filename, last=10, next=5):

    """Returns the inputs (last m states) and outputs (next n states) of a given file as a numpy array."""

    import numpy as np

    blockLength = last + next

    rawArray = np.genfromtxt(filename, delimiter=',', skip_header=1)
    (numStates, dataWidth) = rawArray.shape

    inputs = []
    outputs = []

    for i in range( numStates - blockLength ):

        temp = rawArray[ i : i + blockLength ]

        inputTemp = temp[:last]
        np.reshape( inputTemp, (1, dataWidth*last) )
        inputs.append( inputTemp )

        outputTemp = temp[last:]
        #TODO: remove torques and other data here, don't need in outputs
        outputWidth = dataWidth - 0 #TODO: obviously change this when we know how many columns to remove, related to above
        np.reshape( outputTemp, (1, outputWidth*next) )
        outputs.append( outputTemp )

    if len(inputs) != 0:
        inputs = np.vstack( inputs )
    else:
        inputs = np.array( inputs )

    if len(outputs) != 0:
        outputs = np.vstack( outputs ) 
    else:
        outputs = np.array( outputs )

    return (inputs, outputs)



def processAllFiles (fileList, last=10, next=5):
    """Steps through a passed file list and returns all inputs and outputs."""

    import numpy as np

    inputs = []
    outputs = []

    for file in fileList:

        (inputTemp, outputTemp) = processFile (file, last, next)

        inputs.append( inputTemp )
        outputs.append( outputTemp )

    if len(inputs) != 0:
        inputs = np.vstack( inputs )
    else:
        inputs = np.array( inputs )

    if len(outputs) != 0:
        outputs = np.vstack( outputs ) 
    else:
        outputs = np.array( outputs )   

    return (inputs, outputs)



def fileData(numFiles, mostRecent=True, verbose=False):
    """Returns a filelist containing the specified number of files, or all files if not enough are found."""

    import os
    import numpy as np

    if type(numFiles) == int:
        if numFiles < 0:
            exit()
    elif numFiles != 'all':
        exit()

    #TODO: will be set by file structure
    sourcePath = '/Users/olivergadsby/Desktop/Example'

    filesSeen = 0

    for (path, dirs, filenames) in os.walk(sourcePath, topdown=True):

        filenames = [path+'/'+f for f in filenames if f[0] != '.' and f[-4:] == '.npy']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        dirs.sort(reverse=mostRecent)
        filenames.sort(reverse=mostRecent)

        if numFiles != 'all':
            filenames = filenames[:numFiles]

        if verbose:
            print( '{}/{} Requested Files Found\n'.format( len(filenames),numFiles ) )
        
        return filenames



if __name__ == "__main__":

    print(processFile.__doc__)
    print(processAllFiles.__doc__)
    print(fileData.__doc__)

    last, next = 10, 5
    fileList = fileData('all', mostRecent=True, verbose=False)

    (inputs, outputs) = processAllFiles(fileList, last, next)

    print( fileList )
    print( inputs.shape )
    print( outputs.shape )

    # now able to feed into neural network here