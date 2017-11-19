# Logs Analysis Reporting Tool

This project is an exercise as part of the **Full Stack Web Developer Nanodegree**, by **Udacity**. It creates a report from the analysis of a database, prints the analysis and also builds a file with the result.

The database contains newspaper articles, as well as the web server log generated from a newspaper site. The log has a database row for each time a reader loaded a web page. Using that information, the  code will answer questions about the site's user activity.

The report will show:
- The most popular three articles of all time.
- The most popular article authors of all time.
- On which days did more than '1%' of requests lead to errors.

# Installation

* The project makes use of a Linux-based virtual machine (VM). To install this machine, please:

  1. Install **VirtualBox**: <ttps://www.virtualbox.org/wiki/Download_Old_Builds_5_1>
  2. Install **Vagrant** (for automated building the VM according with some set of configurations): <https://www.vagrantup.com/>
  3. Make a directory at local machine, for the project;
  4. Download the file `Vagrantfile`, that is a configuration file for the VM, created by **Udacity** for the course (this file will be accessed by the **Vagrant** to build the VM):
  <https://github.com/udacity/fullstack-nanodegree-vm>
  5. Put the file `Vagrantfile` in the local directory that you created for the project;
  6. With a **Git Bash** terminal, go to that directory (where the `Vagrantfile` is) and command `vagrant up`. 

* The previous steps will create the VM, with the database `news`.
* The `vagrant` directory is automatically installed by **Vagrant** as a shared directory between the local machine and the VM. So, it is easy to share files between them.👍
* The database `news` was created automatically by the `Vagrantfile`, at the VM, but we need to setup the database before using by the report.

* Setting up the database:


  1. Get the file `newsdata.sql` from the repository <https://github.com/udacity/fullstack-nanodegree-vm> and save in your local machine, at the `vagrant` shared directory, and `unzip` the file;
  2. Turn on the VM with command `vagrant up` in your local machine at the **Git Bash**;
  3. Log into the VM with command `vagrant ssh` typed at the **Git Bash**;
  4. In the VM, go to `vagrant` directory, and load the schema and data for the `news` database, with the command `psql -d news -f newsdata.sql` (you are using the **PostgreSQL** that was already automatically installed when creating the VM).


* Before running the report, we need to access the database `news` with the `psql` command (from the **PostgreSQL**), and create some `views` in the database:

        psql news

    ```sql
    CREATE VIEW totalqueries AS
    SELECT to_char(time, 'Mon DD, YYYY') AS day, count(*) AS num
    FROM log
    GROUP BY day;
    ```
    ```sql
    CREATE VIEW errorqueries AS
    SELECT to_char(time, 'Mon DD, YYYY') AS day, count(*) AS num
    FROM log
    WHERE status != '200 OK'
    GROUP BY day;   
    ```

* You need to copy the **Python** program `logs_analysis.py` to the same machine as the database `news`. So, copy the `logs_analysis.py` to the `\vagrant` local directory, because that directory is a shared folder with the VM.


# Common usage

* After creating the views, run the `logs_analysis.py` in the VM, where the database is installed (**Python** is already installed in the VM):
  - use a **Git Bash** shell (if you are in **Windows**)
  - with that shell, go to the `\vagrant` directory that was previously created when installing the `vagrant` virtual machine
  - run the virtual machine with `vagrant up` command
  - open a remote terminal with the `vagrant ssh` command
  - in remote machine, using the terminal, go to the `\vagrant` directory
  - check to see if the `logs_analysi.py` is there
  - in remote machine, run the python code with `python3 logs_analysis.py`
* The program will print the analysis and also generate a file `report.txt`.
* After finishing, `exit` from remote terminal and type `vagrant halt` in the **Git Bash** local shell to turn off the virtual machine.
* The results of the report can be accessed in the `report.txt` file on your `\vagrant` local directory.
