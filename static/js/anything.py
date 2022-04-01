import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

engine=create_engine(df)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()