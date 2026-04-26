from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ClaimAI Multi-Agent AI Service")

class ClaimRequest(BaseModel):
    description: str
    amount: float = 0.0
    claimType: str = "medical"

@app.post("/orchestra/analyze")
async def multi_agent_analyze(claim: ClaimRequest):
    # Simulate multiple agents working together
    intake = f"Summary: {claim.description[:80]}..."
    fraud_score = round(random.uniform(1, 25), 1)
    policy_match = random.choice(["High", "Medium", "Low"])
    medical_valid = random.choice(["Valid", "Needs Review", "Invalid"])

    final_recommendation = "Auto-Approve" if fraud_score < 12 and policy_match == "High" else "Manual Review Required"

    return {
        "agents": {
            "intake_agent": intake,
            "fraud_agent": f"Fraud Risk: {fraud_score}%",
            "policy_agent": f"Policy Match: {policy_match}",
            "validation_agent": f"Medical Validation: {medical_valid}"
        },
        "final_recommendation": final_recommendation,
        "confidence": round(random.uniform(85, 98), 1),
        "message": "Multi-Agent Orchestra completed analysis"
    }
