---
title: Lab 2 — Research Data Management and Dissemination
date: 2026-05-20
label: lab2
numbering:
  heading_2: false
---

# Introduction

:::{important}
**Submission deadline:** *To be determined*  
**Team formation:** You must complete this laboratory in a team of two students.
:::

This laboratory introduces research data management practices in the context of open and reproducible science. You will work through the final steps of the lifecycle of a research dataset, from organization and documentation to publication and dissemination.

---

# Dataset Selection

You must choose one dataset among the following options.

## Option 1 — Own Research Data (Recommended)

Use unpublished research data from your own work or laboratory activities.

:::{warning}
Ensure that your dataset does not contain sensitive, confidential, or unauthorized information.
:::

## Option 2 — Existing Public Dataset

Select an existing published dataset that is not already hosted on Borealis.

You must identify the dataset using OpenAlex:
https://openalex.org/

---

### Finding a dataset using OpenAlex

OpenAlex is a database that you can use to identify research outputs, including datasets and dataset-associated publications.

You should:

1. Go to https://openalex.org/
2. Use keywords related to your domain (e.g., "neuroimaging", "climate", "microscopy", etc.)
3. In the "Type" field, select "Dataset"
4. In the "License" field select "CC0" or "CC-BY".
5. Use additional fields that you consider important.
6. Open a result that corresponds to a research publication or dataset-related output
7. Inspect the "Works" page and associated links (DOI, publisher, repository links)
8. Identify whether the underlying data is accessible and reusable

---

### License requirement (CC0 / CC-BY only)

You may only use datasets released under one of the following licenses:

- CC0 (public domain dedication)
- CC-BY (Creative Commons Attribution)

These licenses are commonly used in open research data publishing and ensure compatibility with redistribution in Borealis.

You must verify the license explicitly by checking:
- the dataset repository page (preferred);
- the authors' data availability statement;
- or the associated DOI landing page.

---

# Data Organization and Standardization

## Community Standards

You must identify whether a community standard applies to your data.

Examples include:
- BIDS (neuroimaging);
- OME-TIFF (microscopy);

---

<!-- ## Repository Structure

You must organize your dataset in a reproducible structure such as:

- `data/`
- `code/`
- `docs/`

You must implement all transformations, renaming, or preprocessing operations in reproducible scripts stored under `code/`.

--- -->

# Documentation

## README File

Your project must include a `README.md` containing:

- dataset origin and provenance;
- description of structure;
- explanation of variables (columns, rows, formats);
- units of measurement;
- preprocessing steps;
- software requirements;
- usage instructions;
- abbreviation descriptions;
- associated publications;
- licensing and citation information.

Your README must be sufficient for another researcher to understand and reuse your dataset independently. Include any other information you judge pertinent to facilitate others' interpretation of the dataset.

## Metadata

You must include appropriate metadata describing:
- authorship;
- acquisition context;
- data type and modality;
- preprocessing pipeline;
- version information;
- related publications or references.

---

# Dissemination Strategy — Borealis Dataverse

This section describes the publication workflow for research datasets using the Borealis Dataverse platform (demo environment). The dissemination process is a key component of FAIR data practices (Findable, Accessible, Interoperable, Reusable).

The workflow is divided into the data deposit first, followed later by code deposit, followed by the publication of the data and code.

---

## Platform Access and Account Setup

<!-- You must create an account on the Borealis demo platform:

- https://demo.borealisdata.ca/ -->

You must verify access to the ING8100 Collection on Polytechnique Dataverse:

- https://demo.borealisdata.ca/dataverse/polytechnique
TODO : Update with link to ING8100 collection once published

:::{important}
Report any access issues before proceeding with dataset submission.
:::

---

## Course Dataverse Structure

A shared Dataverse is created:

- Name: `ING8100`

This serves as the parent container for all student submissions.

## Dataset Publication Workflow

You must publish your dataset in Borealis following these steps:

### Create Dataset
Inside `ING8100`, create a new dataset via **Add Data → New Dataset**.

### Metadata Entry
Complete obligatory metadata fields including minimally:
- title;
- authors;
- identifier;
- point of contact;
- keywords;
- description;

:::{note}
Metadata quality is an evaluation criterion. Poor metadata reduces dataset usability and reproducibility. Add additional information in the relevant metadata fields depending on disciplinary norms, community standards, your judgement, etc.
:::

### Upload Data
Upload all dataset files ensuring:
- clear naming conventions;
- consistent structure;
- minimal unnecessary compression.

:::{note} Borealis automatically unzips all .zip files. If you have a zipped file, double-zip the file.:::
:::{note} Ensure that your files and folders are properly structured *before* uploading it into Borealis.:::

### License Definition
Assign a license appropriate to your dataset:
- ensure compatibility with reused data;
- document justification in your README.

### Save Dataset
Once you have completed the metadata, license and uploaded the data, select **Save Dataset** This will create a **draft (unpublished)** dataset. Make any further modifications to the dataset as necessary by choosing **Edit Dataset**

---

## Github integration

TODO : Ajouter intégration GitHub

---

## File level editing
Add embargoes, tags, file level descriptions or restrict access by choosing **Edit Files**

---
### Submit for Review
Submit your dataset to change its status to **draft (in review)** for instructor review before publication.

:::{note} Ensure that the dataset is all complete as possible before submitting it for review. Once the dataset is published, it can be edited, but cannot be removed. Borealis' linear versionning system ensures that all previous versions of a dataset remain accessible to all users.:::

TODO : Explication que ce sera accepté par nous puis les modifications pourront être faites pour avoir du versionage.

## Dataset Evolution and Versioning

After your initial upload to Borealis, you must perform controlled modifications to your dataset in order to generate a new version and document its evolution. When you edit your published dataset a new **draft (unpublished)** version of your dataset. You can then repeat the steps above before submitting it for review by the instructors again.

This step is required to demonstrate dataset versioning practices commonly used in research data management systems.

---

### Dataset modifications

You must apply at least one modification to the dataset you already uploaded on Borealis. Examples include:

- adding new data files;
- removing incorrect or irrelevant data;
- correcting an error in the dataset;
- updating metadata or file structure;
- modifying preprocessing decisions.

Your modification must be meaningful and reproducible.

---

### Versioning and semantic tagging

<!-- Each modification must correspond to a new dataset version.

You must assign a version tag following semantic versioning principles:

- **patch**: small corrections (e.g., fixing errors, minor updates)
- **minor**: small corrections or changes to existing data, code and metadata (e.g. fixing errors, metadata modifications, etc.) Dataset will pass from v.1.0 → v.1.1)
- **major**: major changes or updates to data or code (e.g. new data files, adding restricted access, etc.) Dataset will pass from v.1.0 → v.2.0)

You must justify the chosen version type in your CHANGELOG. -->

TODO : Explication version majeure et version mineure

---

### CHANGELOG.md
<!--
You must maintain a `CHANGELOG.md` file describing all dataset modifications.

Each entry must include:
- date of modification;
- type of change (patch/minor/major);
- description of modification;
- affected files or data components.

--- -->

TODO : demander au niveau du CHANGELOG.md à Julien

### Derivative data generation

<!-- You must process part of your dataset to generate derivative data.

Examples include:
- filtered or cleaned subsets;
- transformed or resampled data;
- extracted features or summaries;
- format conversions.

Your derivative data must be:
- reproducible from the original dataset;
- generated using scripts stored in your repository. -->

TODO: Est-ce qu'on souhaite avoir les jeux de données brutes et les données traitées sur Boréalis?

En général, il y a les données traitées et pas les données brutes sur Boréalis.

---

### Storage of derivatives

<!-- You must store derivative datasets separately from raw data using a clear structure, for example:

- raw data: original uploaded dataset
- derivatives: processed or transformed outputs

You must implement all processing steps in scripts located in the `code/` directory. -->

TODO: voir encore une fois si on garde les raw et les derivatives.

---

### Reproducibility across versions 

TODO : voir si on garde tout dépendant de si on a des données traités ou pas.

You must verify that your processing pipeline can be re-executed on at least two dataset versions:

- the original uploaded version;
- the modified version after dataset evolution.

You must observe and document:
- whether the pipeline runs without errors on both versions;
- whether outputs remain comparable;
- whether modifications affect reproducibility of results.

TODO : Voir pour le rapport pour les modifications, on veut voir le raisonnement au niveau des modifications qui ont été faites. 

:::{note}
The goal is not only to modify the dataset, but to ensure that dataset evolution remains traceable and computationally reproducible.
:::

---


## GitHub Integration for Data Transfer

*work in progress*

You will explore automated dataset publishing using GitHub integration tools.

### Purpose
This step demonstrates:
- reproducible data publication from version-controlled repositories;
- FAIR-aligned dissemination workflows;
- integration between computation and archival storage.

### Tooling
- Dataverse GitHub uploader action:
  https://github.com/marketplace/actions/dataverse-uploader-action

- Documentation:
  https://learn.scholarsportal.info/all-guides/borealis/files/#GitHub-Integration

  ---

# Evaluation
*to be determined*

- Notes de versionnement 
- Structure des dossiers et fichiers dans Boréalis
- README.me ++ 
- Metadonnée ++
- Rapport sur jeu de données (nom du répertoire où le jeux de données à été trouvé, auteur, article associé au jeu de donnée, pourquoi il a été choisi)
- Intégration GitHub
- License
- Gestion des fichiers (fichier restreint, fichier en embargo, description des fichiers)
