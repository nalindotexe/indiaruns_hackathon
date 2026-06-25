#!/usr/bin/env python3
import argparse
import gzip
import json
import csv
import sys
import os

# Add current directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ranker.traps import is_honeypot, get_stuffer_penalty, get_ghost_penalty, is_hard_filtered
from ranker.features import extract_features
from ranker.scorer import compute_score
from ranker.reasoning import generate_reasoning

def process_candidates(input_path):
    results = []
    
    # Handle both .gz and plain .jsonl/json
    opener = gzip.open if input_path.endswith('.gz') else open
    mode = 'rt' if input_path.endswith('.gz') else 'r'
    
    with opener(input_path, mode, encoding='utf-8') as f:
        # If it's a JSON array (like sample_candidates.json)
        if input_path.endswith('.json'):
            data = json.load(f)
            iterator = data
        else:
            iterator = f
            
        for line_or_item in iterator:
            if isinstance(line_or_item, str):
                line = line_or_item.strip()
                if not line:
                    continue
                candidate = json.loads(line)
            else:
                candidate = line_or_item
                
            cid = candidate.get('candidate_id')
            if not cid:
                continue
                
            # 1. Hard filters and honeypots (Instant 0)
            if is_honeypot(candidate) or is_hard_filtered(candidate):
                # We can skip computing features and just set score to 0
                results.append((cid, 0.0, "Candidate does not meet base criteria or failed validation."))
                continue
                
            # 2. Trap penalties
            stuffer_penalty = get_stuffer_penalty(candidate)
            if stuffer_penalty == 0:
                results.append((cid, 0.0, "Profile aligns with non-engineering tracks."))
                continue
                
            ghost_penalty = get_ghost_penalty(candidate)
            
            # 3. Feature extraction
            features = extract_features(candidate)
            
            # 4. Score calculation
            score = compute_score(features, ghost_penalty, 1.0, stuffer_penalty)
            
            # 5. Reasoning generation
            reasoning = generate_reasoning(candidate, features)
            
            # Round score to 4 decimal places BEFORE appending and sorting
            # This ensures that tie-breaks are determined precisely how the CSV validator reads them.
            results.append((cid, round(score, 4), reasoning))
            
    return results

def main():
    parser = argparse.ArgumentParser(description='Redrob Hackathon Ranker')
    parser.add_argument('--candidates', required=True, help='Path to candidates.jsonl or .gz')
    parser.add_argument('--out', required=True, help='Path to output submission.csv')
    args = parser.parse_args()
    
    print(f"Processing candidates from {args.candidates}...")
    scored_candidates = process_candidates(args.candidates)
    
    print(f"Sorting {len(scored_candidates)} candidates...")
    # Sort by score descending, then candidate_id ascending for deterministic tie-breaks
    scored_candidates.sort(key=lambda x: (-x[1], x[0]))
    
    # Get top 100
    top_100 = scored_candidates[:100]
    
    print(f"Writing top 100 to {args.out}...")
    with open(args.out, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['candidate_id', 'rank', 'score', 'reasoning'])
        for rank, (cid, score, reasoning) in enumerate(top_100, 1):
            writer.writerow([cid, rank, f"{score:.4f}", reasoning])
            
    print("Done! 🎉")

if __name__ == '__main__':
    main()
