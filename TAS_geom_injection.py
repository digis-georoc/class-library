# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 09:22:47 2026

@author: larsa
"""

from sqlalchemy import create_engine, URL, text
import pandas as pd
import geopandas as gpd
#from imports import password
import matplotlib.pyplot as plt

password = 'classification_library'


# ENTER BASE DIRECTORY 
base_dir = r"C:\GEOROC\GIS_Classification\TAS"

# ENTER CSV-FILENAME
csv = 'TAS.csv'

# ENTER COLUMN NAMES AS THEY ARE IN CSV
x_column = 'sio2_plutonic'
y_column = 'alkali_plutonic'
plutonic_label = 'plutonic_label'
volcanic_label = 'volcanic_label'

# ENTER TABLE AND SCHEMA NAME
table_name = 'tas' #needs all lower case!
schema_name = 'class_library'



source_table = schema_name + '.' + table_name
target_table = schema_name + '.' + table_name + '_geom'

# Create a connection object to the database
url = URL.create(
    "postgresql+psycopg2",
    username = 'postgres',
    password = password,
    host = 'localhost',
    database="postgres",
)
con = create_engine(url)

#Read csv table
df = pd.read_csv(csv)

#Drop empty columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# Save as new table in database

df.to_sql(name = table_name, schema = "class_library", con = con, index = False, if_exists = "replace")

#Create geometry table

query = f'''
    DROP TABLE IF EXISTS {target_table};                     
                         
    CREATE TABLE {target_table} AS
    WITH  
    points AS (
        SELECT ST_collect(ST_Makepoint({x_column}, {y_column})) as geom, {plutonic_label}, {volcanic_label} FROM {source_table} 
        GROUP BY {plutonic_label}, {volcanic_label}
    ),
    lines AS (
        SELECT ST_Makeline(geom) AS geom, {plutonic_label}, {volcanic_label} FROM points
        GROUP BY {plutonic_label}, {volcanic_label}
    ),
    lines2 AS (
        SELECT ST_AddPoint(geom, ST_StartPoint(geom)) AS geom, {plutonic_label}, {volcanic_label} FROM lines
    )
    SELECT (ST_Dump(ST_Polygonize(geom))).geom AS geom, {plutonic_label}, {volcanic_label} FROM lines2
    GROUP BY {plutonic_label}, {volcanic_label}
'''

with con.connect() as connect:
    connect.execute(text(query))
    connect.commit()
    
idx_query = f'''
                     DROP INDEX IF EXISTS class_library.{table_name}_idx;
                     
                     CREATE INDEX {table_name}_idx
                     ON {target_table}
                     USING GIST(geom)
                     '''

# Add spatial indexes
with con.connect() as connect:
    connect.execute(text(idx_query))
    connect.commit()
    

'''
# Check if adding spatial indexes worked
with con.connect() as connect:
    index_query = """
        SELECT indexname, indexdef 
        FROM pg_indexes 
        WHERE schemaname = 'class_library'
        AND tablename = 'tas_geom';
    """
    
    indexes = pd.read_sql(index_query, connect)
    print("\nAttached Indexes:")
    print(indexes)
'''

geojson_query = f'''
                    SELECT * FROM {target_table}
'''

geojson_geom = gpd.read_postgis(geojson_query, con = con)

filepath = rf'{base_dir}\{table_name}_geom.geojson'

geojson_geom.to_file(filepath, driver="GeoJSON")

#ST_contains, ST_within


#show a basic plot
ax = geojson_geom.plot(column="plutonic_label", figsize= (8,8))
'''
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_aspect('auto')
'''
'''
ax.set_xscale('log')
ax.set_xlim(0.001, 10)
ax.set_aspect('auto')
'''
plt.show()

create_function_query = f'''
    CREATE OR REPLACE FUNCTION {schema_name}.tas_class(p_sio2 float, p_na2o float, p_k2o float, p_volcanic boolean DEFAULT TRUE) RETURNS text
    AS $$
    DECLARE
        v_result text;

    BEGIN
        WITH
        lookup as (
            SELECT 
                ST_Intersects(ST_Point(p_sio2, p_na2o+p_k2o), geom) as touch, 
                {plutonic_label}, 
                {volcanic_label}
            FROM {target_table}
            ORDER BY ST_YMax(geom) DESC
        )
        SELECT 
            (CASE WHEN p_volcanic = TRUE OR p_volcanic IS NULL THEN {volcanic_label} ELSE {plutonic_label} END) INTO v_result 
        FROM lookup
        WHERE touch = TRUE
        LIMIT 1;

        RETURN v_result;
    END;
    $$ LANGUAGE plpgsql;
'''


with con.connect() as connect:
    connect.execute(text(create_function_query))
    connect.commit()
    
classification_query = f'''
    SELECT class_library.tas_class("SIO2_wtpct", "NA2O_wtpct", "K2O_wtpct", TRUE) 
    FROM class_library.aeolian_example
    LIMIT 100;
'''

aeolian_classified_df = pd.read_sql(classification_query, con=con)