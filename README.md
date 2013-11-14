zhiz
====

The dynamic version of [hit9/rux.git](http://github.com/hit9/rux.git)

version v0.0.1

Setup
-----

1. install requirements:

   ```bash
   git clone git://github.com/hit9/zhiz.git
   cd zhiz
   pip install -r requirements.txt
   ```

2. Create database `zhiz`:

   ```sql
   mysql> create database zhiz;
   ```
3. create tables and initialize data:

   ```sql
   mysql> source tables.sql;
   ```

4. Edit conifguration `zhiz/config.py`, and then you can start the server:

   ```bash
   python runserver.py
   ```

5. Go to `/admin` to login, default password is `admin`

Screen-shot
-----------

![](https://dl.dropboxusercontent.com/u/68191343/github/zhiz.png)
