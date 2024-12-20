#!/usr/bin/env python3
import sqlite3
import datetime
from datetime import date
import argparse


def createDatabase():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT NOT NULL,
            date TEXT NOT NULL,
            status INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            habit TEXT PRIMARY KEY NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def parseInput():
    parser = argparse.ArgumentParser()

    parser.add_argument('mode', type=str,
                        help='habits or track or view')
    parser.add_argument('add_args', type=str, nargs='*',
                        help='additional arguments')

    args = parser.parse_args()
    if args.mode == "habits":
        habits(args.add_args)
    elif args.mode == "track":
        track(args.add_args)
    elif args.mode == "view":
        view(args.add_args)
    else:
        print("invalid mode. -h for more information")


def habits(arguments):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    if arguments:
        cursor.execute("""
            SELECT habit
            FROM habits
        """)

        # flatten the results
        result = [row[0] for row in cursor.fetchall()]

        for n in arguments:
            if n in result:
                cursor.execute("""
                    DELETE FROM habits
                    WHERE habit = ?
                """, (n,))
            else:
                cursor.execute("""
                    INSERT INTO habits (habit)
                    VALUES (?)
                """, (n,))

    conn.commit()
    cursor.execute("""
        SELECT habit
        FROM habits
    """)
    result = [row[0] for row in cursor.fetchall()]

    print("Habits Being Tracked: ", end="")
    for n in result:
        print(f"{n} ", end="")
    print("")

    conn.close()


def track(arguments):
    if not arguments or len(arguments) != 2:
        print("provide proper number of arguments. refer to README or -h for help")
        return
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit
        FROM habits
    """)

    result = [row[0] for row in cursor.fetchall()]

    if arguments[0] not in result:
        print("habit does not exist. input a valid habit.")
        return
    else:
        print("processing")

    conn.commit()
    conn.close()


def view():
    pass


def submission(args):
    todays_date = datetime.datetime.today()
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO log (habit, date, status)
        VALUES (args.habit, todays_date, args.status)
    """)
    conn.commit()
    conn.close()


def displayMap():
    green_square = "\033[32m■\033[0m"  # Green square
    black_square = "\033[30m■\033[0m"  # Black square


def editChoices():
    pass


def main():
    createDatabase()
    args = parseInput()

    # args = parseInput()
    # todays_date = datetime.datetime.today()
    # date_object = datetime.date(
    #     todays_date.year, todays_date.month, todays_date.day)


if __name__ == "__main__":
    main()
