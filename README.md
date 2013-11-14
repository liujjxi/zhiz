zhiz
====

The dynamic version of [hit9/rux.git](http://github.com/hit9/rux.git)

Setup
-----

```bash
git clone git://github.com/hit9/zhiz.git
cd zhiz
pip install -r requirements.txt
```

Then, create database `zhiz`:

```sql
mysql> create database zhiz;
```

create tables:

```sql
mysql> source tables.sql;
```

Edit conifguration `zhiz/config.py`, and then you can start the server:

```bash
python runserver.py
```
