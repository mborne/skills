# uv et PyTorch : variantes de configuration

Synthèse de <https://docs.astral.sh/uv/guides/integration/pytorch/>
(consultée en novembre 2026). Les exemples de la doc utilisent
`requires-python = ">=3.14"`, `torch>=2.11.0` et `torchvision>=0.26.0`.

## Index disponibles

| Backend | Nom d'index usuel | URL |
| --- | --- | --- |
| CPU | `pytorch-cpu` | `https://download.pytorch.org/whl/cpu` |
| CUDA 11.8 | `pytorch-cu118` | `https://download.pytorch.org/whl/cu118` |
| CUDA 12.6 | `pytorch-cu126` | `https://download.pytorch.org/whl/cu126` |
| CUDA 12.8 | `pytorch-cu128` | `https://download.pytorch.org/whl/cu128` |
| CUDA 13.0 | `pytorch-cu130` | `https://download.pytorch.org/whl/cu130` |
| ROCm 7.2 | `pytorch-rocm` | `https://download.pytorch.org/whl/rocm7.2` |
| Intel GPU | `pytorch-xpu` | `https://download.pytorch.org/whl/xpu` |

D'autres index existent hors de cette liste (`cu121`, `cu124`, `cu129`,
`cu132`…) ; même syntaxe, en vérifiant les versions publiées (voir
`SKILL.md`).

Chaque index se déclare avec `explicit = true` :

```toml
[[tool.uv.index]]
name = "pytorch-cu128"
url = "https://download.pytorch.org/whl/cu128"
explicit = true
```

## Plateformes supportées par backend

| Backend | Linux | Windows | macOS |
| --- | --- | --- | --- |
| CPU | oui | oui | oui |
| CUDA | oui | oui | non → marqueur `sys_platform == 'linux' or sys_platform == 'win32'` |
| ROCm | oui | non | non → marqueur `sys_platform == 'linux'` |
| XPU | oui | oui | non → marqueur `sys_platform == 'linux' or sys_platform == 'win32'` |

Hors des plateformes couvertes par le marqueur, uv retombe sur PyPI.

## CPU seul sur toutes les plateformes

```toml
[project]
name = "project"
version = "0.1.0"
requires-python = ">=3.14.0"
dependencies = [
  "torch>=2.11.0",
  "torchvision>=0.26.0",
]

[tool.uv.sources]
torch = [
    { index = "pytorch-cpu" },
]
torchvision = [
    { index = "pytorch-cpu" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

## CUDA sous Linux, CPU ailleurs (marqueurs)

```toml
[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", marker = "sys_platform != 'linux'" },
  { index = "pytorch-cu130", marker = "sys_platform == 'linux'" },
]
torchvision = [
  { index = "pytorch-cpu", marker = "sys_platform != 'linux'" },
  { index = "pytorch-cu130", marker = "sys_platform == 'linux'" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true
```

## ROCm (AMD) sous Linux

Les paquets Triton ROCm doivent aussi être déclarés en dépendances et
épinglés sur l'index :

```toml
[project]
dependencies = [
  "torch>=2.11.0",
  "torchvision>=0.26.0",
  "pytorch-triton-rocm>=3.5.1 ; sys_platform == 'linux'",
  "triton-rocm>=3.6.0 ; sys_platform == 'linux'",
]

[tool.uv.sources]
torch = [{ index = "pytorch-rocm", marker = "sys_platform == 'linux'" }]
torchvision = [{ index = "pytorch-rocm", marker = "sys_platform == 'linux'" }]
pytorch-triton-rocm = [{ index = "pytorch-rocm", marker = "sys_platform == 'linux'" }]
triton-rocm = [{ index = "pytorch-rocm", marker = "sys_platform == 'linux'" }]

[[tool.uv.index]]
name = "pytorch-rocm"
url = "https://download.pytorch.org/whl/rocm7.2"
explicit = true
```

## XPU (Intel)

```toml
[project]
dependencies = [
  "torch>=2.11.0",
  "torchvision>=0.26.0",
  "triton-xpu>=3.7.0 ; sys_platform == 'win32' or sys_platform == 'linux'",
]

[tool.uv.sources]
torch = [{ index = "pytorch-xpu", marker = "sys_platform == 'win32' or sys_platform == 'linux'" }]
torchvision = [{ index = "pytorch-xpu", marker = "sys_platform == 'win32' or sys_platform == 'linux'" }]
triton-xpu = [{ index = "pytorch-xpu", marker = "sys_platform == 'win32' or sys_platform == 'linux'" }]

[[tool.uv.index]]
name = "pytorch-xpu"
url = "https://download.pytorch.org/whl/xpu"
explicit = true
```

## Choix CPU / CUDA par extra

Usage : `uv sync --extra cpu` ou `uv sync --extra cu130`. Les extras sont
déclarés en conflit pour que uv les résolve séparément.

```toml
[project]
name = "project"
version = "0.1.0"
requires-python = ">=3.14.0"
dependencies = []

[project.optional-dependencies]
cpu = [
  "torch>=2.11.0",
  "torchvision>=0.26.0",
]
cu130 = [
  "torch>=2.11.0",
  "torchvision>=0.26.0",
]

[tool.uv]
conflicts = [
  [
    { extra = "cpu" },
    { extra = "cu130" },
  ],
]

[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", extra = "cpu" },
  { index = "pytorch-cu130", extra = "cu130" },
]
torchvision = [
  { index = "pytorch-cpu", extra = "cpu" },
  { index = "pytorch-cu130", extra = "cu130" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true
```

L'extra `cu130` échoue sous macOS (pas de build GPU).

## Extensions GPU précompilées (index Astral)

<https://wheels.astral.sh/> fournit des wheels précompilés (`flash-attn`,
`deepspeed`, `deep-gemm`, `torch-scatter`, `vllm`…) par version de CUDA :

```bash
uv add flash-attn --index astral-cu128=https://wheels.astral.sh/simple/cu128/
```

Puis rendre l'index explicite :

```toml
[tool.uv.sources]
flash-attn = { index = "astral-cu128" }

[[tool.uv.index]]
name = "astral-cu128"
url = "https://wheels.astral.sh/simple/cu128/"
explicit = true
```

La version locale indique la cible (`+cu.12.8.torch.2.11` = CUDA 12.8 et
torch 2.11) : elle doit correspondre au torch installé et à son backend.

## Interface `uv pip`

Hors projet (`uv pip` dans un venv existant), il suffit de remplacer `pip3`
dans les commandes données par <https://pytorch.org/get-started/locally/> :

```bash
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

Sélection automatique de l'index selon le GPU détecté (pilote CUDA, GPU AMD
ou Intel ; repli sur CPU sinon) :

```bash
uv pip install torch --torch-backend=auto
UV_TORCH_BACKEND=auto uv pip install torch
```

Ou un backend précis : `--torch-backend=cu130` / `UV_TORCH_BACKEND=cu130`.
`--torch-backend` n'existe que pour `uv pip`, pas pour `uv add`/`uv sync`.
