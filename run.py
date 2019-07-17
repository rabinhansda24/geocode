import time
from app import app
import os
from flask import request, render_template, send_file
import pyexcel as excel
import pandas as pd
from collections import OrderedDict
from app.functions.get_geocode import get_geocode


@app.route('/')
def hello():
    return 'Hellow, World!'


@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        #get the excel file from post request object
        df = pd.read_excel(request.files.get('file'))
        # Convert it into pandas data frame
        data = pd.DataFrame(df)
        pd.options.display.max_colwidth = 100
        dealy = 5
        address_with_latlng = []
        # Iterate through the address in the excel 
        for index, row in df.iterrows():
            # Calling the get_geocode function to get the GeoCode of an address
            lat, lang = get_geocode(row['Address'])
            latlng = 'lat:' + str(lat) + ', lang:' + str(lang)
            # Appending the newly aquired lat lang to the row
            row['LatLng'] = latlng
            # Appending the entire row in a new list
            address_with_latlng.append(row.tolist())
            # Dealying the API call by 5 sec to avoid google api policy
            time.sleep(dealy)

        # Getting the current folder
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Folder where the excel file will be saved
        new_path = dir_path + '/app/files/'
        # Saving the data to excel file
        excel.save_as(array=address_with_latlng, dest_file_name=new_path+"address.xlsx")
        # Rendering the download page
        return render_template('download.html')
    return render_template('upload.html')

@app.route('/return-file')
def return_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    new_path = dir_path + '/app/files/'
    try:
        return send_file(new_path+'address.xlsx', attachment_filename='address.xlsx')
    except Exception as e:
        print str(e)
        return str(e)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
