import os
import sys

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add the parent parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# import the necessary packages
from experiments.se_experiments.se_experiment_utils import *
import pandas as pd
from collections import defaultdict

PROBS_FILE = "se_files/se_bigs.probs"
SOL_FILE = "se_files/se_heuristic_sol_bigs.csv"

MIN_NUM_OF_MODULES = 10
MAX_NUM_OF_MODULES = 10
MIN_NUM_OF_CLASSES = 50
MAX_NUM_OF_CLASSES = 50
NUM_OF_PROBS = 100

sol_files = ["se_files/heuristic_experiments/se_sol_" + heuristic.value + ".csv" for heuristic in Heuristic]


def main():
    se_probs = CreateSeProbs(min_modules=MIN_NUM_OF_MODULES,
                             max_modules=MAX_NUM_OF_MODULES,
                             min_classes=MIN_NUM_OF_CLASSES,
                             max_classes=MAX_NUM_OF_CLASSES,
                             num_of_probs=NUM_OF_PROBS)

    se_probs.create_probs()
    se_probs.write_probs_to_file(PROBS_FILE)  # writes problems in file

    se_probs = read_probs_from_file(PROBS_FILE)

    # costs = defaultdict(list)
    node_expansions = defaultdict(list)

    for i, heuristic in enumerate(Heuristic):
        solutions = run_experiment(se_probs, heuristic=heuristic.value, print_paths=True)

        for solution in solutions["sol_stats"]:
            # costs[heuristic.value].append(solution["cost"])
            node_expansions[heuristic.value].append(solution["nodes_expanded"])
        print("Finished", heuristic.value)

    # cost_data = pd.DataFrame(costs)
    node_expansions_data = pd.DataFrame(node_expansions)

    # append cost data to node expansions data as data
    # for heuristic in Heuristic:
    #     node_expansions_data[heuristic.value + "_cost"] = cost_data[heuristic.value]
    # change alg names to alg names + node expansions
    node_expansions_data.columns = [heuristic.value + "_n_expansions" for heuristic in Heuristic]# + [heuristic.value + "_cost" for heuristic in Heuristic]
    data = node_expansions_data

    data.to_csv(SOL_FILE, index=False, header=True)


if __name__ == "__main__":
    main()
