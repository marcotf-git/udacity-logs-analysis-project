#!/usr/bin/env python3
"""This program makes an analysis of the 'log' table in the database 'news'
and shows:
1) The most popular three articles of all time.
2) The most popular article authors of all time.
3) On which days did more than '1%' of requests lead to errors.
"""

import psycopg2


def get_popular_articles():
    """"Makes a query to the database 'news', tables 'log' and 'articles',
    fo find the most popular three articles of all time, based on total
    queries.

    Returns:
        A list with the corresponding most popular articles, in the form of
        tuples (str, int) with the name of the article and the number of total
        queries for that article. For example:

        [('title of the article', 99),
         ('title of second article', 51),
         ('title of third article', 30)]
    """
    news = psycopg2.connect(database='news')
    cursor = news.cursor()
    cursor.execute("select articles.title, count(*) as num\
                    from log, articles\
                    where ('/article/'||articles.slug) = log.path\
                    group by articles.title\
                    order by num desc\
                    limit 3;")
    pop_articles = cursor.fetchall()
    news.close()
    return pop_articles


def get_popular_authors():
    """"Makes a query to the database 'news', tables 'log', 'articles' and
    'authors', fo find the most popular three authors of all time, based on
    total queries.

    Returns:
        A list with the corresponding most popular four authors, in the form of
        tuples (str, int) with the name of the author and the number of total
        queries for that author. For example:

        [('name of first author', 99),
         ('name of second author', 51),
         ('name of third author', 30),
         ('name of fourth author', 10)]
    """
    news = psycopg2.connect(database='news')
    cursor = news.cursor()
    cursor.execute("select authors.name, count(*) as num\
                    from log, articles, authors\
                    where (('/article/'||articles.slug) = log.path) and\
                    (articles.author = authors.id)\
                    group by authors.name\
                    order by num desc\
                    limit 4;")
    pop_authors = cursor.fetchall()
    news.close()
    return pop_authors


def get_error_days():
    """"Makes a query to the database 'news', views 'totalqueries' and
    'errorqueires', fo find the days on which more than '1%'' of requests led
    to errors.

    The corresponding SQL commands to create the views are:
        create view totalqueries as
        select to_char(time, 'Mon DD, YYYY') as day, count(*) as num
        from log
        group by day;

        create view errorqueries as
        select to_char(time, 'Mon DD, YYYY') as day, count(*) as num
        from log
        where status != '200 OK'
        group by day;

    Returns:
        A list with the corresponding days, in the form of
        tuples (str, int, int, decimal) with the day in the form
        'Mon dd, YYYY', the total queries, the errors and the fraction of
        errors or (total errors)/(total queries) for that day. For example:

        [ ('Jul 01, 2016', 50000, 1000, 0.02)]
    """
    news = psycopg2.connect(database='news')
    cursor = news.cursor()
    cursor.execute('select totalqueries.day, totalqueries.num as\
                    "total queries", errorqueries.num as "errors",\
                    (errorqueries.num::numeric/totalqueries.num::numeric)\
                    ::numeric(4,3) as "fraction of errors"\
                    from totalqueries, errorqueries\
                    where totalqueries.day = errorqueries.day\
                    and  (errorqueries.num::numeric/totalqueries.num::numeric)\
                     > 0.01;')
    error_days = cursor.fetchall()
    news.close()
    return error_days


def main():
    """Runs the program"""
    # Creates the file report
    my_file = open('report.txt', 'w')

    # Writes the most popular articles
    my_file.write('\n\nThe most three popular articles of all time:\n\n')
    articles = get_popular_articles()
    for article in articles:
        my_file.write('"' + article[0] + '"' + ' ---  ' + str(article[1]) +
                      ' views\n')

    # Writes the most popular authors
    my_file.write('\n\nThe most three popular authors of all time:\n\n')
    authors = get_popular_authors()
    for author in authors:
        my_file.write(author[0] + ' ---  ' + str(author[1]) + ' views\n')

    # Writes the days with more than 1% query errors
    my_file.write('\n\n' + 'Days with more than {:.1%} of'.format(0.01) +
                  'requests with errors:\n\n')
    days = get_error_days()
    for day in days:
        my_file.write(day[0] + ' ---  ' + ' {:.1%} errors\n'.format(day[3]))

    # Close the file to commit information
    my_file.write('\n\n')
    my_file.close()

    # Prints the report
    my_file = open('report.txt', 'r')
    for line in my_file:
        print(line, end="")
    my_file.close()


# Runs the program
main()
