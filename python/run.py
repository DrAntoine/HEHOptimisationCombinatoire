
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


experience.settings(geneMutationFactor=0.45, populationSize=500)

experience.initiate_population()
# for p in experience.population:
#     print(p)
for i in range(nombreGeneration):
    scoredPopulation = experience.selection()
    logging.debug(f"{i} - score : Ultimate Best Mean Worst - {experience.ultimateScore} {experience.bestScore} {experience.medianScore} {experience.worstScore} {len(experience.population)}")
    print(scoredPopulation[0])
    tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore)
    experience.reproduction(scoredPopulation)


experience.selection()
logging.debug(f"{i} - score : Ultimate Best Mean Worst - {experience.ultimateScore} {experience.bestScore} {experience.medianScore} {experience.worstScore} {len(experience.population)}")
print(f"{experience.decodeIndividu(experience.bestPopulation[0][1])}{experience.bestPopulation[0][0]}€")
print()