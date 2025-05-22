from flask import Flask, render_template, send_file, request
import subprocess
from searchObject import SearchObject 
import json
import os
searcher = SearchObject() 


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calcSearch.html')

@app.route('/exchange_data', methods=['POST']) 
def exchange_data():
    if(request.method == 'POST'):
        query = request.form.get('query')
        print(query, flush=True)
        searcher.set_params(query)
        results = searcher.compile_info()
        return render_template('results.html', results=results)
    
@app.route('/view_results')
def view_result():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/exchange_data',methods=['POST'])
def handle_data():
    with open("temporary.txt",'w') as f:
        data = request.get_data(as_text=true)
        f.write(data)
    