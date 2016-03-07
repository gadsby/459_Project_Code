import numpy as np
from scipy import interpolate

import config


class torqueListManager:

	def __init__(self, torqueProfilePath):
		self.torqueProfilePath = torqueProfilePath
		self.genTorqueList()


	def genTorqueList(self):

		time, kneeTorques, hipTorques = np.genfromtxt(self.torqueProfilePath, delimiter=',', unpack=True, usecols=[0,7,8])

		self.fallTime = time[-1]
		pointsPerSecond = 10000

		self.resolution = 1.0 / pointsPerSecond
		self.numberOfTargets = int(self.fallTime*pointsPerSecond)

		kneeTorques_interpolator = interpolate.interp1d(time, kneeTorques, kind='cubic')
		hipTorques_interpolator = interpolate.interp1d(time, hipTorques, kind='cubic')

		self.time_EXPANDED = np.arange(time[0], time[-1]+self.resolution, self.resolution)
		self.kneeTorque_EXPANDED = kneeTorques_interpolator(self.time_EXPANDED)
		self.hipTorque_EXPANDED = hipTorques_interpolator(self.time_EXPANDED)

		self.timeLimit = self.time_EXPANDED[-1]

		print('\tTorque Profile: {}'.format(config.torqueListPath))
		print('\tResolution (s): {}'.format(self.resolution))
		print('\tPoints Per Second: {}'.format(pointsPerSecond))
		print('\tFalltime (s): {}'.format(self.fallTime))
		print('\tResolution Multiplier: {}\n'.format(1.0*len(self.time_EXPANDED)/len(time)))


	def torqueGoals(self, timeVal):
		index = int(timeVal/self.resolution)
		if timeVal > self.timeLimit:
			return (0,0)
		return self.kneeTorque_EXPANDED[index], self.hipTorque_EXPANDED[index]

