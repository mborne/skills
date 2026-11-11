# uv-pytorch-cuda

Configurer un projet [uv](https://docs.astral.sh/uv/) qui installe PyTorch
avec accélération GPU CUDA, depuis l'index `download.pytorch.org` qui
correspond à la machine (index explicite, `tool.uv.sources`, marqueurs de
plateforme). Voir [SKILL.md](SKILL.md) pour les instructions de la skill et
[references/uv-pytorch.md](references/uv-pytorch.md) pour les variantes (CPU,
ROCm, XPU, extras, extensions GPU, `uv pip --torch-backend`).

Source : [Using uv with PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/).

Exemple de demande : « crée-moi un projet uv pour une formation PyTorch sur
GPU avec torchvision et matplotlib ».

## Voir aussi

- [Using uv with PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/) :
  la documentation uv de référence.
- [PyTorch – Get Started](https://pytorch.org/get-started/locally/) :
  sélecteur officiel de commande d'installation selon la plateforme et le
  backend.
- [Astral GPU indexes](https://wheels.astral.sh/) : wheels précompilés
  d'extensions GPU (`flash-attn`, `deepspeed`, `vllm`…).
- Skill [`uv`](https://github.com/astral-sh/claude-code-plugins/tree/main/plugins/astral/skills/uv)
  d'Astral : bonnes pratiques générales de uv (projets, scripts, outils,
  migration depuis pip/pyenv), complémentaire de celle-ci.
- Skill [`uv-cuda-setup`](https://github.com/nblog/video2doc/blob/HEAD/.agents/skills/uv-cuda-setup/SKILL.md)
  (nblog/video2doc) : approche similaire, orientée Windows/PowerShell.
