# Logs-Analysis

The **Logs-Analysis** is a project written for **Udacity's Full Stack Developer Nanodegree Program**. 

In this project, the `python` script will produce an output file of three different queries:

* Top 3 Articles by Views
* Authors Ranking by Arcticle Views
* Date(s) with Reporte Errors > 1%

## Requirments

Please ensure your system contains the following software prior to using this project:

* Virtual Box
* Custom Vagrant file from Udacity.com
* Newsdata.sql file from Udacity.com

## Download

To obtain a copy of this project download the entire contents of this repository in a `.zip` file onto your desktop or folder of choice and unzip it to your vagrant folder. Below are also the required links that you will need to download and install for the requirements.

* [Newsdata.sql File](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Vagrant Configuration File](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)

## Usage

1) Open terminal or command prompt and navigate to your Vagrant folder.

2) Enter `vagrant up` to initially set up your virtual machine.

3) Once Vagrant has finished setting up, enter `vagrant ssh`. 

4) Navigate to your vagrant folder inside vagrant using `cd /vagrant/`. 

5) Setup your database by running `psql -d news -f create_views.sql`.

6) Enter the database by running `psql news`.

7) Enter `python /vagrant/main.py` to run the script.

8) The results of the query will be located in the same folder as `main.py` named `output.txt` as well as on terminal/command prompt.

## Source

## Disclaimer

Please use this project at your own risk. I, _J. Ye._, am not responsible for any damage(s) that the end-user's computer may experience while using this project.

## License
