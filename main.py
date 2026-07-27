from enum import Enum
from hashlib import sha256
from random import Random
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="ClaimAI Multi-Agent AI Service",
    version="1.0.0",
    description="Deterministic multi-agent claim analysis service",
)


class ClaimType(str, Enum):
    MEDICAL = "MEDICAL"
    AUTO = "AUTO"
    PROPERTY = "PROPERTY"
    DISPUTE = "DISPUTE"
    DENTAL = "DENTAL"
    VISION = "VISION"
    OTHER = "OTHER"


class ClaimRequest(BaseModel):
    claimId: Optional[str] = None

    description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    amount: float = Field(
        ...,
        gt=0,
    )

    patientName: str = Field(
        ...,
        min_length=1,
    )

    policyNumber: str = Field(
        ...,
        min_length=1,
    )

    claimType: ClaimType


class AgentResults(BaseModel):
    intakeAgent: str
    fraudAgent: str
    policyAgent: str
    validationAgent: str


class ClaimResponse(BaseModel):
    claimId: str
    fraudRisk: str
    approvalConfidence: str
    recommendation: str
    message: str
    processedAmount: float
    fallback: bool
    agents: AgentResults


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "UP",
        "service": "ClaimAI Multi-Agent AI Service",
    }


@app.post(
    "/orchestra/analyze",
    response_model=ClaimResponse,
)
async def multi_agent_analyze(
    claim: ClaimRequest,
) -> ClaimResponse:

    claim_id = claim.claimId or (
        f"CLM-{uuid4().hex[:8].upper()}"
    )

    randomizer = create_randomizer(claim)

    fraud_score = round(
        randomizer.uniform(1, 25),
        1,
    )

    policy_match = randomizer.choice(
        ["HIGH", "MEDIUM", "LOW"]
    )

    validation_status = randomizer.choice(
        ["VALID", "NEEDS_REVIEW", "INVALID"]
    )

    recommendation = determine_recommendation(
        fraud_score=fraud_score,
        policy_match=policy_match,
        validation_status=validation_status,
        amount=claim.amount,
    )

    confidence = calculate_confidence(
        fraud_score=fraud_score,
        policy_match=policy_match,
        validation_status=validation_status,
    )

    return ClaimResponse(
        claimId=claim_id,
        fraudRisk=f"{fraud_score}%",
        approvalConfidence=f"{confidence}%",
        recommendation=recommendation,
        message="Multi-agent claim analysis completed",
        processedAmount=claim.amount,
        fallback=False,
        agents=AgentResults(
            intakeAgent=build_summary(
                claim.description
            ),
            fraudAgent=(
                f"Fraud Risk: {fraud_score}%"
            ),
            policyAgent=(
                f"Policy Match: {policy_match}"
            ),
            validationAgent=(
                f"{claim.claimType.value} "
                f"Validation: {validation_status}"
            ),
        ),
    )


def create_randomizer(
    claim: ClaimRequest,
) -> Random:
    seed_source = (
        f"{claim.claimId}|"
        f"{claim.description}|"
        f"{claim.amount}|"
        f"{claim.policyNumber}|"
        f"{claim.claimType.value}"
    )

    digest = sha256(
        seed_source.encode("utf-8")
    ).hexdigest()

    return Random(int(digest[:16], 16))


def build_summary(
    description: str,
) -> str:
    normalized = " ".join(description.split())

    if len(normalized) <= 120:
        return f"Summary: {normalized}"

    return f"Summary: {normalized[:120].rstrip()}..."


def determine_recommendation(
    fraud_score: float,
    policy_match: str,
    validation_status: str,
    amount: float,
) -> str:

    if fraud_score >= 18:
        return "REJECT_OR_INVESTIGATE"

    if validation_status == "INVALID":
        return "REJECT"

    if amount >= 10000:
        return "MANUAL_REVIEW"

    if (
        fraud_score < 12
        and policy_match == "HIGH"
        and validation_status == "VALID"
    ):
        return "AUTO_APPROVE"

    return "MANUAL_REVIEW"


def calculate_confidence(
    fraud_score: float,
    policy_match: str,
    validation_status: str,
) -> float:

    confidence = 96.0 - fraud_score * 0.25

    if policy_match == "MEDIUM":
        confidence -= 4

    if policy_match == "LOW":
        confidence -= 10

    if validation_status == "NEEDS_REVIEW":
        confidence -= 5

    if validation_status == "INVALID":
        confidence -= 15

    return round(
        max(50.0, min(confidence, 99.0)),
        1,
    )
