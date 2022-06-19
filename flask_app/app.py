from flask import Flask, render_template, request, jsonify
import pyodbc



# Trusted Connection to Named Instance
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-NRFAP4L;DATABASE=Originex;Trusted_Connection=yes;')



app = Flask(__name__)



@app.route('/', )
def index():
    return render_template('home.html')
        

@app.route('/Township')
def Township():
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT PREMISE_TOWN from Originex.[dbo].[SAP_STATEMENT_RECORDS_2022_04] where PREMISE_TOWN is not null order by PREMISE_TOWN")
    towns = cursor.fetchall() 
    return render_template('Township.html', towns=towns)

@app.route('/fetch_towns', methods=["POST","GET"])
def fetch_towns():
    cursor = connection.cursor()
    if request.method == 'POST':
        query = request.form.get('query')
        if query == '':
            sql_query = "SELECT top 10 PREMISE_ID ,PREMISE_ADDRESS, ADDR1, ADDR2, ADDR3, ADDR4, ADDR5, EMAIL_ADDR from Originex.[dbo].[SAP_STATEMENT_RECORDS_2022_04] where PREMISE_TOWN is not null and PREMISE_TOWN is null"
            cursor.execute(sql_query)
            towns_data = cursor.fetchall()
        else:
            town_name = request.form.get('query')  
            town_name = town_name.split("('")[1].split("'")[0]
            sql_query = "SELECT PREMISE_ID ,PREMISE_ADDRESS, ADDR1, ADDR2, ADDR3, ADDR4, ADDR5, EMAIL_ADDR from Originex.[dbo].[SAP_STATEMENT_RECORDS_2022_04] where PREMISE_TOWN = '"  + str(town_name) + "'"
            cursor.execute(sql_query)
            towns_data = cursor.fetchall()
    return jsonify({'htmlresponse': render_template('town_response.html', towns_data=towns_data)})


@app.route('/Scheme')
def Scheme():
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT SCHEME_NAME_DESC from Originex.[dbo].[dbo_SAP_STATEMENT_RECORDS_2022_$] where SCHEME_NAME_DESC is not null order by SCHEME_NAME_DESC")
    schemes = cursor.fetchall()
    return render_template('Scheme.html', schemes=schemes)


if __name__ == '__main__':
    app.run(debug=True)
