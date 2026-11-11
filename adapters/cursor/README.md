# cursor adapter

Installs an always-applied core rule and ten description-routed `.mdc` rules under `.cursor/rules`. Workflow rules use `alwaysApply: false`; use explicit rule selection when automatic routing is insufficient. Existing rules are preserved.

```sh
python scripts/framework.py --adapter cursor --target /path/to/project --dry-run
python scripts/framework.py --adapter cursor --target /path/to/project
```

Restart or refresh the host's skill/rule discovery as needed. Verify the chosen workflow is visible before relying on it. Host permission and instruction precedence remain in force. See [sources and limitations](../../docs/SOURCES.md).
