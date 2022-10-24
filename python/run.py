from my_modules import tools
import math
from joblib import Parallel, delayed
import multiprocessing
from chrono import Timer
import argparse
import os

def main_code(nbPlate, experience):
    experience.settings(geneMutationFactor=0.8, populationSize=100, magnitudeOfGeneMutation = 500, genLen=nbPlate+1, geneMinimalValue=1, geneMaximalValue=15000)
    experience.population = []
    experience.bestPopulation = []
    experience.initiate_population()#parallélisable 
    genX = 0
    converged = False
    bestScore = 0
    lastBest = 0
    generationLastBest = 0
    while genX <= experience.NOMBRE_GENERATIONS_MAX and not converged:
        scoredPopulation = experience.selection()
        if genX==0:
            bestScore = experience.bestScore
            lastBest = bestScore
        else:
            newBest = min(bestScore, experience.bestPopulation[0][0])
            if newBest != bestScore :
                lastBest=bestScore
                bestScore=newBest
                generationLastBest = genX
            else:
                bestScore = newBest
        if experience.LOGS: 
            tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore) 
            print(f"{nbPlate}# {genX} {experience.bestPopulation[0][0]}, {experience.medianScore}, {experience.worstScore}")
        if genX != generationLastBest:
            nbGenerationPasse = genX-generationLastBest
            delta = (lastBest-bestScore)/nbGenerationPasse
            if delta < 10 or nbGenerationPasse > 20:
                return experience.bestPopulation[0]
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

    parser.add_argument(
        "-s",
        "--sequential",
        action="store_true",
        default="False", 
        help="Run in sequential mode"
    )

    args = parser.parse_args()
    filePath = args.input

    experience = tools.load(filename=filePath)
    if args.logs :
        tools.cleanLogs()
    experience.setLogs(args.logs)
    MAXIMAL_PLATES_NUMBER = experience.NOMBRE_COUVERTURES
    MINIMAL_PLATES_NUMBER = math.ceil(experience.NOMBRE_COUVERTURES/experience.NOMBRE_SLOTS)
    Solution = []
    if args.sequential == True:
        with Timer() as timed:
            if experience.LOGS: print("Algorithme en sequentiel")
            for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1):
                Solution.append(main_code(experience=experience, nbPlate=nbPlate))
    else:
        if experience.LOGS: print("Algorithme en parallele")
        num_cores = multiprocessing.cpu_count()
        with Timer() as timed:
            Solution.append(Parallel(n_jobs=num_cores)(delayed(main_code)(nbPlate, experience) for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1)))

    print()
    print("Time spent: {0} seconds".format(timed.elapsed))
    print()

    tools.showResult(experience, Solution)
    filename = args.input
    filename = os.path.basename(filename)
    filename = filename.split(".")[0]
    tools.writeResult(experience, Solution, f"{filename}.out")

if __name__ == "__main__":
    main()
    # random.seed = 42