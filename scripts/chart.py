import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

# Get the base directory (prompt_attacks)
base_dir = Path(__file__).parent.parent
output_dir = base_dir / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# Load data
reviewed = pd.read_csv(output_dir / "MANUAL_REVIEW.csv")

# Compute metrics
# Attack Success Rate (ASR) - percentage of attacks that succeeded per model
asr = reviewed[reviewed['manual'] == 'YES'].groupby('model').size() / reviewed.groupby('model').size() * 100
asr = asr.round(2)

# OSR: % of all 112 attacks that succeeded (per model)
total_success = reviewed[reviewed['manual'] == 'YES'].groupby('model').size()
osr = (total_success / 112 * 100).round(2)

print("ATTACK SUCCESS RATE (ASR):")
print(asr)
print("\nOUTPUT SUCCESS RATE (OSR):")
print(osr)

# Chart - show YES/NO distribution per model
plt.figure(figsize=(10, 6))
manual_counts = reviewed.groupby(['model', 'manual']).size().unstack(fill_value=0)
manual_counts_pct = manual_counts.div(manual_counts.sum(axis=1), axis=0) * 100
manual_counts_pct.plot(kind='bar', ax=plt.gca(), color=['#d62728', '#2ca02c'])
plt.title("Jailbreak Manual Review Results – YES vs NO")
plt.ylabel("Percentage (%)")
plt.xlabel("Model")
plt.ylim(0, 100)
plt.legend(title='Result', labels=['NO', 'YES'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "asr_final.png", dpi=200, bbox_inches='tight')
plt.show()

# Top 5 attacks (if any successful ones exist)
top5 = reviewed[reviewed['manual'] == 'YES'].groupby(['id', 'type', 'prompt']).size()
if len(top5) > 0:
    top5 = top5.reset_index(name='success_count').sort_values('success_count', ascending=False).head(5)
    top5_markdown = "\n".join([
        "| ID | Type | Prompt | Count |",
        "|---|---|---|---|"
    ] + [f"| {row['id']} | {row['type']} | {row['prompt'][:50]}... | {row['success_count']} |" for _, row in top5.iterrows()])
else:
    top5_markdown = "*No successful attacks marked in manual review*"


# Pie chart - Attack type distribution
plt.figure(figsize=(10, 8))
attack_type_counts = reviewed['type'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
plt.pie(attack_type_counts.values, labels=attack_type_counts.index, autopct='%1.1f%%',
        colors=colors[:len(attack_type_counts)], startangle=90, textprops={'fontsize': 11, 'weight': 'bold'})
plt.title("Distribution of Attack Types Used", fontsize=14, weight='bold', pad=20)
plt.axis('equal')
plt.tight_layout()
plt.savefig(output_dir / "attack_types_pie_chart.png", dpi=200, bbox_inches='tight')
plt.show()


print(f"CHART: {output_dir / 'asr_final.png'}")
print(f"ATTACK TYPES PIE CHART: {output_dir / 'attack_types_pie_chart.png'}")
print(f"REVIEW: {output_dir / 'MANUAL_REVIEW.csv'}")    