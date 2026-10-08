"""Repeat both search methods across five seeds with equal evaluation budgets."""

import csv
from pathlib import Path
import numpy as np
from main import make_terrain, optimize, random_layout, random_search


def main():
    allowed = make_terrain(30)
    rows = []
    for seed in [0, 1, 2, 3, 42]:
        initial = random_layout(allowed, 5, np.random.default_rng(seed))
        _, history = optimize(initial, allowed, 6, 1500, seed + 1)
        _, baseline = random_search(initial, allowed, 6, 1500, seed + 2)
        rows.append([seed, 1501, history[0] * 100, history[-1] * 100, baseline * 100])
    Path("results").mkdir(exist_ok=True)
    with Path("results/benchmark.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["initial_seed", "evaluations_per_method", "initial_percent", "hill_climbing_percent", "random_search_percent"])
        writer.writerows(rows)
    for row in rows:
        print(f"Seed {row[0]:2d}: initial {row[2]:.2f}%, hill climbing {row[3]:.2f}%, random search {row[4]:.2f}%")
    print("Five illustrative runs; not a statistical performance guarantee.")


if __name__ == "__main__":
    main()
