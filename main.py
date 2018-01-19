#!/usr/bin/env python

import psycopg2
import os
from datetime import datetime

DATABASE = "news"

VIEWPOPULARARTICLES = '''
    SELECT articles.title, COUNT(log.path) AS NUMBEROFVIEWS FROM log
    LEFT JOIN articles ON '/article/' || articles.slug = log.path
    WHERE articles.title IS NOT NULL
    GROUP BY title
    ORDER BY NUMBEROFVIEWS DESC
    LIMIT 3;
    '''

VIEWPOPULARAUTHORS = '''
    SELECT authors.name, COUNT(log.path) AS NUMBEROFVIEWS FROM log
    LEFT JOIN articles ON '/article/' || articles.slug = log.path
    LEFT JOIN authors ON authors.id = articles.author
    WHERE authors.name IS NOT NULL
    GROUP BY name
    ORDER BY NUMBEROFVIEWS DESC
    '''

VIEWERRORS = '''
    SELECT d, (errorcount*100.0/totalcount)
    FROM errorlog;
    '''


def create_output():
    """ This function stores the output of these three PSQL queries in a
        .txt file called output. After performing the queries and writing the
        file.
        """
    content = ""
    content += popular_articles()
    content += popular_authors()
    content += http_errors()
    print(content)
    output_file = open('output.txt', 'w')
    output_file.write(content)
    output_file.close()


def popular_articles():
    """ This function shall return the most popular articles of all time in
        descending order limitted to the top 3.
        """
    content = ""
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWPOPULARARTICLES)
    results = c.fetchall()
    content += "TOP 3 ARTICLES BY VIEWS\n"
    content += "---------------------------------\n"
    for e in results:
        content += '\"{}\" -- {:n} views\n'.format(e[0], e[1])
    content += "\n"
    db.close()
    return content


def popular_authors():
    """ This function shall return the most popular authors of all time in
        descending order limitted to the top 3.
        """
    content = ""
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWPOPULARAUTHORS)
    results = c.fetchall()
    content += "\nAUTHORS RANKED BY ARTICLE VIEWS\n"
    content += "---------------------------------\n"
    for e in results:
        content += '\"{}\" -- {:n} views\n'.format(e[0], e[1])
    content += "\n"
    db.close()
    return content


def http_errors():
    """ This function shall return the days with errors greater than 1%.
        """
    content = ""
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWERRORS)
    results = c.fetchall()
    content += "\nDATE(S) WITH REPORTED ERRORS > 1% \n"
    content += "---------------------------------\n"
    for e in results:
        if(e[1] > 1.00):
            errordate = e[0]
            content += str(errordate)
            content += " -- {:.2f}% errors\n".format(e[1])
    content += "\n"
    db.close()
    return content


# Calls the main function at the start of the program
if __name__ == '__main__':
    create_output()
