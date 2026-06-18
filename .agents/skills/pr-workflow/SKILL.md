---
name: pr-workflow
description: Use when opening, reviewing, or describing a Pull Request. Covers the Conventional Commits title format, the sectioned PR body template, the labels used by the project (refactor, fix, enhancement), the branch naming convention, and the pre-PR checklist.
---

# PR Workflow Skill

Tracklinker's PRs follow a strict, repeatable format. Every PR opened against `main` should use the template at `.github/PULL_REQUEST_TEMPLATE.md` (auto-populated by GitHub when you open a PR) and follow the rules below.

## Branch naming

Every branch **must** be one of:

```
feat/<feature-name>     # new feature or refactor in a feature module
fix/<short-description>  # bug fix
refactor/<short-description>
docs/<short-description>
chore/<short-description>
test/<short-description>
```

Look at any `git branch -a` listing — there is exactly one `feat/<name>` per module (auth, users, products, categories, subcategories, suppliers, output_orders, warranties, dashboard, reports, suggestions, testing). All work for a given feature goes on its dedicated branch.

## Commit and PR title format

This project uses **Conventional Commits** for both commit messages and PR titles:

```
<type>(<scope>): <short imperative description>
```

| `type` | Used for | Affects `version`? |
| --- | --- | --- |
| `feat` | New feature, new endpoint, new module | MINOR |
| `fix` | Bug fix | PATCH |
| `refactor` | No behavior change, no API change | none |
| `perf` | Performance improvement | none |
| `docs` | Documentation only | none |
| `chore` | Build, CI, deps, housekeeping | none |
| `test` | Adding or fixing tests | none |

`<scope>` is the **module or layer** the change lives in. Examples observed in the repo:

- `feat(cors)`, `feat(cache)`, `feat(agents)`
- `fix(categories)`, `fix(suppliers_repository)`, `fix(auth)`
- `refactor(warranties)`, `refactor(users)`, `refactor(output_orders)`
- `docs(readme)`, `chore(deps)`

The description is **lowercase**, **imperative mood**, **no period** at the end.

## PR body structure

Use the GitHub PR template (`.github/PULL_REQUEST_TEMPLATE.md`). At a minimum, the PR must include:

### 1. `## Description`

A 1–3 sentence summary in English answering:
- What does this PR do?
- Why is it needed?

### 2. `## Changes`

Group the changes by **area** using the `### <Area>` subheading. Pick the areas that apply; delete the rest. The standard area list, in the order the reviewer expects them:

| Area | Use when |
| --- | --- |
| `Architecture` | Layered structure changes, new feature module, service-to-repository migration |
| `Modeling` | Pydantic models added/renamed/split, response shape changes |
| `Service layer` | Business logic in any `*Service` |
| `Repository` | SQL changes in any `*Repository` |
| `Routes` | New endpoints, new middlewares on existing endpoints |
| `Security` | RBAC changes, rate limit changes, JWT, cookies |
| `Database` | Schema changes, new indexes, new views, seed updates |
| `Documentation` | README, `AGENTS.md`, `.agents/skills/*` updates |
| `Cleanup` | Dead imports removed, typos fixed, unused parameters removed |

Each bullet should be **one logical change** and should mention the file path (in backticks) and the symbol (function / class) it touches.

### 3. `## Related issues / PRs`

Link related issues with `Closes #123` or `Refs #45`. If the PR depends on or is blocked by another open PR, link it here too.

## Labels

**Always add at least one label to every PR.** Pick the one that best describes the dominant type of change:

| Label | Color | Use for |
| --- | --- | --- |
| `refactor` | `#688577` | No behavior change, no API change |
| `fix` | `#2c0bcc` | Bug fix |
| `enhancement` | `#a2eeef` | New feature or request |

For mixed PRs (e.g. a `fix` that also requires a small `refactor`), apply **both** labels. `docs` and `chore` PRs still get a label — pick the closest one (`refactor` for `docs`, `refactor` for `chore` is acceptable) or extend the label set if needed. Never open a PR without a label.

## Pre-PR checklist (run locally before requesting review)

The PR body does **not** include a checklist section. Run this list silently and only fix what fails; do not paste it into the PR description.

1. `uv sync` — deps in sync.
2. `pytest` — exits 0.
3. `pip-audit` — no new high-severity CVE.
4. Manual smoke test of the touched endpoints in `/docs`.
5. If you touched SQL, run the query manually in MySQL Workbench / CLI to confirm the result shape.
6. **Architecture rule**: service → repository only. No service-to-service calls.
7. **Modeling rule**: `*Schema` for inputs, `*Response` for outputs, no suffix for internal.
8. **Spanish error messages** in every user-facing string.

## Opening a PR with `gh`

```bash
# 1. Make sure you are on the right branch and it's pushed
git checkout feat/auth
git push origin feat/auth

# 2. Open the PR with the template and the matching label
gh pr create \
  --base main \
  --head feat/auth \
  --title "refactor(auth): <short description>" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --label "refactor"
```

For mixed PRs, pass `--label` multiple times:

```bash
gh pr create \
  --base main \
  --head feat/auth \
  --title "fix(auth): harden token refresh and reorganize service" \
  --body-file .github/PULL_REQUEST_TEMPLATE.md \
  --label "fix" \
  --label "refactor"
```

To edit the body after creating:

```bash
gh pr edit <number> --body-file .github/PULL_REQUEST_TEMPLATE.md
```

To fill in the template sections quickly, prefer copying from a similar recent PR in the repo:

```bash
# List recent merged PRs
gh pr list --state merged --limit 10 --json number,title,body
```

## Anti-patterns to avoid

- ❌ Empty body. Always include at least `## Description` and `## Changes`.
- ❌ Title with capital first letter, period at the end, or no scope: `feat: Add new feature` → use `feat(auth): add login endpoint`.
- ❌ Mixing unrelated changes in one PR (e.g. warranty fix + README typo + dependency bump → three PRs).
- ❌ Calling `UsersService` from `AuthService` (or any cross-service call) — that is a code-review blocker.
- ❌ Skipping the manual smoke test "because the tests pass".
- ❌ Force-pushing after review has started. If you must rebase, coordinate in the PR comments first.

## Reference paths

- `.github/PULL_REQUEST_TEMPLATE.md` — the template that auto-fills new PRs.
- `agents.md` — project rules referenced by the PR checklist.
- `.agents/skills/architecture/SKILL.md` — the architectural rules the PR must respect.
- `.agents/skills/code-conventions/SKILL.md` — the naming and style conventions.
- `.agents/skills/development-workflow/SKILL.md` — the pre-PR commands to run.
