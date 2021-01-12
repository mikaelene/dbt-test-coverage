import glob
import yaml
import os
import colorama
from colorama import Fore, Style

colorama.init()


def load_yaml(stream):
    try:
        return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        # logger.error(exc)
        print(exc)


def load_file_contents(path, strip=True):
    if not os.path.exists(path):
        # logger.error(path + " not found")
        print(path + " not found")
    with open(path, "rb") as handle:
        to_return = handle.read().decode("utf-8")
    if strip:
        to_return = to_return.strip()
    return to_return


def load_schema_yml(path):
    contents = load_file_contents(path)
    yml = load_yaml(contents)
    return yml


def parse_sources(schema):
    if not schema.get("sources"):
        return None, None

    test_status = []
    for source in schema["sources"]:
        source_name = source["name"]
        source_db = source["database"]
        source_schema = source["schema"]
        for table in source["tables"]:
            model_name = table.get("name")
            table_identifier = table.get("identifier")
            table_test = False
            if "'tests':" in str(table):
                table_test = True
            test_status.append(
                [
                    source_name,
                    source_db,
                    source_schema,
                    table_identifier,
                    model_name,
                    table_test,
                ]
            )
    # Calculate aggregated test status
    statuses = 0
    tested = 0
    for status in test_status:
        statuses += 1
        if status[5]:
            tested += 1

    test_status_agg = [statuses, tested, round(tested / statuses * 100)]

    return test_status, test_status_agg


def get_models(schema):
    if not schema.get("models"):
        return None, None
    # Create dict of models and test status
    try:
        models = {}
        for model in schema["models"]:
            name = model["name"]
            if "'tests':" in str(model):
                tested = True
            else:
                tested = False
            models.update({name: tested})
        return models
    except:
        pass


def get_sources(schema):
    try:
        source_results, source_results_agg = parse_sources(schema)
        source_col_width = 20
        model_col_width = 50
        test_col_width = 10
        source_agg_col_width = 77
        sources_agg = 0
        if source_results:
            for source_result in source_results:
                sources_agg += 1
                documented = "True"
                # If yml sources has test
                if source_result[5] == 1:
                    tested = "True"
                    print(
                        f" Source: {source_result[0]: <{source_col_width}}"
                        f" Model: {source_result[4]: <{model_col_width}}"
                        f" Docs: "
                        + Fore.GREEN
                        + f"{documented: <{test_col_width}}"
                        + Style.RESET_ALL
                        + f"Tests: "
                        + Fore.GREEN
                        + f"{tested: <{test_col_width}}"
                        + Style.RESET_ALL
                        + f" Source Table: {source_result[1]}.{source_result[2]}.{source_result[3]: <{model_col_width}}"
                    )
                # If yml sources doesn't have test
                else:
                    tested = "False"
                    print(
                        f" Source: {source_result[0]: <{source_col_width}}"
                        f" Model: {source_result[4]: <{model_col_width}}"
                        f" Docs: "
                        + Fore.GREEN
                        + f"{documented: <{test_col_width}}"
                        + Style.RESET_ALL
                        + f"Tests: "
                        + Fore.RED
                        + f"{tested: <{test_col_width}}"
                        + Style.RESET_ALL
                        + f" Source Table: {source_result[1]}.{source_result[2]}.{source_result[3]: <{model_col_width}}"
                    )
        print(
            f" Sources: {source_results_agg[0]: <{source_agg_col_width}}"
            f" Docs: {(source_results_agg[0])} (100%) "
            f" Tests: {(source_results_agg[1])} ({source_results_agg[2]}%)"
        )
        print(" ")

    except:
        pass


def compare_files(sql_models, yml_models, unique_sql_folders):
    models_agg = 0
    test_agg = 0
    docs_agg = 0
    folder_col_width = 20
    model_col_width = 50
    docs_col_width = 10
    model_agg_col_width = 78
    docs_true = "True"
    docs_false = "False"
    for sql_folder in unique_sql_folders:
        models = 0
        test = 0
        docs = 0
        for sql_s in sql_models:
            item = sql_s[1]
            sql_folders = sql_s[0]
            if sql_folder == sql_folders:
                models_agg += 1
                models += 1
                if item in yml_models:
                    # If yml models exists and has test
                    if yml_models.get(item):
                        tested = "True"
                        test += 1
                        test_agg += 1
                        print(
                            f" Folder: {sql_folder: <{folder_col_width}}"
                            f" Model: {item: <{model_col_width}}"
                            f" Docs: "
                            + Fore.GREEN
                            + f"{docs_true: <{docs_col_width}}"
                            + Style.RESET_ALL
                            + f"Tests: "
                            + Fore.GREEN
                            + f"{tested}"
                            + Style.RESET_ALL
                        )
                    # If yml models exists but doesn't have test
                    else:
                        tested = "False"
                        print(
                            f" Folder: {sql_folder: <{folder_col_width}}"
                            f" Model: {item: <{model_col_width}}"
                            f" Docs: "
                            + Fore.GREEN
                            + f"{docs_true: <{docs_col_width}}"
                            + Style.RESET_ALL
                            + f"Tests: "
                            + Fore.RED
                            + f"{tested}"
                            + Style.RESET_ALL
                        )
                    docs += 1
                    docs_agg += 1

                    # If yml models doesn't exists
                else:
                    if not yml_models.get(item):
                        tested = "False"
                        print(
                            f" Folder: {sql_folder: <{folder_col_width}}"
                            f" Model: {item: <{model_col_width}}"
                            f" Docs: "
                            + Fore.RED
                            + f"{docs_false: <{docs_col_width}}"
                            + Style.RESET_ALL
                            + f"Tests: "
                            + Fore.RED
                            + f"{tested}"
                            + Style.RESET_ALL
                        )
        if models:
            print(
                f" Models: {models: <{model_agg_col_width}}"
                f" Docs: {docs} ({round((docs / models) * 100)}%) "
                f" Tests: {test} ({round((test / models) * 100)}%)"
            )
        else:
            print("No existing models in path")
        print(" ")

    print(f" TOTAL")
    print(
        f" Models: {models_agg: <{model_agg_col_width}}"
        f" Docs: {docs_agg} ({round((docs_agg / models_agg) * 100)}%) "
        f" Tests: {test_agg} ({round((test_agg / models_agg) * 100)}%)"
        f""
    )


def test_coverage(path, recursive=True):
    if recursive:
        schema_path = f"{path}/**/*.yml"
        sql_path = f"{path}/**/*.sql"
    else:
        schema_path = f"{path}/*.yml"
        sql_path = f"{path}/*.sql"

    ymls = glob.glob(schema_path, recursive=recursive)
    ymls = [yml for yml in ymls if os.path.isfile(yml)]

    sqls = glob.glob(sql_path, recursive=recursive)

    # Create a list of all sql files
    sql_models = []
    for sql_file_list in sqls:
        sql_file_folder = os.path.basename(os.path.dirname(sql_file_list))
        sql_files = os.path.basename(sql_file_list)
        sql_models.append([sql_file_folder, sql_files[:-4]])

    sql_folders = []
    for sql_file_list in sqls:
        sql_file_folder = os.path.basename(os.path.dirname(sql_file_list))
        sql_folders.append(sql_file_folder)
        unique_sql_folders = list(set(sql_folders))

    if not ymls:
        print(f"No schema files found in: {path}")
        return

    for yml in ymls:
        schema = load_schema_yml(yml)
        try:
            # Select all yml sources with test details
            get_sources(schema)

        except:
            pass

    yml_models = {}
    for yml in ymls:
        schema = load_schema_yml(yml)

        # Select all yml models with test details
        try:
            yml_model = get_models(schema)
            yml_models = {**yml_models, **yml_model}
        except:
            pass

    try:
        compare_files(sql_models, yml_models, unique_sql_folders)

    except:
        print("Failed to compare files")

