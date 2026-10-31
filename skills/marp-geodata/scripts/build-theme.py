#!/usr/bin/env python3
"""Génère theme/geodata.css à partir de theme/geodata.base.css.

Les logos et habillages de assets/ sont embarqués en data URI afin que le
thème soit autonome (aucun chemin relatif à résoudre au moment du rendu).

Usage : python3 scripts/build-theme.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PLACEHOLDERS = {
    "__LOGO_COULEUR__": ("geodata-paris-logo-couleur.png", "image/png"),
    "__LOGO_BLANC__": ("geodata-paris-logo-blanc.png", "image/png"),
    "__LIGNES_BLANC__": ("lignes-blanc.svg", "image/svg+xml"),
    "__LIGNES_BAS_BLANC__": ("lignes-bas-blanc.svg", "image/svg+xml"),
}


def data_uri(name: str, mime: str) -> str:
    data = base64.b64encode((ASSETS / name).read_bytes()).decode("ascii")
    return f'url("data:{mime};base64,{data}")'


def main() -> None:
    css = (ROOT / "theme" / "geodata.base.css").read_text(encoding="utf-8")
    css = css.replace(
        "NE PAS ÉDITER theme/geodata.css : il est généré depuis ce fichier",
        "FICHIER GÉNÉRÉ — éditer theme/geodata.base.css puis relancer",
    )
    for key, (name, mime) in PLACEHOLDERS.items():
        css = css.replace(key, data_uri(name, mime))
    out = ROOT / "theme" / "geodata.css"
    out.write_text(css, encoding="utf-8")
    print(f"{out.relative_to(ROOT)} ({out.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
