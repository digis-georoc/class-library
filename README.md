# GEOROC's classification library
*A geochemical classification diagram library for SQL databases written natively in PostgreSQL using PostGIS.*

*By M. K. Traun and L. Alfke*

## The library content
What is the library and what is in it.
### Class_library schema

### Citing the library
Cite our work!

Cite the original diagram references included in the citation table. 

There the references are also available in RIS format for easy format conversion through reference managers (e.g. Zotero).

## Installing the library
### *Important Requirements!*
The classification library uses the PostGIS extension to make the geometries for the diagrams and the classification functions (which uses geometric intercepts).
The library assumes PostGIS is already installed, if not most Postgres installations come with the PostGIS extention, and it can be activated using this SQL command within a Postgres database:
```
CREATE EXTENSION postgis;
```
The classification library was first written under Postgres version 18.1 and PostGIS version 3.6.0.

### From the SQL dump

#### Restore the dump

#### Create indexes

### From the class-library extension
Coming soon...

## Using the library
### Classification of samples demo
Jupyter notebook

### Adding diagrams demo
Jupyter notebook

## References
- Our poster presentation at GeoMinBochum 2026.
- Our paper when sublished
- Geoplotters.com
- GEOROC precomplied file Aleutian Arc
- Postgres
- PostGIS

### BibTeX reference format
```
hello world
```

### RIS reference format
```
hello world
```
