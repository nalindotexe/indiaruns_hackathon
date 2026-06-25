# Redrob AI Ranker

A lightning-fast, highly optimized candidate ranking engine built for the Redrob Intelligent Candidate Discovery Challenge.

This solution completely avoids LLM bottlenecks by employing a hand-crafted, multi-stage heuristic pipeline. It processes 100,000 candidates in under **10 seconds** on a standard CPU, utilizing zero external dependencies to drastically reduce memory overhead.

## Setup

We use pure Python Standard Library components for maximum efficiency, but a Conda environment file is provided for isolated reproducibility.

```bash
# 1. Create the isolated environment
conda env create -f environment.yml

# 2. Activate the environment
conda activate redrob-ranker
```

## Reproducing the Submission

To generate the exact `team_submission.csv` from the 100k candidate pool, run this single command:

```bash
python rank.py --candidates candidates.jsonl --out team_submission.csv
```

*(Note: The script natively accepts both `.jsonl` and `.jsonl.gz` formats without modification).*

## Validating the Output

To verify the generated CSV perfectly matches the Hackathon specifications:

```bash
python validate_submission.py team_submission.csv
```

## Architecture Overview
* **Zero-dependency Data Streaming**: Memory footprint stays under 2GB by streaming the JSON lines sequentially.
* **Honeypot/Trap Detectors**: Instantly drops impossible timeline profiles and non-engineering keyword stuffers.
* **Weighted Signal Matrix**: Combines Technical Depth (45%), Experience Quality (25%), Shipper Mentality (20%), and Behavioral Platform Engagement (10%) into a robust final score.
* **Dynamic Reasoning Engine**: Assembles factual justification sentences strictly based on parsed candidate keys.

# Results

- `output.valid.csv` is the generated output csv file from `rank.py` script, which is validated by the `validate_submission.py`
- and they asked us to perform this by just using the CPU, completely avoiding the GPU, in **5 min**
- but this script generates that in just **7 sec**
