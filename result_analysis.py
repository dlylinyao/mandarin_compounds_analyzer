import pandas as pd
import os

def main():
    ground_truth_file = 'test_words_structrues.csv'
    results_file = 'results.txt'
    output_file = 'experiment_results_comparison.csv'

    if not os.path.exists(ground_truth_file) or not os.path.exists(results_file):
        print(f"Error: Input files not found. Please ensure '{ground_truth_file}' and '{results_file}' are in the current directory.")
        return

    print("Reading data...")

    try:
        df_gt = pd.read_csv(ground_truth_file)
        df_gt['Word'] = df_gt['Word'].astype(str).str.strip()
        df_gt['Expected_Structure'] = df_gt['Expected_Structure'].astype(str).str.strip()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    parsed_data = []
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) < 3:
                    continue
                
                word = parts[0].strip()
                type_field = parts[1].strip()
                score_str = parts[2].strip()
                
                if type_field.startswith('Structure:'):
                    structure = type_field.replace('Structure:', '').strip()
                    try:
                        score = float(score_str)
                        parsed_data.append({
                            'Word': word, 
                            'Predicted_Structure': structure, 
                            'Weight': score
                        })
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return

    if not parsed_data:
        print("No valid data extracted from TXT file, please check file format.")
        return

    df_preds_raw = pd.DataFrame(parsed_data)

    df_preds_raw = df_preds_raw.sort_values(by=['Word', 'Weight'], ascending=[True, True])
    
    best_preds = df_preds_raw.drop_duplicates(subset=['Word'], keep='first')

    df_merged = pd.merge(df_gt, best_preds[['Word', 'Predicted_Structure', 'Weight']], on='Word', how='left')

    df_merged['Predicted_Structure'] = df_merged['Predicted_Structure'].fillna('No Prediction')

    df_merged['is_correct'] = df_merged['Expected_Structure'] == df_merged['Predicted_Structure']


    total_words = len(df_merged)
    correct_count = df_merged['is_correct'].sum()
    accuracy = correct_count / total_words if total_words > 0 else 0

    print("-" * 40)
    print(f"Calculation Complete!")
    print(f"Total Words: {total_words}")
    print(f"Correct Predictions: {correct_count}")
    print(f"Accuracy: {accuracy:.2%}")
    print("-" * 40)


    output_df = df_merged[['Word', 'Expected_Structure', 'Predicted_Structure', 'Weight', 'is_correct']].copy()
    output_df.rename(columns={'is_correct': 'Correct'}, inplace=True)
    
    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Detailed comparison results saved to: {output_file}")

if __name__ == "__main__":
    main()