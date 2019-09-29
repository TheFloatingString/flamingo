from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgres://dmguzjxxsmloic:5948608b6a121bda4af1489059dcca556334daf592af381eaf6f40add0606d5e@ec2-174-129-229-106.compute-1.amazonaws.com:5432/d49b6n4290m484",echo = True)

meta = MetaData()
Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	password = Column(String)

	def __repr__(self):
		return "<User(first_name='%s', last_name='%s', email='%s', password='%s')>" \
		% (self.first_name, self.last_name, self.email, self.password)

class StressEntry(Base):
	__tablename__ = "stress_entries"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	datetime_start = Column(String)
	datetime_end = Column(String)
	stres_level = Column(Integer)

	def __repr__(self):
		return "<StressEntry(user_id='%s', datetime_start='%s', datetime_end='%s', stres_level='%s')>" \
		% (self.user_id, self.datetime_start, self.datetime_end, self.stres_level)

if __name__ == '__main__':
	Base.metadata.create_all(engine)