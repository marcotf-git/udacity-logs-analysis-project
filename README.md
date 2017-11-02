# Logs Analysis Reporting Tool

This project is an exercise as part of the **Full Stack Web Developer Nanodegree**,
by **Udacity**. It creates a report from the analysis of a database, prints the analysis and also builds a file with the result.

The database contains newspaper articles, as well as the web server log genetared from a newspaper site. The log has a database row for each time a reader loaded a web page. Using that information, the  code will answer questions about the site's user activity.

The report will show:
- The most popular three articles of all time.
- The most popular article authors of all time.
- On which days did more than '1%' of requests lead to errors.

# Installation

* Before running the report, we need to access the database `news` with the
`psql` command (you need to get **PostgreSQL** instaled), and create some `views`
 in the database:

        psql news

        create view totalqueries as
        select to_char(time, 'Mon DD, YYYY') as day, count(*) as num
        from log
        group by day;

        create view errorqueries as
        select to_char(time, 'Mon DD, YYYY') as day, count(*) as num
        from log
        where status != '200 OK'
        group by day;    

* You need to put the `logs_analysis.py` file in the same machine as the database is installed.
In the case of the course, it is a `vagrant` virtual machine. So, for the program be accessed by the virtual machine, you need to copy the `logs_analysis.py` to the `\vagrant` directory that was previously created when installing the `vagrant` virtual machine (that is a shared folder of `vagrant` virtual machine with your local machine).


# Common usage

* After creating the views, run the `logs_analysis.py` in the virtual machine, where the database is installed (you need to get **Python** installed first):
  - use a **Git Bash** shell (if you are in **Windows**)
  - with that shell, go to the `\vagrant` directory that was previously created when installing the `vagrant` virtual machine
  - run the virtual machine with `vagrant up` command
  - open a remote terminal with the `vagrant ssh` command
  - in remote machine, using the terminal, go to the `\vagrant` directory
  - check to see if the `logs_analysi.py` is there
  - in remote machine, run the python conde with `python3 logs_analysis.py`
* The program will print the analysis and also generate a file `report.txt`.
* After finishing, `exit` from remote terminal and type `vagrant halt` in the **Git Bash** local shell to turn off the virtual machine.
* The results of the report can be accessed in the `report.txt` file on your `\vagrant` local directory.
