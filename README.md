# uniprot-ac-assign

Script for assigning UniProt ACs to entry or entries in a flatfile

1. We have a list of available ACs (AC_list).
2. When a curator needs an AC they send us their flatfile which can contain more than one entry.
3. The script retrieves the latest AC (at the top of the AC list), assigns it to the first ID/entry in the flatfile, and then removes that AC from the AC list.
4. Then it moves to the next ID in the flatfile and repeats 3.
5. When it's finished reading the flatfile it writes all the data to a data file, and the output in the AC datafile looks like this:

```
Date,  Accession,  ID,  User,  Curator name and purpose
7/6/2023 C0HM92 CO1AB_EPIAE kwarner for Kate's sub work
7/6/2023 C0HM93 CO1AA_EPICA kwarner for Kate's sub work
8/6/2023 C0HM94 CO1A2_DROME kwarner for Kate's sub work
9/6/2023 C0HM95 CO1AB_HUMAN kwarner for Kate's sub work
```

Once the script has been run I would expect:

1. The flatfile to be exactly the same (no change)
2. The ACs that have been assigned to be removed from the AC list
3. The AC datafile to be appended with the information on the latest assignment (the output above).

# TODO

- [ ] update README for new users
- [x] finalize directory structure

```
F:\ACNumbers
  available_acs.txt          # Accession to be assigned
  assigned_acs.txt           # Accessions already assigned with info
  ac_backup/
    available_acs(1).txt
    assigned_acs(1).txt
```

- [x] create another function to revert to latest in archive
- [x] create installation/update script
- [x] test revert.py
- [x] test install.py
- [ ] create nicer user feedback on assertion failures
- [ ] inform user when there are less than 10 accessions in ac_list
- [ ] add docstrings
- [ ] add explicit file encodings
- [ ] move repo to ebi
