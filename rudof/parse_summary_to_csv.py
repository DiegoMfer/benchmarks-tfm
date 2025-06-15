import re
import csv

input_file = "all_runs_summary.txt"
output_file = "rudof_benchmark_results.csv"

pattern = re.compile(
    r"Graph with (\d+) entities and (\d+) triples was generated in ([\d\.]+)s"
)

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["run", "entities", "time_seconds", "triples"])
    for i, line in enumerate(infile, 1):
        match = pattern.search(line)
        if match:
            entities = int(match.group(1))
            triples = int(match.group(2))
            time_seconds = float(match.group(3))
            writer.writerow([i, entities, time_seconds, triples])
