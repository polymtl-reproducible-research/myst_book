---
title: Organizing and Versioning Research Data
date: 2026-08-06
label: lecture4
---

:::{iframe} https://docs.google.com/presentation/d/1ktRXjISKrDN2aLeubFAEph3Qbmhm7FyW6Jm9iE6Dm-8/embed?start=false&loop=false&delayms=3000
:width: 100%
:align: center
:title: Lecture 4 slides

[Open in Google Slides](https://docs.google.com/presentation/d/1ktRXjISKrDN2aLeubFAEph3Qbmhm7FyW6Jm9iE6Dm-8/edit?usp=sharing)
:::

# What is Research Data Management ? 

To put it briefly, Research Data Management are all of the processes, strategies and policies that will be put in place before, during and after a research project, in order to ensure that your research data is being properly, stored, organized, manipulated, shared, preserved, etc. 

One of the key factors influencing the replicability crisis, is that data is often improperly managed and documented. For example ; 
 - There is insufficient documentation to explain how the data was collected, organized and manipulated.
 - The dataset is incomplete, files are missing and no one knows where they are.
 - Key variables are not sufficiently described.
 - Researchers do not know how to request access to the data.
 - Etc.

Remember that replicability is a spectrum, not a binary. The more actions you take during your project to ensure that your data is properly managed, the more likely it is that your results or data, can be replicated or reused afterwards.

:::{admonition} Key takeaway
:class: important
Research data management is not a single act or step in your research workflow, 
but is a series of overlaping actions that you will take throughout your project, 
to ensure that at the end of your project, you have a well managed and organized dataset, 
that can be reused by yourself and others.
:::

## What We'll Cover

- Principles for structuring data directories and file naming
- Documenting datasets with metadata and documentation
- Versioning data alongside code
- Choosing where and how to store and share data
- Ethical considerations when it comes to research data management
- The FAIR principles (Findable, Accessible, Interoperable, Reusable)
- Research data management basics when using Git


## The Data Management Lifecycle

Research data management is usually broken into stages: **planning** (before
the project), **data creation and collection**, **analysis and processing**,
**publication and sharing**, **long-term preservation**, and eventually
**destruction** — each with its own decisions about format, access, and
retention. Planning early matters: naming and folder conventions, consent
for future reuse, and a storage plan are all far cheaper to set up before
data exists than to retrofit afterward.

## Organizing Files and Folders

A few low-cost habits make a dataset dramatically easier to reuse — by
others, and by yourself in six months:

- **File names**: prefer dashes, underscores, digits, and plain latin
  letters; avoid spaces, accents, and punctuation like `@ # % * $ ! ?`,
  which behave inconsistently across operating systems and tools.
- **Ordering**: use `YYYY-MM-DD` ([ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html))
  for dates, and leading zero-padded numbers for thematic ordering
  (`01_raw-data`, `02_treated-data`, `03_documentation`), so files sort the
  way you'd read them.
- **Raw data**: keep it in its own folder, ideally read-only, separate from
  anything derived or "treated" — and note any parameters or filters that
  were active when it was generated.
- **Backups**: back up regularly, and consider the 3-2-1 rule — 3 copies of
  your data, on 2 different kinds of media, with 1 copy off-site.

:::{admonition} Example structure
:class: tip
```
example_dataset/
├── README.md
├── 01_raw-data/
├── 02_treated-data/
├── 03_documentation/
└── 04_admin/
```
:::

## Documentation
Having detailed documentation that explains how your data is organized and its evolution, is key if you want your dataset to be reuseable in the future. Keeping documentation and keeping it up to date is like writing a letter to your future self, explaining all of the small details that you will later forget. Here are some of the main types of documentation that you might come across when working with research data.

| Name | Definition | Scope | Source |
|------|------------|:---:|:---:|
| **Data Dictionary** | A document that outlines the structure, content, and meaning of a given variable | File level | [National Center for Data Services](https://www.nnlm.gov/resources/data/data-glossary/data-dictionary) |
| **README Files** | A file included in a folder, also called a directory, to explain how to use and understand other files in the directory | Dataset level | [National Center for Data Services](https://www.nnlm.gov/resources/data/data-glossary/readme) |
| **Data Management Plans** | Details how data will be collected, processed, analyzed, described, preserved, and shared during the course of a research project [...] DMPs ensure that data will be properly documented and available for use by other researchers in the future | Project level | [National Center for Data Services](https://www.nnlm.gov/resources/data/data-glossary/readme) |

## Research Ethics and Personal Data

Any research involving human participants or their data — surveys,
interviews, biological materials, medical records — requires approval from
your institution's research ethics board (an REB, or IRB in the US) before
you access data or recruit participants, even if you're collecting it
yourself (*primary* collection) or requesting data someone else already
collected for another purpose (*secondary use*). For primary collection,
the board helps you draft an informed consent form; for secondary use, it
checks that the original consent actually covers your new use. (At
Polytechnique Montréal, this is the REB.)

Personal information — anything that can identify someone, directly or
indirectly — is *sensitive* when people have a high expectation of privacy
around it (health information, ethnicity, financial data, and similar). Data
shared publicly must be properly anonymized, and jurisdictions increasingly
regulate how — for example, Quebec's regulation on the anonymization of
personal information (A-2.1, r. 0.1). A handful of research topics are also
subject to export-control and sanctions regimes that restrict dissemination
— check with your institution's research security office if that might
apply to you. (At Polytechnique, that's
[secretariat.general@polymtl.ca](mailto:secretariat.general@polymtl.ca) for
anonymization questions, and
[securite.recherche@polymtl.ca](mailto:securite.recherche@polymtl.ca) for
research security.)

## Sharing Data and Code

A dedicated data-sharing platform (e.g., [Borealis](https://borealisdata.ca/),
[Zenodo](https://zenodo.org/), or a discipline-specific one like
[OpenNeuro](https://openneuro.org/)) gives a finished dataset a citable
landing page, searchable metadata, a DOI, and linear versioning — exactly
what the FAIR principles from [Lecture 1](lecture1.md) ask for. In this
course, Lab 2 uses
[Polytechnique's Borealis Dataverse](https://demo.borealisdata.ca/dataverse/fall2026/)
— built on Harvard's Dataverse software and supported by the [Digital
Research Alliance of Canada](https://www.alliancecan.ca/en/services/research-software)
— to deposit a real dataset.

## Versioning Large Files with Git

Once a large file is committed to a Git repository, it's part of the
history forever — every future clone and pull pays for it, and deleting it
in a later commit doesn't help. The fix is to keep the large content out of
Git itself: store it somewhere else, addressed by a stable content hash
(like a `sha256sum`), and let Git track only a small pointer to it. A few
ways to do that, roughly from simplest to most flexible:

- **[GitHub release assets](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)** — free, easy, but manual and awkward for many or frequently-changing files.
- **A cloud [object store](https://en.wikipedia.org/wiki/Object_storage)** — scales well and can be automated, but costs money and isn't very browsable.
- **[Git LFS](https://git-lfs.com/)** — natively supported by GitHub, but [free only up to a limit](https://docs.github.com/en/billing/concepts/product-billing/git-lfs).
- **[git-annex](https://git-annex.branchable.com/)** — flexible about where files actually live, at the cost of a steeper learning curve.
- **[DataLad](https://handbook.datalad.org/en/latest/index.html)** — a friendlier wrapper around git-annex, aimed at researchers.

Which one to use depends on your field's norms, your collaborators, and how
much ongoing maintenance you're willing to take on — there's no universally
right answer.

## Further ressources

- [UBC Library - Introduction to RDM](https://ubc-library-rc.github.io/rdm/) — Excellent open ressource covering the basics of Research Data Management.
- [Research Data Management in the Canadian Context](https://ecampusontario.pressbooks.pub/canadardm/) — Open Education Ressource created by Librarians across the country.
- [Cornell University README templates](https://data.research.cornell.edu/data-management/sharing/writing-readmes-for-research-code-software/) — Templates for Code and Data
- [Alliance services catalogue](https://www.alliancecan.ca/en/services/research-software) — List of services offered by the Digital Research Alliance of Canada
- [DMP Assistant](https://dmp-pgd.ca/) — Canadian platform for building a Data Management Plan, with single sign-on via your Polytechnique credentials
- [Tri-Agency - Ethical Conduct for Research Involving Humans](https://ethics.gc.ca/eng/policy-politique_tcps2-eptc2_2022.html) — An important policy statement for any research involving human participants
- [Polytechnique Research Data Management Policy](https://share.polymtl.ca/alfresco/service/api/node/content/workspace/SpacesStore/c2b4b268-f107-4f1f-a039-c2c7037128d8?a=false&guest=true) — Polytechnique's RDM policy
- [Commission d'accès à l'information](https://www.cai.gouv.qc.ca/english) — Ressources from Quebec's privacy watchdog



