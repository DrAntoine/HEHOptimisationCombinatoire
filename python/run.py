
import logging
from my_modules import tools
# import alive_progress as alive_bar
import random

random.seed(42)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nombreGeneration=1500
filePath = "Dataset-Dev/I002.in"

experience = tools.load(filename=filePath)
tools.cleanLogs()
logger.debug(f"""Paramètres d'experience:
nb impression par couv : {experience.COVER_IMPRESSION_NUMBER}
nb couv : {experience.NOMBRE_COUVERTURES}
nb slot : {experience.NOMBRE_SLOTS}
cout plaque : {experience.PLATE_COST} 
cout feuille : {experience.SHEET_COST}""")

Solution = []
bestpop = []
for nbPlate in range(experience.NOMBRE_COUVERTURES):
    experience.settings(geneMutationFactor=0.6, populationSize=250, genLen=nbPlate+1, geneMinimalValue=1, geneMaximalValue=50)
    experience.population = []
    # bestpop.append([experience.bestPopulation])
    experience.bestPopulation = []
    experience.initiate_population()
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
        print(scoredPopulation[0])
        tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore)
        if countBestScore > 50 or experience.medianScore == experience.bestScore:
            Solution.append(scoredPopulation[0])
            converged = True
        if not converged:
            experience.reproduction(scoredPopulation)
            genX += 1 


# experience.selection()
# logging.debug(f"{i} - score : Ultimate Best Mean Worst - {experience.ultimateScore} {experience.bestScore} {experience.medianScore} {experience.worstScore} {len(experience.population)}")
print("="*50)
for s in Solution:
    print(f"{experience.decodeIndividu(s[1])}{s[0]}€")
    # print(s)