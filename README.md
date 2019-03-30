# **Ticket Project**

This is Ticket Management system using Tornado Web server.

Version : 1.0

Build : Passing

Author : arman zareian

Language : Python  3.6.5

# **PreRequirements**

For This Project You Need below Requirements :
- pyhon
- mysql

```shell
$ apt install python mysql
```

# **Requirement**

For runnig code.py file You Need to install below pakcage for python  :

- tornado 
- mysql-connector


```shell
$ python -m pip install mysql-connector tornado
```

## Step0 : Cloning

First of All Clone the Project : 

```shell
$ git clone https://github.com/armanzareian/Ticket.git
$ cd Ticket
```

## Step1 : Connect to MySQL and create a database

Connect to MySQL as a user that can create databases and users:

```shell
$ mysql -u root
```
    
Create a database named "Ticket":
    
```shell
mysql> CREATE DATABASE Ticket;
```

## Step2 : Create the tables in your new database
Create 2 tables
Like below:
With name Users:
![GET](https://github.com/armanzareian/Ticket/blob/master/Screen%20Shot%202019-03-30%20at%207.38.59%20PM.png)
With name comments:
![GET](https://github.com/armanzareian/Ticket/blob/master/Screen%20Shot%202019-03-30%20at%207.39.11%20PM.png)
Then now you Must Put Database information in server.py from line 36 - 41

## Step3 : Run the bank project


With the default user, password, and database you can just run:

```shell
$ python server.py
```

# **Usage**

Now For Sending Requests You Have 2 Options :
1. Postman
2. Our Client Code

## POSTMAN :
Download and install <a href="https://www.getpostman.com/apps" target="_blank">**Postman**</a>. 

In our Project We Support Both POST & GET Method for Requesting

You Can See Example Below : 

### GET :
![GET GIF](https://media.giphy.com/media/1xkyly2FQMuYKu0zSR/giphy.gif)



### POST :


![POST GIF](https://media.giphy.com/media/p49w5NceWzsHsv2yM7/giphy.gif)
## OUR CLIENT CODE:

Just Go To Client Folders and Run Below Code : 

```shell 
$ pip install requests
$ python client.py
```




# **Support**

Reach out to me at one of the following places!

- Telegram at <a href="https://t.me/arman_z99" target="_blank">@arman_z99</a>
- Yahoo at <a href="arman_z1378@yhaoo.com" target="_blank">arman_z1378@yhaoo.com</a>






