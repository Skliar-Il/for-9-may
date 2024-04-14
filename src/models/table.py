from sqlalchemy import Column, Integer, String, VARCHAR, Table, Boolean, ARRAY
from conect_db import metadata

persons=Table("persons", metadata,
              
              Column("id", Integer, primary_key=True),
              Column("SNL", String),
              Column("date_birth", Integer),
              Column("date_death", Integer),
              Column("city", String),
              Column("history", String),
              Column("main_photo", String),
              Column("photo", ARRAY(String)),
              Column("medals", ARRAY(String)),
              Column("date_pulished", Integer),
              Column("rank", String),
              Column("role", Boolean)
              )

admins=Table("admins", metadata,
             
             Column("id", Integer, primary_key=True),
             Column("login", String),
             Column("password", String)
             )