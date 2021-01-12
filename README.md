# dbt-test-coverage
cli tool for showing test coverage in [dbt](https://www.getdbt.com) projects.

Tested with dbt 0.15 and newer!

Install with pip:

    pip install git+https://github.com/mikaelene/dbt-test-coverage.git

 
## Usage
Go to the folder where you have your dbt schema definitions (your yml-files). To search recursive (the folder you are in and all below) type:

    dbt-test-coverage
To only search in the folder you are in:

    dbt-test-coverage --recursive=False

Output for sources will be something like:

    ...
    Source: my_source_system, Database: my_db, Schema: my_schema, Table: my_table, Model name: my_table_model_name, Tested: False
    Source: my_source_system, Database: my_db2, Schema: my_schema2, Table: my_table2, Model name: my_table_model_name2, Tested: True

    Sources: 34, Tested: 1, Coverage: 3%

Output for models will be something like:

    ...
    Model: my_dbt_model, Tested: False
    Model: my_dbt_model2, Tested: True
    
    Models: 6, Tested: 1, Coverage: 17%


## Changelog

### v0.0.1
Initial commit

### v0.0.2
First release

### v0.0.3

#### Fixes:
- Fix error when yml-files are treated as directory.