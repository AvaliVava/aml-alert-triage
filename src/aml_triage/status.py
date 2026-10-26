"""Expose factual project capability status. No AML reasoning is implemented."""


def get_status() -> dict[str, object]:
    """Return only capabilities that actually exist in the repository."""
    return {
        "project": "aml-alert-triage",
        "phase": "week-1-foundation",
        "llm_classifier_implemented": False,
        "synthetic_generator_implemented": False,
        "evidence_assembler_implemented": False,
        "narrative_generator_implemented": False,
    }
