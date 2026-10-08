# Validation record

Validation date: 8 October 2026. Tested using 64-bit Python 3.12.14.

Pinned requirements installed in a new virtual environment without system site packages. Tests and the default CLI were run in that environment. Repeated default JSON, CSV and PNG outputs were byte-for-byte identical to the packaged results.

## Automated unit-test output

```text
test_hand_calculated_center_and_corner (test_main.CoverageTests.test_hand_calculated_center_and_corner) ... ok
test_invalid_models_and_layouts (test_main.CoverageTests.test_invalid_models_and_layouts) ... ok
test_no_input_mutation_and_zero_iterations (test_main.CoverageTests.test_no_input_mutation_and_zero_iterations) ... ok
test_overlap_counted_once_and_excluded_cells_ignored (test_main.CoverageTests.test_overlap_counted_once_and_excluded_cells_ignored) ... ok
test_seed_reproducibility_and_monotonicity (test_main.CoverageTests.test_seed_reproducibility_and_monotonicity) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.084s

OK
```

## Additional checks

Default run, command-line input rejection, documented custom cases, notebook code-cell syntax, README image paths and UTF-8 text were checked. Plots were opened for visual inspection. See the shared upload guide for the combined validation summary.

## Limits

Colab-specific upload/download cells were not executed inside a live Colab session. GitHub account creation and browser upload were not performed. No real RF measurements or power-plant measurements were used. These checks validate the educational implementations.

Additional CLI integration checks passed for both projects: seven invalid input cases exited with a concise error and no traceback; zero-iteration and documented custom runs completed; Rankine partial/empty sweeps were reported correctly and stale empty-sweep artifacts were removed.
