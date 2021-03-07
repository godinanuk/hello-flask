import flask
from flask import request, render_template
from prometheus_flask_exporter import PrometheusMetrics
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
engine = create_engine("mysql://trainuser:m3m0ry@mysql/traindb",echo = True)
meta = MetaData()

conn = engine.connect()

employee = Table(
   'employee', meta, 
   Column('empno', Integer, primary_key = True), 
   Column('ename', String), 
   Column('age', Integer), 
   Column('job', String), 
   Column('salary',Integer),
)

def select_data():
   headings = ('Empno','Ename','Age','Job','Salary')
   s = employee.select()
   data_list = []
   result = conn.execute(s)
   for row in result:
       data_list.append(row)

   data = tuple(data_list)
   return headings,data

# Create the application.
app = flask.Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.start_http_server(5100)  # Prometheus metrics available on port 5100

@app.route('/')
def index():
    return flask.render_template('index.html')

common_counter = metrics.counter(
        'by_endpoint_counter', 'Request count by endpoints',
        labels={'endpoint': lambda: request.endpoint}
)


@app.route("/select", methods=['GET'])
@common_counter
def select():
    print(" request.method :",request.method)
    headings,data = select_data() 
    return render_template('display_table.html', headings=headings, data=data)

@app.route("/insert", methods=['GET', 'POST'])
@common_counter
def insert():
    print(" request.method :",request.method)
    if (request.method == 'POST'): # and request.form["submit"] == "submit"):
        empno=request.form['empno'] 
        ename=request.form['ename'] 
        age=request.form['age'] 
        job=request.form['job'] 
        salary=request.form['salary'] 
       
        ins = employee.insert().values(
                empno=empno,
                ename=ename,
                age=age,
                job=job,
                salary=salary)

        conn.execute(ins)
       
        headings,data = select_data()
        return render_template('display_table.html', headings=headings, data=data)
 
    else:
        return render_template('table.html')

# register additional default metrics
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

if __name__ == '__main__':
    print('SQLAlchemy version is ',sqlalchemy.__version__)
    app.debug=True
    app.run(host='0.0.0.0')
