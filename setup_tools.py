#!/usr/bin/env python3
"""Prepare the optional glyph rasterizer in this checkout's isolated .venv."""
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def main():
    if sys.version_info < (3, 10):
        raise SystemExit('Python 3.10 or newer is required.')
    environment = ROOT / '.venv'
    if environment.is_symlink() or (hasattr(environment, 'is_junction') and environment.is_junction()):
        raise SystemExit('Refusing a linked virtual environment.')
    python = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    if not (environment / 'pyvenv.cfg').is_file() or not python.is_file():
        if environment.exists():
            raise SystemExit('Existing .venv is incomplete; preserve it and choose a clean checkout.')
        venv.EnvBuilder(with_pip=True).create(environment)
    subprocess.run([str(python), '-m', 'pip', 'install', '-r',
                    str(ROOT / 'skills/image-glyph-generator/requirements.txt')], check=True)
    subprocess.run([str(python), '-c', 'from PIL import ImageFont; from fontTools.ttLib import TTFont; print("Glyph dependencies ready")'], check=True)
    print(f'Use this Python for glyph generation: {python}')


if __name__ == '__main__':
    main()
