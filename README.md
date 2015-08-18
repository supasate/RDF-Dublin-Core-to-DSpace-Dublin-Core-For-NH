# RDF Dublin Core to DSpace Dublin Core Converter
A simple commmand line tool that converts RDF Dublin Core to DSpace Dublin Core Simple Archive Format.

---

## Usage
```
python rdfdc2dspace.py <filename>
```
*\<filename\>* is a RDF Dublin Core file.
The program will generate the Dspace Dublin Coer Simple Archive Format in the following structure.
```
archive_directory
  |-- item_00001
  |     |-- dublin_core.xml
  |     |-- contents
  |-- item_00002
  |     |-- dublin_core.xml
  |     |-- contents
  |...
```

## Note
Use [MarcEdit with MARC => RDF Dublin Core XSLT](marcedit.reeset.net/downloads) to convert MARC format (.mrc) into RDF Dublin Core first. 
