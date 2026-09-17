# GEOROC's classification library
*A geochemical classification diagram library for SQL databases written natively in PostgreSQL using PostGIS.*

## The library content
What is the library and what is in it.

### *Class_library* schema


### Citing the library
If using the geochemical citation library, you should cite our work as given here (code and publication):


The references are also provided in BibTeX and RIS (reference information system) format in the reference list below.

Furthermore, you should cite the original diagram references included in the citation table. 
The original references are also available in the *citation_table* in RIS format (*citation_table.ris* column) for easy format conversion through reference managers (e.g. Zotero).

## Installing the library
### *Important Requirements!*
The classification library uses the PostGIS extension to make the geometries for the diagrams and the classification functions (which uses geometric intercepts).
The library assumes PostGIS is already installed, if not most Postgres installations come with the PostGIS extention, and it can be activated using this SQL command within a Postgres database:
```
CREATE EXTENSION postgis;
```
The classification library was first written under Postgres version 18.1 and PostGIS version 3.6.0.

### From the SQL dump
To install the classification library, you have to download and then restore the *class_library_dump.sql* file within a postgres database. For example from the pgAdmin 4 GUI, right click on the database, select "Restore..." and navigate to the dump file.

The restore procedure constructs the *class_library* schema within your postgres database, and thus assumes such a schema does not already exist. If it does, you might get an error and we recommend to delete the old schema prior to a restore installation.

Restore creates the tables and functions, but not the geom GIST indexes and label indexes on the tables for the classification functions to run more efficiently.
To create (if not exists) the indexes after a successful restore, run the included procedure through the following SQL command:
```
CALL class_library.create_indexes();
```
The indexes should now be visible under indexes in each table.

### From the class-library extension
Coming soon...

## Using the library
### Classification of samples demo
Retrieving the diagram to plot in the background of a figure can simply be done by calling geom table, for example from the TAS diagram:
```
SELECT * FROM class_library.tas_geom
```

To classify 

Jupyter and R notebooks coming soon...

### Adding diagrams demo
Jupyter and R notebooks coming soon...

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
