---
title: Lecture 1 — Foundations of Open Science, Reproducibility and Replicability
date: 2026-07-16
label: lecture1
---

:::{iframe} https://docs.google.com/presentation/d/100t7GQeYoFKjA-O44iaJstgfMCzsK46cA47EDUPkQdo/embed?start=false&loop=false&delayms=3000
:width: 100%
:align: center
:title: Lecture 1 slides

Lecture 1 slides
:::

# Why This Course Exists

Modern research increasingly depends on code, data pipelines, and computational
analyses. Yet a large fraction of published results cannot be reproduced or
replicated, even by the original authors. This lecture introduces the
vocabulary, motivation, and guiding principles that the rest of the course
builds on: open science, reproducibility, and replicability.

## The Reproducibility and Replicability Crisis

Concerns about the reliability of published research are not new. Ioannidis
argued that, under common statistical and publication practices, a surprising
share of published findings are likely to be false {cite:p}`ioannidis2005`.
A decade later, a large-scale effort to replicate 100 studies in psychology
succeeded in reproducing the original results for well under half of them
{cite:p}`opensciencecollaboration2015`. These findings, echoed across other
fields, motivated a 2019 consensus report from the U.S. National Academies of
Sciences, Engineering, and Medicine that examined the scope of the problem and
proposed concrete recommendations for researchers, institutions, and funders
{cite:p}`nationalacademies2019`.

:::{admonition} Key takeaway
:class: important
The crisis is not primarily about fraud. It is largely about incentives,
statistical practices, and a lack of transparency in how research is
conducted, reported, and shared.
:::

## Reproducibility vs. Replicability

These two terms are often used interchangeably, but this course follows the
distinction adopted by the National Academies report {cite:p}`nationalacademies2019`:

| Term | Definition | Same data? | Same methods? |
|------|------------|:---:|:---:|
| **Reproducibility** | Obtaining consistent results using the same input data, code, and analysis | Yes | Yes |
| **Replicability** | Obtaining consistent results on new data collected following the same methodology | No | Yes |

In other words, reproducibility is about *computational transparency* — can
someone else re-run your pipeline and get your numbers? Replicability is
about *scientific robustness* — does the underlying effect hold up when the
study is repeated independently?

To cite this page elsewhere in the book, use its `label`: see [](#lecture1).

## Open Science

Open science is the broader movement to make the entire research lifecycle
— data, code, materials, and publications — transparent and accessible.
Munafò et al. propose a manifesto of concrete practices that address the
reproducibility crisis directly, including pre-registration, sharing of data
and code, and reporting guidelines {cite:p}`munafo2017`.

A widely adopted framework for making research outputs usable by others is
the **FAIR** principles {cite:p}`wilkinson2016`:

:::{admonition} FAIR Principles
:class: tip
- **F**indable — data and metadata are assigned a persistent identifier and
  are described richly enough to be discovered.
- **A**ccessible — data can be retrieved using a standard, open protocol,
  with clear conditions for access.
- **I**nteroperable — data use a formal, shared language for knowledge
  representation.
- **R**eusable — data are richly described with accurate provenance and
  clear usage licenses.
:::

Note that FAIR does not require data to be *open* — it is possible for data
to be FAIR yet access-restricted (e.g., for privacy reasons). This is an
important nuance: open science and open data are related but distinct from
FAIRness.

## What This Course Will Cover

Over the following lectures and labs, we will move from these foundational
concepts to hands-on practice:

1. Version control and collaborative workflows (Git/GitHub)
2. Structuring reproducible computational environments
3. Data and code sharing practices, licensing, and persistent identifiers
4. Reporting standards and pre-registration
5. Building a fully reproducible research artifact from end to end

:::{admonition} Note
:class: note
Each lecture is paired with a lab where you will apply the concepts to a
small, concrete research artifact that you will build up over the semester.
:::
