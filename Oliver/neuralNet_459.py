# this is to be used for making, manipulating, and training the neural net models

# PYTHON LIBRARIES
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import numpy as np

# PROJECT LIBRARIES
import getFiles

loadedData = getFiles.fileData('all', mostRecent=True, verbose=False)


inputs = np.ones((20,10))	## temporary, valid until we get real data (or sim data)

# set seed for reproducibility

model = Sequential()
model.add(Dense(10, init='uniform', input_dim=10))
#model.add(Activation('softmax')) ## need new activation because softmax gives probabilities
# add another layer or two? maybe depend on input size?
model.compile(loss='mse', optimizer='sgd') #mse should be fine, find out what sgd is

model.fit(inputs, inputs, nb_epoch=500, batch_size=10, verbose=False) #epochs can be tweaked, probably want validation data too, just use %

print( model.predict(np.ones((1,10))) )

# do stuff with results


exit()


# for every fall dataset, create function that creates data for last n states on one row, next m on another after passing the dataset, n, m
# repeat for every data set to get larger set
# problem: will be more biased towards middle behavior which will have duplicate points, but this is the chaotic part anyway