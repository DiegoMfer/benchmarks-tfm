import subprocess

COMMAND = [
    "cargo", "run", "--release", "-p", "generator", "--",
    "generator/examples/schema.shex", "20000", "generator/examples/output.ttl"
]

with open("all_runs_summary.txt", "w") as summary:
    for i in range(1, 31):
        print(f"Run {i}")
        result = subprocess.run(COMMAND, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("Graph with"):
                summary.write(line + "\n")
                break
