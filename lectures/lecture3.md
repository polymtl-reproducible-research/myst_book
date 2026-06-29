---
title: Lecture 3 — Subject
date: 2026-06-10
label: lecture3
---

# Heading 1

Some references for MyST formatting:

* [60 seconds cheatsheet](https://commonmark.org/help/).
* [MyST "get started"](https://mystmd.org/guide/quickstart-myst-markdown).
* [MyST overview of "directives" and "roles"](https://mystmd.org/guide/syntax-overview).
* [MyST reference for "directives"](https://mystmd.org/guide/directives).
* [MyST reference for "roles"](https://mystmd.org/guide/roles).

## Heading 2

This horizontal rule is exactly 80 characters long:
--------------------------------------------------------------------------------

:::{admonition} Note
:class: note
This is a placeholder admonition. Replace with your own content.
:::

To cite another page of the MyST book, you can use the `label` defined at the
top of the file, with this syntax: see [](#lecture1).

To cite a bibtex reference, use the syntax {cite:p}`sample2026` and make sure
it appears in `bibliography/references.bib`.

You can include equations using LaTeX syntax:

$$
E = mc^2
$$ (lec-3-eq-energy)

Reference it as [](#lec-3-eq-energy).

You can include figures using this syntax:

```{figure} ../images/site_logo.png
:label: lec-3-fig-placeholder
:alt: A placeholder figure
:align: center

A placeholder figure. Replace with your own image.
```

Reference it as [](#lec-3-fig-placeholder).

You can include tables using this syntax:

| Parameter | Value | Unit |
|-----------|-------|------|
| Example   | 42    | --   |
