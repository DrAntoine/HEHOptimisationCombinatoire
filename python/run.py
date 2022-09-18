
import logging
from modules import loadFile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


filePath = "depot/HEHOptimisationCombinatoire/Dataset-Dev/I001.in"
experience = loadFile.load(filename=filePath)

logger.debug(f"""Paramètres d'experience:
nb impression par couv : {experience.nbImpressionCouvertures}
nb couv : {experience.nombreCouvertures}
nb slot : {experience.nombreSlots}
cout plaque : {experience.plateCost} 
cout feuille : {experience.sheetCost}""")

