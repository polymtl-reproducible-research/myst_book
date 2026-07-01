---
title: Code management with version control
date: 2026-06-10
label: lecture3
---

# Introduction

```{figure} http://www.phdcomics.com/comics/archive/phd052810s.gif
:alt: PhD comic about versionning via filenames
:width: 700px
:align: center
PHD Comics - Jorge Cham ([website](https://phdcomics.com/comics/archive.php?comicid=1323))
```

**Paragraph 1**: General context (eg ppl write code continuously, how to manage versions and for waht reasons)
* We write code for different applications: software meant for distribution, processing scripts meant for a single study, pipelines reused by multiple people in a lab, etc.
* This brings along challenges:
  * How can other people use pipelines without issues at the same time that we are continuously developping new features
  * How can we go back and rerun a processing script to reproduce a figure during peer review of a manuscript without stopping development
  * How can we efficiently manage assisting users that may have downloaded our software at different points in time, meaning different "states"
* The answer to nearly all of these question is a concept called version control, applied to software and code.

**Paragraph 2**: Brief overview of version control, and where they may have already encountered similar features.
* Version control is a system or framework than tracks the entire history of changes to files at different timepoints.
* This is typically done by tracking the changes in the files between versions (eg line that was changed, new version of that line), but this can only be done for non-compiled files (mainly, text-based).
  * Version control still works with other types of files, but entire new copies of the files are saved at each timepoint which can substantially increase the disk space usage
  * Other systems exist (git-lfs, git-annex, osf) to deal with data files and large files more efficiently.
* Many tools have version control built in. If you've used Google Docs, you can see this via the version history (see icon). In Google Drive, older versions of files are also accessible
* In software, version control not only allows to go back and view/use older versions of the code, but enables other things such as multiple people editing a project simultaneously (branches), developping new features without impacting the versions that users download and use (protected branches), tagging versions of the files in a human readable format (e.g., v1.0.0, conference-abstract, manuscript-submission, thesis-submission, etc.).

**Paragraph 3**: What we'll cover in this chapter and the aims we hope to achieve.
* After reading this chapter, you should be abe to:
  * Understand good practices of collaborative software development
  * Know strategies of code distributions and their advantages
  * Understand the central role of version control and release artefacts
  * Link the importance of these concepts to reproducible science

# Code management

**Paragraph 1**: 
* Lorem ipsum


**Paragraph 2**: 
* Lorem ipsum

# Version control

**Paragraph 1**: 
* Lorem ipsum

**Paragraph 2**: 
* Lorem ipsum

```{iframe} /public/git-branch-workflow.html
:width: 100%
:height: 560
```

# Software distribution

**Paragraph 1**: 
* Lorem ipsum


**Paragraph 2**: 
* Lorem ipsum

# Applications in research

**Paragraph 1**: 
* Lorem ipsum


**Paragraph 2**: 
* Lorem ipsum

# Resources

Semantic versioning: https://semver.org/

