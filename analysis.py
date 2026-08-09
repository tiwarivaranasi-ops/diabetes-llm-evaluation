from pathlib import Path
import csv
from collections import Counter
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "question_scores.csv"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

with RESULTS.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

systems = ["ChatGPT", "Gemini", "Claude", "Perplexity"]
scores = {system: [int(row[system]) for row in rows] for system in systems}

print("Overall results")
for system in systems:
    total = sum(scores[system])
    print(f"{system:12s} {total:2d}/96  ({total/96*100:.2f}%)")

print("\nScore distributions")
for system in systems:
    counts = Counter(scores[system])
    print(system, {score: counts.get(score, 0) for score in range(4)})

percentages = [sum(scores[s]) / 96 * 100 for s in systems]
plt.figure(figsize=(8, 5))
plt.bar(systems, percentages)
plt.ylabel("Score (%)")
plt.title("Overall Diabetes LLM Evaluation Scores")
plt.ylim(0, 100)
for i, value in enumerate(percentages):
    plt.text(i, value + 1.5, f"{value:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(FIGURES / "overall_scores.png", dpi=200, bbox_inches="tight")
plt.close()

bottom = [0] * len(systems)
plt.figure(figsize=(9, 5))
for score in range(4):
    values = [scores[s].count(score) for s in systems]
    plt.bar(systems, values, bottom=bottom, label=f"Score {score}")
    bottom = [bottom[i] + values[i] for i in range(len(systems))]
plt.ylabel("Number of Questions")
plt.title("Distribution of Rubric Scores")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "score_distribution.png", dpi=200, bbox_inches="tight")
plt.close()
