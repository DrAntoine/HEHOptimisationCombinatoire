from ast import parse
from turtle import st
from my_modules import tools
import math
import random
from joblib import Parallel, delayed
import multiprocessing
from chrono import Timer
import argparse

def main_code(nbPlate, experience):
    experience.settings(geneMutationFactor=0.3, populationSize=1000, genLen=nbPlate+1, geneMinimalValue=1, geneMaximalValue=99999)
    experience.population = []
    experience.bestPopulation = []
    experience.initiate_population()#parallélisable 
    genX = 0
    converged = False
    bestScore = 0
    countBestScore = 0
    while genX <= experience.NOMBRE_GENERATIONS_MAX and not converged:
        scoredPopulation = experience.selection()
        if genX==0:
            bestScore = experience.bestScore
        else:
            newBest = min(bestScore, experience.bestScore)
            if newBest == bestScore :
                countBestScore += 1
            else:
                countBestScore = 0
                bestScore = newBest
        if experience.LOGS: tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore)
        if countBestScore > 150 or experience.medianScore == experience.bestScore:
            return scoredPopulation[0]
        if not converged:
            experience.reproduction(scoredPopulation)
            genX += 1

def main():
    
    desc = "Algorithme génétique pour la résolution du problème de mariage de couverture."
    parser = argparse.ArgumentParser(
        prog="algen",
        description=desc,
        usage="algen [option] ...",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-l",
        "--logs",
        action="store_true",
        default=False,
        help="print logs"
    )

    parser.add_argument(
        "-i",
        "--input",
        type = str,
        metavar="",
        required=True,
        help = "Input file in .in format"
    )

    args = parser.parse_args()
    # print("What's name of ur file (without extension) ? ")
    # x=input()

    # filePath = "../Dataset-Dev/" + x + ".in"
    filePath = args.input

    experience = tools.load(filename=filePath)
    if args.logs :
        tools.cleanLogs()
    experience.setLogs(args.logs)

    MAXIMAL_PLATES_NUMBER = experience.NOMBRE_COUVERTURES
    MINIMAL_PLATES_NUMBER = math.ceil(experience.NOMBRE_COUVERTURES/experience.NOMBRE_SLOTS)

    Solution = []
    bestpop = []

    num_cores = multiprocessing.cpu_count()

    with Timer() as timed:

        Solution.append(Parallel(n_jobs=num_cores)(delayed(main_code)(nbPlate, experience) for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1)))

    print()
    print("Time spent: {0} seconds".format(timed.elapsed))
    print()

    tools.showResult(experience, Solution)

if __name__ == "__main__":
    main()