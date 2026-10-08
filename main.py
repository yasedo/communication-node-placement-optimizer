"""Educational coverage optimization on a synthetic grid. No RF model."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle
import numpy as np


def make_terrain(size: int = 30, restricted: bool = True) -> np.ndarray:
    """True cells are both placement candidates and coverage targets."""
    if not isinstance(size, int) or not 5 <= size <= 80:
        raise ValueError("Grid size must be an integer between 5 and 80.")
    allowed = np.ones((size, size), dtype=bool)
    if restricted:
        # These are excluded cells, not radio-blocking obstacles.
        allowed[size // 3:size // 2, size // 5:2 * size // 5] = False
        allowed[2 * size // 3:4 * size // 5, 3 * size // 5:4 * size // 5] = False
    return allowed


def validate_model(allowed: np.ndarray, nodes: int, radius: float) -> None:
    if allowed.ndim != 2 or allowed.dtype != bool or not allowed.any():
        raise ValueError("Terrain must be a nonempty 2D Boolean mask with target cells.")
    if not isinstance(nodes, int) or not 1 <= nodes <= np.count_nonzero(allowed):
        raise ValueError("Node count must be between 1 and the available cell count.")
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("Coverage radius must be finite and positive.")


def validate_layout(layout: np.ndarray, allowed: np.ndarray) -> None:
    if layout.ndim != 2 or layout.shape[1] != 2 or len(layout) == 0:
        raise ValueError("Layout must have shape (node_count, 2).")
    if not np.issubdtype(layout.dtype, np.integer):
        raise ValueError("Node coordinates must be integers.")
    x, y = layout.T
    if np.any(x < 0) or np.any(x >= allowed.shape[1]) or np.any(y < 0) or np.any(y >= allowed.shape[0]):
        raise ValueError("Node coordinates must be inside the grid.")
    if not allowed[y, x].all() or len(np.unique(layout, axis=0)) != len(layout):
        raise ValueError("Nodes must occupy distinct allowed cells.")


def coverage_mask(layout: np.ndarray, allowed: np.ndarray, radius: float) -> np.ndarray:
    """A cell is covered when its center is within radius of any node."""
    validate_model(allowed, len(layout), radius)
    validate_layout(layout, allowed)
    y, x = np.indices(allowed.shape)
    squared_distance = (x[..., None] - layout[:, 0]) ** 2 + (y[..., None] - layout[:, 1]) ** 2
    return allowed & np.any(squared_distance <= radius ** 2, axis=2)


def coverage_score(layout: np.ndarray, allowed: np.ndarray, radius: float) -> float:
    return float(coverage_mask(layout, allowed, radius).sum() / allowed.sum())


def random_layout(allowed: np.ndarray, nodes: int, rng: np.random.Generator) -> np.ndarray:
    # np.argwhere gives (y, x); the rest of the application uses (x, y).
    positions = np.argwhere(allowed)[:, ::-1]
    return positions[rng.choice(len(positions), size=nodes, replace=False)].copy()


def optimize(initial: np.ndarray, allowed: np.ndarray, radius: float,
             iterations: int = 1500, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """Monotone stochastic hill climbing; no claim of a global optimum."""
    if not isinstance(iterations, int) or iterations < 0:
        raise ValueError("Iteration count must be a nonnegative integer.")
    validate_model(allowed, len(initial), radius)
    validate_layout(initial, allowed)
    rng = np.random.default_rng(seed)
    positions = np.argwhere(allowed)[:, ::-1]
    best = initial.copy()
    score = coverage_score(best, allowed, radius)
    history = [score]
    step = max(1, int(round(radius / 2)))
    for _ in range(iterations):
        candidate = best.copy()
        i = int(rng.integers(len(best)))
        if rng.random() < 0.25:
            new_position = positions[rng.integers(len(positions))]
        else:
            new_position = best[i] + rng.integers(-step, step + 1, size=2)
        x, y = new_position
        valid = 0 <= x < allowed.shape[1] and 0 <= y < allowed.shape[0]
        if valid and allowed[y, x] and not np.any(np.all(best[np.arange(len(best)) != i] == new_position, axis=1)):
            candidate[i] = new_position
        # Even an invalid proposal consumes one evaluation, for equal budgets.
        candidate_score = coverage_score(candidate, allowed, radius)
        if candidate_score > score:
            best, score = candidate, candidate_score
        history.append(score)
    return best, np.asarray(history)


def random_search(initial: np.ndarray, allowed: np.ndarray, radius: float,
                  iterations: int, seed: int) -> tuple[np.ndarray, float]:
    """Equal-budget baseline: best of independent random layouts plus initial."""
    if not isinstance(iterations, int) or iterations < 0:
        raise ValueError("Iteration count must be a nonnegative integer.")
    validate_model(allowed, len(initial), radius)
    validate_layout(initial, allowed)
    rng = np.random.default_rng(seed)
    best = initial.copy()
    score = coverage_score(best, allowed, radius)
    for _ in range(iterations):
        candidate = random_layout(allowed, len(initial), rng)
        candidate_score = coverage_score(candidate, allowed, radius)
        if candidate_score > score:
            best, score = candidate, candidate_score
    return best, score


def plot_results(initial, optimized, allowed, radius, history, output):
    colors = ListedColormap(["#e2e8f0", "#fff4d6", "#89c5ef"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), constrained_layout=True)
    for ax, layout, title in zip(axes, [initial, optimized], ["Initial random placement", "Hill-climbing result"]):
        covered = coverage_mask(layout, allowed, radius)
        raster = np.where(~allowed, 0, np.where(covered, 2, 1))
        ax.imshow(raster, origin="lower", cmap=colors, vmin=0, vmax=2,
                  extent=(-0.5, allowed.shape[1] - 0.5, -0.5, allowed.shape[0] - 0.5))
        for number, (x, y) in enumerate(layout, start=1):
            ax.add_patch(Circle((x, y), radius, fill=False, edgecolor="#12446b", linewidth=1, alpha=.5))
            ax.scatter(x, y, s=50, color="#123859", zorder=3)
            ax.annotate(str(number), (x, y), xytext=(4, 4), textcoords="offset points", fontsize=9)
        ax.set_title(f"{title}\nCoverage: {100 * coverage_score(layout, allowed, radius):.2f}%", fontweight="bold")
        ax.set_xlabel("x [grid units]")
        ax.set_ylabel("y [grid units]")
        ax.set_xlim(-.5, allowed.shape[1] - .5)
        ax.set_ylim(-.5, allowed.shape[0] - .5)
        ax.set_aspect("equal")
    fig.suptitle("Synthetic area coverage | blue: covered, cream: uncovered, gray: excluded", fontsize=12)
    fig.savefig(output / "coverage_comparison.png", dpi=170)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)
    ax.plot(np.arange(len(history)), 100 * history, color="#1379ae", linewidth=2)
    ax.set(xlabel="Proposal iterations", ylabel="Best coverage [%]", title="Best-so-far coverage (seeded hill climbing)")
    ax.grid(alpha=.25)
    fig.savefig(output / "convergence.png", dpi=170)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid-size", type=int, default=30)
    parser.add_argument("--nodes", type=int, default=5)
    parser.add_argument("--radius", type=float, default=6.0)
    parser.add_argument("--iterations", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--open-terrain", action="store_true", help="Remove excluded areas.")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args(argv)
    try:
        if args.seed < 0 or args.iterations < 0:
            raise ValueError("Seed and iterations must be nonnegative.")
        allowed = make_terrain(args.grid_size, not args.open_terrain)
        validate_model(allowed, args.nodes, args.radius)
        initial = random_layout(allowed, args.nodes, np.random.default_rng(args.seed))
        best, history = optimize(initial, allowed, args.radius, args.iterations, args.seed + 1)
        _, baseline = random_search(initial, allowed, args.radius, args.iterations, args.seed + 2)
    except ValueError as exc:
        parser.error(str(exc))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plot_results(initial, best, allowed, args.radius, history, args.output_dir)
    summary = {
        "model": "Discrete circular coverage; excluded cells are not RF obstacles",
        "algorithm": "Stochastic hill climbing with local moves and uniform jumps",
        "grid_size": args.grid_size, "nodes": args.nodes, "radius_grid_units": args.radius,
        "restricted_areas": not args.open_terrain, "seed": args.seed,
        "optimizer_seed": args.seed + 1, "random_search_seed": args.seed + 2,
        "iterations": args.iterations, "evaluations_per_method": args.iterations + 1,
        "target_cells": int(allowed.sum()),
        "initial_covered_cells": int(coverage_mask(initial, allowed, args.radius).sum()),
        "optimized_covered_cells": int(coverage_mask(best, allowed, args.radius).sum()),
        "initial_coverage_percent": float(history[0] * 100),
        "optimized_coverage_percent": float(history[-1] * 100),
        "improvement_percentage_points": float((history[-1] - history[0]) * 100),
        "random_search_coverage_percent": baseline * 100,
        "numpy_version": np.__version__, "matplotlib_version": matplotlib.__version__,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (args.output_dir / "node_positions.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["node", "initial_x", "initial_y", "optimized_x", "optimized_y"])
        for i, (before, after) in enumerate(zip(initial, best), 1):
            writer.writerow([i, *before, *after])
    with (args.output_dir / "convergence.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["iteration", "best_coverage_percent"])
        writer.writerows(enumerate(history * 100))
    print(json.dumps(summary, indent=2))
    print(f"Saved plots and data to: {args.output_dir.resolve()}")
    return summary


if __name__ == "__main__":
    main()
