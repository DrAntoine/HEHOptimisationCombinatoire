import logging
import random
import math

class Experience():
    NOMBRE_COUVERTURES = 1
    NOMBRE_SLOTS=1
    SHEET_COST=1
    PLATE_COST=1
    COVER_IMPRESSION_NUMBER = []
    #====================
    POPULATION_SIZE = 100
    CHROMOSOMAL_MUTATION_FACTOR = 0.1
    GENE_MUTATION_FACTOR = 0.1
    CHROMOSOME_NUMBER_MUTATIONS = 2
    COPY_NUMBER_MUTATIONS = 50
    MAXIMAL_NUMBER_OF_CHROMOSOMES = 50
    MINIMAL_NUMBER_OF_CHROMOSOMES = 1
    MINIMAL_NUMBER_OF_PLATE_COPY = 100
    MAXIMAL_NUMBER_OF_PLATE_COPY = 1000
    bestScore = 0
    meanScore = 0
    worstScore = 0
    population = []
    # reproductionChance=[]

    def __init__(self, nbCouv, nbSlot, sheetCost, plateCost, printPerCov):
        self.NOMBRE_COUVERTURES = nbCouv
        self.NOMBRE_SLOTS = nbSlot
        self.SHEET_COST = sheetCost
        self.PLATE_COST = plateCost
        self.COVER_IMPRESSION_NUMBER = printPerCov
        self.MINIMAL_NUMBER_OF_CHROMOSOMES = max(math.ceil(self.NOMBRE_COUVERTURES/self.NOMBRE_SLOTS), 1)
        self.MAXIMAL_NUMBER_OF_PLATE_COPY = max(self.COVER_IMPRESSION_NUMBER)
        self.settings()

    def settings(self, populationSize = 100, chromosomalMutationFactor=0.1, geneMutationFactor=0.1, chromosomeNumberMutations=2, 
        copyNumberMutation=50, maximalNumberOfChromosomes=50, minimalNumberOfPlateCopy=100):
        self.POPULATION_SIZE = populationSize
        self.CHROMOSOMAL_MUTATION_FACTOR = chromosomalMutationFactor
        self.GENE_MUTATION_FACTOR = geneMutationFactor
        self.CHROMOSOME_NUMBER_MUTATIONS = chromosomeNumberMutations
        self.COPY_NUMBER_MUTATIONS = copyNumberMutation
        self.MAXIMAL_NUMBER_OF_CHROMOSOMES= maximalNumberOfChromosomes
        self.MINIMAL_NUMBER_OF_PLATE_COPY = minimalNumberOfPlateCopy



    def __coherence__(self, individu):
        """
        La fonction __coherence__ s'assure que l'individu passé en parametre propose une solution viable pour l'algo
        """
        nbImpression = [0 for _ in range(self.NOMBRE_COUVERTURES)]
        if len(individu.chromosomes) <= 0:
            return False
        for chromosome in individu.chromosomes:
            lenght = len(chromosome.agencementSlot)
            if lenght <0 or lenght>self.NOMBRE_SLOTS:
                return False
            for cover in chromosome.agencementSlot:
                if cover < 0 or cover >= self.NOMBRE_COUVERTURES:
                    return False
                nbImpression[cover]+= chromosome.numberCopy
        for i in range(self.NOMBRE_COUVERTURES):
            if self.COVER_IMPRESSION_NUMBER[i]>nbImpression[i]:
                return False
        # Le return true n'arrive que si l'ensemble des conditions ont été respectée
        return True

    def __estimateCost__(self, individu):
        if(self.__coherence__(individu)):
            cost = len(individu.chromosomes)*self.PLATE_COST
            for chromosome in individu.chromosomes:
                cost += chromosome.numberCopy * self.SHEET_COST
            return cost
        else:
            return -1
    
    def selection(self):
        scores = []
        for individu in self.population:
            individu.setScore(self.__estimateCost__(individu))
            if individu.score > 0 :
                scores.append(individu)
        try:
            if len(scores) <2:
                raise ValueError("Trop peu d'individu dans la population pour une nouvelle génération")
        except ValueError as E:
            print(E)
            exit()
        else:
            scores.sort()
            if len(scores)>self.POPULATION_SIZE//2:
                scores = scores[:self.POPULATION_SIZE//2]
            self.bestScore=round(scores[0].score,2)
            self.worstScore= round(scores[-1].score,2)
            meanScore = 0
            for score in scores:
                meanScore+=score.score
            self.meanScore = round(meanScore/len(scores))
            self.population=[score for score in scores]


    def actualBestScore(self):
        return self.bestScore
    
    def actualMeanScore(self):
        return self.meanScore
    
    def actualWorstScore(self):
        return self.worstScore

    def reproduction(self):
        new_generation = [] #self.population
        sample1 = 0
        sample2 = 0
        populationLenght = len(self.population)
        countRound = 0
        autofill = False
        while len(new_generation)<self.POPULATION_SIZE:
            if countRound < 5 and not autofill: 
                if sample2 == sample1:
                    sample2 +=1
                if sample2 > populationLenght-1:
                    sample2 = 0
                    sample1 +=1
                if sample1 > populationLenght-1:
                    sample1 = 0
                    sample2 = 1
                    countRound +=1
                # print(f"\r{len(new_generation)} - {sample1} {sample2}")
                child = self.__accouplement__(self.population[sample1], self.population[sample2])
            else:
                # print("Creation individu")
                child = self.__create_individu__()
            if self.__estimateCost__(child)>0:
                new_generation.append(child)
            sample2+=1
        self.population=new_generation

    def __accouplement__(self, individu_1, individu_2):
        full_chromo = list(individu_1.chromosomes) + list(individu_2.chromosomes)
        new_nb_chromo = math.ceil(len(full_chromo)/2)
        if random.random() < self.CHROMOSOMAL_MUTATION_FACTOR:
            new_nb_chromo += random.randint(-self.CHROMOSOME_NUMBER_MUTATIONS, self.CHROMOSOME_NUMBER_MUTATIONS)
        if new_nb_chromo > len(full_chromo):
            new_nb_chromo = len(full_chromo)
        if new_nb_chromo < 1:
            new_nb_chromo = 1
        new_chromo = []
        for _ in range(new_nb_chromo):
            chromo = random.choice(full_chromo)
            # full_chromo.remove(chromo)
            chromo = self.__mutate__(chromo)
            new_chromo.append(chromo)
        return Individu(new_chromo)


    def __mutate__(self, chromosome):
        chromosome_muted = chromosome
        if random.random() < self.GENE_MUTATION_FACTOR:
            chromosome_muted.numberCopy = random.randint(-self.COPY_NUMBER_MUTATIONS, self.COPY_NUMBER_MUTATIONS)
        for i in range(len(chromosome_muted.agencementSlot)):
            if random.random() < self.GENE_MUTATION_FACTOR:
                chromosome_muted.agencementSlot[i] = random.randint(0, self.NOMBRE_COUVERTURES)
        return chromosome_muted


    def initiate_population(self):
        while len(self.population) < self.POPULATION_SIZE:
            individu = self.__create_individu__()
            if(self.__estimateCost__(individu)!=-1):
                self.population.append(individu)
                logging.debug(f"\rPopulation = {len(self.population)}")
    
    def __create_individu__(self):
        mini = self.MINIMAL_NUMBER_OF_CHROMOSOMES
        maxi = self.MAXIMAL_NUMBER_OF_CHROMOSOMES
        chromosomes = [self.__create_chromosome__() for _ in range(random.randint(mini, maxi))]
        return Individu(chromosomes)
    
    def __create_chromosome__(self):
        copyNumber = random.randint(self.MINIMAL_NUMBER_OF_PLATE_COPY, self.MAXIMAL_NUMBER_OF_PLATE_COPY)
        agencement = [random.randint(0, self.NOMBRE_COUVERTURES) for _ in range(self.NOMBRE_SLOTS)]
        return Chromosome(copyNumber, agencement)


class Individu():
    chromosomes = []
    score = 0

    def __init__(self, chromosomesList):
        self.chromosomes = chromosomesList
    
    def __repr__(self) -> str:
        return f"{self.chromosomes}"
    
    def setScore(self, score):
        self.score = score
    
    def __gt__(self, other):
        if(self.score > other.score):
            return True
        else:
            return False
    
    def __lt__(self, other):
        if(self.score < other.score):
            return True
        else:
            return False


class Chromosome():
    numberCopy = 1
    agencementSlot = []

    def __init__(self, nbCopy, agencement):
        self.numberCopy = nbCopy
        self.agencementSlot = agencement
    
    def __repr__(self) -> str:
        return f"({self.numberCopy},{self.agencementSlot})"
