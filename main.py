import json
import os
from matplotlib import pyplot as plt
from VRP import VRP
import xml.etree.ElementTree as ET
from or_tools import or_tools_solve
import numpy as np

def plot_sol(data, best_sol):
    # Depot
    plt.scatter(*data["data"][0], color="red", s=200)
    # Klienci
    plt.scatter(*zip(*data["data"][1:]), s=200)

    for txt, coords in enumerate(data["data"]):
        plt.text(*coords, txt, ha="center", va="center", color="white")

    for i in range(len(best_sol)):
        color = colors[i]
        for j in range(len(best_sol[i]) - 1):
            plt.annotate(
                "", xytext=data["data"][best_sol[i][j]], xy=data["data"][best_sol[i][j + 1]],
                arrowprops=dict(arrowstyle="->,head_length=1,head_width=0.5", color=color)
            )

    plt.show()

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

for file in os.listdir("./data_bench"): # zmiana katologu pod testowanie petli
    print(f"\nReading {file}")

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
        tree = ET.parse("./data_bench/" + file) # zmiana katologu pod testowanie petli
        root = tree.getroot()

        for node in root.findall("network/nodes/node"):
            dataset["data"].append([
                float(node.find("cx").text),
                float(node.find("cy").text)
            ])

        for node in root.findall("fleet/vehicle_profile"):
            dataset["num_of_vehicles"] += 1
    
    """
    # Tutaj dałem wcześniejsze wywoływanie VRP przed benchmarkiem
    
    vrp_problem: VRP = VRP(
                dataset["data"],
                dataset["num_of_vehicles"],
                5,
                seed
            )
    # tabu search
    best_sol, best_cost = vrp_problem.tabu_search(2000)
    print(f"Tabu:\n{best_sol}\n{best_cost}")
    plot_sol(dataset, best_sol)
    # or-tools        
    best_sol, best_cost = or_tools_solve(dataset)
    print(f"Or-Tools:{best_sol}\n{best_cost}")
    plot_sol(dataset, best_sol)
    """
    
    max_iters = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500]
    results = []
    np.random.seed(42)
    
    for it in max_iters:
        costs = []
        for id in range(10):
            seed = np.random.randint(0, 1e6)
            vrp_problem: VRP = VRP(
                dataset["data"],
                dataset["num_of_vehicles"],
                5,
                seed
            )
            best_sol, best_cost = vrp_problem.tabu_search(it)
            costs.append(best_cost)
            results.append({
                "algorithm": "Tabu",
                "run_id": id,
                "seed": seed,
                "max_iter": it,
                "cost": best_cost
            })
        avg_cost = np.mean(costs)
        print(f"Tabu\t{it}\t{avg_cost:.2f}")
    
    # or-tools
    best_sol, best_cost = or_tools_solve(dataset)
    print(f"Or-Tools:{best_sol}\n{best_cost}")
    results.append({
        "algorithm": "or-tools",
        "run_id": 0,
        "seed": "-",
        "cost": best_cost
    })
