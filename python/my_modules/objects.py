# from itertools import count
import logging
import random
import math
import pulp as p

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Experience():
    NOMBRE_COUVERTURES = 1
    NOMBRE_SLOTS=1
    SHEET_COST=1
    PLATE_COST=1
    COVER_IMPRESSION_NUMBER = []
    #====================
    POPULATION_SIZE = 100
    #CHROMOSOMAL_MUTATION_FACTOR = 0.1 #insertion/deletion
    GENE_MUTATION_FACTOR = 0.1
    MAGNITUDE_OF_GENE_MUTATION = 12
    GENE_MAXIMAL_VALUE = 1000
    GENE_MINIMAL_VALUE = 1
    MAXIMAL_GENOTYPE_LENGHT = 50
    MINIMAL_GENOTYPE_LENGHT = 1
    GENOTYPE_LENGHT = 0
    bestScore = 0
    medianScore = 0
    worstScore = 0
    ultimateScore = 0
    population = []
    scores = []
    bestPopulation = []


    def __init__(self, nbCouv, nbSlot, sheetCost, plateCost, printPerCov):
        self.NOMBRE_COUVERTURES = nbCouv
        self.NOMBRE_SLOTS = nbSlot
        self.SHEET_COST = sheetCost
        self.PLATE_COST = plateCost
        self.COVER_IMPRESSION_NUMBER = printPerCov
        self.MAXIMAL_GENOTYPE_LENGHT = (self.NOMBRE_SLOTS+1)*self.NOMBRE_COUVERTURES
        self.MINIMAL_GENOTYPE_LENGHT = math.ceil(self.NOMBRE_COUVERTURES/self.NOMBRE_SLOTS)*(self.NOMBRE_SLOTS+1)
        # print(f"Minimal genotype size : {self.MINIMAL_GENOTYPE_LENGHT}\nMaximal genotype lenght : {self.MAXIMAL_GENOTYPE_LENGHT}")
        #input()
        self.settings()

    def settings(self, populationSize = 100, magnitudeOfGeneMutation=10, geneMutationFactor=0.1, geneMaximalValue = 100, geneMinimalValue=1, genLen = 5):
        self.POPULATION_SIZE = populationSize
        self.MAGNITUDE_OF_GENE_MUTATION = magnitudeOfGeneMutation
        self.GENE_MUTATION_FACTOR = geneMutationFactor
        self.GENE_MAXIMAL_VALUE = geneMaximalValue
        self.GENE_MINIMAL_VALUE = geneMinimalValue
        self.GENOTYPE_LENGHT = genLen * (self.NOMBRE_SLOTS +1)
        # TODO remove next line
        #self.MAXIMAL_GENOTYPE_LENGHT = self.MINIMAL_GENOTYPE_LENGHT


    def __coherence__(self, plateComposition):
        # Verifier la cohérence d'une solution (si le livre 2 n'est pas présent le rajouter)
        coherent = False
        while not coherent:
            plateCompositionDecoded = self.decodePlate(plateComposition)
            coverInPlates = []
            SurplusCorver = []
            if len(plateComposition) != 4:
                pass
            for cov in plateCompositionDecoded:
                if cov not in coverInPlates:
                    coverInPlates.append(cov)
                else:
                    SurplusCorver.append(cov)
            logger.debug(f"Code couverture brute : {plateComposition}")
            logger.debug(f"Code couverture decodé : {plateCompositionDecoded}")
            logger.debug(f"Couvertures présentes : {coverInPlates}")
            if len(coverInPlates) == self.NOMBRE_COUVERTURES:
                coherent = True
                return plateCompositionDecoded
            else:
                # TODO Mettre en place ici la logique de correction des plaques
                """
                Énumerer les couvertures manquantes
                Pour chaque couvertures trouver les couvertures candidates pouvant remplacer celles ci
                """
                missingCover = [i+1 for i in range(self.NOMBRE_COUVERTURES) if i+1 not in coverInPlates]
                logger.debug(f"Couvertures manquantes : {missingCover}")
                # input("Wait - Cover missed")
                step = int((self.GENE_MAXIMAL_VALUE-self.GENE_MINIMAL_VALUE)/self.NOMBRE_COUVERTURES)
                milieuxClasse = [self.GENE_MINIMAL_VALUE+(step//2)+(step*(i)) for i in range(self.NOMBRE_COUVERTURES)]
                deltaCandidats = []
                for i in range(len(plateComposition)):
                    if plateCompositionDecoded[i] in SurplusCorver:
                        delta = abs(plateComposition[i]-milieuxClasse[missingCover[0]-1])
                        deltaCandidats.append(int(delta))
                bestDelta=min(deltaCandidats)
                j = 0
                for i in range(len(plateComposition)):
                    if plateCompositionDecoded[i] in SurplusCorver:
                        if deltaCandidats[j] == bestDelta:
                            if plateComposition[i] > milieuxClasse[missingCover[0]-1]:
                                plateComposition[i] = max(plateComposition[i] - step , self.GENE_MINIMAL_VALUE)
                            else:
                                plateComposition[i] = min(plateComposition[i] + step, self.GENE_MAXIMAL_VALUE)
                            break
                        else: j+=1
            # return plateCompositionDecoded

    def __estimateCost__(self, individu, printCost=False):
        printPerPlate, plateComposition = self.decodeIndividu(individu)
        # maxRequiredPrint = 0
        # for i in range(len(self.COVER_IMPRESSION_NUMBER)):
        #     coverproportion = 0
        #     for p in range(len(plateRatio)):
        #         numberOfCov = 0
        #         for s in plateComposition[p*self.NOMBRE_SLOTS:(p+1)*self.NOMBRE_SLOTS]:
        #             if s == i+1:
        #                 numberOfCov+=1
        #         coverproportion += plateRatio[p]*numberOfCov
        #     if coverproportion != 0:
        #         maxRequiredPrint = max(maxRequiredPrint, math.ceil(self.COVER_IMPRESSION_NUMBER[i]/coverproportion))

            # if printCost : print(f"Nombre total de copie requise :{maxRequiredPrint}")
        cost = len(printPerPlate)*self.PLATE_COST
        for i in printPerPlate:
            cost += i*self.SHEET_COST
        if printCost:
            print(f"{cost}€")
        # input()
        # TODO Résoudre le calcul du nombre d'impression total 
        # TODO S'assurer que le nombre d'impression de chaque plaque soit un nombre entier pour l'estimation
        # NOTE Cette fonction sera celle à modifier si on utilise un algo d'opti d'eq linéaire pour retirer le plateRatio
        return cost


    def decodePlate(self, plateComposition):
        step = (self.GENE_MAXIMAL_VALUE-self.GENE_MINIMAL_VALUE)/self.NOMBRE_COUVERTURES
        plateCompositionDecoded = []
        for s in plateComposition:
            for i in range(self.NOMBRE_COUVERTURES+1):
                if s < (i*step)+1 or i == self.NOMBRE_COUVERTURES:
                    plateCompositionDecoded.append(i)
                    break
        return plateCompositionDecoded

    def extractData(self, individu):
        plateRatio = []
        plateComposition = []
        truncateLen = len(individu)%(self.NOMBRE_SLOTS+1)
        for i in range(len(individu)-truncateLen):
            modulo = i % (self.NOMBRE_SLOTS+1)
            if modulo == 0:
                plateRatio.append(individu[i])
            else:
                plateComposition.append(individu[i])
        #plateImpressionNumber = self.compute_nb_impression(plateRatio, plateComposition)
        # return plateImpressionNumber, plateComposition
        #sumPlateRatio = sum(plateRatio)
        #minRatio = min(plateRatio)
        # plateRatio = [round(i/minRatio,2) for i in plateRatio]
        #plateRatio = [round(i/sumPlateRatio,2) for i in plateRatio]
        return plateRatio, plateComposition
    
    def compute_nb_impression(self,plateRatioNumber, plateComposition):
        minRatioNumber = min(plateRatioNumber)
        #ratio = [i/minRatioNumber for i in plateRatioNumber]
        ratio = [math.ceil(i/minRatioNumber) for i in plateRatioNumber]
        nbCovTotal = [0 for i in range(self.NOMBRE_COUVERTURES)]
        for i in range(len(ratio)):
            for slot in plateComposition[i*self.NOMBRE_SLOTS:(i+1)*self.NOMBRE_SLOTS]:
                nbCovTotal[slot-1]+=1*ratio[i]
        nbPrintPerSlot = [0 for i in range(self.NOMBRE_COUVERTURES)]
        for i in range(len(nbPrintPerSlot)):
            nbPrintPerSlot[i] = math.ceil(self.COVER_IMPRESSION_NUMBER[i]/nbCovTotal[i])
        nbPrintPerPlate = [0 for i in range(len(plateComposition)//(self.NOMBRE_SLOTS))]
        for i in range(len(nbPrintPerPlate)):
            for j in plateComposition[i*self.NOMBRE_SLOTS: (i+1)*self.NOMBRE_SLOTS]:
                nbPrintPerPlate[i] = max(nbPrintPerPlate[i], nbPrintPerSlot[j-1])
        # print(nbPrintPerPlate)
        # input()
        return nbPrintPerPlate

    def decodeIndividu(self, individu):
        plateRatio, plateComposition = self.extractData(individu)
        plateCompositionDecodedAndFixed = self.__coherence__(plateComposition)
        printPerPlate = self.compute_nb_impression(plateRatio, plateCompositionDecodedAndFixed)
        return printPerPlate, plateCompositionDecodedAndFixed

    def selection(self):
        ScoredPopulation = [(self.__estimateCost__(individu), individu) for individu in self.population]
        ScoredPopulation.sort()
        self.bestPopulation += ScoredPopulation
        self.bestPopulation.sort()
        self.bestPopulation = self.bestPopulation[:self.POPULATION_SIZE]
        self.logs(ScoredPopulation)
        return ScoredPopulation

    def logs(self, ScoredPopulation):
        self.bestScore= round(ScoredPopulation[0][0],2)
        self.worstScore= round(ScoredPopulation[-1][0],2)
        med = ScoredPopulation[len(ScoredPopulation)//2][0]
        self.medianScore = round(med)
        self.ultimateScore = self.bestPopulation[0][0]


    def reproduction(self, scoredPopulation):
        new_generation = [] #self.bestPopulation[:self.POPULATION_SIZE//10]
        # for i in range(self.POPULATION_SIZE//10):
        #     scoredPopulation.append(self.bestPopulation[i])
        scoredPopulation = self.bestPopulation
        lotery = []
        delta = self.worstScore - self.bestScore
        for id_p in range(len(scoredPopulation)):
            reproductionRate = 5
            if delta != 0: reproductionRate = math.ceil((1-((scoredPopulation[id_p][0] - self.bestScore)/delta))*10)
            lotery.extend(id_p for _ in range(reproductionRate))
        random.shuffle(lotery)
        sample1 = 0
        sample2 = 0
        for i in range(self.POPULATION_SIZE//10):
            # new_generation.append(self.__create_individu__(random.randint(1, self.NOMBRE_COUVERTURES)*(self.NOMBRE_SLOTS+1)))
            new_generation.append(self.__create_individu__(self.GENOTYPE_LENGHT))
        while len(new_generation)<self.POPULATION_SIZE:
            sample1 = random.choice(lotery)
            sample2 = random.choice(lotery)
            while sample2 == sample1:
                sample2 = random.choice(lotery)
            child = self.__accouplement__(scoredPopulation[sample1][1], scoredPopulation[sample2][1])
            child_score = self.__estimateCost__(child)
            if child_score>0 and child_score < self.bestScore*1.5:
                new_generation.append(child)
                lotery.remove(sample1)
                lotery.remove(sample2)
        self.population=new_generation

    def __accouplement__(self, individu_1, individu_2):
        min_lenght = min(len(individu_1), len(individu_2))
        maxi_lenght = max(len(individu_1), len(individu_2))
        new_nb_genes = random.choice([min_lenght, maxi_lenght])
        # if random.random() < self.CHROMOSOMAL_MUTATION_FACTOR:
        #     new_nb_chromo += random.randint(-self.CHROMOSOME_NUMBER_MUTATIONS, self.CHROMOSOME_NUMBER_MUTATIONS)
        # new_nb_chromo = min(new_nb_chromo, len(full_chromo))
        # new_nb_chromo = max(new_nb_chromo,1)
        new_chromo = []
        len1 = len(individu_1)
        len2 = len(individu_2)
        for i in range(new_nb_genes):
            if i < len1 and i < len2:
                choice = random.randint(1,2)
                if choice == 1:
                    new_chromo.append(individu_1[i])
                else:
                    new_chromo.append(individu_2[i])
            elif i < len1:
                new_chromo.append(individu_1[i])
            else:
                new_chromo.append(individu_2[i])
            new_chromo = self.__mutate__(new_chromo)
        return new_chromo


    def __mutate__(self, chromosome):
        chromosome_muted = chromosome
        # if random.random() < self.GENE_MUTATION_FACTOR:
        #     chromosome_muted.numberCopy = random.randint(-self.COPY_NUMBER_MUTATIONS, self.COPY_NUMBER_MUTATIONS)
        for i in range(len(chromosome_muted)):
            if random.random() < self.GENE_MUTATION_FACTOR:
                # chromosome_muted[i] = random.randint(self.GENE_MINIMAL_VALUE, self.GENE_MAXIMAL_VALUE)
                mutation = chromosome_muted[i]+random.randint(-self.MAGNITUDE_OF_GENE_MUTATION,self.MAGNITUDE_OF_GENE_MUTATION)
                if mutation > self.GENE_MAXIMAL_VALUE:
                    chromosome_muted[i] = self.GENE_MAXIMAL_VALUE
                elif mutation < self.GENE_MINIMAL_VALUE:
                    chromosome_muted[i] = self.GENE_MINIMAL_VALUE
                else:
                    chromosome_muted[i]=mutation
        return chromosome_muted


    def initiate_population(self):
        # genotypeSizes = []
        # for a in range(self.NOMBRE_COUVERTURES):
        #     print(f"nb couv : {a}")
        #     genotypeSizes.append((a+1)*(self.NOMBRE_SLOTS +1))
        # self.GENOTYPE_LENGHT = nbPlate*(self.NOMBRE_SLOTS +1)
        while len(self.population) < self.POPULATION_SIZE:
            # indexGenotypeSize = min(len(self.population)//(self.POPULATION_SIZE// self.NOMBRE_COUVERTURES), len(genotypeSizes)-1)
            # print(indexGenotypeSize)
            # if nbPlate == 0:
            #     genotypeSize = random.randint(1, self.NOMBRE_COUVERTURES)*(self.NOMBRE_SLOTS +1)
            # else :
            #     genotypeSize = nbPlate*(self.NOMBRE_SLOTS +1)
            # genotypeSize = genotypeSizes[indexGenotypeSize]
            individu = self.__create_individu__(size=self.GENOTYPE_LENGHT)
            # print(individu)
            # print(self.__estimateCost__(individu))
            self.population.append(individu)
            # logging.debug(f"\rPopulation = {len(self.population)}")
    
    def __create_individu__(self, size=0):
        # genotypeSize = 0
        # if size != 0:
        #     genotypeSize = size
        # else:
        #     genotypeSize = random.randint(self.MINIMAL_GENOTYPE_LENGHT, self.MAXIMAL_GENOTYPE_LENGHT)
        genotype = [random.randint(self.GENE_MINIMAL_VALUE, self.GENE_MAXIMAL_VALUE) for _ in range(self.GENOTYPE_LENGHT)]
        return genotype

    def get_best_sample(self):
        score = list(self.scores)
        for i in score:
            if i <= 0:
                score[score.index(i)] = math.inf()
        return self.population[score.index(min(score))]
