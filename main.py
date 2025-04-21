import json
import os
from matplotlib import pyplot as plt
from VRP import VRP

for file in os.listdir("./data"):
    with open("./data/" + file) as f:
        json_file = json.load(f)

        vrp_problem: VRP = VRP(
            json_file["data"],
            2
        )

        vrp_problem.init_solution()

        pass

        # # Scatter plot na pokazanie punktów
        # # annotate aby pokazać trasę pomiędzy punktami
        # plt.scatter(*zip(*json_file["data"]))
        # plt.annotate(
        #     "", xytext=json_file["data"][0], xy=json_file["data"][1],
        #     arrowprops=dict(arrowstyle="->", color="red")
        # )
        # plt.show()
