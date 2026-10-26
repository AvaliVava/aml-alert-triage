# Investigation workflow — Phase 1

## Educational ten-stage lifecycle
1. **Alert generated:** monitoring or referral identifies unusual activity.
2. **Intake and assignment:** alert reference, owner and operational status are recorded.
3. **Initial review:** verify alert reason, source completeness and material initial context.
4. **Information gathering:** retrieve permitted customer, account, transaction and evidence records.
5. **Transaction analysis:** calculate amounts, chronology, counterparties and historical deviations.
6. **Evidence assessment:** distinguish verified facts, claims, conflicts and unresolved gaps.
7. **Case documentation:** preserve actions, sources, findings and internal narrative.
8. **Recommendation:** close/investigate/escalate per approved rubric.
9. **Human decisions:** authorized staff perform actual dispositions and SAR determinations.
10. **Follow-up and audit:** retain relevant history, revisions and continuing work.

These are explanatory stages, not a mandated common bank workflow. Cases can loop back to additional information gathering.

## Identity and state distinctions
- Transaction ID = particular financial movement or event.
- Alert ID = specific detection event.
- Case ID = investigation container, potentially for multiple alerts.
- Workflow status (`new`, `in_progress`, `awaiting_information`, etc.) is distinct from proposed disposition.

## Prototype scope
Given a supplied synthetic alert package: validate, calculate, assess, assemble evidence, draft narrative and return a human-review package. No live queue integration, real bank data, automatic regulatory filing or final banking decisions.
