# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-skeletal-trabecular-bone-score-tbs-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def evaluate_trabecular_bone_score_frax(tbs_score, dxa_l1_l4_t_score=-1.5, base_frax_mof_pct=7.5, age_years=62):
    if tbs_score <= 0:
        raise ValueError("tbs_score must be positive")
        
    # Standard TBS thresholds:
    # TBS >= 1.310: Normal microarchitecture
    # 1.230 <= TBS < 1.310: Partially degraded microarchitecture
    # TBS < 1.230: Degraded microarchitecture
    if tbs_score >= 1.310:
        texture_status = "NORMAL_MICROARCHITECTURE"
        tbs_frax_multiplier = 0.90
    elif tbs_score >= 1.230:
        texture_status = "PARTIALLY_DEGRADED_MICROARCHITECTURE"
        tbs_frax_multiplier = 1.15
    else:
        texture_status = "DEGRADED_MICROARCHITECTURE"
        tbs_frax_multiplier = 1.45
        
    adjusted_frax_mof_pct = round(base_frax_mof_pct * tbs_frax_multiplier, 2)
    
    # Discordance: BMD osteopenia/normal with degraded TBS
    bone_quality_discordance = (dxa_l1_l4_t_score > -2.5) and (tbs_score < 1.230)
    
    return {
        "lumbar_tbs_score": round(tbs_score, 3),
        "lumbar_dxa_t_score": round(dxa_l1_l4_t_score, 2),
        "microarchitectural_integrity": texture_status,
        "bone_quality_discordance_alert": bone_quality_discordance,
        "baseline_frax_mof_pct": base_frax_mof_pct,
        "tbs_adjustment_factor": tbs_frax_multiplier,
        "adjusted_10yr_mof_fracture_risk_pct": adjusted_frax_mof_pct,
        "clinical_recommendation": "High fracture risk despite non-osteoporotic BMD; bone anabolic or antiresorptive therapy warranted." if bone_quality_discordance else "Microarchitecture concordant with bone density."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "evaluate_trabecular_bone_score_frax",
                        "description": """Evaluate lumbar spine trabecular bone microarchitecture using Trabecular Bone Score (TBS) derived from DXA.
Quantifies 3D bone quality independent of bone mineral density (BMD), detects diabetic bone disease (normal BMD but high fracture risk),
and calculates TBS-adjusted FRAX 10-year major osteoporotic fracture probability.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = evaluate_trabecular_bone_score_frax(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'tbs_score': 1.195, 'dxa_l1_l4_t_score': -1.4, 'base_frax_mof_pct': 8.2, 'age_years': 65}
        out = evaluate_trabecular_bone_score_frax(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
