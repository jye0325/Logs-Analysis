# !/usr/bin/python3.6

import psycopg2
import os

DATABASE = "news"

''' --TEST THIS OUT ~ USE SUBQUERIES
CREATE TABLE sometable (t TIMESTAMP, d DATE);
INSERT INTO sometable SELECT '2011/05/26 09:00:00';
UPDATE sometable SET d = t; -- OK
-- UPDATE sometable SET d = t::date; OK
-- UPDATE sometable SET d = CAST (t AS date); OK
-- UPDATE sometable SET d = date(t); OK
SELECT * FROM sometable ;
'''

VIEWERRORS = '''
CREATE TABLE filterdate (t TIMESTAMP, d DATE);
INSERT INTO filterdate SELECT time FROM log;
UPDATE filterdate SET d = t;

CREATE VIEW ERRORCOUNT
AS SELECT method, status, d
FROM (SELECT *
FROM filterdate JOIN log 
ON filterdate.t = log.time) as results
WHERE (status <> '200 OK')
GROUP BY d;
'''

SQLERRORS = '''
SELECT (COUNT(log.status) AS NUMBEROFREQUESTS FROM LOGS /ERRORCOUNT.COUNT(status)) + (NUMBEROFREQUESTS%ERRORCOUNT.COUNT(status))
'''


def create_output():
    content = ""
    output_file = open('output.txt', 'w')
    content = popular_articles(content)
    content = popular_authors(content)
    #http_errors(content)
    print(content)
    output_file.write(content)
    output_file.close()


def popular_articles(content):
    content = content
    VIEWPOPULARARTICLES = '''
    SELECT articles.title, COUNT(log.path) AS NUMBEROFVIEWS FROM log
    LEFT JOIN articles on articles.slug = split_part(log.path, '/', 3)
    WHERE articles.title is not null
    GROUP BY title
    ORDER BY NUMBEROFVIEWS DESC;
	'''
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(VIEWPOPULARARTICLES)
    results = c.fetchall()
    test = content + "POPULAR ARTICLES OF ALL TIME\n" + "---------------------------------\n" + '\n'.join(str(e) for e in results) + "\n"
    db.close()
    return test



def popular_authors(content):
	writecontent = content
	VIEWPOPULARAUTHORS = '''
	SELECT authors.name, COUNT(log.path) AS NUMBEROFVIEWS FROM log
	LEFT JOIN articles on articles.slug = split_part(log.path, '/', 3)
	LEFT JOIN authors ON authors.id = articles.author
	WHERE authors.name is not null 
	GROUP BY name
	ORDER BY NUMBEROFVIEWS DESC;
	'''
	db = psycopg2.connect(database=DATABASE)
	c = db.cursor()
	c.execute(VIEWPOPULARAUTHORS)
	results = c.fetchall()
	test = writecontent + "\nPOPULAR AUTHORS OF ALL TIME\n" + "---------------------------------\n" + '\n'.join(str(e) for e in results) + "\n"
	return test
	db.close()


def http_errors(content):
	content = content
	VIEWERRORS = '''
	'''
	db = psycopg2.connect(database=DATABASE)
	c = db.cursor()
	c.execute(VIEWERRORS)
	results = c.fetchall()
	writecontent = writecontent + "\nREPORTED ERRORS > 1\%\n" + "---------------------------------\n" + ''.join(str(e) for e in results) + "\n"
	return content
	db.close()
	
create_output()
