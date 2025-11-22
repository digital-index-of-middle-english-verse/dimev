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

# Data files

## Overview

DIMEV data are contained in XML files and a Zotero Group Library.

### XML files

There are five XML files:

- `Records.xml`: The principal file, collecting metadata on verse items, transcriptions of witnesses to verse items, and cross-references for acephalous or fragmentary texts
- `Manuscripts.xml`, `PrintedBooks.xml`, `Inscriptions.xml`: Bibliographic details for witnesses cited in `Records.xml`
- `Glossary.xml`: Definitions and dictionary references for some lexical items that appear in DIMEV transcriptions

These XML files are located within the directory `data/` in DIMEV's principal [GitHub repository].
Each file employs a custom structure, documented in two forms:

1. A human-readable specification, provided in the following subsections of this documentation
1. Machine-readable schemas, written as XSD files and located in the directory `schemas/`

The Python script `validator.py` can be used to validate XML files against the corresponding XSD file.
For instructions see the comment at the head of `validator.py`.

### Zotero Library

DIMEV's [Zotero Group Library] records bibliographic details for modern transcriptions, editions, and facsimiles cited elsewhere in DIMEV data.
The library is periodically exported as Zotero RDF and logged in DIMEV's principal [GitHub repository], within the directory `data/`.
The RDF file is intended only as an archival backup.

## `Records.xml`

### Overview {#overview-records}

This XML file stores information on verse items, including extracts and acephalous texts.
Each verse item is represented within a `record` element.
`record` elements are serialized as children of the root element `records`.

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

### Document structure {#doc-struct-records}

#### Root element {#root-records}

- Name: `records`
- Description: contains a collection of bibliographic entries for Middle English verse items
- Content: `record` elements

#### Child elements of `records`

- Name: `record`
- Description: contains a bibliographic entry for a single Middle English verse item
- Content and Attributes: as detailed in the following sections.
  **Note**: the specification in the following sections applies to full `record` elements, as defined above in the [Overview](#overview-records) to `Records.xml`.

#### Attributes of `record`

Each full `record` element carries an attribute `xml:id`.
This is a unique identifier, assigned by DIMEV editors.
The unique identifier has two hyphen-delimited components: (1) the invariant string `record`; (2) a number, usually integer but sometimes with one or two decimal places.
The unique identifier allows for cross-reference within `Records.xml` and from DIMEV's other XML files.
The numerical component of the unique identifier is the "DIMEV number" for the item; it may be used in scholarship as a persistent bibliographic pointer to the item.

#### Child elements of `record`

Each full `record` element may have the following child elements.
Except `name` and `alpha`, which are required, all child elements are optional.

- `name`. The *incipit*, or first line of the verse item, employed for purposes of identification in a textual tradition in which most items are anonymous and untitled.
  Spellings are standardized.
  Data type: usually string; may contain inline formatting or `gloss` elements.
- `alpha`. Another standardized first line, manually forced to downcase string and sometimes truncated.
  This is used for alphabetical sorting of items.
  Data type: string
- `repertories`. Reference numbers assigned to the item in other reference works, namely, @BrownIndexMiddleEnglish1943, @RobbinsSupplementIndexMiddle1965, @BoffeyNewIndexMiddle2005, @RinglerBibliographyIndexEnglish1988, @RinglerBibliographyIndexEnglish1992, @WhitingProverbsSentencesProverbial1968, and the [Bibliography of the Middle English Compendium](https://quod.lib.umich.edu/m/middle-english-dictionary/bibliography), among others.
- `description`. Descriptive commentary on the item.
  Data type: free text with mixed content (recursively mixed where allowed), including inline formatting and references to witnesses, scholarly publications, and other item records.
- `descNote`. Descriptive commentary on the item, similar to the content of `description` but usually more limited in scope or importance.
  Data type: free text with mixed content like `description`.
- `authors`. Any generally accepted author attributions for the item.
  Dubious attributions may be flagged with a question mark in the child element `suffix` (see below).
  Author attributions given by documentary witnesses are transcribed within the element `MSAuthor`, a child of `witness`.
  See [Child elements of `witness`].
  Data type: an array of one or more child elements with the tag `author`.
  Each `author` element is a structured sequence with child elements `last`, `first`, and `suffix`, each of which has string content.
  There is no controlled vocabulary.
- `titles`. Any titles generally assigned to the item in modern scholarship.
  Titles given by documentary witnesses are transcribed within the element `MSTitle`, a child of `witness`.
  See [Child elements of `witness`].
  Data type: an array of one or more child elements with the tag `title`.
  Content of the element `title` is ordinary string but may contain inline formatting.
- `subjects`. Descriptive keywords for content.
  Data type: an array of one or more child elements with the tag `subject`.
  Content of the element `subject` is string.
  There is no controlled vocabulary.
- `verseForms`. Descriptive keywords for prosodic characteristics.
  Data type: an array of one or more child elements with the tag `verseForm`.
  Content of the element `versePattern` is string.
  There is no controlled vocabulary.
- `versePatterns`. Descriptive keywords for rhyme scheme and other prosodic characteristics, sometimes overlapping with `verseForms`.
  Data type: an array of one or more child elements with the tag `versePatterns`.
  Content of the element `versePattern` is string.
  There is no controlled vocabulary.
- `languages`. Names of languages employed in the item, other than English.
  Data type: an array of one or more child elements with the tag `language`.
  There is no controlled vocabulary.
- `ghosts`. Any bibliographic ghosts, that is, documents which, in prior scholarly tradition, are erroneously claimed to contain a copy of this item.
  Data type: an array of one or more child elements with the tag `ghost`, each of which contains free text with mixed content (recursively mixed where allowed), including inline formatting and references to witnesses, scholarly publications, and other item records.
- `witnesses`. The original witnesses to the item (usually manuscripts, sometimes inscriptions or early printed books).
  Data type: an array of one or more child elements with the tag `witness`.
  See [Attributes of `witness`] and [Child elements of `witness`].

#### Attributes of `witness`

Each `witness` element carries attributes that (1) supply a unique identifier for the witness and (2) indicate whether the witness has accompanying music or illustration.
The attributes are:

- `xml:id`. This is a unique identifier for the witness, assigned by DIMEV editors.
It has three hyphen-delimited components: (1) the invariant string `wit`; (2) the "DIMEV number" for the item (see [Attributes of `record`]); (3) an integer designating this witness.
The unique identifier allows for cross-reference within `Records.xml` and from DIMEV's other XML files.
- `illust`. Report of accompanying illustrations. Values are 'y' (for *yes*) and 'n' (for *no*).
- `music`. Report of accompanying music. Values are 'y' (for *yes*) and 'n' (for *no*).

**Caveat lector**: The final component of DIMEV's unique identifier for a witness may differ from the positional number assigned to that witness on [dimev.net].
The witness numbers printed on the current website are generated anew during each build, as a function of witness order, and can change without notice.
Scholars are advised to reference witnesses by manuscript shelfmarks, not the number assigned to a given witness on DIMEV's current website.

#### Child elements of `witness`

Each `witness` element must have *either* (1) the child element `allLines` *or* (2) one or more sequences of the child elements `firstLines` and `lastLines`.
(These options are exclusive.)
The child element `source` is also obligatory.
All other child elements are optional.

- `allLines`. A full transcription of the item as transmitted in the document.
  Data type: text with inline formatting.
- `firstLines`. A transcription of the first lines of the item as transmitted in the document.
  Data type: text with inline formatting.
- `lastLines`. A transcription of the last lines of the item as transmitted in the document.
  Data type: text with inline formatting.
  The elements `firstLines` and `lastLines` may repeat in alternation.
  This is employed when a witness comprises two or more discontinuous fragments or excerpts of the item.
- `source`. Bibliographic citation for the witness.
  Data type: a complex element containing attributes and child elements.
  See [Attributes of `source`] and [Child elements of `source`].
- `sourceNote`. Notes regarding the witness.
  Data type: free text with mixed content (recursively mixed where allowed), including inline formatting and references to scholarly publications and other witnesses, items, or documents.
- `MSAuthor`. Any author attribution transmitted with the witness.
  Data type: free text with mixed content (recursively mixed where allowed), including inline formatting and references to scholarly publications and other witnesses, items, or documents.
- `MSTitle`. Any title attribution transmitted with the witness.
  Data type: free text with mixed content (recursively mixed where allowed), including inline formatting and references to scholarly publications and other witnesses, items, or documents.
- `facsimiles`. References to published facsimile reproductions of the source document.
  Data type: an array of one or more child elements with the tag `facsimile`.
  Each child element carries an attribute `key`, which links to an item in the [Zotero Group Library].
  The content of `facsimile` is often string but may be mixed.
  **Note**: facsimiles are recorded by DIMEV under individual witnesses, even when the facsimile reproduction is of the entire source document.
- `editions`. References to modern scholarly transcriptions and editions.
  Data type: an array of one or more child elements with the tag `edition`.
  Each child element carries an attribute `key`, which links to an item in the [Zotero Group Library].
  The content of `edition` is often string but may be mixed.
  **Note**: critical editions are recorded by DIMEV under the witness employed as base text.
  This confuses the categories of critical and diplomatic editions.

#### Attributes of `source`

Each `source` element carries two attributes, as follows:

- `key`. This identifies the source document by linking to a unique entry in the XML files `Manuscripts.xml`, `PrintedBooks.xml`, or `Inscriptions.xml`.
- `prefix`: This indicates the unit of navigation (folios, pages, or signatures).

#### Child elements of `source`

Each `source` element may have the following child elements:

- `start`. The location at which the text of the witness begins.
  Data type: optional attributes and string.
- `end`. The location at which the text of the witness ends.
  Data type: optional attributes and string.

The elements `start` and `end` may each carry the attributes `loc`, `col`, and `pre`.
For books with leaf-based navigation systems, the attribute `loc` is employed to record the side of a leaf (recto or verso, abbreviated "r" and "v").
For books with multi-columnar page designs, the attribute `col` is employed to record the column in which the item begins or ends.
Columns are designated by sequential lower-case letters ("a", "b", "c").
The attribute `pre` is used to record irregularities in foliation (or pagination).

Note:

- The `loc` attribute may be omitted when the reference is to the recto of a leaf.
- The element `start` will appear alone if the text of the witness occupies a single side of one leaf.
- The elements `start` and `end` may repeat in alternation to record discontinuous ranges.

### Technical direction {#tech-dir-records}

- Atomize, writing each full `record` element to a separate file within a new sub-directory `records/`, to enable effective use of [git] distributed file history
- Collect partial `record` elements (i.e., those `record` elements serving as cross-references to full `record` elements) in a single separate file, perhaps named `cross-references.xml`
- In the element `author` (child of `authors`), disaggregate name suffixes and query marks indicating dubious attributions
- Allow for critical editions to be attached to the `record` element, rather than only the `witness` sub-element
- Supply controlled vocabularies for the content of `subject`, `verseForm`, `versePattern`, and `language`

## `Manuscripts.xml`

### Overview {#overview-manuscripts}

This XML file stores bibliographic information on medieval manuscripts cited as witnesses in the XML file `Records.xml`.
It also includes some individual copies of early printed books, cited within `Records.xml` for manuscript additions entered into them.
Other such copies are recorded instead within `PrintedBooks.xml`.
See [`PrintedBooks.xml`], below.

Each entry is contained within a uniquely identified `item` element.
`item` elements are serialized as children of the root element `mss`.

### Document structure {#doc-struct-manuscripts}

#### Root element {#root-manuscripts}

- Name: `mss`
- Description: Represents a collection of bibliographic entries for medieval manuscripts (and particular copies of early printed books)
- Content: Contains `item` elements

#### Child elements of `mss`

- Name: `item`
- Description: Represents a single bibliographic entry for a medieval manuscript (or a particular copy of an early printed book)
- Attributes: `xml:id`. The attribute value must be unique. It allows bibliographic entries in `Manuscripts.xml` to be referenced within DIMEV's other XML files.
- Content: Child elements as described in the following section

#### Child elements of `item`

- `loc`: The city or town in which the manuscript is held at present.
  Equivalent to the element `settlement` in @TEIConsortiumTEIP5Guidelines2024, [manuscript description module].
  Data type: Usually string; may contain inline formatting.
- `repos`: The repository in which the manuscript is held at present.
  Equivalent to the elements `institution` and `repository` in the TEI [manuscript description module].
  Data type: Usually string; may contain inline formatting.
- `desc`: The present shelfmark of the manuscript.
  Equivalent to the elements `collection` and `idno` in the TEI [manuscript description module].
  Previous shelfmarks may be supplied after the current shelfmark; these are usually enclosed in square brackets and prefixed with "*olim*".
- `lang`: Localization of the language of the manuscript, with reference to @LaingLinguisticAtlasEarly2013, @BenskinElectronicVersionLinguistic2013, and subsequent scholarship.
  Data type: free text with mixed content (recursively mixed where allowed), including inline formatting, inset elements `langGrid` and `place`, and references to scholarly publications and other manuscript items.
- `surrogates`: URL links to on-line facsimiles of the manuscripts.

### Technical direction {#tech-dir-manuscripts}

- Distinguish manuscripts from (particular copies of) early printed books, perhaps by adding a new attribute `type` to `item` elements
- Atomize, writing each full `item` element to a separate file within a new sub-directory `sources/`, to enable effective use of [git] distributed file history
- Rename and restructure element names to align with guidelines of the TEI [manuscript description module]
- Extract previous shelfmarks to a new element, `altIdentifier`

## `Inscriptions.xml`

### Overview {#overview-inscr}

This XML file stores bibliographic information on inscriptions and other epigraphic texts cited as witnesses in the XML file `Records.xml`.
Each entry is contained within a uniquely identified `item` element.
`item` elements are serialized as children of the root element `inscriptions`.

### Document structure {#doc-struct-insr}

The structure of `Inscriptions.xml` is essentially the same as `Manuscripts.xml`, except `Inscriptions.xml` has no element `lang`.

### Technical direction {#tech-dir-inscr}

- Add an attribute `type` with value "inscription" to `item` elements
- Atomize, writing each full `item` element to a separate file within a new sub-directory `sources/`, to enable effective use of [git] distributed file history

## `PrintedBooks.xml`

### Overview {#overview-printed-books}

This XML file stores bibliographic information on early printed books cited as witnesses in the XML file `Records.xml`.
Each entry is contained within a uniquely identified `bibl` element.
`bibl` elements are serialized as children of the root element `books`.

An identical XML structure is employed to record two types of witness:

1. Printed texts, transmitted in all intact copies of a given edition
2. Manuscript additions to a particular copy

`bibl` elements of the second type are rare (perhaps only eight in all).
More commonly, references to particular copies are recorded within the files `Manuscripts.xml` and `MSSIndex.xml`.
See the [Overview to `Manuscripts.xml`](#overview-manuscripts), above.

### Document structure {#doc-struct-printed-books}

#### Root element {#root-printed-books}

- Name: `books`
- Description: Represents a collection of bibliographic entries for early printed books
- Content: Contains `bibl` elements

#### Child elements of `books`

- Name: `bibl`
- Description: Represents a single bibliographic entry for an early printed book
- Attributes: `xml:id` and `n`.
  The value of `xml:id` must be unique; it allows entries in `PrintedBooks.xml` to be referenced within DIMEV's other XML files.
  The attribute `n` usually gives the corresponding item number in @PollardShorttitleCatalogueBooks1950, where available.
  For non-English books and other items not recorded in the STC, the value of `n` is often a dummy string ("X").
  Sometimes another value is used.
- Content: Child elements `loc`, `DIMEVCount`, `authorstmt`, `titlestmt`, `pubstmt`, `repos`, and `desc`, as described in the following section

#### Child elements of `bibl`

- `DIMEVCount`. A count of DIMEV items transmitted by the item.
  Data type: string.
- `authorstmt`. Parent of the element `author`, which may contain an author attribution.
  Data type of `author`: string.
- `titlestmt`. Parent of the element `title`, which contains the item title.
  Data type of `title`: attribute and string.
  The `title` element carries the attribute `level`, the value of which is always "m" (for "monograph").
- `pubstmt`. Agent, date, and location of printing, as given in the volume or as reconstructed.
  The element `pubstmt` carries a required attribute `date`, which gives the year of publication (Gregorian calendar, Common Era).
  Data type: attribute and string.
- `repos`. Usually empty, except when the `bibl` element points to a particular copy, in which case the `repos` element gives the holding institution of the cited copy.
- `desc`. Content varies, depending on the reference of the `bibl` element.
  When the `bibl` element points to an edition, the `desc` element usually repeats and concatenates the content of `authorstmt`, `title`, and `pubstmt`;
  when the `bibl` element points to a particular copy, the `desc` element gives the shelfmark of the copy, sometimes in combination with the cataloging metadata usually given for editions.
  Data type: free text with mixed content.

### Technical direction {#tech-dir-printed-books}

- Distinguish between references to copies and editions
- Extract the references to particular copies: re-serialize these to conform to the data structure employed for references to manuscripts, and move to the new directory `sources/`
- For references to editions: implement a standard data structure for XML serialization of bibliographic metadata for early printed books
- Disaggregate references to @PollardShorttitleCatalogueBooks1950 from other content of the attribute `n`
- Supply references to the English Short Title Catalog (ESTC) where available.

## `Glossary.xml`

### Overview {#overview-glossary}

This XML file stores lexicographic information for certain words recorded in transcriptions.
Each entry is contained within a uniquely identified `item` element.
`item` elements are serialized as children of the root element `glossary`.

### Document structure {#doc-struct-glossary}

#### Root element {#root-glossary}

- Name: `glossary`
- Description: Represents a collection of entries for lexical items
- Content: Contains `item` elements

#### Child elements of `glossary`

- Name: `item`
- Description: Represents a single lexical item
- Attributes: `xml:id`. The value must be unique; it allows items in `Glossary.xml` to be referenced within `Records.xml`.
- Content: Contains the elements `lemma`, `source`, `partOfSpeech`, and `def`.

#### Child elements of `item`

- `lemma`. The lemma or headword under which the word is recorded by the source referenced in `source`.
  Data type: string.
- `source`. The source of the definition recorded in `def`.
  Data type: parent of `ref` and `biblio` elements (only one may appear).
  See below.
- `partOfSpeech`. The part of speech of the word.
  Data type: usually string; may contain inline formatting.
- `def`. The definition of the word, sometimes with additional lexicograhic information drawn from the source identified in the element `source`.
  Data type: often string; may contain inline formatting.

#### Child elements of `source`

- `ref`. Bibliographic reference to a dictionary.
  Each `ref` element carries the attributes `type` and `n`.
  The value of `type` is always "url"; `n` gives the base URL of the on-line edition of the dictionary cited.
  The content of the `ref` element gives the abbreviated title of the dictionary cited (usually "OED" or "MED").
  Data type: attribute and string.
- `biblio`. Bibliographic reference to a non-dictionary source.
  Each `biblio` element carries the attribute `key`, which corresponds to the citation key of an item in the [Zotero Group Library].
  The content of the `biblio` element gives the point-locator, usually a page reference.
  Data type: attribute and string.

### Technical direction {#tech-dir-glossary}

To be determined.
If this file and its data are retained:

- Restructure the element `item` to allow for citation of multiple sources:
  the elements `lemma`, `partOfSpeech`, and `def` should be moved under `source`, as its children; `source` should be repeatable
- Restructure references to dictionaries; reference *OED* and *MED* entries by URI
- Make `id`s more robust

# History and responsibility

DIMEV incorporates and extends a bibliographic tradition whose principal earlier efforts are @BrownRegisterMiddleEnglish1916, @BrownIndexMiddleEnglish1943, @RobbinsSupplementIndexMiddle1965, @HamerManuscriptIndexIndex1995, and @BoffeyNewIndexMiddle2005, and it shares a point of origin with the last of these.
In 1993 Julia Boffey, A. S. G. Edwards, and Linne R. Mooney obtained funding to produce an updated index of Middle English verse, which would combine @BrownIndexMiddleEnglish1943 and @RobbinsSupplementIndexMiddle1965, correct error, and record materials that had come to light in the previous thirty years.
In the first year of collaboration the team divided; DIMEV subsequently emerged as a distinct venture, distinguished in three respects from prior efforts in its tradition:

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

# Licensing

DIMEV source data, this documentation, and other contents of the repository that contains them are released under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

# Works Cited
