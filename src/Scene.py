import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from moviepy.editor import ImageSequenceClip
from functools import partial
import multiprocessing
import copy
import re

from Wave import Wave


#-------------------------------------------------------------
class Scene:
#-------------------------------------------------------------
        
    def __init__(self):
        self.xmin = 0
        self.xmax = 6000
        self.tmin = 0
        self.tmax = 2/3
        self.nx = 2000
        self.fps = 30
        self.waves = []    
        self.x0 = 0
        self.imagesFolderPath = "images"
        self.animationsFolderPath = "animations"
        self.isParallelizing = False
        self.nProcessors = 1
        self.na = 0
        self.selectedWave1 = None
        self.selectedWave2 = None
        self.diagramType = None

        
    #---------------------------------------------------------------------------
    def prepare(self):
    #---------------------------------------------------------------------------
        self.X  = np.linspace(self.xmin, self.xmax, self.nx)
        self.na = int((self.tmax-self.tmin)*(10*self.fps))

    #---------------------------------------------------------------------------
    def displayInfo(self):
    #---------------------------------------------------------------------------
        print ("nx           {}".format(self.nx))    
        print ("na           {}".format(self.na))    
        print ("xmin         {}".format(self.xmin))    
        print ("xmax         {}".format(self.xmax))    
        print ("tmin         {}".format(self.tmin))    
        print ("tmax         {}".format(self.tmax))    
        print ("Parallezing  {}".format(self.isParallelizing))
        print ("Diagram Type {}".format(self.diagramType))
        k = 1
        for wave in self.waves:
            print ("Wave {}".format(k))
            wave.displayInfo()
            k += 1

    #---------------------------------------------------------------------------
    def selectWaves(self,wave1,wave2):
    #---------------------------------------------------------------------------
        self.selectedWave1 = wave1
        self.selectedWave2 = wave2
        
    #---------------------------------------------------------------------------
    def calculateWaves(self,t):
    #---------------------------------------------------------------------------
        for wave in self.waves:
            wave.calculateWave(self.X,t)

    #---------------------------------------------------------------------------
    def sumWavesArray (self,waveArray1,waveArray2):
    #---------------------------------------------------------------------------
        if len(waveArray1) == 0:
            return waveArray2
        if len(waveArray2) == 0:
            return waveArray1

        sumArray = []
        for a,b in zip(waveArray1,waveArray2):
            sumArray . append (a+b)
    
        return sumArray
    
    
    #---------------------------------------------------------------------------
    def sumWaves(self):
    #---------------------------------------------------------------------------
        n = len(self.waves)
        npoints = len(self.waves[0].waveArray) 
        i = 0
        sumArray = []
        for wave in self.waves:
            if i ==0:
                for k in range(0,npoints):
                    sumArray.append (wave.waveArray[k])
            else:        
                for k in range(0,npoints):
                    sumArray [k] += wave.waveArray[k]
            i += 1
        return sumArray                
            
    #---------------------------------------------------------------------------
    def drawDiagrams (self, i, waveArray3):        
    #---------------------------------------------------------------------------

        k = np.argmin(np.abs(self.X - self.x0))

        if self.diagramType == 1:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8), gridspec_kw={'height_ratios': [1, 1, 2]}, sharex=True)
            ax1.set_xlim([self.xmin, self.xmax])
            ax1.set_ylim([-self.amplitudeMax-0.5, self.amplitudeMax+0.5])
            ax1.set_ylabel('Amplitude')
            ax1.set_title('Onde 1')
            ax1.plot( self.X, self.selectedWave1.waveArray)
            ax1.plot([self.x0], [self.selectedWave1.waveArray[k]], 'go')

            ax2.set_xlim([self.xmin, self.xmax])
            ax2.set_ylim([-self.amplitudeMax-0.5, self.amplitudeMax+0.5])
            ax2.set_ylabel('Amplitude')
            ax2.set_title('Onde 2')
            ax2.plot( self.X, self.selectedWave2.waveArray)
            ax2.plot([self.x0], [self.selectedWave2.waveArray[k]], 'go')

            ax3.set_xlim([self.xmin, self.xmax])
            ax3.set_ylim([-self.sumAmplitudeMax-0.5, self.sumAmplitudeMax+0.5])
            ax3.set_xlabel('x')
            ax3.set_ylabel('Amplitude')
            ax3.set_title('Somme des ondes')
            ax3.plot( self.X, waveArray3)
            ax3.plot([self.x0], waveArray3[k], 'go')
        
        elif self.diagramType == 2:    

            fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(6, 8), gridspec_kw={'height_ratios': [1, 1]}, sharex=True)
            ax1.set_xlim([self.xmin, self.xmax])
            ax1.set_ylim([-self.amplitudeMax-0.5, self.amplitudeMax+0.5])
            ax1.set_ylabel('Amplitude')
            ax1.set_title('Ondes')
            for wave in self.waves:
                ax1.plot( self.X, wave.waveArray)
                ax1.plot([self.x0], [wave.waveArray[k]], 'go')


            n = len (self.waves)
            ax3.set_xlim([self.xmin, self.xmax])
            ax3.set_ylim([-self.sumAmplitudeMax-0.5, self.sumAmplitudeMax+0.5])
            ax3.set_xlabel('x')
            ax3.set_ylabel('Amplitude')
            ax3.set_title('Somme des ondes')
            ax3.plot( self.X, waveArray3)
            ax3.plot([self.x0], waveArray3[k], 'go')
        
        fig.savefig("{}/image{:04d}.png".format(self.imagesFolderPath,i))
        plt.close(fig)



    #---------------------------------------------------------------------------
    def calculateAmplitudeMax(self):
    #---------------------------------------------------------------------------
        sumMax = 0
        max = 0
        for wave in self.waves:
            sumMax += wave.amplitude
            if max < wave.amplitude:
                max = wave.amplitude
        self.sumAmplitudeMax = sumMax 
        self.amplitudeMax = max           

    #---------------------------------------------------------------------------
    def makeDiagrams(self, i, t):
    #---------------------------------------------------------------------------
        self.calculateWaves(t)
        self.calculateAmplitudeMax()
        if self.diagramType == 1:
            waveArray3 = self.sumWavesArray(self.selectedWave1.waveArray, self.selectedWave2.waveArray)
        elif self.diagramType == 2:
            waveArray3 = self.sumWaves()
                
        self.drawDiagrams ( i, waveArray3)


    #---------------------------------------------------------------------------
    def buildAnimationTask(self,i):
    #---------------------------------------------------------------------------
        duplicatedScene = copy.deepcopy(self)
        ti = i / (10 * self.fps )
        print ("{} \t {}".format(i,ti))
        duplicatedScene.makeDiagrams( i, ti )


    #---------------------------------------------------------------------------
    def buildFromScript(self,filename):
    #---------------------------------------------------------------------------
        self.filename=filename
        data = self.parseFile(filename)
        self.buildScene(data)
        self.prepare()
        self.displayInfo()

    #---------------------------------------------------------------------------
    def buildAnimation(self):
    #---------------------------------------------------------------------------
        self.eraseImagesFolder()

        if self.diagramType == None:
            n = len(self.waves)
            if n == 2:
                self.diagramType = 1
            elif n > 2:
                self.diagranType = 2

        if self.diagramType == 1:
            self.selectWaves( self.waves[0], self.waves[1])

        if self.isParallelizing:
            numProcesses = self.nProcessors
            pool = multiprocessing.Pool(numProcesses)
            taskFunc = partial (self.buildAnimationTask)
            taskArgs = range(self.na)
            results = pool.map ( taskFunc, taskArgs)
            pool.close()
            pool.join()
            
        else:    
            for i in range(self.na):
                ti = i / (10 * self.fps )
                print ("{} \t {}".format(i,ti))
                self.makeDiagrams( i, ti)

        self.saveAnimation ()



    #---------------------------------------------------------------------------
    def eraseImagesFolder(self):
    #---------------------------------------------------------------------------
        files = os.listdir(self.imagesFolderPath)
        for file in files:
            filePath = os.path.join(self.imagesFolderPath, file)
            if os.path.exists(filePath):
                os.remove(filePath)

    #---------------------------------------------------------------------------
    def saveAnimation(self):
    #---------------------------------------------------------------------------
        clip = ImageSequenceClip(self.imagesFolderPath, fps=30)
        filename = self.animationsFolderPath + '/' + self.filename + '.mp4'
        clip.write_videofile(filename)


    def parseFile(self, fileName):
        with open ("scripts/"+fileName+".txt", "r") as file:
            fileContent = file.read()

        lines = fileContent.strip().split("\n")
        data = {}
        current_section = None
        for line in lines:
            line = line.strip()
            index = line.find('#')
            if index != -1:
                line = line [:index]
                line.strip()

            if line == '':
                continue
            elif line.startswith("xmin"):
                data["xmin"] = int(line.split()[1])
                current_section = None
            elif line.startswith("xmax"):
                data["xmax"] = int(line.split()[1])
                current_section = None
            elif line.startswith("x0"):
                data["x0"] = float(line.split()[1])
            elif line.startswith("parallel"):
                data["parallel"] = int(line.split()[1])
                current_section = None
            elif line.startswith("type"):
                data["type"] = int(line.split()[1])
                current_section = None

            elif line.startswith("nx"):
                data["nx"] = int(line.split()[1])
                current_section = None
            elif line.startswith("na"):
                data["na"] = int(line.split()[1])
                current_section = None
            elif line.startswith("fps"):
                data["fps"] = int(line.split()[1])
                current_section = None
            elif line.startswith("tmin"):
                data["tmin"] = float(line.split()[1])
                current_section = None
            elif line.startswith("tmax"):
                data["tmax"] = float(eval(line.split()[1]))
                current_section = None


            elif line.startswith("wave") :
                if "waves" not in data:
                    data["waves"] = []
                current_section = "wave"
                wave = {}
                data["waves"].append(wave)

            elif line.startswith("v"):
                if current_section == "wave":
                    wave["v"] = float(line.split()[1])
            elif re.match(r'^f\b', line):
                if current_section == "wave":
                    wave["f"] = float(line.split()[1])
            elif line.startswith("phase"):
                if current_section == "wave":
                    wave["phase"] = float(line.split()[1])
            elif line.startswith("amplitude"):
                if current_section == "wave":
                    wave["amplitude"] = float(line.split()[1])
                
        return data




    def buildScene(self,data):
        if "xmin" in data:
            self.xmin = data["xmin"]
        if "xmax" in data:
            self.xmax = data["xmax"]

        if "nx" in data:
            self.nx = data["nx"]
        if "na" in data:
            self.ny = data["na"]
        if "tmin" in data:
            self.tmin = data["tmin"]
        if "tmax" in data:
            self.tmax = data["tmax"]
        if "fps" in data:
            self.fps = data["fps"]
        if "x0" in data:
            self.x0 = data["x0"]
        if "parallel" in data:
            self.isParallelizing = True    
            self.nProcessors = data["parallel"]
        if "type" in data:
            self.diagramType = data["type"]

            
        if "waves" in data:
            nWaves = len (data["waves"])
            for k in range(0,nWaves):
                wave = Wave(self)
                waveData = data["waves"][k]

                if "v" in waveData:
                    wave.setSpeed (waveData["v"])
                if "f" in waveData:
                    wave.setFrequence (waveData["f"])
                if "phase" in waveData:
                    wave.setPhase (waveData["phase"])
                if "amplitude" in waveData:
                    wave.amplitude = waveData["amplitude"]

        return self
