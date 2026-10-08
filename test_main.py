import unittest
import numpy as np
from main import coverage_mask, coverage_score, make_terrain, optimize, random_layout, random_search, validate_model


class CoverageTests(unittest.TestCase):
    def test_hand_calculated_center_and_corner(self):
        terrain = np.ones((5, 5), dtype=bool)
        self.assertEqual(coverage_mask(np.array([[2, 2]]), terrain, 1).sum(), 5)
        self.assertEqual(coverage_mask(np.array([[0, 0]]), terrain, 1).sum(), 3)

    def test_overlap_counted_once_and_excluded_cells_ignored(self):
        terrain = np.ones((5, 5), dtype=bool)
        terrain[2, 2] = False
        self.assertEqual(coverage_score(np.array([[0, 0], [4, 4]]), terrain, 10), 1.0)
        self.assertFalse(coverage_mask(np.array([[0, 0]]), terrain, 10)[2, 2])

    def test_seed_reproducibility_and_monotonicity(self):
        terrain = make_terrain(12)
        initial = random_layout(terrain, 3, np.random.default_rng(7))
        a, history = optimize(initial, terrain, 3, 100, 8)
        b, repeated = optimize(initial, terrain, 3, 100, 8)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(history, repeated)
        self.assertTrue(np.all(np.diff(history) >= 0))
        self.assertEqual(len(history), 101)
        self.assertGreaterEqual(history[-1], history[0])
        self.assertTrue(terrain[a[:, 1], a[:, 0]].all())
        self.assertEqual(len(np.unique(a, axis=0)), 3)

    def test_no_input_mutation_and_zero_iterations(self):
        terrain = make_terrain(10)
        initial = random_layout(terrain, 2, np.random.default_rng(4))
        original = initial.copy()
        best, _ = optimize(initial, terrain, 2, 0, 5)
        np.testing.assert_array_equal(initial, original)
        np.testing.assert_array_equal(best, initial)
        _, baseline = random_search(initial, terrain, 2, 0, 6)
        self.assertEqual(baseline, coverage_score(initial, terrain, 2))

    def test_invalid_models_and_layouts(self):
        terrain = make_terrain(10)
        for nodes, radius in [(0, 2), (1000, 2), (1, 0), (1, float("nan")), (1, float("inf"))]:
            with self.assertRaises(ValueError):
                validate_model(terrain, nodes, radius)
        for layout in [np.array([[-1, 0]]), np.array([[0, 0], [0, 0]]), np.array([[0.5, 0]])]:
            with self.assertRaises(ValueError):
                coverage_mask(layout, terrain, 2)
        with self.assertRaises(ValueError):
            optimize(np.array([[0, 0]]), terrain, 2, -1)


if __name__ == "__main__":
    unittest.main()
