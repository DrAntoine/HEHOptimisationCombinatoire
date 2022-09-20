
import logging
from modules import tools
# from modules import objects as obj

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


filePath = "depot/HEHOptimisationCombinatoire/Dataset-Dev/I002.in"
experience = tools.load(filename=filePath)
tools.cleanLogs()

logger.debug(f"""Paramètres d'experience:
nb impression par couv : {experience.COVER_IMPRESSION_NUMBER}
nb couv : {experience.NOMBRE_COUVERTURES}
nb slot : {experience.NOMBRE_SLOTS}
cout plaque : {experience.PLATE_COST} 
cout feuille : {experience.SHEET_COST}""")
experience.settings(geneMutationFactor=0.1, chromosomalMutationFactor=0.085, populationSize=100)
experience.initiate_population()
for i in range(50):
    experience.selection()
    logging.debug(f"score : Best Mean Worst - {experience.actualBestScore()} {experience.actualMeanScore()} {experience.actualWorstScore()}")
    tools.writeLogs(best=experience.actualBestScore(), mean=experience.actualMeanScore(), worst=experience.actualWorstScore())
    experience.reproduction()
experience.selection()
logging.debug(f"score : Best Mean Worst - {experience.actualBestScore()} {experience.actualMeanScore()} {experience.actualWorstScore()}")
