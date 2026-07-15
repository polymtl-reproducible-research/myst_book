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
**Team composition:** You must complete this laboratory in a team of two students.
:::

This laboratory introduces research data management practices in the context of open and reproducible science. Students will work through the final steps of the lifecycle of a research dataset, from organization and documentation to publication and dissemination. **Please be aware that the dataset you select for this lab will be used in Lab 3.**

This laboratory consists of three main components:

1. Selecting a dataset for publication based on the required criteria.
2. Preparing the dataset for sharing by organizing the files and completing the required documentation according to best practices.
3. Submitting the dataset to Borealis with sufficient metadata and documentation.

---

# Dataset Selection

You must choose between the following two options, please ensure that the dataset meets the following criteria.
1. No individual file exceeds 5 GB.
2. The entirety of the dataset does not exceed 20 GB.
3. The number of individual files included in the dataset does not exceed 500.

## Option 1 — Own Research Data (Recommended)

Use unpublished research data from your own work or laboratory activities.

:::{warning}
Ensure that your dataset does not contain sensitive, confidential, or unauthorized information.
:::

## Option 2 — Existing Public Dataset

Select an existing published dataset that is not already hosted on [Borealis](https://borealisdata.ca/).

You must identify the dataset using OpenAlex:
https://openalex.org/works

---

### Finding a dataset using OpenAlex

OpenAlex is a database that you can use to identify research outputs, including datasets and dataset-associated publications.

You should:

1. Go to https://openalex.org/works
2. Use keywords related to your domain (e.g., "neuroimaging", "climate", "microscopy", etc.)
3. In the "Type" field, select "Dataset"
4. In the "License" field, select "CC0" or "CC-BY".
5. Use additional fields that you consider important.
6. Open a result that corresponds to a research publication or dataset-related output
7. Inspect the "Works" page and associated links (DOI, publisher, repository links)
8. Identify whether the underlying data is accessible and reusable

---

### License requirement (CC0 / CC-BY only)

You may only reuse datasets released under one of the following licenses:

<!-- We use html instead of figures bloc since
it can go on the same line as the text  -->

**CC0** <img src="../images/lab2/cc_zero_logo.svg" alt="CC0 logo">
<br>
Public domain dedication — no rights reserved.

**CC-BY** <img src="../images/lab2/by_logo.svg" alt="BY logo">
<br>
Creative Commons Attribution — reuse permitted with credit.

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

# Documentation

## README File

Your project must include a `README.md` containing (when applicable):

- dataset origin and provenance;
- description of structure;
- explanation of variables (columns, rows, formats);
- units of measurement;
- preprocessing steps;
- software requirements (if certain files are in proprietary formats);
- usage instructions;
- abbreviation descriptions;
- associated publications;
- licensing and citation information.

Your README must be sufficient for another researcher to understand and reuse your dataset independently. Include any other information you judge pertinent to facilitate others' interpretation of the dataset.

## Report

Prepare a brief report describing the rationale behind your dataset selection. Include this report as part of the documentation uploaded with your dataset on Borealis.

Your report should address the following points:

- The repository or source from which the dataset was obtained.
- The dataset creator(s) or author(s).
- The publication associated with the dataset (if applicable), including its citation or DOI.
- The reasons for selecting this dataset, including its relevance to the objectives of this laboratory.

---

# Dissemination Strategy — Borealis Dataverse

This section describes the publication workflow for research datasets using the Borealis Dataverse platform (demo environment). The dissemination process is a key component of FAIR data practices (Findable, Accessible, Interoperable, Reusable).

The workflow is divided into:  data deposit, then code deposit, and finally the publication of the data and code.

---

## Platform Access and Account Setup

You must verify access to the ING8100 collection on Polytechnique Dataverse:

- https://demo.borealisdata.ca/dataverse/ING8100

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
### Metadata Entry

Complete **all** of the following required metadata fields before publishing your dataset:

- Title
- Author
- Point of Contact
- Description
- Subject
- Keyword
- Related Publication --> Only if applicable
- Data Source

### Upload Data
Upload all dataset files ensuring:
- clear naming conventions;
- consistent structure;
- minimal unnecessary compression.

:::{note} 
Borealis automatically unzips all .zip files. To preserve your dataset's folder hierarchy, please zip your file before depositing. If you have a zipped file, double-zip the file.
:::

:::{note} 
Ensure that your files and folders are properly structured *before* uploading them into Borealis. Borealis automatically unzips all '.zip' files. To preserve your dataset's folder structure, please zip your dataset before depositing it on Borealis.
:::

### License Definition
Assign a license appropriate to your dataset:
- ensure compatibility with reused data;
- document justification in your README.

### Save Dataset
Once you have completed the metadata, license and uploaded the data, select **Save Dataset**. This will create a **draft (unpublished)** version of your dataset, visible only to you and the course evaluators. Make any further modifications to the dataset by choosing **Edit Dataset**.

---

## File-level editing
Add embargoes, tags, or descriptions for specific files by following these steps;
1. In the "Files" tab, select all files that you wish to add edits to.
2. With the files selected, click on **Edit Files** and choose one of the following options
   - Metadata : to add a description for the selected files
   - Restrict : to require users to request access in order to download the file
   - Tags : to add a "Documentation", "Data" or "Code" tag to the file to describe its contents.
   - Embargo : to restrict access to the file until a certain date has passed.

---
## Submit for Review
Submit your dataset to change its status to **draft (in review)** so that the course evaluators can review it before publication.

:::{note} 
Ensure that the dataset is as complete as possible before submitting it for review. **Once the dataset is published, it can be edited, but cannot be removed.** Borealis' linear versioning system ensures that all previous versions of a dataset remain accessible to all users. Once your dataset has been accepted by the course evaluators, it will be published and you can proceed with the versioning module of the lab.
:::

## Dataset Evolution and Versioning

After your initial upload to Borealis, you must perform controlled modifications to your dataset in order to generate a new version and document its evolution. When you edit your published dataset, a new **draft (unpublished)** version of your dataset is created. You can then repeat the steps above before submitting it for review by the instructors again.

This step is required to demonstrate dataset versioning practices commonly used in research data management systems.

---

### Dataset modifications

You must apply at least one modification to the dataset you already uploaded on Borealis. Examples include:

- adding new data files;
- removing incorrect or irrelevant data;
- correcting an error in the dataset;
- updating metadata or file structure;
- modifying preprocessing decisions.
---

# Evaluation

The evaluation emphasizes the application of research data management best practices, including documentation, metadata, versioning, and organization.

| Criterion | Weight | Description |
|---|---:|---|
| Version Control | 20% | Version history is coherent, commit messages are meaningful, semantic versioning is used appropriately. |
| License | 10% | An appropriate open-source license is included and is compatible with the selected dataset. |
| README.md | 20% | The README clearly documents the dataset, repository structure, variables, preprocessing steps, software requirements, usage instructions, and citation information. |
| Metadata | 20% | Metadata is complete, accurate, and sufficient for another researcher to discover, understand, and reuse the dataset. |
| Folder Structure | 10% | The repository is organized using a clear structure that separates data, code, and documentation. |
| Dataset Report | 15% | The report clearly justifies the dataset selection by describing its source, authorship, associated publication (if applicable), and relevance to the laboratory objectives. |
| File-Level Editing | 5% | Appropriate use of Borealis file-level editing features to improve the organization and management of the dataset. |
