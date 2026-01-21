# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `Bibliography.rdf`: add this file as a backup of DIMEV's Zotero library (#23; 31aaf5e4bfb0421381662d4e507713b366fd199d)
- `Manuscripts.xml`: add links to on-line facsimiles (#22; c23bebc9fb82c0768974db518b46fb9fd792c7b7)
- `Manuscripts.xml`: supply missing Bodleian SC numbers (9cd87c72a67f74527ffde809044f9a96fec098ab)
- `Records.xml`: add references to the Bibliography of the Middle English Compendium as repertory (#31; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- `README.md`: add instructions for contributors (9ad3e6a246d0eedf4981d19ec479292a5809c3b0)
- validation: check xml-ids and bibliographic citation keys for uniqueness and well-formedness (#9, #33; 4d7de46398019a4788a129340a24f2f22661a3f3, af6d0739c10f458d3156175bb8309154a74d1bf3)
- validation: check that key references in `Records.xml` point to a recorded textcarrier (manuscript, early printed book, or inscription) or modern scholarly work (#33; ee36fb2e3a9ed656fd3bddd837b6cdbb072dacf4, 91801c136d2c0c94bcd5840b3a8da5c19af7b988)
- style: add `formatter.py` to pretty-print and lineate XML files, with four-space indentation (9214e65479f174ecfe512e8c3175f046a1d093ea)

### Changed

- data files: pretty-print and re-lineate (c0ea1006b5bf4ff1ad53493c11bd9914d5a444c0)
- data files: replace numeric character entity references with Unicode (33b4b1f2637ebec794e7f39fd96b16f4bcd7a014)
- data files: replace curly possessive apostrophes and single and double quotes with the corresponding non-directional characters (33b4b1f2637ebec794e7f39fd96b16f4bcd7a014)
- `Manuscripts.xml`: establish this file as the single source of truth for manuscript details (#21; 574cf0b3c0faacb0242b10b9b35c3bc99767c2a9)
- `Manuscripts.xml`: update location, repository and shelfmark details for items with keys "CollArms316" and "BLAshb27" (574cf0b3c0faacb0242b10b9b35c3bc99767c2a9)
- `Manuscripts.xml`: update repository "Public Record Office" => "The National Archives"; update details for Longleat manuscripts purchased by the British Library (#32, #18; 9cd87c72a67f74527ffde809044f9a96fec098ab)
- `Records.xml`: change DIMEV item number 7684 to 5784; retain the mistaken id as a cross-reference (#20; b9aa6fe5c60591a435063c22e9e16b8195d49c55)
- `Records.xml`: revise subject keywords (#29, #30, #34; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- `Records.xml`: move IMEV, NIMEV, and Ringler numbers from item attributes (and free text) to a new block `repertories`; move Whiting 1968 and Walther refs from free text to the `repertories` block (#25; b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- documentation: update documentation to reflect changes to project data (b6fd92de9af2471d3368f010176003d1d4b97baa)
- validation: rewrite `validator.py` to validate all XML files, unless a file path is specified as an argument (491c8ecd1f49accb2873946a0062e08ae1f009fc, 0bba2694d445432cbbb1af01bf98d8e9011b40fa)
- validation(`manuscripts.xsd`): require string content in the elements `loc` and `desc` (5e25a7fa47fdace713bf7d613633ddcca855459f); add element `surrogates` (05ab06bd42e7ec256614fdd475548a83d728140e)
- validation('records.xsd): update to reflect changes to `Records.xml` data structure (b7aefff35e8048c8c0f8695036845568166281d3)

### Removed

- `Bibliography.xml`: remove the file after porting data to Zotero (9823c245fd555f04034511170ef45b8f85c0d226)
- `MSSIndex.xml`: remove the file after merging data into `Manuscripts.xml` (#21; 574cf0b3c0faacb0242b10b9b35c3bc99767c2a9)
- `Manuscripts.xml`: remove the item with key "Atkinson" (ac05c4db8693427507936153ac62af1b79473409)
- `Manuscripts.xml`: resolve and delete XML comments where possible; delete commented-out items with xml:ids unreferenced elsewhere in DIMEV data; delete commented-out items with xml:ids identical to an active item recorded elsewhere in this file (9cd87c72a67f74527ffde809044f9a96fec098ab)
- `PrintedBooks.xml`: remove the element `loc`; update schema and documentation (dd623751f8888ce3ffd35665d9a90e621ff602ca)
- `PrintedBooks.xml`: remove the item with key "ParisSydrac1486" (0aa70f77d77e098295e6388dc8d9832377b89ac9)
- `Records.xml`: remove XML comments of the type "new number" (b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- validation: remove `mssindex.xsd` and `bibliography.xsd` (5e25a7fa47fdace713bf7d613633ddcca855459f, 96bbe0745a4cdf4cdfc912b712601815163c2807)

### Fixed

- Bibliography: numerous corrections (77342d4ab7ebc86fea8ad50ffb0170a97d27d287, d04177d0491ec927289e1749833c89ea33d3dac2, 3e5983a88a5e337a60315eb2ff23c734fe2d4c07, 1ba3f2dc06317d8ac55241b18a382af31ada710d, 109a00e13188377f09c1e4ca409333a8cd9846a7, 8533b58e343ffb90f2d22699a25acfa4a3e334c5, 9823c245fd555f04034511170ef45b8f85c0d226)
- `Records.xml`: correct validation errors in xml:ids (#9; b9aa6fe5c60591a435063c22e9e16b8195d49c55)
- `Records.xml`: correct validation errors in reported NIMEV and IMEV numbers (#25; b9aa6fe5c60591a435063c22e9e16b8195d49c55, b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
- `Records.xml`: repair invalid and duplicate key references (b2e4df2b3c2b9a6aa6ebdfee6f5b36ceb44049f9)
