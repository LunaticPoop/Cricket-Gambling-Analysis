# System Architecture

## Overview

CricketGenAI is a low-latency cricket analytics engine that combines:

- Implied probability modeling
- Market movement detection
- Toss-based simulation
- Venue profiling
- Volatility scoring
- Dynamic confidence scoring
- Prompt compression via ScaleDown

---

## Data Flow

1. Load structured dataset (matches.csv)
2. Generate cricket match prompt
3. Compress prompt using ScaleDown API
4. Compute implied probability from odds
5. Apply market movement detection
6. Simulate toss-based probability adjustments
7. Classify volatility and confidence
8. Output structured intelligence report

---

## Key Components

### Dataset Layer
Structured CSV with match and odds data.

### Compression Layer
Uses ScaleDown API to reduce token size and latency.

### Analytics Layer
Implements:
- Probability modeling
- Risk classification
- Market sentiment detection
- Scenario simulation

### Output Layer
- Structured mode
- Toddler mode (human-readable explanation)
