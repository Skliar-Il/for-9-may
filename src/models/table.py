from sqlalchemy import Column, Integer, String, VARCHAR, Table, Boolean, ARRAY, JSON, PickleType, TIMESTAMP
import datetime, sys, os

sys.path.append(os.path.join(sys.path[0][:-6]))

from conect_db import metadata


persons=Table("persons", metadata,
              
              Column("id", Integer, primary_key=True),
              Column("SNL", String),
              Column("date_birth", Integer),
              Column("date_death", Integer),
              Column("city", String),
              Column("history", String),
              Column("main_photo", String),
              Column("photo", String),
              Column("medals", String),
              Column("date_pulished", Integer),
              Column("rank", String),
              Column("role", Boolean),
              Column("contact_email", String),
              Column("contact_SNL", String),
              Column("contact_telegram", String),
              Column("check", Boolean, default=False)
              )

admins = Table("admins", metadata,
             
             Column("id", Integer, primary_key=True),
             Column("login", String),
             Column("password", String)
             )

token = Table("token", metadata,
              Column("id", Integer, primary_key=True), 
              Column("token", String)
              )
