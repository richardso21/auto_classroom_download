import argparse
import pandas as pd
import classroom
import drive
from classroom import parse_courses, get_id
from drive import download_from_drive


if __name__ == '__main__':

    ids_df, selection = parse_courses()
    materials_df, materials_selection = get_id(ids_df, selection)
    download_from_drive(materials_df, materials_selection)
