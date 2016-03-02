NLTK Metadata Creator
===================

The NLTK Metadata Creator (MC) aims to parse plain-text files for self-contained strings of information (e.g., figure captions) and generate metadata from these strings, according to *user-supplied mappings* or, by default, *using the Natural Language Toolkit*[^NLTK] package for Python..

----------

How to Use
-------------
To use MC:

1. Download the repository and unzip the folder. Open the newly unzipped directory.
2. Place in the dependencies folder the file containing the text you would like parsed and name it *Figure Captions.txt*. Replace the mapping files (of the form *\*_type.list.txt*) with your own if desired. **Currently, these files must be the same name as those files listed by default in the dependencies folder.**

[//]: # (TODO: make the script general enough to accept arbitrary names for column headers and create appropriate maps.)
[//]: # (TODO: make a way for users to decide what their 'dividing' sequence is.)

> **Note:**
> Please look through the placeholder files in the dependencies folder before replacing them. They contain instructions and examples as to how your replacement files should be formatted.

3\.  Run autoexec.bat, or manually run *NLTK Metadata Creator.py* using a Python 3.0+ build. The script will output its results in the **outputs** directory, in *Captions Metadata.txt*, in tab-delimited format. To view in an easy-to-read format, open the file in spreadsheet software.


###Qualifications about this Project
- This script was originally created with the field of archaeology in mind. As such, current default files reflect this.
- As the default word mapping is currently sparse and there are no archaeological corpora to mine, the resulting spreadsheet may have a good number of cells empty. We hope to build our default mapping to include more and more common cases in the future. With this in mind, we ask that you help by...

####Contributing to this Project
As there are not annotated corpora of archaeological texts and author styles vary a great deal, one of the best ways to aid this project is to provide the mappings generated for your text, to be merged with the default files -- with the hope that this mapping will encompass more and more terms common in archaeology.

--------
####References

[^NLTK]: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
