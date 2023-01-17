"""
A script that identifies all adult (18 years or older) participants with a
'positive' (virus detected) result dated within the past 30 days, and reports
out their age, most recent test result, and most recent test date.

Example call:

python positive_adults.py participants.json results.json

"""
import argparse
import pandas as pd
import sys

from datetime import datetime as date
from dateutil.relativedelta import relativedelta as rdelta


def process_participants(participant_file: str) -> pd.DataFrame:
    ''' Read and subset participants data from JSON file

    Args:
        participants_file (str):
            The path of a JSON file from which to load the participants data
            from

    Returns:
        (pd.DataFrame):
            New participants dataframe
    '''
    # Make sure input file exits
    try:
        df = (
            pd.read_json(
                participant_file, convert_dates=['birthdate'], orient='records'
            )
        )
    except ValueError:
        print(f"File {participant_file} not found.")
        sys.exit(0)

    # Calculate age
    df['age'] = [rdelta(date.today(), dob).years for dob in df['birthdate']]

    # Subset to adults
    df = df[df['age'] >= 18]

    return df


def process_results(results_file: str) -> pd.DataFrame:
    '''Read participant results data from JSON file

    Args:
        results_file (str):
            The path of a JSON file from which to load results data from

    Returns:
        (pd.DataFrame):
            New results dataframe
    '''

    # Make sure input file exits
    try:
        df = (
            pd.read_json(
                results_file, convert_dates=['date'], orient='records'
            )
        )
    except ValueError:
        print(f"File {results_file} not found.")
        sys.exit(0)

    # Identify how many days since date of test result
    df['days_since_result'] = [(date.today() - d).days for d in df['date']]

    return df


def identify_positives(
    participants: pd.DataFrame, results: pd.DataFrame
) -> None:
    ''' Outputs information about those who tested positive in the last 30 days

    Args:
        participants (pd.DataFrame):
            Dataframe of the participants information
        results (pd.DataFrame):
            Dataframe of the results data

    '''
    # Match participants to their test results
    full_df = pd.merge(
        participants, results, on="participant"
    ).sort_values(by=['date'])

    last_30_days = full_df[full_df.days_since_result <= 30]

    participant_list = list(
        last_30_days[last_30_days.result == "positive"].participant
    )

    for p in sorted(participant_list):
        # Isolate the last entry for given participant
        ind = last_30_days[last_30_days.participant == p].iloc[-1:]

        # Output participant info to screen
        print(
            f"participant {p}, "
            f"age {ind.age.values[0]}, "
            f"result {ind.result.values[0]}, "
            f"date {ind.date.dt.strftime('%Y-%m-%d').values[0]}"
        )


def main(participant_file: str, results_file: str) -> None:
    ''' Output participants information based on recent results

    Args:
        participant_file (str):
            The path of a JSON file from which to load the participants
            data from
        results_file (str):
            The path of a JSON file from which to load the nasal swab test
            results data from
    '''
    # Pre-process participants data
    participants = process_participants(participant_file)

    # Pre-process test results data
    results = process_results(results_file)

    # Print most recent information for select participants
    identify_positives(participants, results)


if __name__ == "__main__":

    # Read in command line arguments
    participant_file = str(sys.argv[1])
    results_file = str(sys.argv[2])

    main(participant_file, results_file)
