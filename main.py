import json
import os
from matplotlib import pyplot as plt
from VRP import VRP
import xml.etree.ElementTree as ET

# Losowe kolory, żeby wykres był ładny i jako tako czytelny
colors = [
    "#5e49b8",
    "#73d464",
    "#b34bd6",
    "#cad04b",
    "#c34a95",
    "#5c7d3c",
    "#d34844",
    "#78cabc",
    "#472c56",
    "#c9863d",
    "#718ec6",
    "#7a3d35",
    "#cabe92",
    "#425146",
    "#cb98b5"
]

for file in os.listdir("./data"):
    dataset = {
        "data": [],
        "num_of_vehicles": 0
    }

    if file.endswith(".json"):
        with open("./data/" + file) as f:
            json_file = json.load(f)
        dataset["data"] = json_file["data"]
        dataset["num_of_vehicles"] = json_file["num_of_vehicles"]

    elif file.endswith(".xml"):
        tree = ET.parse("./data/" + file)
        root = tree.getroot()

        for node in root.findall("network/nodes/node"):
            dataset["data"].append([
                node.find("cx").text,
                node.find("cy").text
            ])

    vrp_problem: VRP = VRP(
        dataset["data"],
        dataset["num_of_vehicles"],
        5
    )

    best_sol, best_cost = vrp_problem.tabu_search(1000)

    print(best_sol)
    print(best_cost)

    # Scatter plot na pokazanie punktów
    # annotate aby pokazać trasę pomiędzy punktami

    # Depot
    plt.scatter(*dataset["data"][0], color="red", s=200)
    # Klienci
    plt.scatter(*zip(*dataset["data"][1:]), s=200)

    for txt, coords in enumerate(dataset["data"]):
        plt.text(*coords, txt, ha="center", va="center", color="white")

    for i in range(len(best_sol)):
        color = colors[i]
        for j in range(len(best_sol[i]) - 1):
            plt.annotate(
                "", xytext=dataset["data"][best_sol[i][j]], xy=dataset["data"][best_sol[i][j + 1]],
                arrowprops=dict(arrowstyle="->,head_length=1,head_width=0.5", color=color)
            )

    # Template
    # plt.annotate(
    #     "", xytext=json_file["data"][0], xy=json_file["data"][1],
    #     arrowprops=dict(arrowstyle="->", color="red")
    # )

    plt.show()
