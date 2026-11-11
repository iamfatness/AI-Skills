# claude-code adapter

Installs ten native skills under `.claude/skills/<id>/SKILL.md`. Each embeds the universal core. The core applies when a workflow is loaded. Invoke `/systematic-debugging` or allow host discovery. Existing CLAUDE.md is untouched.

```sh
python scripts/framework.py --adapter claude-code --target /path/to/project --dry-run
python scripts/framework.py --adapter claude-code --target /path/to/project
```

Restart or refresh the host's skill/rule discovery as needed. Verify the chosen workflow is visible before relying on it. Host permission and instruction precedence remain in force. See [sources and limitations](../../docs/SOURCES.md).
