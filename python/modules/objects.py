import random

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
    mutation_chromosome_number = 2
    mutation_copy_number = 50

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
        scores = []
        for individu in self.population:
            score = self.estimateCost(individu)
            if score > 0 :
                scores.append((score, individu))
        if len(scores) <2:
            raise ValueError("Trop peu d'individu dans la population pour une nouvelle génération")
            #TODO terminer la selection
        pass

    def mixage(self, individu_1, individu_2):
        full_chromo = []#individu_1.chromosomes + individu_2.chromosomes
        new_nb_chromo = len(full_chromo)/2
        if random.random() < self.mutation_chromosome_factor:
            new_nb_chromo += random.randint(-self.mutation_chromosome_number, self.mutation_chromosome_number)
        new_chromo = []
        for _ in range(new_nb_chromo):
            chromo = random.choice(full_chromo)
            full_chromo.remove(chromo)
            chromo = self.mutate(chromo)
            new_chromo.append(chromo)


    def mutate(self, chromosome):
        chromosome_muted = Chromosome
        if random.random() < self.mutation_gene_factor:
            chromosome_muted.numberCopy = random.randint(-self.mutation_copy_number, self.mutation_copy_number)
        for i in range(len(chromosome_muted.agencementSlot)):
            if random.random() < self.mutation_gene_factor:
                chromosome_muted.agencementSlot[i] = random.randint(0, self.nombreCouvertures)
        return chromosome_muted


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
