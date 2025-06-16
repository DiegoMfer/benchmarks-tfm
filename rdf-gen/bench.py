import subprocess
import time
import csv
import rdflib

def run_rdfgen(input_shape: str, output_file: str, instance_count: int):
    """
    Calls the rdfgen CLI to generate RDF data from SHACL shapes.

    :param input_shape: Path to the SHACL shape file (Turtle)
    :param output_file: Path to the RDF output file
    :param instance_count: Number of RDF entities to generate
    """
    try:
        print(f"Generating RDF data with: {input_shape}, {instance_count} instances...")
        subprocess.run(["rdfgen", input_shape, output_file, str(instance_count)],
                       check=True)
        print(f"✅ RDF data successfully written to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ rdfgen failed with error: {e}")

def count_triples(rdf_file):
    g = rdflib.Graph()
    try:
        g.parse(rdf_file, format="turtle")
        return len(g)
    except Exception as e:
        print(f"Error parsing {rdf_file}: {e}")
        return None

def benchmark_rdfgen(shape_file, output_file, num_instances, n_runs=10, csv_filename="results.csv"):
    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["run", "entities", "time_seconds", "triples"])
        for i in range(1, n_runs + 1):
            start = time.time()
            run_rdfgen(shape_file, output_file, num_instances)
            end = time.time()
            triples = count_triples(output_file)
            exec_time = end - start
            print(f"Run {i}: Execution time = {exec_time:.2f} s, Triples = {triples}")
            writer.writerow([i, num_instances, f"{exec_time:.12f}", triples])
            time.sleep(1)

if __name__ == "__main__":
    # Example usage
    shape_file = "input-shape.ttl"
    output_file = "output.ttl"
    num_instances = 50
    n_runs = 30
    csv_filename = "rdfgraphgen_benchmark_results.csv"
    benchmark_rdfgen(shape_file, output_file, num_instances, n_runs, csv_filename)
