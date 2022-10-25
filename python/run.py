from my_modules import tools
import math
from joblib import Parallel, delayed
import multiprocessing
from chrono import Timer
import argparse
import os
import random
import time

def main_code(nbPlate, experience):
    stop = False
    t= time.process_time()
    experience.settings(populationSize=100, magnitudeOfGeneMutation = 500, genLen=nbPlate+1, geneMinimalValue=1, geneMaximalValue=15000)
    experience.population = []
    experience.bestPopulation = []
    experience.initiate_population()#parallélisable 
    genX = 0
    bestScore = 0
    generationLastBest = 0
    countBest = 0
    while genX <= experience.NOMBRE_GENERATIONS_MAX :
        elapsed_time = time.process_time() - t
        if elapsed_time > 55.0/(experience.NOMBRE_COUVERTURES+1):
            stop = True
        scoredPopulation = experience.selection()
        if genX==0:
            bestScore = experience.bestScore
        else:
            newBest = min(bestScore, experience.bestPopulation[0][0])
            if newBest != bestScore :
                bestScore=newBest
                countBest=0
            else:
                countBest+=1
        
        if experience.LOGS: 
            tools.writeLogs(best=experience.bestScore, mean=experience.medianScore, worst=experience.worstScore, ultimate=experience.ultimateScore, genX=genX, nbPlate=nbPlate) 
            print(f"{nbPlate}# {genX} {experience.bestPopulation[0][0]}, {experience.medianScore}, {experience.worstScore}")
    
        if stop or genX >5000 or countBest > 50:
            if experience.LOGS:
                print(f"###{nbPlate} STOP ###")
            return((experience.bestPopulation[0],genX))
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
    nb_gen = 0
    sol = []
    if args.sequential == True:
        with Timer() as timed:
            if experience.LOGS: print("Algorithme en sequentiel")
            for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1):
                sol.append(main_code(experience=experience, nbPlate=nbPlate))
    else:
        if experience.LOGS: print("Algorithme en parallele")
        num_cores = multiprocessing.cpu_count()
        with Timer() as timed:
            sol.append(Parallel(n_jobs=num_cores-1)(delayed(main_code)(nbPlate, experience) for nbPlate in range(MINIMAL_PLATES_NUMBER,MAXIMAL_PLATES_NUMBER+1)))
    if type(sol) == type([]) and len(sol) == 1:
        sol=sol[0]

    for s in sol:
        Solution.append(s[0])
        nb_gen += s[1]

    print()
    timeElapsed = timed.elapsed
    print(f"Time spent: {timeElapsed} seconds")
    print(f"Solutions per second : {round((nb_gen*experience.POPULATION_SIZE)/timeElapsed, 2)}")
    print()
    tools.showResult(experience, Solution)
    filename = args.input
    filename = os.path.basename(filename)
    filename = filename.split(".")[0]
    tools.writeResult(experience, Solution, f"{filename}.out")

if __name__ == "__main__":
    main()
    random.seed = 42