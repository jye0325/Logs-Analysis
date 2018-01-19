-- PSQL QUERY SETUP --
CREATE VIEW errorlog AS
SELECT time::date AS d,
	   COUNT(status) AS totalcount,
	   COUNT(CASE WHEN status <> '200 OK' THEN 1 ELSE NULL END) AS errorcount
FROM log
GROUP BY time::date;