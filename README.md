# genpark-personal-agent-skeletal-trabecular-bone-score-tbs-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Lumbar spine Trabecular Bone Score (TBS) microarchitectural texture evaluation & FRAX fracture risk adjustor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `evaluate_trabecular_bone_score_frax`
- **Category**: `personal_agent`

### Method Documentation
Evaluate lumbar spine trabecular bone microarchitecture using Trabecular Bone Score (TBS) derived from DXA.
Quantifies 3D bone quality independent of bone mineral density (BMD), detects diabetic bone disease (normal BMD but high fracture risk),
and calculates TBS-adjusted FRAX 10-year major osteoporotic fracture probability.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "evaluate_trabecular_bone_score_frax",
    "arguments": {
    "tbs_score": 1.195,
    "dxa_l1_l4_t_score": -1.4,
    "base_frax_mof_pct": 8.2,
    "age_years": 65
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
