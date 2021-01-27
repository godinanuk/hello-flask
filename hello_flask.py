import flask
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine("mysql://trainuser:m3m0ry@mysql/traindb",echo = True)
meta = MetaData()

conn = engine.connect()

employee = Table(
   'employee', meta, 
   Column('empno', Integer, primary_key = True), 
   Column('ename', String), 
   Column('age', Integer), 
   Column('job', String), 
)

s = employee.select()

result = conn.execute(s)
for row in result:
    print(row)

# Create the application.
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    print('SQLAlchemy version is ',sqlalchemy.__version__)
    app.debug=True
    app.run(host='0.0.0.0')
