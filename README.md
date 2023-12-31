# uniprot-ac-assign

---

## Description

**Python script for assigning available UniProt ACs to entry or entries in a flatfile.**

Accession numbers are assigned manually for the following:

- submissions
- new entries from published sequences
- entries created from `NOT_ANNOTATED_CDS`
- demerged entries

### How the script works

1. We have a list of available ACs (`available_acs.txt`).
2. When a curator needs an AC they send us their flatfile which can contain more than one entry.
3. The script retrieves the latest AC (at the top of the available_acs list), assigns it to the first ID/entry in the flatfile, and then removes that AC from available_acs.
4. Then it moves to the next ID in the flatfile and repeats 3.
5. When it's finished reading the flatfile it writes all the data (Date, assigned accession/s, ID/s, User, Curator name and purpose) to the bottom of the `assigned_acs.txt`. The output in assigned_acs should look like this:

```
7/6/2023 C0HM92 CO1AB_EPIAE kwarner for ylussi's sub work
7/6/2023 C0HM93 CO1AA_EPICA ylussi for Kate's sub work
8/6/2023 C0HM94 CO1A2_DROME kwarner for Kate's curation work
9/6/2023 C0HM95 CO1AB_HUMAN ebowler for Kate's curation work
```

6. The script then prints the assigned ACs and their IDs within the Command prompt window, so that you can copy them and send them to the curator that needs them
7. Each time the script is run, it backs up the last five versions of the available_acs and assigned_acs files into a folder (`F:\ACNumbers\ac_backup`) in case something happens to the latest files in the `F:\ACNumbers` folder.

## How to use

Make sure you have the latest version of Python 3 installed on your machine. You can download Python from the Microsoft store or via the [Python Website](https://www.python.org/downloads/).

### Where are the necessary files kept?

The script and all the AC files are in the `F:\ACNumbers` folder.
For the script to work, the script and AC files (`available_acs.txt` and `assigned_acs.txt`) must be in this folder - DO NOT MOVE THEM - if you have to move them you will have to edit the script.

In contrast, the location of the flatfile that requires the new AC/s, can be anywhere in your directory.

ACNumbers directory structure:
```
F:\ACNumbers
ac_assign.py # The python script for assigning ACs.
available_acs.txt # Available accessions to be assigned (was called uniprot_acc.lost).
assigned_acs.txt # Info on accessions that have already been assigned (was called ASSIGNEDACS.TXT).
ac_backup/ # Folder containing a backup of the last 5 versions of the acs files
 available_acs(1).txt # File backup versions with the highest number being the latest version
 assigned_acs(1).txt
revert.py # This script allows you to revert the available_acs and assigned_acs in the main folder, to   one of the versions in the backup folder
old_script/ # Folder containing the old script written in Perl and old ac files
```

### How to assign accession numbers - using the ac_assign.py script

1. Open a Command prompt window (`Windows Key + R`, then type `cmd`) or open py.command.
2. Type in the following: `python` followed by the path to the script, the location of the flatfile that needs a new AC (this can be anywhere on your drive), and add a comment about the curator needing the AC and why they need it. For example:

```
python F:\ACNumbers\ac_assign.py -f C:\Users\kwarner\flatfile.sp -c "For Kate's sub work"
```

3. The script reads the flatfile and determines the number of entries (i.e. IDs) that require new ACs. It then removes the number of ACs it needs from the available_acs file and adds the assignment info to the bottom of the assigned_acs file. It also prints the assigned ACs and their IDs within the Command prompt window, so that you can copy them and send them to the curator that needs them. It also tells you how many ACs are remaining in the available_acs file.

### How to revert the ac files to earlier versions in the backup folder - using the revert.py script

Each time the `ac_assign.py` is run it sends a copy of the updated available_acs and assigned_acs files to the backup folder in the ACnumbers folder. We keep the last five backups or versions in the backup folder with the highest number being the latest version. 

If something happens to the ac files in the main folder, you can revert to one of the earlier versions in the backup folder using `revert.py` 

1. Open a Command prompt window (`Windows Key + R`, then type `cmd`) or open py.command.
2. Type in the following: `python` followed by the path to the script:

```
python F:\ACNumbers\revert.py
```
3. The script will give you some information about the different versions in the backup folder and then ask you to select which version you would like to revert to. Enter the number of the version and the ac files in the main folder should be automatically replaced by this version. 
---

