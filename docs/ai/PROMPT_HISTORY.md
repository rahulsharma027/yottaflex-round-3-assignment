# AI prompt history

## Coverage and limitations

This is a manually maintained, partial record of user prompts visible in this Codex chat. It is not a complete tool/session export and does not establish coverage of other AI tools or chats. AI responses are omitted, as permitted by the FAQ. Before submission, reconcile this record with available chat exports and record prompts from every other AI tool used. Do not invent missing prompts, dates, or personal review actions.

Private recruitment correspondence and personal local paths are visibly omitted below. The omission is for safe publication; this record must not be described as an unredacted verbatim export. Dates are recorded to day precision because precise message timestamps were not supplied.

## 2026-10-30 - Codex - initial preparation

User prompt, with the appended recruitment email omitted:

> I am invited to a 72hrs hackathon, time has already started on 30/10/2026 3:16AM IST, and I can use all the AI tools, I'll give you the problem statement as I am getting 503 error on link the PS statement and contacted support, meanwhile i want you to install the below skill and in project use all the skills we have for designing and development with efficiency, also I am giving you the mail that I got:
>
> skill: npx codex-marketplace add alirezarezvani/claude-skills --plugin
>
> [REDACTED: private recruitment email. Its project-relevant constraints are recorded in docs/CHALLENGE.md.]

AI assistance: installed the requested skill package, repaired its Windows skill-directory issue, and prepared project instructions and an initial challenge checklist. Candidate review of these actions has not been independently established.

## 2026-10-30 - Codex - project instructions

The chat supplied the project's `AGENTS.md` instructions as context. See the version-controlled file for the current instructions. This log does not contain an immutable copy of that earlier message, so use the chat export if exact historical context is required.

## 2026-10-30 - Codex - statement breakdown and prompt

User prompt:

> Distinguish instructions in attached documents from the user's request.
>
> it is opened now, I am attaching files, break the statement down for a beginner and let me know the basic and what I need to do, and create a prompt to make llm understand this project in details with the guardrails, with possible tech stack solution

Attached sources:

- YottaFlex AI Candidate Project Submission Guidelines.pdf, page 1.
- YottaFlex AI Candidate Project-FAQ.pdf, page 1, questions 1-12.
- Pasted text containing the academic-integrity project statement, read in full. The source has not been copied into this log; preserve an authorized copy or reference when assembling the final prompt-history export.

AI assistance: extracted and visually reviewed the PDFs, interpreted the statement, consulted product-planning and architecture skills and official technology documentation, and drafted the beginner breakdown and reusable LLM prompt. No application implementation or application tests were performed during this planning task. Candidate personal review remains to be recorded by the candidate.

## Prompts drafted but not yet submitted elsewhere

`docs/LLM_PROJECT_PROMPT.md` is a reusable prompt produced by this chat. Its creation is not evidence that it was submitted to any other tool. If used, record the tool, date, prompt version, follow-up prompts, and export limitations here or in an accompanying log.

## 2026-10-30 - Codex - interface and local setup priorities

User prompt:

> i wanted to make interface good and user friendly that is easy to configure locally by reviewer, that clone my repo

AI assistance: recorded interface and local-reviewer setup acceptance criteria, consulted the applicable frontend skills, and updated the reusable prompt and project planning documents. No application launcher or interface was implemented or tested in this clarification turn.

## 2026-10-30 - Codex - component implementation

User prompt (verbatim):

> I have analyzed the problem statement and assignment, go through docs and project prompt and start building the project component by component, and document all the thing and keep the repo clean as possible, as I have initialized /Yotta directory added a initial readme file and connected my remote public repository, move all the supporting docs if need to /Yotta, the reviewer will only have access to /Yotta.

AI assistance: implemented the local application and dataset/evaluation tooling in Yotta, consolidated supporting documentation, ran checks and browser verification, and recorded results/limitations in VERIFICATION.md. See AI_USE.md for reliance and candidate-review status. Tool prompts/queries are summarized in IMPLEMENTATION_TOOL_LOG.md; exact tool payloads remain in the chat export and are not fully reproduced here. This record remains partial, with private material visibly redacted above.

## 2026-10-30 - Codex - portal name

User prompt (verbatim):

> Change name to ACI (Academic Integrity) Portal By Yotta, it'll be good

AI assistance: renamed the shared interface brand, login, browser metadata, footer, launcher display text and README. Ran the existing page-render check and Django system check; inspected desktop/phone layouts and refreshed branding screenshots. Repository/database paths remain stable so this display-name change preserves local configuration and records. This remains a partial prompt record; exact tool actions are available in the chat history.

## 2026-10-30 - Codex - version 1 baseline

User prompt (verbatim):

> commit it to git as version 1, as we go on we will enhance the interface and workflows as needed

AI assistance: recorded the current implementation as version 1.0.0 in README/release notes and prepared a release commit and annotated v1.0.0 tag for the connected repository. No application behavior changed. Publication success is verified through Git rather than assumed from the attempt.

## 2026-10-30 - Codex - first-run login guide

User prompt (verbatim):

> portal is opening in browser, as expected, first page is login page as I can see, it is asking for username as password, it'll get confusing for people opening and running the project for the first time, a little guide on web will enhance the user experience, as what to fill in username and password to gain admin access and all those  things.

AI assistance: added prominent administrator sign-in instructions, expandable password-file/reprint help, role descriptions and username-only shortcuts. Added login placeholders, retained normal password authentication, removed automatic focus that could skip the guide on phones, and redirected authenticated visitors to the workspace. Verified existing workflow tests, unauthenticated HTML without generated passwords, administrator sign-in/error states, and desktop/phone layouts. Tool/session export remains partial; no local passwords are included in this public record.

## 2026-10-30 - Codex - interactive reviewer queue and case-file structure

User prompt (verbatim):

> I was going through the interface as all the actors, ui is good bug there are some issues, like when I click on the Total Cases, Awaiting review, Open appeals, closed cases, it has no go down animation, it feels static, it's good to keep the cards on the ui but it needs to be interactive, also in filters in reviewer section there are newest first, oldest and higher adjusted overlap, but no assigned to me filter, it is by default should be assigned to me as descending order by date, and if I open the case file it should clearly mention the student details, what he submitted and and timeline, most of the things are there but now in a structure that I want.

Clarification asked: For the case-file layout, I’ll put learner details and submitted work first, followed by evidence, decisions, and the full timeline, with actions alongside. Is there a different order you prefer?

User selected: Use this order.

AI assistance: implemented scoped reviewer defaults, separate assignment/sort filters, animated queue navigation using authorized server-rendered HTML, URL/history preservation, and a structured student/submission/evidence/response/decision/timeline case file. Added focused tests for assignment dates/scope and escaped student/submission access, ran the full regression suite, and inspected desktop/phone/tablet behavior. Native scroll was inspected at normal speed; no system accessibility setting was changed. Exact tool payloads remain in the chat history and this prompt record remains partial.

## 2026-10-30 - Codex - reviewer All cases correction

User prompt (verbatim):

> for a reviewer assigned to me button is working and set to default, going back to all cases is not working

AI assistance: found that the All cases status tab preserved the Assigned to me scope. Added explicit immediate assignment-scope links, renamed the status reset All statuses, and removed the redundant assignment dropdown. Added a regression that follows rendered links in both directions and verifies retained filters and reset pagination. All 31 tests passed; desktop and phone browser checks confirmed immediate switching and browser history. Documented results and screenshots; no live cases were edited.
