---
title: Lab 2 — Research Data Management and Dissemination
date: 2026-04-XX
label: lab2
numbering:
  heading_2: false
---

# Introduction

:::{important}
**Submission deadline:** *To be determined*  
**Team formation:** This laboratory must be completed in teams of two students.
:::

This laboratory introduces research data management practices in the context of open and reproducible science. Students will work through the complete lifecycle of a research dataset, from organization and documentation to publication and dissemination.

The objectives are to:
- structure and standardize research data;
- document datasets using metadata and README files;
- track dataset evolution using Git and changelogs;
- apply appropriate licensing strategies;
- publish datasets in a research data repository;
- reflect on differences between data management systems and dissemination platforms.

---

# Dataset Selection

Students must choose one dataset among the following options.

## Option 1 — Own Research Data (Recommended)

Use unpublished research data from your own work or laboratory activities.

:::{warning}
Ensure that the dataset does not contain sensitive, confidential, or unauthorized information.
:::

## Option 2 — Existing Public Dataset

Select an existing published dataset that is not already hosted on Borealis.

The dataset must be identified using OpenAlex:
https://openalex.org/

---

### Finding a dataset using OpenAlex

OpenAlex is a scholarly knowledge graph that can be used to identify research outputs, including datasets and dataset-associated publications.

Students should:

1. Go to https://openalex.org/
2. Use keywords related to their domain (e.g., “neuroimaging dataset”, “climate data”, “microscopy images”, etc.)
3. Open a result that corresponds to a research publication or dataset-related output
4. Inspect the “Works” page and associated links (DOI, publisher, repository links)
5. Identify whether the underlying data is accessible and reusable

:::{important}
Students must ensure that they are selecting the dataset itself (or a clearly identifiable data source), not only a paper describing unavailable data.
:::

---

### License requirement (CC0 / CC-BY only)

Only datasets released under one of the following licenses may be used:

- CC0 (public domain dedication)
- CC-BY (Creative Commons Attribution)

These licenses are commonly used in open research data publishing and ensure compatibility with redistribution in Borealis.

Students must verify the license explicitly by checking:
- the dataset repository page (preferred);
- the publisher’s data availability statement;
- or the associated DOI landing page.

:::{warning}
If the license is unclear, missing, or restrictive (e.g., CC-BY-NC, CC-BY-ND, proprietary licenses), the dataset must not be used.
:::

---

# Data Organization and Standardization

## Community Standards

You must identify whether a community standard applies to their data.

Examples include:
- BIDS (neuroimaging);
- OME-TIFF (microscopy);

---

## Repository Structure

The dataset must be organized in a reproducible structure such as:

- `data/`
- `code/`
- `docs/`

All transformations, renaming, or preprocessing operations must be implemented in reproducible scripts stored under `code/`.

---

# Documentation

## README File

Each project must include a `README.md` containing:

- dataset origin and provenance;
- description of structure;
- explanation of variables (columns, rows, formats);
- units of measurement;
- preprocessing steps;
- software requirements;
- usage instructions;
- licensing and citation information.

The README must be sufficient for another researcher to understand and reuse the dataset independently.

## Metadata

Students must include appropriate metadata describing:
- authorship;
- acquisition context;
- data type and modality;
- preprocessing pipeline;
- version information;
- related publications or references.

---

# Dissemination Strategy — Borealis Dataverse

This section describes the publication workflow for research datasets using the Borealis Dataverse platform (demo environment). The dissemination process is a key component of FAIR data practices (Findable, Accessible, Interoperable, Reusable).

The workflow is divided into dataset publication first, followed later by code publication.

---

## Platform Access and Account Setup

Students must create an account on the Borealis demo platform:

- https://demo.borealisdata.ca/

They must verify access to the Polytechnique Dataverse:

- https://demo.borealisdata.ca/dataverse/polytechnique

:::{important}
Report any access issues before proceeding with dataset submission.
:::

---

## Course Dataverse Structure

A shared Dataverse is created:

- Name: `INGXXXX`

This serves as the parent container for all student submissions.

## Dataset Publication Workflow

Each team must publish their dataset in Borealis following these steps:

### Create Dataset
Inside `INGXXXX`, create a new dataset via **Add Data → New Dataset**.

### Metadata Entry
Complete metadata fields including:
- title;
- authors and affiliations;
- description;
- keywords;
- methodology;
- experimental or acquisition context.

:::{note}
Metadata quality is an evaluation criterion. Poor metadata reduces dataset usability and reproducibility.
:::

### Upload Data
Upload all dataset files ensuring:
- clear naming conventions;
- consistent structure;
- minimal unnecessary compression.

### License Definition
Assign a license appropriate to the dataset:
- ensure compatibility with reused data;
- document justification in README.

### Submit for Review
Submit dataset as a **draft (provisional version)** for instructor review before publication.

## Dataset Evolution, Versioning, and CHANGELOG

After the initial upload to Borealis, students must perform controlled modifications to their dataset in order to generate a new version and document its evolution.

This step is required to demonstrate dataset versioning practices commonly used in research data management systems.

---

### Dataset modifications

Students must apply at least one modification to the dataset already uploaded on Borealis. Examples include:

- adding new data files;
- removing incorrect or irrelevant data;
- correcting an error in the dataset;
- updating metadata or file structure;
- modifying preprocessing decisions.

The modification must be meaningful and reproducible.

---

### Versioning and semantic tagging

Each modification must correspond to a new dataset version.

Students must assign a version tag following semantic versioning principles:

- **patch**: small corrections (e.g., fixing errors, minor updates)
- **minor**: addition of new data without breaking structure
- **major**: structural or format changes that affect compatibility

The chosen version type must be justified in the CHANGELOG.

---

### CHANGELOG.md

Students must maintain a `CHANGELOG.md` file describing all dataset modifications.

Each entry must include:
- date of modification;
- type of change (patch/minor/major);
- description of modification;
- affected files or data components.

---

### Derivative data generation

Students must process part of the dataset to generate derivative data.

Examples include:
- filtered or cleaned subsets;
- transformed or resampled data;
- extracted features or summaries;
- format conversions.

Derivative data must be:
- reproducible from the original dataset;
- generated using scripts stored in the repository.

---

### Storage of derivatives

Derivative datasets must be stored separately from raw data using a clear structure, for example:

- raw data: original uploaded dataset
- derivatives: processed or transformed outputs

All processing steps must be implemented in scripts located in the `code/` directory.

---

### Reproducibility across versions

Students must verify that their processing pipeline can be re-executed on at least two dataset versions:

- the original uploaded version;
- the modified version after dataset evolution.

They must observe and document:
- whether the pipeline runs without errors on both versions;
- whether outputs remain comparable;
- whether modifications affect reproducibility of results.

:::{note}
The goal is not only to modify the dataset, but to ensure that dataset evolution remains traceable and computationally reproducible.
:::

---

## GitHub Integration for Data Transfer

*work in progress*

Students will explore automated dataset publishing using GitHub integration tools.

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