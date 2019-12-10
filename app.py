import classroom
import drive
from classroom import parse_courses, get_id
from drive import download_from_drive


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='only if you know what you\'re doing')
    # parser.add_argument('')

    ids_df, selection = parse_courses()

    materials_df, materials_selection = get_id(ids_df, selection)

    download_from_drive(materials_df, materials_selection)
