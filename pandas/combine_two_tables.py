import pandas as pd


def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    combined = person.merge(address, on='personId', how='left')
    columns = ['firstName', 'lastName', 'city', 'state']
    combined = combined[columns]
    return combined


if __name__ == '__main__':
    person = pd.read_csv('data/person.csv')
    address = pd.read_csv('data/address.csv')

    combined = combine_two_tables(person, address)
    print(combined)
