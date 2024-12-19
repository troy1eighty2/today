import sqlite3
import datetime
from datetime import date
import argparse


def createDatabase():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT NOT NULL,
            date TEXT NOT NULL,
            status INTEGER
        )
    """)
    conn.commit()
    conn.close()


def parseInput():
    parser = argparse.ArgumentParser()

    parser.add_argument('habit', type=str,
                        help='the str habit you are logging')
    parser.add_argument('status', type=int,
                        help='1 for complete, 0 for incomplete')

    args = parser.parse_args()
    return args


def submission(args):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habits (habit, date, status) 
        VALUES (args.habit, , args.status)
    """)
    conn.commit()
    conn.close()


def displayMap():
    green_square = "\033[32m■\033[0m"  # Green square
    black_square = "\033[30m■\033[0m"  # Black square


def main():
    # createDatabase()
    # displayMap()
    args = parseInput()
    date = datetime.datetime.today()
    print(date)


if __name__ == "__main__":
    main()
