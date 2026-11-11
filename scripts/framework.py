"""Portable rendering and non-destructive installation (Python 3.10+)."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ('codex', 'claude-code', 'cursor', 'chatgpt')

def load(root=ROOT):
    registry = json.loads((root / 'registry.json').read_text(encoding='utf-8'))
    if registry['version'] != (root / 'VERSION').read_text().strip():
        raise ValueError('Version mismatch')
    if registry['adapters'] != list(ADAPTERS) or len(registry['skills']) != 10:
        raise ValueError('Invalid adapters or skill count')
    core = (root / 'core/CORE.md').read_text(encoding='utf-8')
    skills = {}
    for item in registry['skills']:
        name = item['id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
            raise ValueError('Invalid skill ID')
        if name in skills or item['path'] != f'skills/{name}/SKILL.md':
            raise ValueError('Duplicate skill or unsafe path')
        if item['version'] != registry['version']:
            raise ValueError('Skill version mismatch')
        path = root / item['path']
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Source escapes package')
        text = path.read_text(encoding='utf-8')
        expected = f"---\nname: {name}\ndescription: {item['description']}\n---\n"
        if not text.startswith(expected):
            raise ValueError(f'Frontmatter mismatch: {name}')
        skills[name] = (item, text, text[len(expected):].strip())
    return registry, core, skills

def render(adapter, root=ROOT):
    registry, core, skills = load(root)
    if adapter not in ADAPTERS:
        raise ValueError('Unknown adapter')
    files = {}
    if adapter in ('codex', 'claude-code'):
        directory = '.agents/skills' if adapter == 'codex' else '.claude/skills'
        # Embed the core in each workflow: no edits to AGENTS.md or CLAUDE.md.
        for name, (item, text, body) in skills.items():
            header = text[:text.index('\n---\n') + 5]
            files[f'{directory}/{name}/SKILL.md'] = header + '\n' + core + '\n' + body + '\n'
    elif adapter == 'cursor':
        files['.cursor/rules/shared-agent-core.mdc'] = '---\ndescription: Shared agent working principles\nalwaysApply: true\n---\n\n' + core
        for name, (item, text, body) in skills.items():
            files[f'.cursor/rules/shared-{name}.mdc'] = f"---\ndescription: {item['description']}\nalwaysApply: false\n---\n\n{body}\n"
    else:
        files['shared-agent-skills/INSTRUCTIONS.md'] = core + '\nSelect relevant workflows from SKILLS.md by description. Read the selected workflow before acting. If reference files cannot be retrieved, ask for the relevant text. Do not claim access to local files or tools unless this session provides them.\n'
        files['shared-agent-skills/SKILLS.md'] = '# Shared workflows\n\n' + '\n\n'.join(f"## {name}\n\n{item['description']}\n\n{body}" for name, (item, text, body) in skills.items()) + '\n'
        files['shared-agent-skills/registry.json'] = json.dumps(registry, indent=2) + '\n'
    return files

def install(adapter, target, dry_run=False, root=ROOT):
    target = Path(target).absolute()
    if target.is_symlink():
        raise ValueError('Target must not be a symlink')
    base = target.resolve()
    files = render(adapter, root)
    pending = []
    for relative, content in files.items():
        path = target / relative
        # Refuse symlinks, including dangling links and parent junctions.
        for parent in (path, *path.parents):
            if parent == target.parent:
                break
            if parent.is_symlink() or (hasattr(parent, 'is_junction') and parent.is_junction()):
                raise ValueError(f'Linked destination: {parent}')
        if not path.resolve().is_relative_to(base):
            raise ValueError(f'Destination escapes target: {path}')
        if path.exists():
            if not path.is_file() or path.read_bytes() != content.encode('utf-8'):
                raise FileExistsError(f'Conflicting destination (unchanged): {path}')
        else:
            for parent in path.parents:
                if parent == target.parent:
                    break
                if parent.exists() and not parent.is_dir():
                    raise FileExistsError(f'Parent is not a directory: {parent}')
            pending.append((path, content))
    # Preflight the entire plan before creating any files. Never overwrite.
    if not dry_run:
        for path, content in pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(content)
    return [str(path.relative_to(target)) for path, _ in pending]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adapter', choices=ADAPTERS, required=True)
    parser.add_argument('--target', type=Path, required=True, help='Project root or ChatGPT export directory')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        changed = install(args.adapter, args.target, args.dry_run)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'Installation refused: {error}\n')
    print(json.dumps({'adapter': args.adapter, 'dry_run': args.dry_run, 'new_files': changed}, indent=2))

if __name__ == '__main__':
    main()
