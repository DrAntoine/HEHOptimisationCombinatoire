import random
import math
# import numba
# from numba import jit

class Experience():
    NOMBRE_COUVERTURES = 1
    NOMBRE_SLOTS=1
    SHEET_COST=1
    PLATE_COST=1
    COVER_IMPRESSION_NUMBER = []
    #====================
    POPULATION_SIZE = 100
    GENE_MUTATION_FACTOR = 0.1
    MAGNITUDE_OF_GENE_MUTATION = 12
    GENE_MAXIMAL_VALUE = 1000
    GENE_MINIMAL_VALUE = 1
    GENOTYPE_LENGHT = 0
    NOMBRE_GENERATIONS_MAX = 1500000
    LOGS = False

    bestScore = 0
    medianScore = 0
    worstScore = 0
    ultimateScore = 0
    population = []
    scores = []
    bestPopulation = []
    

    def setLogs(self, booleenValue = False):
        self.LOGS = booleenValue

    def __init__(self, nbCouv, nbSlot, sheetCost, plateCost, printPerCov):
        self.NOMBRE_COUVERTURES = nbCouv
        self.NOMBRE_SLOTS = nbSlot
        self.SHEET_COST = sheetCost
        self.PLATE_COST = plateCost
        self.COVER_IMPRESSION_NUMBER = printPerCov
        self.settings()

    def settings(self, populationSize = 100, magnitudeOfGeneMutation=10, geneMutationFactor=0.1, geneMaximalValue = 100, geneMinimalValue=1, genLen = 5):
        self.POPULATION_SIZE = populationSize
        self.MAGNITUDE_OF_GENE_MUTATION = magnitudeOfGeneMutation
        self.GENE_MUTATION_FACTOR = geneMutationFactor
        self.GENE_MAXIMAL_VALUE = geneMaximalValue
        self.GENE_MINIMAL_VALUE = geneMinimalValue
        self.GENOTYPE_LENGHT = genLen * (self.NOMBRE_SLOTS +1)

    def __coherence__(self, plateComposition):
        coherent = False
        while not coherent:
            plateCompositionDecoded = self.decodePlate(plateComposition)
            coverInPlates = []
            SurplusCorver = []
            for cov in plateCompositionDecoded:
                if cov not in coverInPlates:
                    coverInPlates.append(cov)
                else:
                    SurplusCorver.append(cov)
            if len(coverInPlates) == self.NOMBRE_COUVERTURES:
                coherent = True
                return plateCompositionDecoded
            else:
                missingCover = [i+1 for i in range(self.NOMBRE_COUVERTURES) if i+1 not in coverInPlates]
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
    
    def __estimateCost__(self, individu):
        printPerPlate, plateComposition = self.decodeIndividu(individu)
        cost = len(printPerPlate)*self.PLATE_COST
        for i in printPerPlate:
            cost += i*self.SHEET_COST
        return int(cost)


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
        return plateRatio, plateComposition
    
    def compute_nb_impression(self,plateRatioNumber, plateComposition):
        UpBound = max(10000000, max(self.COVER_IMPRESSION_NUMBER)*10)
        DownBound = 1
        constante = 0
        delta = UpBound-DownBound
        nbCoverPerPlate = []
        minRatioNumber = min(plateRatioNumber)
        ratio = [i/minRatioNumber for i in plateRatioNumber]
        for i in range(len(plateRatioNumber)):
            nbCovInPlate = [0 for _ in range(self.NOMBRE_COUVERTURES)]
            for cov in plateComposition[i*self.NOMBRE_SLOTS:(i+1)*self.NOMBRE_SLOTS]:
                nbCovInPlate[cov-1] += 1
            nbCoverPerPlate.append(nbCovInPlate)
        while delta > 1:
            delta = UpBound - DownBound
            if delta == 1:
                constante = DownBound+delta
            else:
                constante = DownBound+(delta//2)
            to_low = False
            for cov in range(self.NOMBRE_COUVERTURES):
                nbPrint = 0
                for plate in range(len(nbCoverPerPlate)):
                    nbPrint += math.floor(constante*ratio[plate])*nbCoverPerPlate[plate][cov]
                if nbPrint < self.COVER_IMPRESSION_NUMBER[cov]:
                    to_low = True
            if to_low:
                DownBound = constante
            else:
                UpBound = constante
        nbPrintPerPlate = [constante*r for r in ratio]
        return nbPrintPerPlate

    def decodeIndividu(self, individu):
        plateRatio, plateComposition = self.extractData(individu)
        plateCompositionDecodedAndFixed = self.__coherence__(plateComposition)
        printPerPlate = self.compute_nb_impression(plateRatio, plateCompositionDecodedAndFixed)
        return printPerPlate, plateCompositionDecodedAndFixed

    def selection(self):
        ScoredPopulation = [(self.__estimateCost__(individu), individu) for individu in self.population]
        self.bestPopulation += ScoredPopulation
        self.bestPopulation.sort()
        self.bestPopulation = self.bestPopulation[:self.POPULATION_SIZE]
        best = 0
        worst = 0
        for i in range(len(ScoredPopulation)):
            if i ==0:
                best=ScoredPopulation[i]
                worst=ScoredPopulation[i]
            else:
                if best[0] > ScoredPopulation[i][0]:
                    best = ScoredPopulation[i]
                if worst[0] < ScoredPopulation[i][0]:
                    worst = ScoredPopulation[i]
        self.bestScore= round(best[0],2)
        self.worstScore= round(worst[0],2)
        if self.LOGS : self.logs()
        return ScoredPopulation

    def logs(self):
        self.medianScore = (self.bestScore+self.worstScore)//2
        self.ultimateScore = self.bestPopulation[0][0]


    def reproduction(self, scoredPopulation):
        new_generation = []
        scoredPopulation = self.bestPopulation
        lotery = [i for i in range(len(scoredPopulation))]
        #random.shuffle(lotery)
        sample1 = 0
        sample2 = 0
        mixage = self.coupleGenerator(lotery)
        for _ in range(self.POPULATION_SIZE//5):
            new_generation.append(self.__create_individu__())
        while len(new_generation)<self.POPULATION_SIZE:
            sample1, sample2 = next(mixage)
            while sample2 == sample1:
                sample1, sample2 = next(mixage)
            child = self.__accouplement__(scoredPopulation[sample1][1], scoredPopulation[sample2][1])
            child_score = self.__estimateCost__(child)
            if child_score>0 :# and child_score < self.bestScore*1.5:
                new_generation.append(child)
                # lotery.remove(sample1)
                # lotery.remove(sample2)
        self.population=new_generation
    
    def coupleGenerator(self, lotery):
        papa=list(lotery)
        mama = list(lotery)
        random.shuffle(papa)
        random.shuffle(mama)
        for i in papa:
            for j in mama:
                yield (i, j)

    def __accouplement__(self, individu_1, individu_2):
        min_lenght = min(len(individu_1), len(individu_2))
        maxi_lenght = max(len(individu_1), len(individu_2))
        new_nb_genes = random.choice([min_lenght, maxi_lenght])
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
        for i in range(len(chromosome_muted)):
            # if random.random() < self.GENE_MUTATION_FACTOR:
            mutation = chromosome_muted[i]+random.randint(-self.MAGNITUDE_OF_GENE_MUTATION,self.MAGNITUDE_OF_GENE_MUTATION)
            if mutation > self.GENE_MAXIMAL_VALUE:
                chromosome_muted[i] = self.GENE_MAXIMAL_VALUE
            elif mutation < self.GENE_MINIMAL_VALUE:
                chromosome_muted[i] = self.GENE_MINIMAL_VALUE
            else:
                chromosome_muted[i]=mutation
        return chromosome_muted


    def initiate_population(self):
        while len(self.population) < self.POPULATION_SIZE:
            individu = self.__create_individu__()
            self.population.append(individu)
    
    def __create_individu__(self):
        return [random.randint(self.GENE_MINIMAL_VALUE, self.GENE_MAXIMAL_VALUE) for _ in range(self.GENOTYPE_LENGHT)]

    def get_best_sample(self):
        score = list(self.scores)
        for i in score:
            if i <= 0:
                score[score.index(i)] = math.inf()
        return self.population[score.index(min(score))]
