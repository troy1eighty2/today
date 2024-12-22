#!/usr/bin/env python3
import dotenv
import sqlite3
import datetime
from datetime import date
import argparse
import getpass


dotenv.load_dotenv()


def createDatabase():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            habit TEXT PRIMARY KEY NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit TEXT NOT NULL,
            date TEXT NOT NULL,
            status INTEGER,
            FOREIGN KEY (habit) REFERENCES habits(habit)
                ON DELETE CASCADE
                ON UPDATE CASCADE
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
        conn.close()
        return
    else:
        if int(arguments[1]) not in [0, 1]:
            print("not a valid status. input 1 for true, 0 for false.")
            conn.close()
            return
        else:
            todays_date = datetime.datetime.today()

            date_object = f"{
                todays_date.year}-{todays_date.month}-{todays_date.day}"
            cursor.execute("""
                SELECT habit, date
                FROM log
                WHERE habit = ? AND date = ?
            """, (arguments[0], date_object))
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute("""
                    INSERT INTO log (habit, date, status)
                    VALUES (?,?,?)
                """, (arguments[0], date_object, int(arguments[1])))
            else:
                cursor.execute("""
                    UPDATE log
                    SET status = ?
                    WHERE habit = ? AND date = ?
                """, (int(arguments[1]), arguments[0], date_object))

    conn.commit()
    conn.close()


def view(arguments):
    green_square = "\033[32m■\033[0m"  # Green square
    black_square = "\033[30m■\033[0m"  # Black square

    # DASHBOARD
    current_hour = datetime.datetime.now().hour
    print("")
    if current_hour <= 12:
        print("Good morning", end="")
    elif current_hour <= 19:
        print("Good afternoon", end="")
    else:
        print("Good evening", end="")
    print(f", {getpass.getuser()}.")
    print("")

    print(f"The date is ")
    print("")
    print(f"The high for today is and the low is")
    print("")

    # if no arguments, then there are no more tasks
    # if there are some tasks left, inform that there are more tasks

    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()

    if not arguments:
        cursor.execute("""
            SELECT *
            FROM log
            ORDER BY habit ASC, date DESC
        """)

        result = cursor.fetchall()
        print(result)

    else:
        pass
        # # print by year month date
        #
        # if len(arguments) == 3:
        # elif len(arguments) == 2:
        # else:


def main():
    createDatabase()
    args = parseInput()


if __name__ == "__main__":
    main()
