"""Validate all tracked text, canonical skills, schema, and rendered adapters."""
import json
import re
import subprocess
from pathlib import Path
import jsonschema
import yaml
from framework import ROOT, ADAPTERS, load, render

def validate(root=ROOT):
    registry, core, skills = load(root)
    schema = json.loads((root / 'schemas/registry.schema.json').read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(registry, schema)
    actual = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    assert actual == set(skills), 'Unregistered or missing skill'
    assert len(core.split()) > 100, 'Core is unexpectedly empty'
    for name, (item, text, body) in skills.items():
        metadata = yaml.safe_load(text.split('---', 2)[1])
        assert metadata == {'name': name, 'description': item['description']}
        for section in ('Inputs', 'Workflow', 'Output', 'Example'):
            assert f'## {section}' in body, f'Missing {section}: {name}'
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    count = 0
    for relative in filter(None, paths):
        path = root / relative
        text = path.read_text(encoding='utf-8')
        assert '\x00' not in text, f'Unexpected binary: {relative}'
        assert text.strip(), f'Empty file: {relative}'
        if path.suffix == '.json':
            json.loads(text)
        if path.suffix in ('.yml', '.yaml'):
            yaml.safe_load(text)
        if path.suffix == '.py':
            compile(text, relative, 'exec')
        if path.suffix == '.md':
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if '://' not in link and not link.startswith('#'):
                    assert (path.parent / link.split('#')[0]).exists(), f'Broken link: {relative}: {link}'
        count += 1
    for adapter in ADAPTERS:
        for relative, text in render(adapter, root).items():
            assert not Path(relative).is_absolute() and '..' not in Path(relative).parts
            if relative.endswith(('SKILL.md', '.mdc')):
                metadata = yaml.safe_load(text.split('---', 2)[1])
                assert isinstance(metadata['description'], str)
                if relative.endswith('.mdc'):
                    assert isinstance(metadata['alwaysApply'], bool)
                else:
                    assert core in text
    return count

if __name__ == '__main__':
    print(f'Validated {validate()} tracked files, 10 skills, and 4 adapter outputs.')
