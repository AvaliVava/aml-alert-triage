# AML Alert Lifecycle — Week 1 research draft

**Status:** Research draft for owner review. **Regulatory context:** US BSA/AML framework; not a replacement for legal or compliance guidance.

## What is AML alert triage?

An alert indicates activity that should be **reviewed**. It is not, by itself, proof of money laundering, a conclusion that a customer is suspicious, or a filing decision. A reviewer needs contextual information to determine whether to recommend closure, perform further investigation, or escalate.

## Five components in the official workflow

The FFIEC BSA/AML Examination Manual identifies five interdependent components of effective suspicious activity monitoring/reporting:

1. **Identification of unusual activity:** Rules, monitoring systems, staff referrals and other mechanisms generate alerts or referrals.
2. **Managing alerts:** Appropriate reviewers research transaction activity, relevant customer information and explanations, and document their conclusions.
3. **SAR decision making:** Authorized persons evaluate the investigation and decide whether a Suspicious Activity Report should be filed; reasons for both filing and not filing are documented.
4. **SAR completion and filing:** If filing is appropriate, the institution prepares and submits a report, with supporting records retained according to its obligations.
5. **Monitoring continuing activity:** Institutions follow relevant continuing activity and repeat filing decisions when necessary.

Sources: [FFIEC manual](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04) and [FFIEC examination procedures](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04_ep).

## Simplified project-specific flow (our design inference)

```text
Synthetic transaction-monitoring alert
      |
      v
Validate alert + customer/transaction records
      |
      v
Calculate reproducible transaction features
      |
      v
Recommend close / investigate / escalate (model output only)
      |
      v
Assemble verified evidence + missing information
      |
      v
Draft factual rationale / optional investigation narrative
      |
      v
Human analyst reviews and decides next action
```

This is a **proposed research pipeline**, not the FFIEC's own technical architecture.

## Six human decision points to understand

These are project questions inferred from the regulatory workflow, not a universal regulatory checklist:

1. Is the alert data complete and suitable for investigation?
2. What expected customer behavior can be established from available records?
3. Which observed activities differ materially from that expected behavior?
4. What ordinary explanations and contradictory evidence should be considered?
5. Is there enough information to recommend closure, further investigation or escalation?
6. What documentation should be passed to a human reviewer for the final decision?

## What the AI may assist with

- Validating inputs and calculating transaction statistics deterministically.
- Identifying relevant transactions for review.
- Producing a provisional recommended action with reasons.
- Drafting a factual, evidence-backed investigation summary.
- Explicitly highlighting missing records, contradictory evidence and uncertainty.

## What the AI must not do

- Conclude that a customer committed a crime from an alert.
- Fabricate documents, transaction identifiers or explanations.
- Automatically close real cases or file regulatory reports.
- Present its recommendation as an institution's final SAR filing decision.

## Narrative grounding

Official guidance emphasizes explaining *who, what, when, where, why* and *how* when describing suspicious activity. Our eventual narrative generator must use verified input evidence; ungrounded narrative text is a failure, even if it sounds convincing. Source: [FinCEN narrative guidance](https://www.fincen.gov/resources/statutes-regulations/guidance/suggestions-addressing-common-errors-noted-suspicious) and [FFIEC SAR quality guidance](https://bsaaml.ffiec.gov/manual/Appendices/13).

## Week 1 learning tasks still open

- [ ] Read the linked FFIEC chapter carefully and summarize the five stages in your own words.
- [ ] Identify at least three types of information an investigator would need beyond a triggered rule.
- [ ] Trace one fictional alert from detection to a human recommendation, noting missing evidence.
- [ ] Compare this simplified workflow against at least one additional official source; record any uncertainties.

## Open design questions for Week 2

- What exact facts must each synthetic alert include to be assessable?
- Which review recommendations can reasonably be labeled in synthetic examples?
- How will we define an ambiguous case without assuming the creator's label is always correct?
- How should invalid evidence references and incomplete inputs be represented?
