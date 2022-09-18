import os
import modules.objects as obj

def load(filename):
    try:
        print(os.path.isfile(filename))
        if not os.path.isfile(filename):
            raise ValueError("Nom de fichier incorrect")
        else:
            with open(filename, "r") as file:
                nbCov = int(file.readline())
                nbSlot = int(file.readline())
                nbImpression = []
                for _ in range(nbCov):
                    nbImpression.append(int(file.readline()))
                coutFeuille = 0
                coutPlaque = 0
                texteBrut = file.readline()
                texteBrut = texteBrut.split(" ")
                coutFeuille = float(texteBrut[0])
                coutPlaque = float(texteBrut[1])
                experience = obj.Experience(nbCouv=nbCov, nbSlot=nbSlot, sheetCost=coutFeuille, plateCost=coutPlaque, printPerCov=nbImpression)
                return experience

    except ValueError as e:
        print(e)
        exit()