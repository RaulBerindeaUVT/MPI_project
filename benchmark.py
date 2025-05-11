import csv
import os
import re
import time

from DPLL import run_dpll_with_timeout
from DP import run_dp_with_timeout
from RES import run_resolution_with_timeout
from parser import parse_cnf_file # type: ignore

OUTPUT_CSV_DPLL_DP = "benchmark_results_DPLL_DP.csv"
OUTPUT_CSV_RES = "benchmark_results_RES.csv"

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def benchmark_solver_dpll_dp(folder_path, timeout=60):
    results = {"SATISFIABLE": 0, "UNSATISFIABLE": 0, "TIMEOUT": 0}
    results_list = []

    print(f"Running DPLL and DP benchmarks in: {folder_path}")
    total_start = time.time()
    idx = 0

        # Save CSV
    fieldnames = ["file", "clauses", "dpll_status", "dpll_time", "dp_status", "dp_time"]
    with open(OUTPUT_CSV_DPLL_DP, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for filename in sorted(os.listdir(folder_path), key=extract_number):
            if filename.endswith(".cnf"):
                idx += 1
                print(f"\nSolving test file #{idx}: {filename}")
                
                path = os.path.join(folder_path, filename)
                clauses = parse_cnf_file(path)
                
                start_dpll = time.time()
                result_dpll = run_dpll_with_timeout(clauses, timeout=timeout)
                elapsed_dpll = (time.time() - start_dpll) * 1000

                start_dp = time.time()
                result_dp = run_dp_with_timeout(clauses, timeout=timeout)
                elapsed_dp = (time.time() - start_dp) * 1000

                if result_dpll is None:
                    dpll_status = "TIMEOUT"
                elif result_dpll:
                    dpll_status = "SATISFIABLE"
                else:
                    dpll_status = "UNSATISFIABLE"

                if result_dp is None:
                    dp_status = "TIMEOUT"
                elif result_dp:
                    dp_status = "SATISFIABLE"
                else:
                    dp_status = "UNSATISFIABLE"

                row = {"file": filename, "clauses": len(clauses), "dpll_status": dpll_status, "dpll_time": round(elapsed_dpll, 2), "dp_status": dp_status, "dp_time": round(elapsed_dp, 2)}
                writer.writerow(row)

                results[dpll_status] += 1
                results_list.append({
                    "filename": filename,
                    "clauses": len(clauses),
                    "dpll_status": dpll_status,
                    "dpll_time": round(elapsed_dpll, 2),
                    "dp_status": dp_status,
                    "dp_time": round(elapsed_dp, 2)
                })
                print(f"DPLL: {filename}: {dpll_status} in {elapsed_dpll:.2f}ms")
                print(f"DP: {filename}: {dp_status} in {elapsed_dp:.2f}ms\n")

    total_elapsed = time.time() - total_start
    total_files = len(results_list)

    print(f"\nBenchmark completed in {total_elapsed:.2f}s")
    print(f"Files resolved: {total_files}")
    print(f"Results saved to {OUTPUT_CSV_DPLL_DP}")
    print("\nSummary of results:")
    for k, v in results.items():
        print(f"{k}: {v}")


def benchmark_solver_resolution(folder_path, timeout=60):
    results = {"SATISFIABLE": 0, "UNSATISFIABLE": 0, "TIMEOUT": 0}
    results_list = []

    print(f"Running Resolution benchmark in: {folder_path}")
    total_start = time.time()
    idx = 0

        # Save CSV
    fieldnames = ["file", "clauses", "res_status", "res_time"]
    with open(OUTPUT_CSV_RES, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for filename in sorted(os.listdir(folder_path), key=extract_number):
            if filename.endswith(".cnf"):
                idx += 1
                print(f"Solving test file #{idx}: {filename}")

                path = os.path.join(folder_path, filename)
                clauses = parse_cnf_file(path)
                
                start = time.time()
                result = run_resolution_with_timeout(clauses, timeout=timeout)
                elapsed = (time.time() - start) * 1000

                if result is None:
                    status = "TIMEOUT"
                elif result:
                    status = "SATISFIABLE"
                else:
                    status = "UNSATISFIABLE"

                row = {"file": filename, "clauses": len(clauses), "res_status": status, "res_time": round(elapsed, 2)}
                writer.writerow(row)

                results[status] += 1
                results_list.append({
                    "filename": filename,
                    "clauses": len(clauses),
                    "dp_status": status,
                    "dp_time": round(elapsed, 2)
                })
                print(f"RES: {filename}: {status} in {elapsed:.2f}ms\n")

    total_elapsed = time.time() - total_start
    total_files = len(results_list)

    print(f"\nBenchmark completed in {total_elapsed:.2f}s")
    print(f"Files resolved: {total_files}")
    print(f"Results saved to {OUTPUT_CSV_RES}")
    print("\nSummary of results:")
    for k, v in results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    benchmark_solver_dpll_dp("./test_files_dpll_dp", timeout=60)
    benchmark_solver_resolution("./test_files_res", timeout=60)
