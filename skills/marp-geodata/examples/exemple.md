---
marp: true
theme: geodata
paginate: true
lang: fr
title: Les forêts françaises face au défi climatique
footer: Colloque recherche — 20/12/2025
---

<!-- _class: titre -->
<!-- _paginate: skip -->
<!-- _footer: "" -->

###### colloque recherche

# Les forêts françaises **face au défi climatique**

mercredi 20 décembre 2025

---

<!-- _class: aside -->

> Contexte
> Données mobilisées
> Premiers résultats

## Un suivi des forêts à grande échelle

### Combiner LiDAR HD et imagerie satellitaire

- Couverture nationale **LiDAR HD** pour caractériser la structure des peuplements
- Séries temporelles **Sentinel-2** pour suivre les dépérissements
- Croisement avec les inventaires de terrain
  - placettes de l'inventaire forestier
  - relevés ponctuels

---

<!-- _class: chapitre -->
<!-- _paginate: hold -->

###### 01

# Données **et méthodes**

## Chaîne de traitement

---

## Une chaîne reproductible

1. Téléchargement des dalles LiDAR HD
2. Calcul du modèle numérique de hauteur
3. Agrégation par maille de 25 m

```bash
pdal pipeline mnh.json --readers.las.filename=dalle.laz
gdal_calc.py -A mns.tif -B mnt.tif --calc="A-B" --outfile=mnh.tif
```

---

## Indicateurs par région

| Région              | Surface boisée (kha) | Hauteur médiane (m) |
| ------------------- | -------------------: | ------------------: |
| Grand Est           |                1 900 |                22,4 |
| Nouvelle-Aquitaine  |                2 900 |                18,1 |
| Occitanie           |                2 600 |                15,7 |

<p class="source">Source : données fictives, à titre d'illustration.</p>

---

<!-- _class: colonnes -->

## Deux colonnes

<div class="col">

### Atouts

- Résolution métrique
- Couverture homogène
- Données ouvertes

</div>
<div class="col">

### Limites

- Volume des données
- Date d'acquisition variable
- Calibrage terrain nécessaire

</div>

---

<!-- _class: centre -->

<div class="chiffre">93 %</div>

### des placettes correctement classées

---

<!-- _class: sable -->

## À retenir

- Le **LiDAR HD** change l'échelle du suivi forestier
- Les méthodes sont **ouvertes** et reproductibles

---

<!-- _class: violet -->

> « Former à rendre le monde lisible. »

---

<!-- _class: fin -->
<!-- _paginate: skip -->
<!-- _footer: "" -->

# **Merci**

contact@exemple.fr
