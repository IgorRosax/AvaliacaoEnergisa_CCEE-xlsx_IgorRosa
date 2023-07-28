
import CCEE
import pandas as pd

from flask import Flask, redirect, render_template, request, send_file, flash,url_for

# Configure application
app = Flask(__name__)
app.secret_key = 'iRosaApp'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/import", methods=["GET", "POST"])
def importCCEEData():
    if request.method == "POST":
                    
        data = CCEE.getCCEEData()

        if data is None:
            flash('Error 503 - Service Unavailable',"error")
            return render_template("import.html")

        if CCEE.storeCCEEData(data) is None:
            flash('Error 500 - Internal Server Error',"error")
            return render_template("import.html")
        
        return redirect("/")
    else:
        return render_template("import.html")
   
@app.route('/export', methods=["GET", "POST"])
def export():
    
    
    
    if request.method == "POST":
        
        arrFilter = [
            'Fiat Betim MG',
            'Karsten Blumenau SC',
            'Metro SP',
            'NESTLE ARACATUBA',
            'SAMSUNG',
            'RICA',
            'INTER LINK',
            'HONDA AUTOMOVEIS'
        ]
        
        # Create DataFrame from file
        data = CCEE.readCCEEStoredData()

        if (data is None):
            flash('Parece que ainda não foram importados dados. Por favor, realize a importação antes da exportação.',"error")
            return redirect('/export')
        
        # Filter the data by the `Carga` column
        filtered_data = data[data['Carga'].isin(arrFilter)]

        # Export the data to CSV and JSON files
        filtered_data.to_csv(f'{CCEE.STORE_DATA}/{CCEE.FILE_NAME}_filtered.csv', index=False, encoding="Windows-1252", sep=';')
        #filtered_data.to_json('data_filtered.json')
        return send_file(f'{CCEE.STORE_DATA}/{CCEE.FILE_NAME}_filtered.csv', as_attachment=True)
        
    else:
        return render_template('export.html')

app.run()