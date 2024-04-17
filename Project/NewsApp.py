import os
import NLP
import re
import mysql.connector as ms

import NLP

conn = ms.connect(
    host='localhost',
    user='root',
    password='m7yt5^9wZy^L',
    db='app1')
if conn.is_connected():
    print("Connected")
else:
    print("Not connected")


def create_table():
    curs = conn.cursor()
    query = '''Create table data
    (
    ID        INT AUTO_INCREMENT PRIMARY KEY,
    Title     varchar(255),
    TopImage    varchar(255),
    Content   TEXT,
    Date      DATE,
    Genre     TEXT,
    Location  varchar(255))'''
    curs.execute(query)
    print("Table created")
    conn.commit()
    curs.close()
    return


# create_table()


def enter_data(Title, TopImage, content, Date, Genre, Location):
    curs = conn.cursor()
    query = '''insert into data(Title,TopImage,content,Date,Genre,Location) values('%s','%s','%s','%s','%s','%s')''' % (
    Title, TopImage, content, Date, Genre, Location)
    curs.execute(query)
    conn.commit()
    curs.close()


# enter_data()


def genre_data(genre):
    curs = conn.cursor()
    curs.execute("Select * from data where Genre='%s'" % genre)
    record = curs.fetchall()
    for row in record:
        print("Title", row[1])
        print("TopImage", row[2])
        print("Content", row[3])
        print("Date", row[4])
        print("Genre", row[5])
        print("Location", row[6])


def location_data(location):
    curs = conn.cursor()
    curs.execute("Select ID,Title,TopImage from data ")
    record = curs.fetchall()
    for row in record:
        print("Title: \t\t", row[0])
        print("TopImage: \t\t", row[1])
    return record


def id_data(id):
    curs = conn.cursor()
    curs.execute("Select Title,TopImage,Content,Date,Genre,Location from data where ID='%s'" % id)
    record = curs.fetchall()
    for row in record:
        print("Title: \t\t", row[0])
        print("TopImage: \t\t", row[1])
        print("Content: \t\t", row[2])
        print("Date: \t\t", row[3])
        print("Genre: \t\t", row[4])
        print("Location: \t\t", row[5])
    return [row[0],row[2]]


def dfs_folder(directory):
    # Stack to store directories
    stack = [directory]

    while stack:
        current_dir = stack.pop()

        entries = os.listdir(current_dir)

        for entry in entries:
            full_path = os.path.join(current_dir, entry)

            if os.path.isdir(full_path):
                stack.append(full_path)
            return full_path


def get_date(file_path):
    # Regular expression pattern to match dates and times
    datetime_pattern = r'\b\d{4}:\d{2}:\d{2}\b'
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the file content
        content = file.read()
        # Find all matches of the pattern
        match = re.search(datetime_pattern, content)
        if match:
            return match.group(0)
        else:
            return None


def get_txt():
    data = r"D:\backendNewsApp\NewsApp\Project\scraped_data"
    subfolders = os.listdir(data)
    for i in subfolders:
        folder_path = os.path.join(data, i)
        file_name = dfs_folder(folder_path)
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as f:
                content = f.readlines()

                text = ""
                for i in content[4:]:
                    if i != "\n":
                        text = text + i
                print(text)
                # Assuming enter_data is a function to insert data into the database
                # Replace 'your_table_name', 'column1', 'column2', etc. with your actual table and column names
                sql = "INSERT INTO data (Title,TopImage,content,Date,Genre,Location) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (content[0], content[3], text, get_date(file_path), i, NLP.analyze_files_in_folder(file_path))

                # Execute the SQL query with the values
                curs = conn.cursor()
                curs.execute(sql, values)
                conn.commit()
                curs.close()
