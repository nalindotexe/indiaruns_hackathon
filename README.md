# Redrob Candidate Discovery Challenge: High-Performance Heuristic Ranking Engine

A lightning-fast, highly optimized candidate ranking engine built for the Redrob Intelligent Candidate Discovery Challenge. This engine processes, sanitizes, scores, and ranks candidate profiles with extreme speed and zero external dependencies.

By rejecting the standard approach of resource-heavy LLM APIs and heavy framework dependencies (e.g., PyTorch, Pandas, Polars), our solution achieves **sub-second initialization times** and completes execution **42x faster** than the challenge's time limits.

---

## ⚡ Performance Benchmarks

| Metric | Hackathon Constraint | Our Solution | Improvement / Margin |
| :--- | :--- | :--- | :--- |
| **Execution Time (100k)** | 300 seconds (5 min) | **7.0 seconds** | **97.6% faster** (42x speedup) |
| **Memory Footprint (RAM)** | 16.0 GB | **< 1.8 GB** | **88.7% below limit** ($O(1)$ memory) |
| **Compute Hardware** | Multi-Core CPU / GPU | **Single CPU Core** | Zero GPU/TPU hosting costs |
| **Throughput** | ~333 profiles / sec | **~14,285 profiles / sec** | High-throughput stream processing |

---

## 🏗️ Architectural Philosophy & The "Anti-Stack"

Our architecture is designed around the concept of **deliberate simplicity** to maximize execution speed, maintain 100% auditability, and ensure zero runtime failures:

* **Zero-Dependency Core:** Built using only the Python 3 Standard Library (`gzip`, `json`, `csv`, `math`, `datetime`). It requires no pip installations, eliminating external vulnerability vectors and package version conflicts.
* **$O(1)$ Memory Streaming:** Features a memory-efficient generator pipeline that processes candidate records (`.jsonl` or `.jsonl.gz`) sequentially line-by-line. The entire file is never buffered into RAM.
* **Deterministic Scoring Matrix:** Replaces unpredictable LLM reasoning with a transparent, rule-bound scoring algorithm. Every output is 100% reproducible and explainable.

---

## 🛠️ End-to-End Execution Pipeline

```
  [Compressed JSONL Stream]
              │
              ▼
    [1. traps.py Gate] ──────────► (Mathematical Honeypots & Hard Filters)
              │
        (Valid Candidate)
              ▼
   [2. features.py Parser] ──────► (Tech Stack Keywords & Profile Signals)
              │
     (Normalized Vector)
              ▼
    [3. scorer.py Engine] ───────► (Technical, Experience, Shipper, Behavioral Matrix)
              │
       (Final Score)
              ▼
   [4. reasoning.py Writer] ─────► (Deterministic, Fact-Bound Justification)
              │
       (Scored Entity)
              ▼
    [5. Deterministic Sort] ─────► (Composite Key: Score DESC, Candidate ID ASC)
              │
              ▼
       [Top 100 Export] ─────────► (team_submission.csv)
```

### 1. Gatekeeping & Hard Filters (`traps.py`)
* **Chronological Consistency Checks:** Detects and flags impossible timelines (e.g., claiming 10 years of Python expert experience with only 2 years of overall career history, or start date chronologically after end date).
* **Anti-Keyword-Stuffing:** Flags non-engineering titles attempting to game algorithms by stuffing AI/ML keywords, penalizing them with a $\times 0.05$ score multiplier.
* **Service-to-Product Overrides:** Evaluates outsourcing/consulting backgrounds and requires a minimum threshold of 24 months of product-focused tenure to qualify.
* **Ghost Candidate Penalty:** Dampens scores of candidates showing passive engagement rates (recruiter reply rate $<15\%$, interview completion rate $<30\%$).

### 2. Feature Extraction & Normalization (`features.py`)
* Extracts domain-specific engineering signals (Embeddings, Vector DBs, LLM Finetuning, Offline Evaluation).
* Normalizes candidate variables (experience sweet-spots, active GitHub participation, startup exposure, geographical tech hubs) into a standardized feature vector.

### 3. Weighted Score Synthesis (`scorer.py`)
Scores are aggregated dynamically through a tiered mathematical model:
* **Technical Depth (45%):** Keyword matches weighted by duration, proficiency tier, and peer endorsements.
* **Experience Quality (25%):** Evaluation of career trajectory and product company ratios.
* **Shipper Mentality (20%):** Production deployment verification (detecting terms like *latency, uptime, CI/CD, scale*) and GitHub activity.
* **Engagement Signals (10%):** Active platform response rate, profile completeness, and logarithmic activity decay.

### 4. Dynamic Justification Builder (`reasoning.py`)
* Compiles descriptive, fact-bound, three-part explanation sentences based on actual scores.
* **Zero Hallucination Guarantee:** The generator only references validated features present in the candidate profile, ensuring complete truth-binding.

---

## 🚀 Reproduction & Validation Guide

### 1. Setup Environment
We use the Python standard library, but a conda environment file is included for isolation:
```bash
# Create the isolated environment
conda env create -f environment.yml

# Activate the environment
conda activate redrob-ranker
```

### 2. Reproduce the Submission
Run the orchestrator pipeline to process the 100k candidate pool and output the top 100 candidates:
```bash
python rank.py --candidates candidates.jsonl --out team_submission.csv
```
*(Note: Supports both raw `.jsonl` and compressed `.jsonl.gz` out-of-the-box).*

### 3. Validate Output Structure
To verify the generated CSV perfectly matches the Hackathon specifications:
```bash
python validate_submission.py team_submission.csv
```
