For Appfog Users
----------------

To deploy this simple blog on appfog, follow these steps:

1. install appfog commandline tool `af` if necessary:

   ```
   gem install af
   ```

2. create a directory:

   ```
   mkdir myblog && cd myblog
   ```

   create environment via virtualenv:

   ```
   virtualenv venv
   . venv/bin/activate
   ```

3. clone codes:

   ```
   git clone git://github.com/hit9/zhiz.git
   cd zhiz
   mv for_appfog/wsgi.py wsgi.py
   ```

4. create app:

   ```
   af login
   af push myblog
   ```

   Remember to create a MySQL service binding to this app, or you can create it
   later youself.

   Waiting this setp ok.

5.  initialize data in mysql:

   ```
   af tunnel
   ```

   Follow what `af` tells you to do, you will login the remote MySQL(the
   service binding to your app), then paste the sqls in tables.sql and run them:

   mysql> show databases;
   mysql> use 21232f297a57a5a743894a0e4a801fc3;
   mysql> here paste the content of tables.sql
