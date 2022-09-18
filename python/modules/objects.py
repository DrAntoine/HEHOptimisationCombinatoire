
class Experience():
    nombreCouvertures = 1
    nombreSlots=1
    sheetCost=1
    plateCost=1
    nbImpressionCouvertures = []
    nb_individu = 100
    population = []
    mutation_chromosome_factor = 0.1
    mutation_gene_factor = 0.1

    def __init__(self, nbCouv, nbSlot, sheetCost, plateCost, printPerCov):
        self.nombreCouvertures = nbCouv
        self.nombreSlots = nbSlot
        self.sheetCost = sheetCost
        self.plateCost = plateCost
        self.nbImpressionCouvertures = printPerCov

    def coherence(self, individu):
        nbImpression = [0 for _ in range(self.nombreCouvertures)]
        if len(individu.chromosomes) <= 0:
            return False
        for chromosome in individu.chromosomes:
            lenght = len(chromosome.agencementSlot)
            if lenght <0 or lenght>self.nombreSlots:
                return False
            for cover in chromosome.agencementSlot:
                if cover < 0 or cover >= self.nombreCouvertures:
                    return False
                nbImpression[cover]+= chromosome.numberCopy
        for i in range(self.nombreCouvertures):
            if self.nbImpressionCouvertures[i]>nbImpression[i]:
                return False
        # Le return true n'arrive que si l'ensemble des conditions ont été respectée
        return True

    def estimateCost(self, individu):
        if(self.coherence(individu)):
            cost = len(individu.chromosomes)*self.plateCost
            for chromosome in individu.chromosomes:
                cost += chromosome.numberCopy * self.sheetCost
            return cost
        else:
            return -1
    
    def selection(self):
        pass

    def mixage(self, individu_1, individu_2):
        pass

    def mutate(self):
        pass


class Individu():
    chromosomes = []

    def __init__(self, chromosomesList):
        self.chromosomes = chromosomesList


class Chromosome():
    numberCopy = 1
    agencementSlot = []

    def __init__(self, nbCopy, agencement):
        self.numberCopy = nbCopy
        self.agencementSlot = agencement