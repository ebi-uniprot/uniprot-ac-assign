# uniprot-ac-assign
Script for assigning UniProt ACs to entry or entries in a flatfile
1. We have a list of available ACs (AC_list).
2. When a curator needs an AC they send us their flatfile which can contain more than one entry.
3. The script retrieves the latest AC (at the top of the AC list), assigns it to the first ID/entry in the flatfile, and then removes that AC from the AC list.
4. Then it moves to the next ID in the flatfile and repeats 3.
5. When it's finished reading the flatfile it writes all the data to a data file, and the output in the AC datafile looks like this:
7/6/2023 C0HM92 CO1AB_EPIAE kwarner for Kate's sub work
7/6/2023 C0HM93 CO1AA_EPICA kwarner for Kate's sub work
7/6/2023 C0HM94 CO1A2_EPICA kwarner for Kate's sub work
7/6/2023 C0HM95 CO1AB_EPICA kwarner for Kate's sub work
