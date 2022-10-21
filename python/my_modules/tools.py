import os
import math
import my_modules.objects as obj

def load(filename):
    try:
        # print(os.path.isfile(filename))
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

def writeLogs(best, mean, worst, ultimate):
    with open(f"logs_score.txt", "a") as file:
        file.writelines(f"{int(ultimate)}\t{int(best)}\t{int(mean)}\t{int(worst)}\n")

def cleanLogs():
    with open("logs_score.txt", "w") as f:
        # f.write("0\t0\t0\n")
        f.write("")

def showResult(experience, Solutions):
    print("=~= "*30)
    FinalBest = math.inf
    solution = []
    for s in Solutions[0]:
        if s[0]< FinalBest:
            solution = s
            FinalBest = s[0]
    gene = experience.decodeIndividu(solution[1])
    printArrondi = [math.floor(g) for g in gene[0]]
    pluriels = ""
    if len(printArrondi)>1:
        pluriels = "s"
    print(f"""Meilleur solution : {len(printArrondi)} plaque{pluriels}
    Coût : {round(solution[0],2)}€""")
    for i in range(len(printArrondi)):
        print(f"""\t Plaque {i+1} :
        \t Impression : {printArrondi[i]} \t Composition : {gene[1][i*experience.NOMBRE_SLOTS:(i+1)*experience.NOMBRE_SLOTS]}""")
    print("=~= "*30)
    print("Contraintes : ")
    nbCovPrinted = [0 for _ in range(experience.NOMBRE_COUVERTURES)]
    for i in range(len(printArrondi)):
        for cov in gene[1][i*experience.NOMBRE_SLOTS:(i+1)*experience.NOMBRE_SLOTS]:
            nbCovPrinted[cov-1] += printArrondi[i]
    for cov in range(len(experience.COVER_IMPRESSION_NUMBER)):
        print(f"Nombre d'impression couverture {cov+1} \t: {experience.COVER_IMPRESSION_NUMBER[cov]}\t Imprimé : {nbCovPrinted[cov]}")
