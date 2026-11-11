import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from framework import ROOT, ADAPTERS, install, load, render
from package import package
from validate import validate

class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'project with spaces'

    def test_all_files_and_schema(self):
        self.assertGreater(validate(), 20)

    def test_all_adapters_roundtrip_idempotent(self):
        for adapter in ADAPTERS:
            with self.subTest(adapter=adapter):
                target = self.target / adapter
                expected = render(adapter)
                self.assertEqual(len(install(adapter, target)), len(expected))
                for relative, text in expected.items():
                    self.assertEqual((target / relative).read_bytes(), text.encode('utf-8'))
                self.assertEqual(install(adapter, target), [])

    def test_dry_run_writes_nothing(self):
        for adapter in ADAPTERS:
            self.assertTrue(install(adapter, self.target, dry_run=True))
            self.assertFalse(self.target.exists())

    def test_conflict_preflight_preserves_every_file(self):
        for adapter in ADAPTERS:
            with self.subTest(adapter=adapter):
                target = self.target / adapter
                relative = list(render(adapter))[-1]
                path = target / relative
                path.parent.mkdir(parents=True)
                path.write_bytes(b'user content\r\n')
                before = {str(p): p.read_bytes() for p in target.rglob('*') if p.is_file()}
                with self.assertRaises(FileExistsError):
                    install(adapter, target)
                after = {str(p): p.read_bytes() for p in target.rglob('*') if p.is_file()}
                self.assertEqual(before, after)

    def test_existing_instructions_preserved(self):
        self.target.mkdir()
        for name in ('AGENTS.md', 'CLAUDE.md', 'unrelated.txt'):
            (self.target / name).write_bytes(b'Keep exact bytes\r\n')
        for adapter in ADAPTERS:
            install(adapter, self.target)
        for name in ('AGENTS.md', 'CLAUDE.md', 'unrelated.txt'):
            self.assertEqual((self.target / name).read_bytes(), b'Keep exact bytes\r\n')

    def test_parent_file_refused_before_write(self):
        self.target.mkdir()
        (self.target / '.agents').write_text('keep')
        with self.assertRaises(FileExistsError):
            install('codex', self.target)
        self.assertEqual(list(self.target.iterdir()), [self.target / '.agents'])

    def test_directory_conflict(self):
        path = self.target / next(iter(render('codex')))
        path.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            install('codex', self.target)

    def test_symlink_parent_refused(self):
        self.target.mkdir()
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        try:
            (self.target / '.agents').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Host does not permit creation of symlinks')
        with self.assertRaises(ValueError):
            install('codex', self.target)
        self.assertEqual(list(outside.iterdir()), [])

    def mutated_source(self):
        source = Path(self.temp.name) / 'source'
        shutil.copytree(ROOT / 'skills', source / 'skills')
        shutil.copytree(ROOT / 'core', source / 'core')
        shutil.copy(ROOT / 'VERSION', source)
        shutil.copy(ROOT / 'registry.json', source)
        return source

    def test_unsafe_registry_path_rejected(self):
        source = self.mutated_source()
        registry = json.loads((source / 'registry.json').read_text())
        registry['skills'][0]['path'] = '../outside.md'
        (source / 'registry.json').write_text(json.dumps(registry))
        with self.assertRaises(ValueError):
            install('codex', self.target, root=source)
        self.assertFalse(self.target.exists())

    def test_duplicate_registry_rejected(self):
        source = self.mutated_source()
        registry = json.loads((source / 'registry.json').read_text())
        registry['skills'][1] = registry['skills'][0]
        (source / 'registry.json').write_text(json.dumps(registry))
        with self.assertRaises(ValueError):
            load(source)

    def test_version_mismatch_rejected(self):
        source = self.mutated_source()
        (source / 'VERSION').write_text('9.9.9')
        with self.assertRaises(ValueError):
            load(source)

    def test_unknown_adapter_rejected(self):
        with self.assertRaises(ValueError):
            install('unknown', self.target)
        self.assertFalse(self.target.exists())

    def test_cli_dry_run_and_invalid_arguments(self):
        command = [sys.executable, str(ROOT / 'scripts/framework.py')]
        result = subprocess.run(command + ['--adapter', 'codex', '--target', str(self.target), '--dry-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)['new_files']), 10)
        self.assertFalse(self.target.exists())
        result = subprocess.run(command + ['--adapter', 'bogus', '--target', str(self.target)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_platform_wrapper(self):
        if os.name == 'nt':
            command = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ROOT / 'scripts/install.ps1')]
        else:
            command = ['sh', str(ROOT / 'scripts/install.sh')]
        result = subprocess.run(command + ['--adapter', 'claude-code', '--target', str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(self.target.rglob('SKILL.md'))), 10)
        path = next(self.target.rglob('SKILL.md'))
        path.write_text('user edit')
        result = subprocess.run(command + ['--adapter', 'claude-code', '--target', str(self.target)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(path.read_text(), 'user edit')

    def test_archive_reproducibility_checksum_and_install(self):
        archive, checksum = package(output=Path(self.temp.name) / 'dist')
        first = archive.read_bytes()
        package(output=archive.parent)
        self.assertEqual(first, archive.read_bytes())
        self.assertEqual(checksum.read_text().split()[0], hashlib.sha256(first).hexdigest())
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertTrue(all('.git/' not in n and '__pycache__' not in n for n in bundle.namelist()))
            bundle.extractall(Path(self.temp.name) / 'unpacked')
        source = Path(self.temp.name) / 'unpacked/shared-agent-skills-0.1.0'
        for adapter in ADAPTERS:
            self.assertTrue(install(adapter, self.target / adapter, root=source))

if __name__ == '__main__':
    unittest.main()
