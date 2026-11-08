# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [Fri 8:30 Group 1]
- Members, GitHub usernames and cohorts: ST1
- lachlan o’meara u3329873 github -lachlano07
- Izayah Baker u3328698 github - IzayahB
- Ben Parnell u3333375 github - BenP64

- Repository URL: https://github.com/BenP64/st1-assignment-3
- Starting SHA: 05627b6

## A Requirement to issue activities

### FR-02 Patient Search

- Title: return the stored patient for a valid patient ID.
- Context: PatientService.find_patient is a deliberate stub that raises NotImplementedError, so staff cannot retrieve a registered patient.
- Requirement: Given a valid patient ID, return the stored Patient object.
- Acceptance criteria: 
•	A registered ID returns the same stored object.
•	An unknown ID raises LookupError.
•	A blank or invalid ID raises ValueError.
•	A failed lookup creates no patient.

- Scope: PatientService.find_patient and its tests only

- Definition of Done: 
- All acceptance criteria pass
- Unit tests added and passing.
- Original tests remain passing.
- Diff reviewed by another team member.
PR merged and issue closed.]
- Owner: [Aadhya]
- Actual issue link: [[response](https://github.com/BenP64/st1-assignment-3/issues/2#issue-6242950079)]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel an appointment while retaining its history. 
- Context: AppointmentService.cancel_appointment is a stub that raises NotImplementedError, so appointments cannot be cancelled.
- Requirement: Cancel an appointment through the domain method - whilst also keeping the appointment record (FR-07).
- Acceptance criteria: •	The returned object has cancelled status.
•	The appointment is still findable after cancellation.
•	An unknown ID raises LookupError.
•	An invalid transition that raises ValueError - this then leaving the state unchanged.

- Scope: AppointmentService.cancel_appointment and its tests only.
- Definition of Done: •	Acceptance tests pass.
•	Original supplied tests still pass.
•	Another member has reviewed the actual diff.
•	PR merged and issue closed.

- Owner: [Aadhya]
- Actual issue link: [[response](https://github.com/BenP64/st1-assignment-3/issues/3#issue-6243022870)]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | weak | not describing what changed|
| final version | Weak | vague - not much information - no details |
| Add patient search by ID | Strong | describes the implemented feature. |
| fix stuff | Weak | no change details - no explanation |
| Prevent cancellation of completed appointments | Strong | the behaviour being changed - it is being explained |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: Refactoring, renaming patient fields, canceling, and adjusting dependencies are examples of unrelated modifications.
- Responsibility and architecture concerns: One PR combines several duties
- Testing and review concerns: Determining which tests exhibit cancelation behavior is difficult.
- Changes to remove or separate, with reasons: Separate PRs should be used for code reorganization, field renaming, and dependency adjustments to facilitate review and reversion.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [Covered requirements, completed tests, edge cases, and scope analysis]
- Follow-up review question 1: Were invalid IDs tested?
- Follow-up review question 2: Are there any unrelated changes in the PR?
- Follow-up review question 3: Which acceptance criteria were tested?
- Follow-up review question 4: What test results were observed?
- Follow-up review question 5: After a cancelation, was the appointment history kept?
- Additional questions if useful: Were any regression tests conducted?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | feature/issue-number-description |
| Commit message convention | Verb and plus a description - "e.g. " |
| PR size | one of the requirements per PR |
| Another-member review requirement | min=1 reviewer |
| Merge rule | tests pass + the reviewer approval is required |
| Significant Copilot disclosure rule | Considerable help noted in the PR remarks |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
 Issue #12| FR-02 Patient Search | Aadhya | Return patient by valid ID - exceptions handled | Closed |
| Issue #13 | FR-06 Appointment Cancellation | Aadhya | Cancellation retained within the history & validated | Closed |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: PR #21 - Add Patient Search by ID
- Linked issue and requirement: Issue #12, FR-02
- Feature branch: feature/12-patient-search
- Changed behaviour: Patients being retrieved using a valid patient ID
- Meaningful commits: Add patient search method
Add lookup error validation tests and Refactor patient search tests
- Test command, directory and observed result: pytest tests/ from repository root, all tests passed.
- Another-member reviewer: Lachlan
- Human observations recorded before Copilot: Review notes documented before automated review.
- Requirement, responsibilities, test assertions and unrelated-scope checks: Confirmed scope - lim to patient search tests with as logics too. 
- Key feedback: Add validation for blank identifiers
- Author response/change and verification: Added ValueError handling - test coverage
- Reviewer recheck and approval: Approved after retest
- Merge outcome and SHA: merged
- Significant Copilot assistance: none
- Linked issue closure: no. #12 closed 
- Each member updated main: All members pulled last main branch
- Integrated verification after merge: pytest tests/ successful on SHA

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Lachlan - Appointment cancellation tests.
- Prompt/purpose and relevant issue/diff: Create potential edge scenarios for canceling an appointment.
- Summary of output: suggested test scenarios for invalid transitions.
- Human check against actual code, requirements and tests: Suggestions were compared to the FR-06 acceptance criteria.
- Decision — Accept / Modify / Reject: modify
- Reason: While some cases met the qualifications, others were not.
- Verification/evidence: After human review, one test was added; all tests were successful.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Blank patient IDs = invalidated.
- Copilot noticed: Possible missing exception handling
- Overlap: valid concerns demonstrated 
- What did the human reviewer notice that Copilot did not: Scope remained larger than needed. 
- What did Copilot identify that the human reviewer initially missed: An additional edge case for incorrect input.
- Unsupported or incorrect Copilot suggestion: During a failed lookup, it was suggested to create a new patient, which was against the rules.
- Human judgement accepted, modified or rejected, and why: Adjusted recommendations after reviewing the specifications.
- Which evidence justified merge approval: Passing exams, receiving review permission, and meeting acceptance requirements.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Aadhya
- Implementation: Implemented FR-02 Patient Search
- Testing: Added tests for valid, invalid, and blank ID
- Review: reviewed the PR for the cancelation of an appointment
- Issue refinement: Clarified acceptance
- Design and responsibility discussion: Discussed the limits of service responsibility.
- Debugging or integration: Resolved lookup exception behavior
- Documentation or team support: Updated project

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Because the quality and impact of commits can vary widely, a large commit count does not always represent a good contribution. A small number of commits may represent significant implementation, testing, reviewing, debugging, and design work.

## L Stage 6 formative questions

1. What is version control?

A method for monitoring and controlling code modifications over time.
2. Why is a feature branch useful?

Until it's time to merge, it separates work from the main branch.
3. What makes a commit a good engineering commit?

It is well-defined, tested, and targeted.
4. What is a pull request?

a request to merge, following review, modifications from one branch into another.
5. What is the purpose of code review?

to find errors, confirm requirements, and enhance code quality.
6. What does a Git diff show?

the precise modifications performed between two code versions.
7. What is a Definition of Done?

a list that indicates when a task is finished.
8. What is the appropriate role of GitHub Copilot in pull-request review?

to help reviewers by making suggestions, but humans will still make the final decisions.
9. Why should individual contribution not be judged only by commit count?

This is because design work, testing, debugging, and reviews are all important contributions.
10. What is the Stage 6 engineering rule?

Issues, code, tests, reviews, and pull requests must all be able to trace requirements.
## M Completion and handover

- Starting SHA: 05627b6
- Final Stage 6 code SHA: 9271a40
- Test command: pytest tests/
- Working directory: project-root/
- Observed result: All tests passed.
- PR and another-member reviewer: [links]
- Unresolved issue or none: none
- Stage 7 handover status: Ready for tutor checkpoint.
- Final submitted SHA if later than tested SHA: evidence-only difference

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
