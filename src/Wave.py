import numpy as np

#-------------------------------------------------------------
class Wave:
#-------------------------------------------------------------
    
    def __init__(self,scene):
        self.v = 6000                               # Initialise la vitesse de l'onde à 6000 m/s
        self.f = 10                                 # Initialise la fréquence de l'onde à 10 Hz
        self.T = 1/self.f                           # Calcule la période par défaut de l'onde à partir de sa fréquence.
        self.lambda0 = self.T * self.v              # Calcule la longueur d'onde de l'onde à partir de sa période et de sa vitesse.
        self.phase = 0
        self.amplitude = 1
        self.scene = scene
        scene.waves.append(self)
        self.waveArray = []

    def setPhase(self,valueInDegree):
        self.phase = valueInDegree * np.pi / 180

    def setSpeed(self,v):
        self.v = v
        self.lambda0 = self.v * self.T
        
    def setFrequence(self,f):
        self.f = f
        self.T = 1.0/self.f
        self.lambda0 = self.v * self.T

    def calculateWave(self,X,t):
        k = 2*np.pi / self.lambda0                  # nombre d'onde
        omega = 2*np.pi / self.T                    # pulsation
        self.waveArray = self.amplitude * np.sin(k*X - omega*t + self.phase)


    def displayInfo(self):
        print("\tv           {}".format(self.v))
        print("\tf           {}".format(self.f))
        print("\tlambda      {}".format(self.lambda0))
        print("\tamplitude   {}".format(self.amplitude))
        print("\tphase       {}".format(self.phase))
