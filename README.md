This project implements a Finite-State Analyzer for Mandarin disyllabic compounds using HFST. It segments words into morphemes and identifies their internal structure (e.g., Verb-Object, Modifier-Head).

1. Environment Setup (Puhti)
This project is designed to run on the CSC Puhti environment.

```bash
module load kieli
```
2. Compilation
Compile the XFST scripts into a binary transducer (.hfst). Note: The command below automatically sources the script, saves the binary, and exits.

```Bash
hfst-xfst -e "source mandarin_compounds.xfst" -e "save stack mandarin_compounds.hfst" -e "quit"
```
3. Testing
Run the analyzer on the test set (test_words.txt) and save the raw output.

```Bash
hfst-lookup -q mandarin_compounds.hfst < test_words.txt > results.txt
```
4. Evaluation
Run the Python script to calculate accuracy and analyze errors.

```Bash
python3 result_analysis.py
```
File Description

* `src/mandarin_compounds.lexc`: Lexicon definitions (POS and SemTags) .
* `src/mandarin_compounds.xfst`: Structural rules and weights used to compile the analyzer .
* `data/test_words.txt`: Raw input file containing 165 compounds for `hfst-lookup` testing .
* `data/test_words_structrues.csv`: Ground truth dataset with expected structures (e.g., ModHead, VerbObj), used for accuracy evaluation .
* `scripts/result_analysis.py`: Python script that calculates accuracy and generates the comparison report .
* `results/experiment_results_comparison.csv`: Final output comparing system predictions vs. ground truth, used for error analysis .
