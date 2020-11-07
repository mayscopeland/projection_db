import pandas as pd
import os
import glob
import re
from enum import Enum


class StatType(Enum):
    BATTING = 1
    PITCHING = 2


def main():

    batting_cols = [
        "system",
        "year",
        "mlbam_id",
        "G",
        "AB",
        "R",
        "H",
        "2B",
        "3B",
        "HR",
        "RBI",
        "SB",
        "CS",
        "BB",
        "SO",
        "IBB",
        "HBP",
        "SH",
        "SF",
        "GIDP",
    ]

    pitching_cols = [
        "system",
        "year",
        "mlbam_id",
        "W",
        "L",
        "G",
        "GS",
        "CG",
        "SHO",
        "SV",
        "IP",
        "H",
        "ER",
        "HR",
        "BB",
        "SO",
        "IBB",
        "WP",
        "HBP",
        "BK",
        "R",
        "SH",
        "SF",
        "GIDP",
        "QS",
        "HLD",
    ]

    batting_projections = pd.DataFrame()
    pitching_projections = pd.DataFrame()

    for filepath in glob.glob(os.path.dirname(__file__) + "\\input\\*"):

        filename = os.path.basename(filepath)
        year = find_filename_year(filename)
        system = find_filename_system(filename)
        stat_type = find_filename_type(filename)

        print(filepath)

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
            # print(df.head())

        elif filepath.find(".xls") > -1:
            df = pd.read_excel(filepath)
            # print(df.head())

        if year is not None:
            df["year"] = year
        
        if system is not None:
            df["system"] = system

        if stat_type == StatType.BATTING:
            df.columns = change_column_names(batting_cols, list(df))

            print(df.head())

            df2 = df.filter(items=batting_cols).round()
            batting_projections = batting_projections.append(df2)
            print(df2.head())

        if stat_type == StatType.PITCHING:
            df.columns = change_column_names(pitching_cols, list(df))

            print(df.head())

            df2 = df.filter(items=pitching_cols).round()
            pitching_projections = pitching_projections.append(df2)
            print(df2.head())
    
    batting_projections.to_csv(os.path.dirname(__file__) + "\\batting_projections.csv", index=False)
    pitching_projections.to_csv(os.path.dirname(__file__) + "\\pitching_projections.csv", index=False)


def change_column_names(stats, columns):
    for stat in stats:
        found = False
        match = stat.lower()
        match = match.replace("_id", "")
        match = match.replace("_", "")

        # First look for an (almost) exact match
        for index, col_name in enumerate(columns):

            col = col_name.strip()

            # For Marcel, every stat is prefixed with "m"
            col = col.lstrip("m")

            col = col.lower()

            if col == match:
                columns[index] = stat
                found = True

        # For strikeouts, let's try "K" instead of "SO"
        if not found:
            for index, col_name in enumerate(columns):
                if stat == "SO" and col_name == "K":
                    columns[index] = stat
                    found = True

        # Otherwise, see if there's a partial match anywhere in the column heading
        if not found:
            # If we didn't find an exact match for G or R, don't try a fuzzy match. It will match too many things.
            if stat != "G" and stat != "R":
                for index, col_name in enumerate(columns):
                    col = col_name.lower().strip()
                    if col.find(match) > -1:
                        columns[index] = stat

    return columns


def find_filename_type(filename):

    filename = filename.lower().replace(" ", "")

    if (filename.find("hitt") > -1) or (filename.find("batt") > -1):
        return StatType.BATTING
    elif filename.find("pitch") > -1:
        return StatType.PITCHING
    else:
        return None


def find_filename_year(filename):

    # Search the filename for four digits between 1000 and 2999.
    match = re.search("[1-2][0-9]{3}", filename)

    if match is not None:
        return match.group()
    else:
        return None


def find_filename_system(filename):

    filename = filename.lower().replace(" ", "")

    system_names = [
        "ATC",
        "The BAT",
        "The BAT X",
        "CAIRO",
        "CHONE",
        "Fans",
        "Marcel",
        "Oliver",
        "PECOTA",
        "Steamer Razzball",
        "Steamer",
        "ZiPS",
    ]

    for system_name in system_names:
        match = system_name.lower().replace(" ", "")

        if filename.find(match) > -1:
            return system_name


if __name__ == "__main__":
    main()
