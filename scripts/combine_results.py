import pandas as pd
from pathlib import Path

# Get the base directory (prompt_attacks)
base_dir = Path(__file__).parent.parent
output_dir = base_dir / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# Load CSV files
phi3 = pd.read_csv(output_dir / "phi-3-mini_results.csv")
llama = pd.read_csv(output_dir / "llama2-7b-chat_results.csv")

phi3['model'] = 'Phi-3-mini'
llama['model'] = 'Llama-2-7B'

df = pd.concat([phi3, llama], ignore_index=True)
print(f"Loaded {len(df)} outputs (112 attacks × 2 models)")
df.to_csv(output_dir / "combined_results.csv", index=False)
print(f"Saved to {output_dir / 'combined_results.csv'}")





# Add manual review column for all outputs
df['manual'] = "YES"

# Save all outputs for manual review
df[['id', 'type', 'prompt', 'output', 'model', 'manual']].to_csv(
    output_dir / "MANUAL_REVIEW.csv", index=False
)
print(f"Saved all {len(df)} outputs to {output_dir / 'MANUAL_REVIEW.csv'} for manual review")

