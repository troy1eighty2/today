#!/usr/bin/env python3
import json
import random
import os
import dotenv
import sqlite3
import datetime
import pandas
from datetime import date
import argparse
import getpass


dotenv.load_dotenv()
config_path = os.path.expanduser("~/MyStuff/today/config.json")
with open(config_path, "r") as file:
    config = json.load(file)


def createDatabase():
    conn = sqlite3.connect(os.path.expanduser(config["path_to_db"]))
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

    conn = sqlite3.connect(os.path.expanduser(config["path_to_db"]))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

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
                conn.commit()
            else:
                cursor.execute("""
                    INSERT INTO habits (habit)
                    VALUES (?)
                """, (n,))
                conn.commit()
                date_range = pandas.date_range(
                    start=f"{config["year"]}-01-01", end=f"{config["year"]}-12-31")
                for el in date_range:
                    # print(el.strftime("%A"))
                    day = f"{
                        el.year}-{el.month:02d}-{el.day:02d}"
                    print(day)
                    # sample complete jawn using random values
                    # rando = random.randint(0, 1)
                    # cursor.execute("""
                    #     INSERT INTO log (habit, date, status)
                    #     VALUES (?,?,?)
                    # """, (n, day, rando))
                    # correct execute
                    cursor.execute("""
                        INSERT INTO log (habit, date, status)
                        VALUES (?,?,?)
                    """, (n, day, 0))
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
    conn = sqlite3.connect(os.path.expanduser(config["path_to_db"]))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

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
                todays_date.year}-{todays_date.month:02d}-{todays_date.day:02d}"
            cursor.execute("""
                SELECT habit, date
                FROM log
                WHERE habit = ? AND date = ?
            """, (arguments[0], date_object))
            result = cursor.fetchall()
            print(result)
            if not result:
                print("date doesnt exist")
            else:
                print("perform operation")
                cursor.execute("""
                    UPDATE log
                    SET status = ?
                    WHERE habit = ? AND date = ?
                """, (int(arguments[1]), arguments[0], date_object))
                conn.commit()

    conn.close()


def dashboard():
    # DASHBOARD
    welcome = datetime.datetime.now().strftime(f"Today is %A, %B %-d, %Y. ")
    current_hour = datetime.datetime.now().hour
    current_day = datetime.datetime.now().strftime(f"%Y-%m-%d")

    if current_hour <= 12:
        print("Good morning", end="")
    elif current_hour <= 19:
        print("Good afternoon", end="")
    else:
        print("Good evening", end="")
    print(f", {getpass.getuser()}.")

    days_left = datetime.datetime(
        config["year"] + 1, 1, 1) - datetime.datetime.now()

    print(f"{welcome}There are only {days_left.days} days left in the year.")

    conn = sqlite3.connect(os.path.expanduser(config["path_to_db"]))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
        SELECT *
        FROM habits
    """)

    activities = [row[0] for row in cursor.fetchall()]

    complete = []
    incomplete = []

    if not activities:
        return
    for activity in activities:
        cursor.execute("""
            SELECT status
            FROM log
            WHERE habit = ? AND date = ?
        """, (activity, current_day))
        result = cursor.fetchall()
        if not result:
            incomplete.append(activity)
        else:
            curr = result[0][0]
            if not curr:
                incomplete.append(activity)
            else:
                complete.append(activity)

    if not incomplete and complete:
        print("You're done for the day.")
    else:
        print("Complete: ", end="")
        for n in complete:
            print(f"{n} ", end="")
        print("")
        print("Incomplete: ", end="")
        for n in incomplete:
            print(f"{n} ", end="")
        print("")


def view(arguments):
    green_square = "\033[32m■\033[0m"  # Green square
    # green_square = "🟩"
    gray_square = "\033[90m■\033[0m"  # Gray square
    # gray_square = "⬜"

    dashboard()
    print("")

    conn = sqlite3.connect(os.path.expanduser(config["path_to_db"]))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        SELECT *
        FROM habits
    """)
    activities = [row[0] for row in cursor.fetchall()]
    if not activities:
        print("No activites tracked")
    else:
        print(
            "Jan     Feb     Mar     Apr     May     Jun     Jul     Aug     Sep     Oct     Nov     Dec")
        for activity in activities:
            cursor.execute("""
                SELECT *
                FROM log
                WHERE habit = ?
                ORDER BY date ASC
            """, (activity,))
            print(activity)
            result = cursor.fetchall()
            weeks_of_the_month = group(result)
            for week in weeks_of_the_month:
                previous_month = 1
                spacing = 7
                for day in week:
                    processed_day = datetime.datetime.strptime(
                        day[2], "%Y-%m-%d")
                    months_offset = processed_day.month - previous_month
                    if processed_day.month != previous_month:
                        for j in range(spacing):
                            print(" ", end="")
                        if months_offset > 1:
                            for i in range(months_offset - 1):
                                for j in range(7):
                                    print(" ", end="")
                            print(" ", end="")
                            for i in range(months_offset-2):
                                print(" ", end="")

                        print(" ", end="")
                        previous_month = processed_day.month
                        spacing = 7
                    if day[-1] == 1:
                        print(green_square, end="")
                    else:
                        print(gray_square, end="")
                    spacing -= 1
                print("")


def group(rows):
    # separate into 12 data structures, 1 for each month
    # initialize 4 rows, one for each week of the month
    # for each month of the habit:
    #   for each day of the month:
    #      if day == sunday:
    #       add to week[n]
    #           n ++
    #       else:
    #          add to week[n]

    # aligned indexing for easier access
    months = [[] for i in range(13)]
    weeks_of_the_month = [[] for i in range(6)]
    counter = 0
    for day in rows:
        processed_day = datetime.datetime.strptime(day[2], "%Y-%m-%d")
        months[processed_day.month].append(day)

    for month in months:
        for day in month:
            processed_day = datetime.datetime.strptime(day[2], "%Y-%m-%d")
            if processed_day.strftime("%A") == "Sunday":
                weeks_of_the_month[counter].append(day)
                counter += 1
            else:
                weeks_of_the_month[counter].append(day)
        counter = 0

    return weeks_of_the_month


def main():
    createDatabase()
    parseInput()


if __name__ == "__main__":
    main()
