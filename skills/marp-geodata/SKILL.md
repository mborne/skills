---
name: marp-geodata
description: Produire des présentations Marp (Markdown → HTML/PDF/PPTX) conformes à la charte graphique de Géodata Paris (ex ENSG-Géomatique, école de l'IGN) — thème « geodata » (bleu #2b317f, Raleway/Roboto, logo, courbes de niveau, pagination 02/35) et règles d'écriture de la marque. Utiliser dès qu'il faut créer, convertir ou mettre en forme des slides, un support de cours, de soutenance, de colloque ou de séminaire pour Géodata Paris, l'ENSG ou l'IGN avec Marp, même si la charte n'est pas citée explicitement (ex. « fais-moi des slides marp pour mon cours à l'ENSG », « passe ce markdown en présentation Géodata »).
---

# Présentations Marp à la charte Géodata Paris

Ce skill fournit un thème Marp `geodata` (`theme/geodata.css`, autonome : logos
et habillages embarqués) et les règles de la charte graphique de Géodata Paris
(octobre 2025) à appliquer au contenu.

Avant de rédiger, lire `references/charte.md` si la question porte sur
l'usage du nom, des couleurs ou du logo. `examples/exemple.md` montre toutes
les mises en page.

## Démarrage

En-tête minimal d'un deck :

```markdown
---
marp: true
theme: geodata
paginate: true
lang: fr
title: Titre de la présentation
footer: Nom de l'événement — JJ/MM/AAAA
---
```

Rendu (le thème doit être passé par `--theme-set`, chemin absolu vers le
dossier de ce skill) :

```bash
SKILL_DIR=<chemin de ce skill>
npx -y @marp-team/marp-cli@latest --html --theme-set "$SKILL_DIR/theme/geodata.css" deck.md -o deck.html
npx -y @marp-team/marp-cli@latest --html --theme-set "$SKILL_DIR/theme/geodata.css" deck.md -o deck.pdf
npx -y @marp-team/marp-cli@latest --html --theme-set "$SKILL_DIR/theme/geodata.css" deck.md -o deck.pptx
```

- `--html` n'est nécessaire que pour les blocs HTML (`colonnes`, `.chiffre`,
  `.source`…). Ajouter `--allow-local-files` si le deck référence des images
  locales en PDF/PPTX.
- Pour VS Code (extension Marp), copier `theme/geodata.css` dans le projet et
  le déclarer dans `.vscode/settings.json` : `"markdown.marp.themes": ["./geodata.css"]`.
- Les polices Raleway, Roboto et Roboto Mono sont chargées depuis Google Fonts :
  sans réseau, les installer localement sinon le rendu bascule sur Arial.
- Si le navigateur n'est pas trouvé : `CHROME_PATH=$(which chromium)`.

## Mises en page (classes)

Appliquer avec `<!-- _class: nom -->` en tête de diapositive.

| Classe | Rôle | Structure Markdown attendue |
| --- | --- | --- |
| `titre` | Couverture, aplat bleu | `###### surtitre` (facultatif), `# Début du titre **fin en gras**`, `## sous-titre` (facultatif), paragraphes = date / lieu / auteur·ices (alignés à droite) |
| *(aucune)* | Contenu standard, fond blanc | `## Titre`, `### chapô` (facultatif), texte, listes, tableaux, code, images |
| `aside` | Contenu + colonne étroite à gauche (accroches, sommaire, fil d'Ariane) | le **premier** blockquote `> …` devient la colonne de gauche, puis `## Titre`… |
| `colonnes` | Deux colonnes (requiert `--html`) | `## Titre` puis `<div class="col">` … `</div>` ×2 (lignes vides autour du Markdown) |
| `centre` | Message ou chiffre clé centré | `<div class="chiffre">93 %</div>` + `### légende` |
| `chapitre` | Intercalaire de partie, aplat bleu | `###### 01` (numéro, en jaune), `# Titre **de partie**`, `## sous-titre` |
| `sable` | Mise en avant sur aplat secondaire sable doré | titre + liste courte, ou citation `>` |
| `violet` | Mise en avant sur aplat secondaire violet foncé | titre + liste courte, ou citation `>` |
| `fin` | Clôture, aplat bleu centré | `# **Merci**`, contacts |
| `plein` | Image pleine page sans logo ni pagination | `![bg](image.jpg)` |

Directives utiles par diapositive : `<!-- _paginate: skip -->` (couverture,
clôture), `<!-- _paginate: hold -->` (intercalaires non comptés),
`<!-- _footer: "" -->` (masquer le pied de page).

Classes de texte (HTML) : `.bleu`, `.violet`, `.mauve`, `.orange`,
`.magenta`, `.brique`, `.framboise`, `.jaune`, `.petit`, `.source` (mention
de source en bas de diapo), `.chiffre`. `<mark>` surligne en jaune pâle
(en jaune sur les aplats bleus).

## Règles de la charte à appliquer au contenu

1. **Nom** : toujours « Géodata Paris » (jamais GéoData, Geodata, GEODATA,
   GP, GDP), non traduit même en anglais. « Géodata » seul seulement en interne
   après une première mention complète. Corriger les occurrences fautives dans
   le contenu fourni et le signaler.
2. **Titres** : Raleway extra-light avec la partie à mettre en relief en
   **gras** — c'est ce que produit `# Texte léger **texte fort**`. Rester
   court : 2 lignes maximum sur la couverture, 1 ligne pour un titre de
   contenu.
3. **Couleurs** : le bleu `#2b317f` porte la parole officielle (titres,
   aplats). Les accents (violet, orange, magenta…) servent uniquement à mettre
   en exergue, avec parcimonie ; jaune et jaune pâle seulement sur aplat bleu.
   Sable doré et violet foncé sont des aplats secondaires : 1 ou 2
   diapositives par deck, pas plus. Pour les graphiques, utiliser la gamme
   d'accents de `references/charte.md`.
4. **Logo** : le thème place déjà le bon logo (couleur sur fond clair, blanc
   sur aplat). Ne pas en ajouter un second, ne pas le déformer ni le recolorer.
   Sur une photo en fond, utiliser la classe `plein` (pas de logo couleur sur
   photo).
5. **Tutelles** : si la couverture doit mentionner l'IGN et l'Université
   Gustave Eiffel, utiliser leurs logos officiels en blanc, en bas à gauche,
   nettement plus petits que le logo Géodata Paris, avec la mention
   « une école de ». Ces logos ne sont pas fournis par ce skill : les demander
   à l'utilisateur·ice plutôt que de les inventer.
6. **Densité** : une idée par diapositive, 3 à 5 puces, phrases courtes. Si
   le contenu déborde, découper en plusieurs diapositives plutôt que réduire
   la police.

## Vérification

Après génération, rendre les diapositives en images et les inspecter :

```bash
npx -y @marp-team/marp-cli@latest --html --theme-set "$SKILL_DIR/theme/geodata.css" --images png deck.md -o /tmp/apercu/deck.png
```

Contrôler : aucun texte qui déborde ou passe sous le logo / la pagination /
le pied de page, titres de couverture sur 2 lignes maximum, nom de la marque
correctement écrit, accents de couleur utilisés avec parcimonie.

## Faire évoluer le thème

Éditer `theme/geodata.base.css` (jamais `theme/geodata.css`, qui est généré),
puis :

```bash
python3 scripts/build-theme.py
```

Le script embarque `assets/*.png|svg` en data URI. Note : Marpit supprime
`content` des règles `::after` des thèmes ; pour masquer la pagination,
utiliser `display: none`.
