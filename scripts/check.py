results = []

for data in attack_data:
    for model_id, generator in models.items():
        print(f"Testing prompt {data['id']} on {model_id}...")
        try:
            # Generate the output
            output = generator(
                data["text"][0],
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                repetition_penalty=1.1
            )[0]['generated_text']

            # Store the result
            results.append({
                "prompt_id": data["id"],
                "attack_type": data["type"],
                "prompt_text": data["text"][0],
                "model": model_id,
                "output": output
            })
        except Exception as e:
            print(f"An error occurred with model {model_id}: {e}")
            results.append({
                "prompt_id": data["id"],
                "attack_type": data["type"],
                "prompt_text": data["text"][0],
                "model": model_id,
                "output": f"Error: {e}"
            })


results_df = pd.DataFrame(results)
results_df.to_csv("attack_results.csv", index=False)

print("Attack runner finished. Results saved to attack_results.csv")
print(results_df.head())