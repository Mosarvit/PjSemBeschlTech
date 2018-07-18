import time
import os
from global_data import project_path
def save(path='data', name='', savetime=True):
    """
    
    INPUT:  path: where to save
            name: foldername
            time: safe time behind foldername
    OUTPUT: path: directory to safe files
    """

    os.chdir(project_path + path)
    # Create folder for results
    if savetime:
        directory = name + '_' + time.strftime("%d_%m_%Y-%H_%M_%S")
    else:
        directory = name

    if not os.path.exists(directory):
        os.makedirs(directory)

    # das steht hier einfach so, ist bestimmt nicht sinnvoll
    folder = False
    if folder:
        if not os.path.exists(directory + "/H"):
            os.makedirs(directory + "/H")
        if not os.path.exists(directory + "/Uin"):
            os.makedirs(directory + "/Uin")
        if not os.path.exists(directory + "/Uout"):
            os.makedirs(directory + "/Uout")
        if not os.path.exists(directory + "/K"):
            os.makedirs(directory + "/K")
        if not os.path.exists(directory + "/a"):
            os.makedirs(directory + "/a")

    path = path + '/' + directory
    return path

def save_text(path=project_path + 'data'):
    os.chdir(path)
    f = open("result.txt", "w")
    x = input("Gebe eine Beschriftung ein: ")
    f.write(x)
    f.close()


    return