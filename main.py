from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ClaimAI AI Service")

class ClaimRequest(BaseModel):
    description: str
    amount: float = 0.0

@app.post("/analyze")
async def analyze_claim(claim: ClaimRequest):
    # Simulate AI Analysis
    fraud_risk = round(random.uniform(1, 15), 1)
    confidence = round(random.uniform(85, 98), 1)
    
    return {
        "claimId": f"CLM-{random.randint(10000, 99999)}",
        "fraudRisk": f"{fraud_risk}%",
        "approvalConfidence": f"{confidence}%",
        "recommendation": "Auto-approve with minor manual review" if fraud_risk < 10 else "Manual review required",
        "message": "AI Analysis completed successfully",
        "processedAmount": claim.amount
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ClaimAI AI Service (Python)"}
