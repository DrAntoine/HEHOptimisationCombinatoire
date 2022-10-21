import logging
from my_modules import tools
import math
import random
from joblib import Parallel, delayed
import multiprocessing
from chrono import Timer
    
def main_code(nbPlate):
    experience.settings(geneMutationFactor=0.8, populationSize=150, genLen=nbPlate+1, geneMinimalValue=1, geneMaximalValue=15000)
    experience.population = []
    # bestpop.append([experience.bestPopulation])
    experience.bestPopulation = []
    experience.initiate_population()#parallélisable 
    genX = 0
    converged = False
    bestScore = 0
    countBestScore = 0
    # input(f"Len ={experience.GENOTYPE_LENGHT}")
    while genX <= nombreGeneration and not converged:
        scoredPopulation = experience.selection()
        # input(experience.bestScore)
        if genX==0:
            bestScore = experience.bestScore
        else:
            newBest = min(bestScore, experience.bestScore)
            if newBest == bestScore :
                countBestScore += 1
            else:
                countBestScore = 0
                bestScore = newBest
        logging.debug(f"{genX} - score : Ultimate Best Mean Worst - {experience.ultimateScore} {experience.bestScore} {experience.medianScore} {experience.worstScore} {len(experience.population)}")
        #print(scoredPopulation[0])
        tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore)
        #print(f"\rNb plaque: {nbPlate} \tGeneration {genX} \tAvancement {(round((countBestScore/16)*100,0)):=6}%", end="")
        if countBestScore > 15 or experience.medianScore == experience.bestScore:
            #Solution.append(scoredPopulation[0])
            return scoredPopulation[0]
            converged = True
            print()
        if not converged:
            experience.reproduction(scoredPopulation)
            genX += 1

print (__name__)
#exit()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nombreGeneration=1500
filePath = "../Dataset-Dev/I009.in"

experience = tools.load(filename=filePath)
tools.cleanLogs()
logger.debug(f"""Paramètres d'experience:
nb impression par couv : {experience.COVER_IMPRESSION_NUMBER}
nb couv : {experience.NOMBRE_COUVERTURES}
nb slot : {experience.NOMBRE_SLOTS}
cout plaque : {experience.PLATE_COST} 
cout feuille : {experience.SHEET_COST}""")

MAXIMAL_PLATES_NUMBER = experience.NOMBRE_COUVERTURES
MINIMAL_PLATES_NUMBER = math.ceil(experience.NOMBRE_COUVERTURES/experience.NOMBRE_SLOTS)

Solution = []
bestpop = []

#for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1):
#     main_code(nbPlate)

num_cores = multiprocessing.cpu_count()
#print(num_cores)

with Timer() as timed:

    Solution.append(Parallel(n_jobs=num_cores)(delayed(main_code)(nbPlate) for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1)))

print()
print("Time spent: {0} seconds".format(timed.elapsed))
print()

tools.showResult(experience, Solution)

