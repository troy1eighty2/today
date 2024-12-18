import sqlite3
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


def argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument()
    pass


def submission():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habits (habit, date, status) 
        VALUES ()
    """)
    conn.commit()
    conn.close()


def displayMap():
    green_square = "\033[32m■\033[0m"  # Green square
    black_square = "\033[30m■\033[0m"  # Black square


def main():
    # createDatabase()
    displayMap()


if __name__ == "__main__":
    main()
