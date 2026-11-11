# chatgpt adapter

Exports `shared-agent-skills/INSTRUCTIONS.md`, `SKILLS.md`, and `registry.json`. Paste INSTRUCTIONS.md into the permitted instruction field and upload SKILLS.md as reference knowledge when your account supports it. In ordinary ChatGPT conversations attach SKILLS.md, paste the instructions, and name the relevant skill. Custom GPT creation/editing availability depends on account and product support. This is a manual export, not an automatic installation or a tool integration.

```sh
python scripts/framework.py --adapter chatgpt --target /path/to/project --dry-run
python scripts/framework.py --adapter chatgpt --target /path/to/project
```

Restart or refresh the host's skill/rule discovery as needed. Verify the chosen workflow is visible before relying on it. Host permission and instruction precedence remain in force. See [sources and limitations](../../docs/SOURCES.md).
