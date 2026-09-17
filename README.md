# GEOROC's classification library
*A geochemical classification diagram library for SQL databases written natively in PostgreSQL using PostGIS.*

## The library content
We present an open PostgreSQL geochemical classification library originally built for the GEOROC database (Geochemistry of Rocks of the Oceans and Continents, www.georoc.eu).
Most geochemical diagram-based classification schemes are based on line or polygon geometries outlining the fields. 
Therefore, we use the PostGIS extension which is built for handling geometric (non-projected) and geospatial (with geographical projection) data and functions to make the geometric tables and intersect functions for the classification schemes. 
The classification schemes included was guided by the community resource Geoplotters (Sheldrick, 2026), and also includes the geological provinces of Hasterok et al. (2022). 

### *Class_library* schema
All classification schemes included in our library and their references are contained within a single database schema, called *class_library*.
Each classification scheme is included in three forms: 
1.	Classification scheme coordinates of boundaries as a table including the label of the field those coordinates outline (e.g. table class_library.tas).
2.	The geometric polygon version of the labelled fields, containing the suffix “_geom” in the table name (e.g. table class_library.tas_geom).
3.	The classification scheme SQL function, used to call the classification labels of sample composition within a SQL query (e.g. table class_library.tas_class(…)).

### Citing the library
If using the geochemical citation library, you should cite our work as given here (code and publication):


The references are also provided in BibTeX and RIS (reference information system) format in the reference list below.

Furthermore, you must cite the original diagram references included in the citation table. 
The original references are also available in the *citation_table* in RIS format (*citation_table.ris* column) for easy format conversion through reference managers (e.g. Zotero).

## Installing the library
### *Important Requirements!*
The classification library uses the PostGIS extension to make the geometries for the diagrams and the classification functions (which uses geometric intercepts).
The library assumes PostGIS is already installed, if not most Postgres installations come with the PostGIS extension, and it can be activated using this SQL command within a Postgres database:
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
Retrieving the diagram polygons to plot in the background of a figure can simply be done by calling geom table, for example from the TAS diagram:
```
SELECT * FROM class_library.tas_geom;
```

To classify geochemical samples within the database, call the classification function with the columns from the sample data as input parameters. For example using the Aeolian precompiled dataset (*aeolian_example*) and the *tas_class* function of within the *class_library*:

```
SELECT class_library.tas_class("SIO2_wtpct", "NA2O_wtpct", "K2O_wtpct", TRUE), * FROM class_library.aeolian_example;
```
This will resort in a column with the volcanic TAS diagram labels next to the sample compositions. The input parameters names and types of the *class_library* functions have to match the order in the function definition, as per SQL convention. 
This information is shown in the function overview of the *class_library* schema. For the tas_class, these are: 

```class_library.tas_class(p_sio2 double precision, p_na2o double precision, p_k2o double precision, p_volcanic boolean)``` 

Jupyter and R notebooks coming soon...

### Adding diagrams demo
Jupyter and R notebooks coming soon...

## References
- Our poster presentation from GeoMinBochum 2026.
- Our paper when published
- Sheldrick, T. (2026, August 24). Geoplotters: Geochemical discriminant diagram templates. Rock classification and series diagrams. Geoplotters. https://geoplotters.com/
- DIGIS Team, 2026, " 2025-12-PVFZCE_AEOLIAN_ARC.csv", GEOROC Compilation: Convergent Margins, https://doi.org/10.25625/PVFZCE, Goettingen Research Online / Data, V1. 
- Stonebraker, M., & Rowe, L. A. (1986). The design of POSTGRES. ACM SIGMOD Record, 15(2), 340–355. https://doi.org/10.1145/16856.16888. https://www.postgresql.org
- PostGIS Project Steering Committee and others. (2026). PostGIS, spatial and geographic objects for postgreSQL (Version 3.6.5) [Computer software]. https://postgis.net
- Hasterok, D., Halpin, J. A., Collins, A. S., Hand, M., Kreemer, C., Gard, M. G., & Glorie, S. (2022). New Maps of Global Geological Provinces and Tectonic Plates. Earth-Science Reviews, 231, 104069. https://github.com/dhasterok/global_tectonics 

### BibTeX reference format
```
hello world
```

### RIS reference format
```
hello world
```
