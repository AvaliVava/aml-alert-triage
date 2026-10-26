# Week 1 primary sources and research notes

Use primary institutional guidance for domain structure; distinguish research findings from proposed software design.

## Source A — FFIEC BSA/AML Examination Manual: SAR
URL: https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04

**Supported points:** five key components of suspicious activity monitoring/reporting; importance of investigating alerts and documenting findings; authorized human filing decisions. Applies to the US banking BSA/AML framework.

**Project inference:** our prototype should stop at an evidence-backed recommendation package and human review, not attempt automatic filing.

## Source B — FFIEC Suspicious Activity Reporting examination procedures
URL: https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04_ep

**Supported points:** review of alerts, research procedures, use of customer due diligence, documentation of decisions and content quality of SARs.

**Project inference:** input data should include customer context and enough transaction evidence to support review.

## Source C — FinCEN: Suggestions for addressing common errors in suspicious activity reporting
URL: https://www.fincen.gov/resources/statutes-regulations/guidance/suggestions-addressing-common-errors-noted-suspicious

**Supported points:** complete narratives describe critical facts and explain why activity is unusual for the customer.

**Project inference:** prose quality without factual grounding is not success.

## Source D — FFIEC Appendix L SAR quality guidance
URL: https://bsaaml.ffiec.gov/manual/Appendices/13

**Supported points:** narrative clarity and the who/what/when/where/why/how elements.

## Research cautions

- These documents explain US regulatory workflows; they do not prove that any LLM prototype meets those requirements.
- Avoid treating externally quoted false-positive rates, analyst times or compliance expenditure as verified project baselines. Verify any such statistics separately before publication.
- Do not use model-generated synthetic labels as if they were reviewed real-world ground truth.
