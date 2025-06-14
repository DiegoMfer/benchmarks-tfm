import subprocess
import time
import os
import csv

def run_lubm_generator(num_universities=1, ontology_path="../uba1.7/univ-bench.owl", output_dir="outputfiles"):
    """
    Runs the LUBM generator and measures the time taken for each run.
    Args:
        num_universities (int): Number of universities to generate.
        ontology_path (str): Path to the univ-bench.owl ontology file, relative to output_dir.
        output_dir (str): Directory where the generator will be run (output files will be created here).
    Returns:
        (float, int): Time taken in seconds, number of triples generated.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Build the command with paths relative to output_dir
    command = [
        "java", "-cp", "../uba1.7/classes",
        "edu.lehigh.swat.bench.uba.Generator",
        "-univ", str(num_universities),
        "-onto", f"file:{ontology_path}"
    ]

    start_time = time.time()
    result = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
    end_time = time.time()

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    elapsed = end_time - start_time
    print(f"LUBM generation for {num_universities} universities took {elapsed:.2f} seconds.")

    # Parse triples from console output
    class_total = None
    prop_total = None
    for line in result.stdout.splitlines():
        if line.strip().startswith("CLASS INSTANCE #:"):
            try:
                class_total = int(line.strip().split(":")[-1].split(",")[0].strip())
            except Exception:
                pass
        elif line.strip().startswith("PROPERTY INSTANCE #:"):
            try:
                prop_total = int(line.strip().split(":")[-1].split(",")[0].strip())
            except Exception:
                pass
    triples = None
    if class_total is not None and prop_total is not None:
        triples = class_total + prop_total
        print(f"Total triples generated (from console output): {triples}")
    else:
        print("Could not determine triple count from console output.")

    return elapsed, triples

def run_multiple_lubm_runs(num_runs=1, num_universities=1, ontology_path="../uba1.7/univ-bench.owl", output_dir="outputfiles", csv_path="../data/lubm_benchmark_results.csv"):
    """
    Runs the LUBM generator multiple times and saves results to a CSV file.
    """
    results = []
    for i in range(num_runs):
        print(f"Run {i+1}/{num_runs}")
        elapsed, triples = run_lubm_generator(num_universities, ontology_path, output_dir)
        results.append({
            'run': i+1,
            'universities': num_universities,
            'time_seconds': elapsed,
            'triples': triples
        })
    # Write results to CSV
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['run', 'universities', 'time_seconds', 'triples']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Results saved to {csv_path}")

if __name__ == "__main__":
    run_multiple_lubm_runs(num_runs=30, num_universities=10, ontology_path="../uba1.7/univ-bench.owl", output_dir="outputfiles", csv_path="../data/lubm_benchmark_results.csv")
