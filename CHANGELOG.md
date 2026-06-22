# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

#### Files added

- `data/Bibliography.rdf`: RDF backup of DIMEV's Zotero Group Library (#23; 31aaf5e4bfb0421381662d4e507713b366fd199d et seq.)
- `data/form-terms.xml`, `data/language-terms.xml`, and `data/subject-terms.xml`: XML files to control vocabularies for verse forms, languages, and subjects (f88d584f889a9aac6aaf8afaeb6c1361e2056a71..139e1c85173c6a9dcfed7f6e7c8677f3546cc4fd)
- `schemas/terms.xsd`: XML Schema to validate `data/form-terms.xml`, `data/language-terms.xml`, and `data/subject-terms.xml` (f88d584f889a9aac6aaf8afaeb6c1361e2056a71 et seq.)
- `schemas/xml.xsd`: local copy of the canonical W3C schema for the XML namespace, so xmllint can resolve `xml:id` and compile the schemas (7faf2d9a4ddb4d790892f1c98a9ff416861f9ea5)
- `schemas/common.xsd`: shared phrase-level and cross-reference types for `manuscripts.xsd` and `inscriptions.xsd`, factored out of the two (previously duplicated verbatim) and included by each via `xs:include` (e941379f39567361ca7dbc161d4a5f54fa0d4c0c)
- `scripts/formatter.py`: Python script to pretty-print XML files with four-space indentation (9214e65479f174ecfe512e8c3175f046a1d093ea..b6234398b60502a231b9bab28346a09939ea4be2)
- `CHANGELOG.md`: This change log

#### Content added to all XML files

- Add processing instructions to associate XML files with schemas (139e1c85173c6a9dcfed7f6e7c8677f3546cc4fd, 14345568f9052090677b5920cbbc41e4701240f9)

#### `Manuscripts.xml`: content added

- Add some Summary Catalog numbers for Bodleian manuscripts (9cd87c72a67f74527ffde809044f9a96fec098ab)
- Add links to on-line facsimiles and catalogue records (#22, #36, #64; c23bebc9fb82c0768974db518b46fb9fd792c7b7, 4442a79aeb71c83e19765d44a2aad755806c6c41, d0375f7a18513db0379a2845d3bf022fc1ce5fb7)

#### `PrintedBooks.xml`: content added

- Add entries for printed books cited in `Records.xml` but previously unrecorded in `PrintedBooks.xml` (STC 17325, 17326, 22595, 22596); de-comment 4853 (#40; 82f0e80768bc4d6edd2acac91d3d79b69e754be2)
- Add STC numbers to items that lack them, where available (08cf30f52f3f6fda112c9337d87f10444681dc81, 7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)
- Add ESTC numbers where available (7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)
- Add an ISTC number for an item not in ESTC (7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)

#### `Records.xml`: content added

- Add references to the Bibliography of the Middle English Compendium as repertory (#31; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- Add "post-1500" as subject term (#34; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- Restore DIMEV 2204 (formerly commented out) (#51; 14345568f9052090677b5920cbbc41e4701240f9)

#### Validation: functions added

- Validate unique identifiers (`xml:id` and bibliographic citation keys) for uniqueness and well-formedness (#9, #33; 4d7de46398019a4788a129340a24f2f22661a3f3, af6d0739c10f458d3156175bb8309154a74d1bf3, 09be893ce6f940c6ccf3bb9ce64f6bb0fe888e66)
- Validate key references in `Records.xml` against the sets of unique identifiers of text-carriers (manuscripts, early printed books, and inscriptions) and modern scholarly works (#33, #39, #40; ee36fb2e3a9ed656fd3bddd837b6cdbb072dacf4, 91801c136d2c0c94bcd5840b3a8da5c19af7b988)
- Validate cross-references in `Records.xml` against `xml:id`s in `Records.xml` (#48; 3d22a3bebfb45586df92ba22c3a81eac31b1eed2, 43c7ddde4d231b3f01b98cddbb9edfa6d9ae5fe4, 702525a60500a6de7795e571cb1a0dc8bda4cab4)
- Validate subjects, verse-forms, and languages against controlled vocabularies (#53; e17f3f9a566bc3e1d94d9d5e14b350da919f0acc, 14345568f9052090677b5920cbbc41e4701240f9)

#### README

- Add instructions for contributors; add Zenodo DOI badge (9ad3e6a246d0eedf4981d19ec479292a5809c3b0)

#### `Documentation.md`

- Add a section "Current Status" (907e3d224bb3d91fc3ade10c0018945ba3a7844b)
- Add a section "Pointing and citation conventions" and align the `bibl`, `mss`, and `ptr` tag-library entries with it (#65; b3e2b2ecc0f33e021f3151294a69a350bdb1da46)
- Add a tag library for each XML file (afa58ca9d21d87ada2cd836e9ca506f71abeeaea et seq.)
- Add guidance on styling of content in `Manuscripts.xml` (852d25a2e44403c8ee983bc47bb7535ec50bfd65)

### Changed

#### Changes affecting multiple XML files

- Replace numeric character entity references with Unicode; replace curly possessive apostrophes and single and double quotes with the corresponding non-directional characters (#1; 33b4b1f2637ebec794e7f39fd96b16f4bcd7a014)
- Pretty-print and re-lineate all XML and XSD files (c0ea1006b5bf4ff1ad53493c11bd9914d5a444c0, 939b3568a29bcc3e7074fa31dca7154b0cec3fc7)
- Reduce xml:id values to ASCII (08cf30f52f3f6fda112c9337d87f10444681dc81, 72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Move records of full-manuscript on-line facsimiles from `Bibliography.xml` to `Manuscripts.xml` (#22, c23bebc9fb82c0768974db518b46fb9fd792c7b7)
- Rationalize citation and cross-reference markup toward TEI P5 Chapter 17, "Linking, Segmentation, and Alignment": retire `ref` in favour of TEI `ptr` for all empty pointers, with internal targets recoded as `#`-fragments (`#` + an `xml:id`) and external targets as absolute URIs; retain `bibl`/`source`/`mss` `key` citations; and disambiguate the resource sense of `bibl` (a `ptr`-wrapper, without `key`, in `surrogates` and `listBibl`) (#65; b3e2b2ecc0f33e021f3151294a69a350bdb1da46)
- Re-home textcarrier items: records of particular copies of printed books, cited for manuscript additions or binding fragments, go to `Manuscripts.xml` (from `PrintedBooks.xml`); a copy of a printed book cited for edition-level material (key: `BodArchGe35`) goes to `PrintedBooks.xml` (from `Manuscripts.xml`); a parchment broadsheet (key: `Barber`) goes to `Manuscripts.xml` (from `Inscriptions.xml`) (#11, #59; 08cf30f52f3f6fda112c9337d87f10444681dc81, 7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6, db7127fa0bf75a8bc6485586c75d5becf858a978)

#### `Manuscripts.xml`

- Establish `Manuscripts.xml` as the project's single source of truth for manuscripts materials (#11, #21; 574cf0b3c0faacb0242b10b9b35c3bc99767c2a9, 08cf30f52f3f6fda112c9337d87f10444681dc81)
- Restructure as TEI `listBibl` and `msDesc`; declare the TEI namespace (#36; 5c9dd0a059024eb5a9a30c785e826ac14b3a1175, 23fd37db6d9b5d8ec4c8e0907c8c6bd1bd420a11, 4442a79aeb71c83e19765d44a2aad755806c6c41, 852d25a2e44403c8ee983bc47bb7535ec50bfd65, 63f489983ba5d913bd4e65d9a8b6f5fba6662936). Conformance is not complete, however: `lang` elements and some administrative and editorial notes remain non-TEI.
- Set a required attribute `type` to identify each record as manuscript or printed (95b5d6cb40ca2b08e3d27a8d5f1d9def593a8b03)
- Add `country`; regularize `settlement` and `repository` names per the issue #36 style guide (#36; 4442a79aeb71c83e19765d44a2aad755806c6c41, 852d25a2e44403c8ee983bc47bb7535ec50bfd65)
- Regularize Bodleian shelfmarks to catalogue form (941ac6ab3e6fec163891c4de49f9ffcebfdd8745)
- Regularize recording of items in private collections, items untraced, and items on deposit (852d25a2e44403c8ee983bc47bb7535ec50bfd65)
- Remove the abbreviation "MS" from most shelfmarks (852d25a2e44403c8ee983bc47bb7535ec50bfd65)
- Rename the element `biblio` as `bibl` (5c9dd0a059024eb5a9a30c785e826ac14b3a1175)
- Change repository "Public Record Office" to "The National Archives" (#32; 9cd87c72a67f74527ffde809044f9a96fec098ab)
- Update details for Longleat manuscripts purchased by the British Library (#18; 9cd87c72a67f74527ffde809044f9a96fec098ab)
- "CollArms316" and "BLAshb27": update location, repository and shelfmark details (574cf0b3c0faacb0242b10b9b35c3bc99767c2a9)

#### `Inscriptions.xml`

- Restructure as TEI `listBibl` and `msDesc`; declare the TEI namespace (#63; 9d68a24d45dd1c9b86af09d29cd2d5f2cc243f1a, 62b732db5d62c40199ae8f2c715722ae86690d92)
- Strip final punctuation and in-line italics from text content (2882d3205bf044a5039952c3748008e322d326d3)

#### `PrintedBooks.xml`

- Restructure as TEI `listBibl` and `biblStruct`; declare the TEI namespace; the file is now valid against TEI P5 (9238790fc29f12d7af93939362db50b0cb800746, 9bfa34205ad3819cc1efeaa3c2d65efc6b6e178d)
- Replace date, title, and printer/publisher name(s) with corresponding ESTC data, downloaded June 2026; for title, use the ESTC uniform title in most cases where that field is available (7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)
- Replace the attribute `n` with the element `idno` (9238790fc29f12d7af93939362db50b0cb800746, 9bfa34205ad3819cc1efeaa3c2d65efc6b6e178d)

#### `Records.xml`

- Cite IMEV, NIMEV, and Ringler in a new element `repertories`; this element also holds references to Whiting's *Proverbs, sentences*, Walther's *Proverbia* and *Initia*, and other repertories (#25, #46; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9, 6da0898ac11bdf940c45161781ecf810cd64357f, 90911075eadbe57068ca460f128b107fd80fd3de)
- Cite critical editions at record level (limited implementation) (#3; 90911075eadbe57068ca460f128b107fd80fd3de)
- Restructure lists of bibliographic references (editions, facsimiles, ghosts) (90911075eadbe57068ca460f128b107fd80fd3de)
- Restructure lists of keywords (subjects, verse-forms, languages) (72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Restructure `ref` elements and their content (#24, #48; 8e48f84731cfac8d8efc079693b7c344e9b0c260, 6da0898ac11bdf940c45161781ecf810cd64357f)
- Convert the values of attributes "music" and "illust" to booleans (14345568f9052090677b5920cbbc41e4701240f9)
- Rename the element `biblio` as `bibl` (90911075eadbe57068ca460f128b107fd80fd3de)
- Rename the element `insc` as `mss` for in-project consistency (90911075eadbe57068ca460f128b107fd80fd3de)
- Change DIMEV item number 7684 to 5784; retain the mistaken identifier as a cross-reference (#20; b9aa6fe5c60591a435063c22e9e16b8195d49c55)
- Revise subject terms (#29, #30, #34; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- Combine verse-form terms and verse-pattern terms and revise (#42, #44; 72e56e266e712a26e7fc05d63e7160c495ab9e22)
- DIMEV 3993: update author name (#3; 90911075eadbe57068ca460f128b107fd80fd3de)
- "Body and soul" poems: revise cross-references, subject terms, repertories (#2; 8e48f84731cfac8d8efc079693b7c344e9b0c260)

#### `validator.py`

- Read schema paths from XML processing instructions (139e1c85173c6a9dcfed7f6e7c8677f3546cc4fd)
- Use `pathlib` for cross-platform compatibility (8bf11f0c6ea9162255f5482a6aeb1bb1083f7c5e)
- Declare dependencies using TOML to accommodate `uv run` (b6234398b60502a231b9bab28346a09939ea4be2)
- Validate all XML files, unless a file path is specified as an argument (491c8ecd1f49accb2873946a0062e08ae1f009fc, 0bba2694d445432cbbb1af01bf98d8e9011b40fa, 8bf11f0c6ea9162255f5482a6aeb1bb1083f7c5e)
- Resolve `ptr` targets in `Records.xml`: check internal `#`-fragment targets against the `xml:id` registry and skip absolute URIs, replacing the transitional Middle English Compendium special-case (#65; b3e2b2ecc0f33e021f3151294a69a350bdb1da46)
- Use the Python `logging` module for output and derive the run's pass/fail status from logged errors, replacing the success flag and error counters threaded through every check; adopt `argparse` for the optional single-file argument (c979466269c9133cd8c1ab73612b550eb0047484)
- Extend the key and `ptr`-target checks to the text-carrier files (`Manuscripts.xml`, `Inscriptions.xml`, `PrintedBooks.xml`) in addition to `Records.xml`, so `bibl`/`source`/`mss` keys and internal pointer targets are validated wherever they occur; internal `ptr` targets continue to resolve against the record and witness `xml:id`s only (#65; a259a04fd68444ccbe2701c71f4ee5dc5f2db8c7)

#### Schemas

- All schemas: give the XML-namespace `import` a `schemaLocation` pointing at the local `schemas/xml.xsd`, so xmllint can compile them for structural validation (7faf2d9a4ddb4d790892f1c98a9ff416861f9ea5)
- All schemas: tighten, restructure, and align with changes to XML file structures; add some inline documentation
- `printedbooks.xsd`: rewrite as a restricted profile of TEI `listBibl` and `biblStruct` (9bfa34205ad3819cc1efeaa3c2d65efc6b6e178d)
- `manuscripts.xsd`: provide for the disaggregated `msIdentifier`, `head`, `history`, and `additional` content model (#36; 4442a79aeb71c83e19765d44a2aad755806c6c41, 63f489983ba5d913bd4e65d9a8b6f5fba6662936); make `msDesc/@type` required and restrict it to the controlled vocabulary {`manuscript`, `printed`} (e941379f39567361ca7dbc161d4a5f54fa0d4c0c)
- `inscriptions.xsd`: rewrite on model of rewritten `manuscripts.xsd` (#63; 9d68a24d45dd1c9b86af09d29cd2d5f2cc243f1a, 62b732db5d62c40199ae8f2c715722ae86690d92)
- `manuscripts.xsd`, `inscriptions.xsd`: factor the verbatim-shared phrase-level and cross-reference types into `common.xsd`, included by both via `xs:include` (e941379f39567361ca7dbc161d4a5f54fa0d4c0c)
- `records.xsd`, `common.xsd`: define an empty `ptr` pointer type and retire `ref`; require internal `ptr` targets to be `#`-fragments; provide for the `ptr`-wrapper (resource) sense of `bibl` (#65; b3e2b2ecc0f33e021f3151294a69a350bdb1da46)
- `records.xsd`: provide for `crossRefs` block (not yet implemented in `Records.xml`) (c28f6af4a0962a5c41552352eafc787c21cec453)

#### Documentation

- Restructure `documentation.md` (cf8ed5a1773c2dcfc94d219a91b2442d7fd5b9af)
- Export `items.yaml` from Zotero 9 (9966eadd82fdc9179c0db8eca51afd3cf8073dbf)

### Removed

#### Files removed

- `Bibliography.xml`: remove file after porting data to Zotero (#23; 9823c245fd555f04034511170ef45b8f85c0d226)
- `Glossary.xml`: remove file as out of scope (#26; f992ee06e77519737a8f03e6220a3021fb0ca0e2)
- `MSSIndex.xml`: remove file after merging data into `Manuscripts.xml` (#21; 574cf0b3c0faacb0242b10b9b35c3bc99767c2a9)
- `mssindex.xsd`, `bibliography.xsd`, and `glossary.xsd`: remove schemas for removed XML files (5e25a7fa47fdace713bf7d613633ddcca855459f, 96bbe0745a4cdf4cdfc912b712601815163c2807, f992ee06e77519737a8f03e6220a3021fb0ca0e2)

#### Content removed from multiple items

- `Manuscripts.xml`, `PrintedBooks.xml`, `Inscriptions.xml`: remove duplicate items; remove items uncited elsewhere in project files
(#38, #50;
ac05c4db8693427507936153ac62af1b79473409,
0aa70f77d77e098295e6388dc8d9832377b89ac9,
08cf30f52f3f6fda112c9337d87f10444681dc81,
5a66c4570a659429799c90b16574453f0d5c2b24,
7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6,
db7127fa0bf75a8bc6485586c75d5becf858a978)
- Delete certain manuscript items cited only as bibliographic ghosts or else within `description` or `sourceNote` elements. Several are photographic facsimiles or post-medieval transcriptions. For each, replace the citation pointer with a keyboarded shelfmark and delete the item record from `Manuscripts.xml`. (General principle: maintain records only for text-carriers cited as witnesses to text-items, not for those merely *mentioned* elsewhere within records.) \(db7127fa0bf75a8bc6485586c75d5becf858a978)

#### `Manuscripts.xml`: items and elements removed

- Resolve and delete certain XML comments: delete commented-out items with xml:ids unreferenced elsewhere in DIMEV data; delete commented-out items with xml:ids identical to an active item elsewhere in `Manuscrips.xml` (9cd87c72a67f74527ffde809044f9a96fec098ab).
(All remaining XML comments are dropped within re-structuring at db7127fa0bf75a8bc6485586c75d5becf858a978.)

#### `PrintedBooks.xml`: items and elements removed

- Remove the elements `loc`, `repos`, and `DIMEVCount` (#11; dd623751f8888ce3ffd35665d9a90e621ff602ca, 08cf30f52f3f6fda112c9337d87f10444681dc81, bfb14aa4c8e8b01151e2b198f6c958f9a3ffd11d)
- Remove the element `desc`; information unique to `desc` (printer names for STC 78 and STC 79, former STC numbers, a remark on the survival of copies) is retained in `publisher` text and in a new element, `note` for further curation (9238790fc29f12d7af93939362db50b0cb800746, 9bfa34205ad3819cc1efeaa3c2d65efc6b6e178d)
- Remove item Rouen1516 as an edition-level record cited by us for copy-level material; the copy is recorded in `Manuscripts.xml` as YorkMinXIO28 (7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)

#### `Records.xml`: elements, items, and content removed

- Remove blocks of commented-out witnesses and records; remove XML comments of the type "new number" (git history is project history) \(db7127fa0bf75a8bc6485586c75d5becf858a978, 8e48f84731cfac8d8efc079693b7c344e9b0c260, b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- Remove `gloss` tags as out of scope (#26; dcf295f8e7a037da6f13ecde3656a8890156a003)
- Remove references to full-manuscript digital on-line facsimiles (these are recorded within the corresponding item in `Manuscripts.xml`) (#39; dcf295f8e7a037da6f13ecde3656a8890156a003)
- Remove the element `versePatterns` after merging content into `verseForms` (#42; 72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Remove empty `subjects` elements (72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Remove an unnumbered stub item as redundant with item 1293 (8e48f84731cfac8d8efc079693b7c344e9b0c260)
- Remove references to HuntingtonRB59135, StPaulBuxtaforius1616, Alliaco1480 (when referencing early printed books, reference either edition or copy, as appropriate, not both) (90911075eadbe57068ca460f128b107fd80fd3de)
- Remove broken web links: partial digitization of Woodward1995; query on http://search.lib.cam.ac.uk/; TCC James catalog (90911075eadbe57068ca460f128b107fd80fd3de)
- Remove the dummy record for cross-reference of 'yif' and 'if' (6da0898ac11bdf940c45161781ecf810cd64357f)
- 5850: remove a bad reference to an edition (#49; 8e48f84731cfac8d8efc079693b7c344e9b0c260)

#### Documentation

- Remove notes on "technical direction" for XML files (0840d3e6d53ca61c30f441d81a0ee91f498e3000)

### Fixed

#### All XML files

- Fix validation errors exposed by updated schema files

#### Bibliography

- `Bibliography.xml`: regularize and correct form and content prior to migration (77342d4ab7ebc86fea8ad50ffb0170a97d27d287..9823c245fd555f04034511170ef45b8f85c0d226)
- De-duplicate (#35; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)

#### `Manuscripts.xml`

- PierpontAcc10360: correct the call number (7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)
- Misc. content correction (4442a79aeb71c83e19765d44a2aad755806c6c41)

#### `Inscriptions.xml`

- Misc. content correction (62b732db5d62c40199ae8f2c715722ae86690d92)

#### `PrintedBooks.xml`

- Correct the STC numbers of items with xml:id STC12142, STC24267, STC5759a, STC15999, STC5086, STC127667 (#57; 5a66c4570a659429799c90b16574453f0d5c2b24, 7c30b0b5829d66d1cd52d28eaaca1df8ea9d17f6)

#### `Records.xml`

- Fix validation errors in `xml:id` values (#9; b9aa6fe5c60591a435063c22e9e16b8195d49c55, dcf295f8e7a037da6f13ecde3656a8890156a003)
- Fix validation errors in reported NIMEV and IMEV numbers (#25; b9aa6fe5c60591a435063c22e9e16b8195d49c55, b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- Fix validation errors in `ref` elements (#48; 8e48f84731cfac8d8efc079693b7c344e9b0c260)
- Fix key errors in bibliographic references to text-carriers (manuscripts, printed books, inscriptions) and modern scholarly works (editions, facsimiles) (#39, #40; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9, dcf295f8e7a037da6f13ecde3656a8890156a003, 6da0898ac11bdf940c45161781ecf810cd64357f, 72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Move subject terms misplaced as verse-forms and vice versa; move verse-forms misplaced as language terms (#30, #42; 72e56e266e712a26e7fc05d63e7160c495ab9e22, b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9, 14345568f9052090677b5920cbbc41e4701240f9)
- 3171: Harley 1706 is not a ghost; add the manuscript as witness (#27; 14345568f9052090677b5920cbbc41e4701240f9)
- 5029: correct extent, range, lastlines (#5; 14345568f9052090677b5920cbbc41e4701240f9)
- 5143: move subjects misplaced in the `titles` element (72e56e266e712a26e7fc05d63e7160c495ab9e22)
- Misc. content correction

#### `validator.py`

- Fix a reference to an undefined variable that raised `NameError` instead of reporting the duplicate when a duplicate `xml:id` was found (c979466269c9133cd8c1ab73612b550eb0047484)
- Fix a no-op comparison that let `xml:id`s duplicated across the record, text-carrier, and citation-key registries pass validation (c979466269c9133cd8c1ab73612b550eb0047484)

## Version 1 [2025-01-01]

Initial release.
Development of this version begins with XML files received from Dan Mosser on 2024-12-18 (6e640a9b716c39890b61fcf7c5b46b60b9941c5c).
Files are released essentially as received, except as recorded under the sections Changed, Removed, and Fixed, below.

### Added

#### Data

- Add XML files `Bibliography.xml`, `Glossary.xml`, `Inscriptions.xml`, `MSSIndex.xml`, `Manuscripts.xml`, `PrintedBooks.xml`, and `Records.xml` in the directory `data`

#### Validation

- Add XML Schema files `bibliography.xsd`, `glossary.xsd`, `inscriptions.xsd`, `manuscripts.xsd`, `mssindex.xsd`, `printedbooks.xsd`, and `records.xsd` in the directory `schemas`
- Add `scripts/validator.py` to validate XML files against schemas

#### Documentation

- Add a project README
- Add Markdown file `docs/documentation.md` as technical introduction to DIMEV data
- Add YAML file `docs/bibliography/items.yaml` to supply bibliographical details for items cited in `documentation.md`
- Add Bash script `docs/build.sh` to build `documentation.pdf` from plain text components
- Add YAML file `docs/config/default.yaml` to supply default metadata for Pandoc
- Add YAML file `.github/workflows/action.yaml` to build `documentation.pdf` with GitHub Actions
- Add `LICENSE` as project license (24aaf24934756ac78d7cceaba78e4ecf4d45af77)

### Changed

- Validation: Replace DTDs with XML Schema files
- Update some citation keys for modern scholarly works (9faf37d9846e3148ac6bcf4421eb0b4271573deb, 8902e5473fd49e3c2088fa466af86f207c32bedd, 2bee12d36ce5dabef74549a17644dd2450e8fa94)

### Removed

- Remove old Document Type Definitions from XML files (these are replaced by XML Schema files) (3a9757cc599430af3f78e659d983fb5146d8daf5, 9faf37d9846e3148ac6bcf4421eb0b4271573deb, 9faf37d9846e3148ac6bcf4421eb0b4271573deb)
- `Bibliography.xml`: remove some unreferenced commented-out items (9faf37d9846e3148ac6bcf4421eb0b4271573deb)
- `Records.xml`: remove some empty elements (2bee12d36ce5dabef74549a17644dd2450e8fa94)

### Fixed

- All XML files: fix validation errors and begin regularization of XML structure and idiom (`Records.xml`: 2bee12d36ce5dabef74549a17644dd2450e8fa94, `Bibliography.xml`: 9faf37d9846e3148ac6bcf4421eb0b4271573deb, other XML files: 3a9757cc599430af3f78e659d983fb5146d8daf5)
- Begin clean-up of the bibliography (9faf37d9846e3148ac6bcf4421eb0b4271573deb, 8902e5473fd49e3c2088fa466af86f207c32bedd)
