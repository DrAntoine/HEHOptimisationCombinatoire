
import logging
from modules import loadFile
from modules import objects as obj

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


filePath = "depot/HEHOptimisationCombinatoire/Dataset-Dev/I001.in"
experience = loadFile.load(filename=filePath)

logger.debug(f"""Paramètres d'experience:
nb impression par couv : {experience.COVER_IMPRESSION_NUMBER}
nb couv : {experience.NOMBRE_COUVERTURES}
nb slot : {experience.NOMBRE_SLOTS}
cout plaque : {experience.PLATE_COST} 
cout feuille : {experience.SHEET_COST}""")
experience.settings(geneMutationFactor=0.6, chromosomalMutationFactor=0.15)
experience.initiate_population()
experience.selection()
logging.debug(f"score : Best Mean Worst - {experience.actualBestScore()} {experience.actualMeanScore()} {experience.actualWorstScore()}")
experience.reproduction()
experience.selection()
logging.debug(f"score : Best Mean Worst - {experience.actualBestScore()} {experience.actualMeanScore()} {experience.actualWorstScore()}")
