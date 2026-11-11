"""Create a deterministic archive from tracked checkout files (requires Git)."""
import hashlib
import subprocess
import zipfile
from pathlib import Path
from framework import ROOT

def package(root=ROOT, output=None):
    output = Path(output) if output else root / 'dist'
    output.mkdir(parents=True, exist_ok=True)
    version = (root / 'VERSION').read_text().strip()
    name = f'shared-agent-skills-{version}'
    archive = output / f'{name}.zip'
    paths = sorted(filter(None, subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')))
    if not paths:
        raise ValueError('No tracked files; stage the reviewed framework before packaging')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for relative in paths:
            path = root / relative
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f'Unsafe package source: {relative}')
            info = zipfile.ZipInfo(f'{name}/{relative}', date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = output / f'{name}.sha256'
    checksum.write_text(f'{digest}  {archive.name}\n', encoding='utf-8')
    return archive, checksum

if __name__ == '__main__':
    for path in package():
        print(path)
