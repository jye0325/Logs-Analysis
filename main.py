# !/usr/bin/python3.6

import psycopg2
import os

DATABASE = "news"

# PSQL QUERY SETUP

ERRORSETUP = '''
    CREATE TABLE filterdate (t TIMESTAMP, d DATE);
    INSERT INTO filterdate SELECT time FROM log;
    UPDATE filterdate SET d = t;
    
    CREATE VIEW modifiedlog
    AS SELECT d, status
    FROM (SELECT *
    FROM filterdate JOIN log
    ON filterdate.t = log.time) AS results;
    
    CREATE TABLE ecount (ed date, errors integer);
    INSERT INTO ecount (ed, errors) SELECT d, COUNT(status)
    FROM modifiedlog WHERE (status <> '200 OK') GROUP BY d;
    
    CREATE TABLE tcount (td date, total integer);
    INSERT INTO tcount (td, total) SELECT d, COUNT(status)
    FROM modifiedlog GROUP BY d;
    
    CREATE TABLE pcount (pd date, percentage float);
    INSERT INTO pcount (pd, percentage) SELECT ed, (errors*100/total)
    FROM (SELECT * FROM ecount JOIN tcount ON ecount.ed = tcount.td) AS results;
    '''

VIEWPOPULARARTICLES = '''
    SELECT articles.title, COUNT(log.path) AS NUMBEROFVIEWS FROM log
    LEFT JOIN articles on articles.slug = split_part(log.path, '/', 3)
    WHERE articles.title IS NOT NULL
    GROUP BY title
    ORDER BY NUMBEROFVIEWS DESC;
    '''

VIEWPOPULARAUTHORS = '''
    SELECT authors.name, COUNT(log.path) AS NUMBEROFVIEWS FROM log
    LEFT JOIN articles on articles.slug = split_part(log.path, '/', 3)
    LEFT JOIN authors ON authors.id = articles.author
    WHERE authors.name IS NOT NULL
    GROUP BY name
    ORDER BY NUMBEROFVIEWS DESC;
    '''

VIEWERRORS = '''
    SELECT * FROM pcount WHERE percentage >= 1;
    '''

DBCLEANUP = '''
    DROP TABLE ecount, tcount, pcount;
    DROP VIEW modifiedlog;
    DROP TABLE filterdate;
    '''


def create_output():
    """ This function stores the output of these three PSQL queries in a
        .txt file called output. After performing the queries and writing the
        file, the function will perform necessary cleanups before exiting the
        program.
        """
    content = ""
    content = popular_articles(content)
    content = popular_authors(content)
    content = http_errors(content)
    print(content)
    output_file = open('output.txt', 'w')
    output_file.write(content)
    output_file.close()
    database_cleanup()


def popular_articles(content):
    """ This function shall return the most popular articles of all time in
        descending order.
        """
    content = content
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWPOPULARARTICLES)
    results = c.fetchall()
    content = content \
        + "POPULAR ARTICLES OF ALL TIME\n" \
        + "---------------------------------\n" \
        + '\n'.join(str(e) for e in results) \
        + "\n"
    db.close()
    return content


def popular_authors(content):
    """ This function shall return the most popular authors of all time in
        descending order.
        """
    content = content
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWPOPULARAUTHORS)
    results = c.fetchall()
    content = content \
        + "\nPOPULAR AUTHORS OF ALL TIME\n" \
        + "---------------------------------\n" \
        + '\n'.join(str(e) for e in results) \
        + "\n"
    return content
    db.close()


def http_errors(content):
    """ This function shall return the days with errors greater than 1%.
        """
    content = content
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(ERRORSETUP)
    c.execute(VIEWERRORS)
    results = c.fetchall()
    content = content \
        + "\nREPORTED ERRORS > 1%\n" \
        + "---------------------------------\n" \
        + ''.join(str(e) for e in results) \
        + "\n"
    return content
    db.close()


def database_cleanup():
    """This function shall cleanup the database by dropping all of the created
        views and tables that were not originally created by newsdata.sql.
        """
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(DBCLEANUP)
    db.close()

# Calls the main function at the start of the program
create_output()
