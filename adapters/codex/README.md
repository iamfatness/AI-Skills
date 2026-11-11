# codex adapter

Installs ten native skills under `.agents/skills/<id>/SKILL.md`. Each embeds the universal core so no global instruction file is overwritten. The core applies when a workflow is loaded, not automatically to unrelated requests. Invoke a skill by name (for example `$systematic-debugging`) or allow host discovery.

```sh
python scripts/framework.py --adapter codex --target /path/to/project --dry-run
python scripts/framework.py --adapter codex --target /path/to/project
```

Restart or refresh the host's skill/rule discovery as needed. Verify the chosen workflow is visible before relying on it. Host permission and instruction precedence remain in force. See [sources and limitations](../../docs/SOURCES.md).
