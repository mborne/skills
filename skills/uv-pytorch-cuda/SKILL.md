---
name: uv-pytorch-cuda
description: Créer ou configurer un projet Python géré par uv qui installe PyTorch (torch, torchvision, torchaudio) avec accélération GPU CUDA — choix de l'index download.pytorch.org (cu118, cu126, cu128, cu130…), `[[tool.uv.index]]` explicite, `[tool.uv.sources]`, marqueurs de plateforme, extras cpu/cuda, variantes ROCm/XPU/CPU, `uv pip --torch-backend`. Utiliser dès que l'utilisateur veut un pyproject.toml uv avec torch sur GPU, que `torch.cuda.is_available()` renvoie False dans un projet uv, ou qu'il demande « projet pytorch cuda avec uv », « installer torch GPU avec uv », « uv sync installe torch CPU », même sans citer l'index PyTorch.
---

# Projet PyTorch + CUDA avec uv

Référence : <https://docs.astral.sh/uv/guides/integration/pytorch/> (synthèse
et variantes dans `references/uv-pytorch.md`).

## Principe

- Les wheels PyTorch par accélérateur sont publiés sur des index dédiés
  (`https://download.pytorch.org/whl/<backend>`), avec un suffixe de version
  locale (`2.11.0+cu130`, `2.11.0+cpu`…).
- Sur PyPI, `torch` est CPU sur Windows/macOS et CUDA (version par défaut du
  moment) sur Linux. Pour une version CUDA précise, ou du GPU sous Windows, il
  faut déclarer l'index PyTorch.
- L'index est déclaré avec `explicit = true` pour qu'il ne serve **que** les
  paquets épinglés dans `[tool.uv.sources]`, le reste venant de PyPI.
- Les wheels embarquent le runtime CUDA : seul un pilote NVIDIA suffisamment
  récent est requis, pas le CUDA Toolkit.
- Nécessite uv ≥ 0.5.3.

## Démarche

1. **Choisir le backend CUDA.** `nvidia-smi` affiche « CUDA Version: X.Y » :
   c'est la version maximale supportée par le pilote. Prendre l'index `cuXY`
   le plus récent qui reste ≤ cette version **et** qui publie la version de
   torch voulue (voir « Vérifier un index » ci-dessous). Sans indication de
   l'utilisateur, prendre le plus récent compatible avec le pilote.
2. **Créer le projet** (si besoin) : `uv init --python 3.13 <nom>`.
3. **Ajouter l'index et les sources** dans `pyproject.toml` (modèle
   ci-dessous), en remplaçant `cu130` par le backend retenu partout.
4. **Ajouter les dépendances** : `uv add torch torchvision` (+ `torchaudio`
   au besoin). Les sources déjà déclarées sont respectées.
5. **Vérifier** :

   ```bash
   uv run python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
   ```

   Attendu : version suffixée `+cuXYZ` et `True`. Une version `+cpu` ou sans
   suffixe indique une source mal prise en compte (voir « Dépannage »).

## Modèle `pyproject.toml` (CUDA)

```toml
[project]
name = "mon-projet"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "torch>=2.11.0",
    "torchvision>=0.26.0",
]

[tool.uv.sources]
torch = [
  { index = "pytorch-cu130", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
torchvision = [
  { index = "pytorch-cu130", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
torchaudio = [
  { index = "pytorch-cu130", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true
```

- Le marqueur `sys_platform` fait retomber macOS (pas de build CUDA) sur PyPI.
  Si le projet ne cible que Linux, la forme courte suffit :
  `torch = { index = "pytorch-cu130" }`.
- Épingler dans `[tool.uv.sources]` **chaque** paquet de l'écosystème torch
  utilisé (`torch`, `torchvision`, `torchaudio`) : sinon il viendra de PyPI
  avec un build potentiellement incompatible.
- Correspondance des versions : `torchvision` 0.(N+15) va avec `torch` 2.N
  (2.6 ↔ 0.21, 2.11 ↔ 0.26, 2.14 ↔ 0.29). `torchaudio` (2.N pour
  `torch` 2.N) n'est plus publié au-delà de 2.11 (novembre 2026) et uv
  n'impose pas l'alignement avec `torch` : ne l'inclure que s'il est demandé,
  et vérifier alors qu'il fonctionne avec la version de `torch` résolue.

## Vérifier un index

Les index disponibles évoluent (nouveaux `cuXYZ` ajoutés, anciens figés).
Pour connaître la dernière version de torch publiée sur un index :

```bash
curl -s https://download.pytorch.org/whl/cu130/torch/ | grep -oE 'torch-2\.[0-9]+\.[0-9]+' | sort -uV | tail -1
```

Repères relevés en novembre 2026 (dernière version de torch publiée) :
`cu118` → 2.7.1, `cu121` → 2.5.1, `cu124` → 2.6.0, `cu126` → 2.14.1,
`cu128` → 2.11.0, `cu129` → 2.13.0, `cu130` → 2.14.1, `cu132` → 2.15.0.
Un index figé (ex. `cu124`) reste utilisable mais bloque torch à sa dernière
version : préférer un index encore alimenté pour un nouveau projet.

## Autres cas

Voir `references/uv-pytorch.md` pour :

- CPU seul, ROCm (AMD), XPU (Intel) ;
- CUDA sous Linux et CPU ailleurs (marqueurs) ;
- choix CPU/CUDA par extra (`uv sync --extra cpu` / `--extra cu130`) ;
- extensions GPU précompilées (`flash-attn`, `deepspeed`, `vllm`…) via les
  index Astral ;
- interface `uv pip` et `--torch-backend=auto`.

## Dépannage

- **`+cpu` ou `cuda.is_available()` False** : vérifier que le paquet est bien
  dans `[tool.uv.sources]`, que le nom d'index correspond exactement, puis
  `uv lock --upgrade-package torch && uv sync`. Contrôler `nvidia-smi`
  (pilote absent, ou version CUDA du pilote < backend choisi).
- **« No solution found » / version introuvable** : la version demandée
  n'existe pas sur cet index (index figé) ou pas pour cette version de
  Python ; vérifier avec la commande `curl` ci-dessus ou abaisser
  `requires-python`.
- **Un paquet générique (ex. `jinja2`) cherché sur l'index PyTorch** :
  `explicit = true` manquant.
