# AI-Skills

Shared agent skills framework **v0.1.0**: one universal core and ten reusable workflows for Codex, Claude Code, Cursor, and ChatGPT/custom GPTs.

## Install

Requires Python 3.10 or newer. Install from a reviewed checkout or the versioned release archive; runtime uses only the Python standard library.

```sh
git clone https://github.com/iamfatness/AI-Skills.git
cd AI-Skills
git checkout v0.1.0
python scripts/framework.py --adapter codex --target /path/to/project --dry-run
python scripts/framework.py --adapter codex --target /path/to/project
```

On Windows, use `./scripts/install.ps1 --adapter codex --target C:/path/to/project`. On macOS/Linux, use `sh scripts/install.sh --adapter codex --target /path/to/project`. Both wrappers accept the same arguments as the Python installer.

| Adapter | Output | Loading |
| --- | --- | --- |
| [Codex](adapters/codex/README.md) | `.agents/skills/*/SKILL.md` | Native skill discovery; core embedded per skill |
| [Claude Code](adapters/claude-code/README.md) | `.claude/skills/*/SKILL.md` | Native skill discovery; core embedded per skill |
| [Cursor](adapters/cursor/README.md) | `.cursor/rules/*.mdc` | Always-applied core; description-routed workflows |
| [ChatGPT/custom GPTs](adapters/chatgpt/README.md) | Instructions, knowledge, registry export | Manual upload/paste; subject to account capabilities |

Installation preflights all destinations and refuses conflicts or linked destination paths. Identical files are skipped, making repeated installation idempotent. Existing AGENTS.md, CLAUDE.md, and unrelated skills are untouched. No force-overwrite option is provided. On conflict, review and back up the affected file, then move it aside only if replacement is intended. A failed OS write may leave newly created files; rerun to complete after resolving the error. Do not run concurrent installers into the same target.

To remove an installation, delete only the exact generated paths listed by the relevant adapter/render output after checking for your edits. Do not delete shared parent directories. To upgrade, compare the new render against your installed files, back up edited files, and explicitly reconcile differences.

## Workflows

| Skill | Purpose |
| --- | --- |
| task-planning | Scope, dependencies, acceptance evidence |
| evidence-research | Primary sources and traceable conclusions |
| scoped-implementation | Focused code changes and preserved contracts |
| systematic-debugging | Reproduction, diagnosis, targeted verification |
| code-review | Actionable defect findings |
| test-design | Behavioral invariants and failure coverage |
| ui-quality | Rendered UI, accessibility, responsive interactions |
| api-design | Contracts, errors, compatibility, retry semantics |
| technical-documentation | Verified task-oriented instructions |
| release-delivery | Authorized, traceable publication |

[registry.json](registry.json) is the machine-readable catalog; [its schema](schemas/registry.schema.json) defines the v0.1.0 contract. [core/CORE.md](core/CORE.md) is the universal instruction source. Platform-specific formats are generated deterministically by `scripts/framework.py` rather than maintained as divergent copies.

## Validate and package

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/package.py
```

Validation covers the registry/schema, all source frontmatter, local Markdown links, UTF-8 text, version agreement, and generated adapter metadata. Tests exercise installation, conflict preservation, dry runs, path guards, CLI wrappers, and reproducible release archives. GitHub Actions runs these checks on Windows and Linux with Python 3.10 and 3.12.

The archive and SHA-256 checksum are written to `dist/`. Packaging requires a Git checkout and includes the current contents of tracked repository files; it never includes `.git`, virtual environments, caches, or arbitrary untracked files. Release from a clean reviewed commit. CI uploads the built package for review; publication is an explicit maintainer action.

## Contribute and limitations

Edit canonical skills and registry together, run validation/tests, and review the generated installation plan. Keep descriptions narrowly routed and workflows portable. Adding or renaming a skill changes the v0.1.0 schema's fixed ten-skill contract and requires an intentional versioned update.

These are instruction workflows, not executable agent runtimes. Automated format and installer checks do not prove model adherence or certify live vendor integration. [Sources and provenance](docs/SOURCES.md) document Skill Issue inspiration and official compatibility references. [CHANGELOG.md](CHANGELOG.md) records releases.
