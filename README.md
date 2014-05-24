zhiz
====

The dynamic version of [hit9/rux.git](http://github.com/hit9/rux.git)

version v0.2.0

Testing url: http://zhizblog.ap01.aws.af.cm/ (admin ur: `/admin`, password: `admin`)

Setup
-----

1. install requirements:

   ```bash
   git clone git://github.com/hit9/zhiz.git
   cd zhiz
   virtualenv venv
   . venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create database `zhiz`:

   ```sql
   mysql> create database zhiz;
   ```
3. create tables and initialize data:

   ```sql
   mysql> use zhiz;
   mysql> source tables.sql;
   ```

4. Edit conifguration `zhiz/config.py`, and then you can start the server:

   ```bash
   python runserver.py
   ```

5. Site is served at `http://0.0.0.0:5000`, go to `/admin` to login, default password is `admin`, 

About
-----

- Write posts in Markdown

- Ability to save drafts, preview

- Clean style

Thanks
-------

- Thanks for @lepture's awesome markdown editor.

- Thanks for iconmoon's free and nice icons.

Screen-shot
-----------

![](https://dl.dropboxusercontent.com/u/68191343/github/zhiz.png)
