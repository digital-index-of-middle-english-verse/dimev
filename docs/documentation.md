---
title: The Digital Index of Middle English Verse
subtitle: A Technical Introduction
author:
- Ian Cornelius
- Michael Johnston
date: \today
thanks: The authors gratefully acknowledge the advice and support of Linne Mooney and Daniel Mosser. The section [History and Responsibility] incorporates text authored by Mooney.
---

\newpage

[dimev.net]: http://www.dimev.net
[manuscript description module]: https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html
[git]: https://git-scm.com/
[sandbox repository]: https://github.com/digital-index-of-middle-english-verse/sandbox
[GitHub repository]: https://github.com/digital-index-of-middle-english-verse/dimev
[Zenodo]: https://zenodo.org/
[Zotero Group Library]: https://www.zotero.org/groups/6111344/dimev_bibliography

# General Introduction

The *Digital Index of Middle English Verse* (DIMEV) is a comprehensive, open-access bibliographic database of the surviving English-language verse from the period 1200--1525.
The aim is to record each surviving item of Middle English verse and the documentary sources by which it is transmitted, with transcriptions of at least the first two lines and last two lines of each copy.
Copies after 1525 are recorded only if derived from an exemplar that no longer survives.
References to modern scholarly transcriptions and critical editions are supplied where available; references to digital facsimiles have been added for some items.
Other recorded metadata include author, scribe, verse form, subject-matter, standard bibliographic reference numbers, and linguistic descriptions of manuscript witness.

Like any finding aid or bibliographic register, DIMEV aims to keep the surviving historical record visible, verifiable, and accessible:
we aim to enable students and researchers to identify, locate, and retrieve texts relevant to their research questions or areas of inquiry.
The importance of DIMEV to its scholarly community is illustrated by a search for "DIMEV" on [Google Books](https://www.google.com/search?tbm=bks&q=dimev).
Search results show that DIMEV is employed in scholarship on Middle English literature and culture as a standard way of identifying texts under discussion and as a launching point for deeper study.

DIMEV has been live online at [dimev.net] since 2011, updated regularly to supply omissions, record newly identified items and witnesses, record newly published transcriptions, editions, and facsimiles, and correct error.
**Updates of dimev.net ceased on 31 December 2024, to accommodate modernization of source data and maintenance practices.**

In due course, the current DIMEV website will be replaced by a new one.
Until such time, users who seek the most current authoritative record of Middle English verse should consult DIMEV's source data directly.

Source data are maintained in a public [GitHub repository] and archived within [Zenodo], an open data repository.
Zenodo supplies a DOI, suitable for citation: see @MooneyDigitalIndexMiddle2025.
The document you are reading serves as a guide to the source data.
Readers new to XML should consult an introductory grammar, for instance @TEIConsortiumTEIP5Guidelines2024, [A Gentle Introduction to XML](https://tei-c.org/release/doc/tei-p5-doc/en/html/SG.html).

# History and responsibility

DIMEV incorporates and extends a bibliographic tradition whose principal earlier efforts are @BrownRegisterMiddleEnglish1916, @BrownIndexMiddleEnglish1943, @RobbinsSupplementIndexMiddle1965, @HamerManuscriptIndexIndex1995, and @BoffeyNewIndexMiddle2005, and it shares a point of origin with the last of these.
In 1993 Julia Boffey, A. S. G. Edwards, and Linne R. Mooney obtained funding to produce an updated index of Middle English verse, which would combine @BrownIndexMiddleEnglish1943 and @RobbinsSupplementIndexMiddle1965, correct error, and record materials that had come to light in the previous thirty years.
In the first year of collaboration the team divided.
DIMEV subsequently emerged as a distinct venture, distinguished in three respects from prior efforts in its tradition:

1. Digital medium
2. Return to primary sources
3. Transcription of opening and closing lines of witnesses

Digital medium has shaped the project fundamentally:
it allows for incremental updates and correction of error;
it also removes constraints of space, allowing DIMEV to give much fuller attention to individual witnesses than was possible in print indexes.
Transcriptions of opening and closing lines provide a snapshot of textual and linguistic variation among witnesses.
They are a product of DIMEV's general survey method, returning to primary sources and verifying each reference anew.
This survey method serves also to remove accreted error from the bibliographic tradition.
The three distinctive features form a coherent working method.

Mooney's initial work on DIMEV was assisted by Elizabeth Solopova and funded by a grant from the National Endowment for the Humanities (University of Maine, 1995--97).
In 2004 Mooney was offered a position at the University of York, a post that enabled her to resume data collection in UK libraries.
From 2007 onwards she has been aided by Daniel W. Mosser who became involved while in York on a Leverhulme Visiting Professorship (2007--9).
Mosser provided the technical vision and contacts to serialize DIMEV data in XML.
With assistance from Dave Radcliffe, DIMEV went live online in 2011.

In 2012 Mooney obtained funding from the Modern Humanities Research Association to hire a part-time research assistant.
In this position Deborah Thorpe continued DIMEV's survey of British Library manuscripts.
The survey of British Library manuscripts was completed by Mooney in 2024, supported by an Emeritus Fellowship for two years from the Leverhulme Trust (awarded 2022).

From 2007 to 2025 Mooney and Mosser served as co-editors of DIMEV, sharing responsibility for content.
Mosser was technical editor, maintaining data files and pushing updates to [dimev.net].
In 2025 editorial responsibility passed to Ian Cornelius and Michael Johnston.
Cornelius is technical editor and lead author of this documentation.

# Overview of DIMEV Data

DIMEV data are contained in XML files and a Zotero Group Library.

## Zotero Library

DIMEV's [Zotero Group Library] records bibliographic details for modern transcriptions, editions, and facsimiles cited elsewhere in DIMEV data.
The library is periodically exported as Zotero RDF and logged in DIMEV's principal [GitHub repository], within the directory `data/`.
The RDF file is intended only as an archival backup.

## XML files

XML files are of three types:

- `Records.xml`: The principal file, collecting metadata on verse items, transcriptions of witnesses to verse items, and cross-references for acephalous or fragmentary texts
- `Manuscripts.xml`, `PrintedBooks.xml`, `Inscriptions.xml`: Bibliographic details for witnesses cited in `Records.xml`
- `subject-terms.xml`, `form-terms.xml`, `language-terms.xml`: Controlled vocabularies for the elements `subjects`, `verseForms`, and `languages` in `Records.xml`

These XML files are located within the directory `data/` in DIMEV's principal [GitHub repository].
Structures are documented in two forms:

1. A human-readable specification, provided in the following subsections of this documentation
1. Machine-readable schemas, written as XSD files and located in the directory `schemas/`

The Python script `validator.py` can be used to validate XML files against the corresponding XSD file.
For instructions see the comment at the head of `validator.py`.

# `Records.xml`

## Overview {#overview-records}

This XML file stores information on verse items, including extracts and acephalous texts.
The root element is `records`.

The XML structure makes an implicit distinction between two types of `record` items:

1. **Full `record` items**.
  These represent items with the bibliographic status of *works*.
  Each has a unique identifier (recorded as the attribute `xml:id`) and a child element `witnesses`, listing one or more documentary witnesses to the item.
1. **Partial `record` items**.
  These represent extracts, fragments, and acephalous texts of *works*, or else an erroneous superseded item number.
  Each supplies a cross reference to the relevant full `record` element.
  Cross references are supplied in the child element `description`.
  Partial `record` elements usually lack a unique identifier.
  They also lack most child elements of full `record` items, and always lack the element `witnesses`.

## Tag library

### `records`

- **Description**
  Root element containing a collection of bibliographic entries
- **Attributes**
  None
- **Must contain**
  - `record` (one or more)

### `record`

- **Description**
  A single record describing a verse item
- **Attributes**
  - `xml:id` — optional unique identifier, assigned by DIMEV editors; most stub records lack this attribute, while full records with `witnesses` require it in practice.
    The unique identifier has two hyphen-delimited components: (1) the invariant string `record`; (2) a number, usually integer but sometimes with one or two decimal places.
    The numerical component of the unique identifier is the "DIMEV number" for the item; it may be used in scholarship as a persistent bibliographic pointer to the item.
- **Must occur within**
  - `records`
- **Must contain**
  - `name` (exactly one)
  - `alpha` (exactly one)
- **May contain**
  - `repertories` (zero or one)
  - `editions` (zero or one)
  - `crossRefs` (zero or one)
  - `description` (zero or one)
  - `descNote` (zero or one)
  - `authors` (zero or one)
  - `titles` (zero or one)
  - `subjects` (zero or one)
  - `verseForms` (zero or one)
  - `languages` (zero or one)
  - `ghosts` (zero or one)
  - `witnesses` (zero or one)

### `name`

- **Description**
  An *incipit*, or first line of the verse item, employed for purposes of identification in a textual tradition in which most items are anonymous and untitled.
  Spellings are standardized.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **May contain**
  Mixed text and:
  - `i` (zero or more)

### `alpha`

- **Description**
  Another standardized first line, manually forced to downcase string and sometimes truncated.
  This is used for alphabetical sorting of items.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  Text only (`xs:string`)

### `repertories`

- **Description**
  Reference numbers assigned to the item in other reference works, namely, @BrownIndexMiddleEnglish1943, @RobbinsSupplementIndexMiddle1965, @BoffeyNewIndexMiddle2005, @RinglerBibliographyIndexEnglish1988, @RinglerBibliographyIndexEnglish1992, @WhitingProverbsSentencesProverbial1968, and the [Bibliography of the Middle English Compendium](https://quod.lib.umich.edu/m/middle-english-dictionary/bibliography), among others.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `item` (one or more)

### `editions`

- **Description**
  List of references to scholarly transcriptions or critical editions
- **Attributes**
  None
- **May occur within**
  - `record` (for critical editions)
  - `witness` (for diplomatic editions and transcriptions)
- **Must contain**
  - `item` (one or more)

### `crossRefs`

- **Description**
  Container for cross-references to other `record` items; defined for future use and not yet implemented
- **Attributes**
  None
- **May occur within**
  - `record`
- **Must contain**
  - `item` (one or more)

### `description`

- **Description**
  Descriptive note on the item in a very permissive mixed-content form, including inline formatting and references to witnesses, scholarly publications, and other item records.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `descNote`

- **Description**
  Additional descriptive note in a very permissive mixed-content form, like `description` but usually more limited in scope or importance
- **Attributes**
  None
- **May occur within**
  - `record`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `authors`

- **Description**
  Container for any generally accepted author attributions for the item.
  Author attributions given by documentary witnesses are transcribed instead within `MSAuthor`.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `author` (one or more)

### `author`

- **Description**
  Author name
- **Attributes**
  None
- **Must occur within**
  - `authors`
- **May contain**
  - `first`
  - `last`
  - `suffix`

### `titles`

- **Description**
  Container for title any titles generally assigned to the item in modern scholarship.
  Titles given by documentary witnesses are transcribed within the element `MSTitle`.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `title` (one or more)

### `title`

- **Description**
  Title associated with the record
- **Attributes**
  None
- **Must occur within**
  - `titles`
- **May contain**
  Mixed text and:
  - `i` (up to two occurrences)

### `subjects`

- **Description**
  List of descriptive keywords, mostly for content;
  Controlled vocabulary is set by `subject-terms.xml`
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `term` (one or more)

### `verseForms`

- **Description**
  List of descriptive keywords for verse-form: rhyme scheme, stanza length, etc.; controlled vocabulary is set by `form-terms.xml`.
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `term` (one or more)

### `languages`

- **Description**
  List of languages employed in the item, other than English; controlled vocabulary is set by `language-terms.xml`
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `term` (one or more)

### `ghosts`

- **Description**
  List of manuscripts or other text-carrying documents erroneously claimed in prior scholarship to contain a copy of the item
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `item` (one or more)

### `witnesses`

- **Description**
  List of original witnesses to the item (usually manuscripts, sometimes inscriptions or early printed books).
- **Attributes**
  None
- **Must occur within**
  - `record`
- **Must contain**
  - `witness` (one or more)

### `witness`

- **Description**
  A witness to the item, including transcription, source, and related metadata
- **Attributes**
  - `xml:id` — required unique identifier, assigned by DIMEV editors, composed of three hyphen-delimited components: (1) the invariant string `wit`; (2) the "DIMEV number" for the item; (3) an integer designating this witness.
     The unique identifier allows for cross-reference within `Records.xml` and from DIMEV's other XML files.[^wit-caveat]
  - `illust` — optional boolean indicating whether the witness has accompanying illustration
  - `music` — optional boolean indicating whether the witness has accompanying music
- **Must occur within**
  - `witnesses`
- **Must contain**
  - either `allLines` or one or more paired occurrences of `firstLines` and `lastLines`.
    The elements `firstLines` and `lastLines` are repeated in alternation to record items broken across two or more discontinuous ranges.
  - `source` (exactly one)
- **May contain**
  - `sourceNote` (zero or one)
  - `MSAuthor` (zero or one)
  - `MSTitle` (zero or one)
  - `facsimiles` (zero or one)
  - `editions` (zero or one)

[^wit-caveat]: **Caveat lector**: The final component of DIMEV's unique identifier for a witness may differ from the positional number assigned to that witness on [dimev.net].
The witness numbers printed on the current website are generated anew during each build, as a function of witness order, and can change without notice.
Scholars are advised to reference witnesses by manuscript shelfmarks, not the number assigned to a given witness on DIMEV's current website.

### `allLines`

- **Description**
  Transcription of the full text of the witness
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `del`
  - `i`
  - `lb`
  - `sic`
  - `sup`

### `firstLines`

- **Description**
  Transcription of the opening lines of the witness
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `del`
  - `i`
  - `lb`
  - `sic`
  - `sup`

### `lastLines`

- **Description**
  Transcription of the closing lines of the witness
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `del`
  - `i`
  - `lb`
  - `sic`
  - `sup`

### `source`

- **Description**
  Reference to the text-carrying source document for a witness, with one or more locational ranges
- **Attributes**
  - `key` — required source identifier, linking to a unique entry in the XML files `Manuscripts.xml`, `PrintedBooks.xml`, or `Inscriptions.xml`
  - `prefix` — optional unit of navigation, usually folio, page, or signature
- **Must occur within**
  - `witness`
- **May contain**
  Zero or more repetitions of:
  - `start`
  - `end` (optional after each `start`)

### `start`

- **Description**
  Location at which the text of the witness begins; may repeat to record discontinuous ranges
- **Attributes**
  - `loc` — optional folio-side ("r" for "recto" or "v" for "verso") or similar locator, used for documents with leaf-based navigation systems; may be omitted in references to the recto of a leaf
  - `col` — optional column designation (where present, usually "a" or "b"), used for documents with multi-columnar page designs
  - `pre` — optional ad hoc prefix, used to record irregularities in foliation or pagination
- **Must occur within**
  - `source`
- **Must contain**
  Text only (`xs:string`)

### `end`

- **Description**
  Location at which the text of the witness ends; may be omitted if the text of the witness occupies a single side of one leaf
- **Attributes** As in [start]
- **Must occur within**
  - `source`
- **Must contain**
  Text only (`xs:string`)

### `sourceNote`

- **Description**
  Note on the source, using permissive mixed content
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `MSAuthor`

- **Description**
  Any author attribution transmitted with the witness
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `MSTitle`

- **Description**
  Any title attribution transmitted with the witness
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `facsimiles`

- **Description**
  List of published facsimile reproductions of the source document
- **Attributes**
  None
- **Must occur within**
  - `witness`
- **Must contain**
  - `item` (one or more)

### `item`

- **Description**
  Generic list item used within `repertories`, `editions`, `crossRefs`, `ghosts`, and `facsimiles`
- **Attributes**
  None
- **Must occur within**
  - `repertories`
  - `editions`
  - `crossRefs`
  - `ghosts`
  - `facsimiles`
- **Must contain**
  Content depends on parent element:
  - in `repertories`, `editions`, and `facsimiles`: either `bibl` with optional `note`, or `note` alone
  - in `crossRefs`: `ref` with optional `note`
  - in `ghosts`: either `mss` with optional `note`, or `note` alone

### `bibl`

- **Description**
  Bibliographical citation or reference
- **Attributes**
  - `key` — required reference key, designating an item in the [Zotero Group Library].
- **May occur within**
  - `item`
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
- **May contain**
  Mixed text and:
  - `i`
  - `sup`

### `mss`

- **Description**
  Manuscript citation or manuscript reference
- **Attributes**
  - `key` — required reference key
- **May occur within**
  - `item`
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
- **May contain**
  Mixed text and:
  - `i`
  - `sup`

### `ref`

- **Description**
  Empty cross-reference pointing element
- **Attributes**
  - `target` — required target value
- **May occur within**
  - `item`
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
- **Must contain**
  No child elements or text

### `note`

- **Description**
  Note associated with a bibliographical item, ghost item, or cross-reference item
- **Attributes**
  None
- **Must occur within**
  - `item`
- **May contain**
  Mixed text and any number of:
  - `add`
  - `bibl`
  - `del`
  - `i`
  - `lb`
  - `mss`
  - `ref`
  - `scribe`
  - `sic`
  - `sup`

### `term`

- **Description**
  Controlled term or keyword in a term list
- **Attributes**
  None
- **Must occur within**
  - `subjects`
  - `verseForms`
  - `languages`
- **Must contain**
  Text only (`xs:string`)

### `i`

- **Description**
  Inline italic text
- **Attributes**
  None
- **May occur within**
  - `name`
  - `title`
  - `bibl`
  - `mss`
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
- **May contain**
  - in `name` and `title`: text only (`xs:string`)
  - elsewhere: mixed text and any number of `add`, `del`, `lb`, `scribe`, `sup`

### `sup`

- **Description**
  Inline superscript text
- **Attributes**
  None
- **May occur within**
  - `bibl`
  - `mss`
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
  - `i`
- **Must contain**
  Text only (`xs:string`)

### `add`

- **Description**
  Added text in a transcription or note
- **Attributes**
  None
- **May occur within**
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
  - `i`
- **Must contain**
  Text only (`xs:string`)

### `del`

- **Description**
  Deleted text in a transcription or note
- **Attributes**
  None
- **May occur within**
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
  - `i`
- **Must contain**
  Text only (`xs:string`)

### `lb`

- **Description**
  Line-break marker
- **Attributes**
  None
- **May occur within**
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
  - `i`
- **Must contain**
  No child elements or text

### `scribe`

- **Description**
  Inline person name identifying a scribe
- **Attributes**
  None
- **May occur within**
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `i`
- **May contain**
  - `first`
  - `last`
  - `suffix`

### `sic`

- **Description**
  Text marked as erroneous or reproduced as found
- **Attributes**
  None
- **May occur within**
  - `description`
  - `descNote`
  - `sourceNote`
  - `MSAuthor`
  - `MSTitle`
  - `allLines`
  - `firstLines`
  - `lastLines`
- **Must contain**
  Text only (`xs:string`)

### `first`

- **Description**
  First name or given name
- **Attributes**
  None
- **Must occur within**
  - `author`
  - `scribe`
- **Must contain**
  Text only (`xs:string`)

### `last`

- **Description**
  Last name or surname
- **Attributes**
  None
- **Must occur within**
  - `author`
  - `scribe`
- **Must contain**
  Text only (`xs:string`)

### `suffix`

- **Description**
  Suffix attached to a personal name, but also used to flag dubious attributions (with a question mark)
- **Attributes**
  None
- **Must occur within**
  - `author`
  - `scribe`
- **Must contain**
  Text only (`xs:string`)


## Technical direction {#tech-dir-records}

- Atomize, writing each full `record` element to a separate file within a new sub-directory `records/`, to enable effective use of [git] distributed file history
- Collect partial `record` elements (i.e., those `record` elements serving as cross-references to full `record` elements) in a single separate file, perhaps named `cross-references.xml`
- In the element `author` (child of `authors`), disaggregate name suffixes and query marks indicating dubious attributions

# `Manuscripts.xml`

## Overview {#overview-manuscripts}

This XML file stores bibliographic information on medieval manuscripts cited as witnesses in the XML file `Records.xml`.
It also includes some individual copies of early printed books, cited within `Records.xml` for manuscript inscriptions or binding fragments.
The root element is `list`.

## Tag library

### `list`

- **Description**
  Root element containing a list of bibliographic entries for medieval manuscripts and particular copies of early printed books
- **Attributes**
  None
- **Must contain**
  - `item` (one or more)

### `item`

- **Description**
  A bibliographic entry for a medieval manuscript or a particular copy of an early printed book
- **Attributes**
  - `xml:id`: required unique identifier
- **Must occur within**
  - `list`
- **Must contain** (in sequence)
  - `settlement` (exactly one)
  - `repos` (exactly one)
  - `desc` (exactly one)
- **May contain**
  - `lang` (zero or one)
  - `surrogates` (zero or one)

### `settlement`

- **Description**
  The city or town in which the manuscript is held at present.
  Equivalent to the element `settlement` in @TEIConsortiumTEIP5Guidelines2024, [manuscript description module].
- **Attributes**
  None
- **Must occur within**
  - `item`
- **Must contain**
  Text only (`xs:string`)

### `repos`

- **Description**
  The repository in which the manuscript is held at present.
  Equivalent to the elements `institution` and `repository` in the TEI [manuscript description module].
- **Attributes**
  None
- **Must occur within**
  - `item`
- **Must contain**
  Text only (`xs:string`)

### `desc`

- **Description**
  The present shelfmark of the manuscript.
  Equivalent to the elements `collection` and `idno` in the TEI [manuscript description module].
  Previous shelfmarks may be supplied after the current shelfmark; these are usually enclosed in square brackets and prefixed with "*olim*".
- **Attributes**
  None
- **Must occur within**
  - `item`
- **May contain**
  Mixed text and any number of the following:
  - `i`
  - `sup`
  - `mss`
  - `bibl`

### `i`

- **Description**
  Inline italic text
- **Attributes**
  None
- **May occur within**
  - `desc`
  - `lang`
- **Must contain**
  Text only (`xs:string`)

### `sup`

- **Description**
  Inline superscript text
- **Attributes**
  None
- **May occur within**
  - `desc`
- **Must contain**
  Text only (`xs:string`)

### `mss`

- **Description**
  Cross-reference to a manuscript entry
- **Attributes**
  - `key`: required reference key
- **May occur within**
  - `desc`
  - `lang`
- **Must contain**
  No child elements or text

### `bibl`

- **Description**
  Citation of an item in DIMEV's Zotero Group Library
- **Attributes**
  - `key`: required citation key
- **May occur within**
  - `desc`
  - `lang`
- **May contain**
  Text only (`xs:string`)

### `lang`

- **Description**
  Localization of the language of the manuscript, with reference to @LaingLinguisticAtlasEarly2013, @BenskinElectronicVersionLinguistic2013, and subsequent scholarship.
- **Attributes**
  None
- **May occur within**
  - `item`
- **Must contain**
  At least one of the following:
  - `langGrid`
  - `i`
  - `mss`
  - `bibl`
  - `place`

### `langGrid`

- **Description**
  LALME language grid coordinates
- **Attributes**
  None
- **May occur within**
  - `lang`
- **Must contain**
  Text only (`xs:string`)

### `place`

- **Description**
  Place-name referenced within a language note
- **Attributes**
  - `country`: optional country name
  - `county`: optional county name
  - `town`: optional town name
- **May occur within**
  - `lang`
- **Must contain**
  Text only (`xs:string`)

### `surrogates`

- **Description**
  Container for references to on-line facsimiles of the manuscripts.
- **Attributes**
  None
- **May occur within**
  - `item`
- **Must contain**
  - `ref` (one or more)

### `ref`

- **Description**
  Reference to an on-line facsimile
- **Attributes**
  - `target`: required URI target
- **Must occur within**
  - `surrogates`
- **Must contain**
  No child elements or text

## Technical direction {#tech-dir-manuscripts}

- Distinguish manuscripts from (particular copies of) early printed books, perhaps by adding a new attribute `type` to `item` elements
- Atomize, writing each full `item` element to a separate file within a new sub-directory `sources/`, to enable effective use of [git] distributed file history
- Rename and restructure element names to align with guidelines of the TEI [manuscript description module]
- Extract previous shelfmarks to a new element, `altIdentifier`

# `Inscriptions.xml`

## Overview {#overview-inscr}

This XML file stores bibliographic information on inscriptions and other epigraphic texts cited as witnesses in the XML file `Records.xml`.

`Inscriptions.xml` employs a simpler variant of the document structure employed in `Manuscripts.xml`.
The root element is `list`.

## Tag library

### `list`

- **Description**
  Root element containing a list of inscribed objects and epigraphic texts
- **Attributes**
  None
- **Must contain**
  - `item` (one or more)

### `item`

- **Description**
  A single entry representing an inscribed object or epigraph
- **Attributes**
  - `xml:id`: required unique identifier
- **Must occur within**
  - `list`
- **Must contain** (in sequence)
  - `settlement` (exactly one)
  - `repos` (exactly one)
  - `desc` (exactly one)

### `settlement`

- **Description**
  Settlement or place where the item is located
- **Attributes**
  None
- **Must occur within**
  - `item`
- **Must contain**
  Text only (`xs:string`)

### `repos`

- **Description**
  The institutional holder of the item
- **Attributes**
  None
- **Must occur within**
  - `item`
- **Must contain**
  Text only (`xs:string`)

### `desc`

- **Description**
  Institutional identifier and/or brief description of the item
- **Attributes**
  None
- **Must occur within**
  - `item`
- **Must contain**
  Text only (`xs:string`)

## Technical direction {#tech-dir-inscr}

- Add an attribute `type` with value "inscription" to `item` elements
- Atomize, writing each full `item` element to a separate file within a new sub-directory `sources/`, to enable effective use of [git] distributed file history

# `PrintedBooks.xml`

## Overview {#overview-printed-books}

This XML file stores bibliographic information for editions of early printed books cited as witnesses in the XML file `Records.xml`.
The root element is `list`.

## Tag library {#doc-struct-printed-books}

### `list`

- **Description**
  Root element containing a collection of bibliographic records
- **Attributes**
  None
- **Must Contain**
  `bibl` (one or more)

### `bibl`

- **Description**
  A single bibliographic record
- **Attributes**
  - `xml:id`: required unique identifier
  - `n`: required identifier, usually the corresponding item number in @PollardShorttitleCatalogueBooks1950, where available.
    For non-English books and other items not recorded in the STC, the value of `n` is often a dummy string ("X").
    Sometimes another value is used.
- **Must occur within**
  `list`
- **Must contain** (in order)
  - `authorstmt`
  - `titlestmt`
  - `pubstmt`
  - `desc`

### `authorstmt`

- **Description**
  Container for author information
- **Attributes**
  None
- **Must occur within**
  `bibl`
- **Must contain**
  `author` (exactly one)

### `author`

- **Description**
  Name of the author
- **Attributes**
  None
- **Must occur within**
  `authorstmt`
- **Must contain**
  Text only (`xs:string`)

### `titlestmt`

- **Description**
  Container for title information
- **Attributes**
  None
- **Must occur within**
  `bibl`
- **Must contain**
  `title` (exactly one)

### `title`

- **Description**
  Title of the work
- **Attributes**
  - `level`: required value indicating the bibliographic level or title type.
    The value of which is always "m" (for "monograph").
- **Must occur within**
  `titlestmt`
- **Must contain**
  Text only (`xs:string`)

### `pubstmt`

- **Description**
  Agent, date, and location of printing, as given in the volume or as reconstructed
- **Attributes**
  - `date`: publication year (Gregorian calendar, Common Era) (`xs:gYear`)
- **Must occur within**
  `bibl`
- **Must contain**
  Text only (`xs:string`)

### `desc`

- **Description**
  Descriptive note for the bibliographic item
- **Attributes**
  None
- **Must occur within**
  `bibl`
- **May contain**
  Mixed text content with up to two occurrences total of:
  - `name`
  - `i`
- **Notes**
  This content model is intentionally restrictive to reflect current data.

### `name`

- **Description**
  Name referenced within a description
- **Attributes**
  None
- **May occur within**
  `desc`
- **Must contain**
  Text only (`xs:string`)

### `i`

- **Description**
  Inline element for italicized text
- **May occur within**
  `desc`
- **May contain**
  Mixed text with zero or more of `sup`

### `sup`

- **Description**
  Inline superscript text
- **May occur within**
  - `i`
  - `desc`
- **Must contain** Text only (`xs:string`)

## Technical direction {#tech-dir-printed-books}

- For references to editions: implement a standard data structure for XML serialization of bibliographic metadata for early printed books
- Disaggregate references to @PollardShorttitleCatalogueBooks1950 from other content of the attribute `n`
- Supply references to the English Short Title Catalog (ESTC) where available.

# Controlled vocabularies: `subject-terms.xml` and others

## Overview {#overview-vocab}

The XML files `subject-terms.xml`, `verseForm-terms.xml`, and `language-terms.xml` specify controlled vocabularies for `subjects`, `verseForms`, and `languages` in `Records.xml`.
These files share a single data model.

## Tag library

### `list`

- **Description**
  Root element representing a simple list with a heading and one or more items
- **Attributes**
  None
- **Must contain**
  - `head` (exactly one)
  - `item` (one or more)

### `head`

- **Description**
  Textual heading for the list
- **Attributes**
  None
- **Must occur within**
  `list`
- **Must contain**
  Text only (`xs:string`)

### `item`

- **Description**
  Individual list entry
- **Attributes**
  None
- **Must occur within**
  `list`
- **Must contain**
  `term` (exactly one)

### `term`

- **Description**
  A controlled term or keyword employed in `Records.xml`
- **Attributes**
  None
- **Must occur within**
  `item`
- **Must contain**
  Text only (`xs:string`)

# Licensing

DIMEV source data, this documentation, and other contents of the repository that contains them are released under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

# Works Cited
