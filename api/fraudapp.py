import io

from flask import Flask, redirect, request, url_for, jsonify, render_template, send_file, safe_join, \
    send_from_directory, make_response
from .utils import *
import os
import zipfile

app = Flask(__name__)


@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        try:
            value, value1,ccode ,citime= [], [], [], []
            count = 0
            csv_file = request.files['file']
            value.append(request.form.getlist('check1'))
            value.append(request.form.getlist('check2'))
            value.append(request.form.getlist('check3'))
            value.append(request.form.getlist('check4'))
            value1.append(request.form.getlist('text1'))
            value1.append(request.form.getlist('text2'))
            value1.append(request.form.getlist('text3'))
            ccode.append(request.form.getlist('text4'))
            citime.append(request.form.getlist('text5'))
            apkv = value1[0][0]
            sdkv = value1[1][0]
            osv = value1[2][0]
            for on in value:
                if on == ['on']:
                    count = count + 1
            if count > 1:
                return jsonify({"error": "please select only one checkbox"})
            c = value.index(['on'])
            if (c == 0):
                df = pd.read_excel(csv_file)
                df = df.fillna('NaN')
                df, err = clickinject(df,citime)
                if (err == True):
                    return jsonify({"err": "wrong type of dataset"})
                df = clickspam(df)
                df, err = osversioncheck(df, osv,c)
                if (err == True):
                    return jsonify({"err": "wrong  os input type"})
                df, err = apkversioncheck(df, apkv)
                if (err == True):
                    return jsonify({"err": "wrong apk input type"})
                df, err = sdkversioncheck(df, sdkv)
                if (err == True):
                    return jsonify({"err": "wrong sdk input type"})
                df=countrycheck(df,ccode)
                dff = summary(df,c)



            elif (c == 1):
                df = pd.read_csv(csv_file)
                df = df.fillna('NaN')
                df, err = osversioncheck(df, osv,c)
                if (err == True):
                    return jsonify({"err": "wrong  os input type"})
            elif (c == 2):
                df = pd.read_csv(csv_file, skiprows=5)
                df = df.fillna('NaN')
            elif (c == 3):

                colnames = ['GAID', 'GID Name', 'IP', 'Site ID', 'Partner', 'Campaign name', 'Group', 'Click DT',
                            'Attributed Touch Time', 'Inst DT', 'Install Time', 'Click Id', '12', '13', 'Version', '16',
                            '17', '18', '19', '20', '21', '22','23','24','25','26','27','28','29','30']
                df = pd.read_excel(csv_file)
                colcount=df.shape[1]
                while colcount!=len(colnames):
                    colnames.pop()
                df = pd.read_excel(csv_file, names=colnames, header=None)
                df = df.fillna('NaN')
                df.to_csv("11.excel")
                df.drop([0], inplace=True)
                df=clickinject2(df,citime)
                df=clickspam2(df)
                df, err = osversioncheck(df, osv, c)
                if (err == True):
                    return jsonify({"err": "wrong  os input type"})
                dff=summary(df,c)


            file_List = [df, dff]
            name_list = ['Raw_data_report.csv', 'fraud_summary.csv']
            def zipFiles(file_List):
                outfile = io.BytesIO()
                with zipfile.ZipFile(outfile, 'w') as zf:
                    for name, data in zip(name_list, file_List):
                        zf.writestr(name, data.to_csv())
                return outfile.getvalue()

            zipped_file = zipFiles(file_List)
            response = make_response(zipped_file)
            response.headers["Content-Type"] = "application/octet-stream"
            response.headers["Content-Disposition"] = "attachment; filename=FraudReport.zip"
            return response


        except Exception as ee:
            print(ee)
            return jsonify({"error":"invalid File Type"})

        return redirect(url_for('upload_csv'))
    return render_template('header.html')



