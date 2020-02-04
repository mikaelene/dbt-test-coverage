import glob
import yaml
import os


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


def parse_models(schema):
    if not schema.get("models"):
        return None, None
    # Create list of models and test status
    test_status = []
    for model in schema["models"]:
        model_name = model["name"]
        model_test = False
        if "'tests':" in str(model):
            model_test = True
        # print(f"Model name: {model_name}, tested: {model_test}" )
        test_status.append([model_name, model_test])

    # Calculate aggregated test status
    statuses = 0
    tested = 0
    for status in test_status:
        statuses += 1
        if status[1]:
            tested += 1

    test_status_agg = [statuses, tested, round(tested / statuses * 100)]

    return test_status, test_status_agg


def parse_schema(schema):

    try:
        source_results, source_results_agg = parse_sources(schema)
        if source_results:
            for source_result in source_results:
                print(
                    f"Source: {source_result[0]}, Database: {source_result[1]}, Schema: {source_result[2]}, "
                    f"Table: {source_result[3]}, Model name: {source_result[4]}, Tested: {source_result[5]}"
                )
            print(" ")
            print(
                f"Sources: {source_results_agg[0]}, Tested: {str(source_results_agg[1])}, "
                f"Coverage: {source_results_agg[2]}%"
            )
    except:
        print("Failed to parse sources")

    try:
        model_results, model_results_agg = parse_models(schema)
        if model_results:
            for model_result in model_results:
                print(f"Model: {model_result[0]}, Tested: {model_result[1]}")
            print(" ")
            print(
                f"Models: {model_results_agg[0]}, Tested: {str(model_results_agg[1])}, "
                f"Coverage: {model_results_agg[2]}%"
            )
    except:
        print("Failed to parse models")

    print("\n")


def test_coverage(path, recursive=True):
    if recursive:
        schema_path = f"{path}/**\*.yml"
    else:
        schema_path = f"{path}\*.yml"

    ymls = glob.glob(schema_path, recursive=recursive)

    if not ymls:
        print(f"No schema files found in: {path}")
        return

    for yml in ymls:
        print(yml)
        schema = load_schema_yml(yml)
        parse_schema(schema)
