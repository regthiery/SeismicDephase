import argparse
import sys
from multiprocessing import freeze_support

sys.path.append("src")

from Scene import Scene


#-------------------------------------------------------------------------
#   Main code
#-------------------------------------------------------------------------

if __name__ == '__main__':
    freeze_support()
    

    parser = argparse.ArgumentParser(description='View seismic waves dephasing')
    parser.add_argument('script',  type=str, help='the script file name')
    parser.add_argument('--parallel', type=int, help='Nombre de processus en parallèle')
    args = parser.parse_args()
    filename = args.script
    parallel = args.parallel
    
    print ("Process script {}".format(filename))

    scene = Scene()
    if parallel != None:
        scene.isParallelizing = True
        scene.nProcessors = parallel

    scene.buildFromScript(filename)
    scene.buildAnimation()


        
