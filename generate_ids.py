"""A script that 1) updates an input file by appending a new set of randomly
generated identifiers, and 2) prints only the new identifiers to
the output.

Example call:

python generate_ids.py \
    --identifier-set-file identifier_set.json \
    --new-identifiers-quantity 5

"""
import argparse
import pandas as pd
import random
import re
import sys


def read_json_file(identifier_set_file: str) -> pd.DataFrame:
    ''' Read list of identifiers from JSON file

    Args:
        identifier_set_file (str):
            The path of a JSON file from which to load the existing identifier
            set

    Returns:
        (pd.DataFrame):
            Given set of identifiers dataframe
    '''
    dtypes = {'barcode': 'str'}

    # Make sure input file exits
    try:
        identifier_set = (
            pd.read_json(identifier_set_file, dtype=dtypes, orient='records')
        )
    except ValueError:
        print(f"File {identifier_set_file} not found.")
        sys.exit(0)

    return identifier_set


def create_new_set(identifier_set: str, new_quantity: int) -> pd.DataFrame:
    ''' Creates new randomized set of barcode identifiers

    Args:
        identifier_set_file (str):
            The path of a JSON file from which to load the existing identifier
            set
        new_quantity (int):
            The number of new identifiers to be generated

    Returns:
        (pd.DataFrame):
            New identifiers in json format

    '''
    # Create randomized list
    new_set = []
    while len(new_set) < new_quantity:
        new_identifier = (
            "".join([f"{random.randint(0, 9)}" for num in range(7)]) + "g"
        )
        # Check if randomly generated identifier is already in existing set
        if new_identifier not in (set(identifier_set.barcode) & set(new_set)):
            new_set.append(new_identifier)
        else:
            continue

    # Output new identifiers to console
    print(" ".join(new_set))

    # Update data into the correct format
    new_df = pd.DataFrame(new_set, columns=['barcode'])

    return new_df


def output_json_file(idenifier_file: str, full_set: pd.DataFrame) -> None:
    '''Output all identifiers to JSON file

    Args:
        identifier_file (str):
            The path of a JSON file for which to write out the new set
        full_set (pd.DataFrame):
            The combined set of new and old identifiers

    '''
    # Transform dataframe of identifiers to json string
    out = '[\n\t{' + full_set.to_json(orient='records')[2:]

    # Reformatting spacing between brackets
    to_replace = {'},{': '},\n\t{', '}]': '}\n]'}

    for char in to_replace.keys():
        out = re.sub(char, to_replace[char], out)

    # Writing out full set to same input file path
    with open(idenifier_file, 'w') as f:
        f.write(out)


def main(identifier_set_file: str, new_identifiers_quantity: int) -> None:
    ''' Generate new ids and then output all ids to a JSON file

    Args:
        identifier_set_file (str):
            The path of a JSON file from which to load the existing identifier
            set
        new_identifiers_quantity (int):
            A positive integer quantity of new identifiers to to generate
    '''

    # Read in new identifiers list
    identifier_set = read_json_file(identifier_set_file)

    new_set = create_new_set(identifier_set, new_identifiers_quantity)

    # Combine existing and new identifiers into one set
    full_set = identifier_set.append(new_set)

    # Reformat and output full set
    output_json_file(identifier_set_file, full_set)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--identifier-set-file",
        type=str,
        required=True,
        help=(
            "The path of a JSON file from which to load the existing "
            "identifier set."
        )
    )
    parser.add_argument(
        "--new-identifiers-quantity",
        type=int,
        required=True,
        help=("A positive integer quantity of new identifiers to generate.")
    )

    args = parser.parse_args()

    main(args.identifier_set_file, args.new_identifiers_quantity)
