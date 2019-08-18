import math
import pandas as pd
import numpy as np
from dateutil import parser
def clickinject(data_frame,citime):
    try:
        ti=int(citime[0][0])
    except:
        ti=15
        pass
    err=False
    if 'Attributed Touch Time' in data_frame.columns:
        data_frame['Attributed Touch Time'] = pd.to_datetime(data_frame['Attributed Touch Time'],format='%d-%m-%Y %H:%M')
        data_frame['Install Time'] = pd.to_datetime(data_frame['Install Time'],format='%d-%m-%Y %H:%M')
        data_frame['IT-CT'] = data_frame['Install Time'] - data_frame['Attributed Touch Time']
        data_frame['IT-CT'] = data_frame['IT-CT'] / np.timedelta64(1, 's')
        data_frame['CI'] = 0
        r = data_frame.shape[0]
        for i in range(0, r):
            if data_frame['IT-CT'][i] <= ti:
                data_frame['CI'][i] = 1
        return data_frame,err
    else:
        err=True
        return data_frame,err

def clickspam(data_frame):
    data = data_frame['Site ID'].value_counts()
    r = data_frame.shape[0]
    count=0
    data_frame['CS'] = 3
    for i in range(0, r):
        try:
            if data_frame['CS'][i] == 3 and data_frame['Site ID'][i] != 'NaN':
                count = 0
                c = data_frame['Site ID'][i]
                d = math.floor(0.75 * data[c])
                for j in range(0, r):
                    if (data_frame['Site ID'][j] == data_frame['Site ID'][i] and data_frame['IT-CT'][j] < 7200):
                        count = count + 1
                if (count < d and data[c] > 30):
                    for k in range(0, r):
                        if (data_frame['Site ID'][k] == data_frame['Site ID'][i]):
                            data_frame['CS'][k] = 1
                else:
                    for k in range(0, r):
                        if (data_frame['Site ID'][k] == data_frame['Site ID'][i]):
                            data_frame['CS'][k] = 0
        except:
            pass


    return data_frame

def apkversioncheck(data_frame,apkv):
    data_frame['apkfraud']=1
    err=False
    r = data_frame.shape[0]
    d = apkv.split(".")
    try:
        for i in range(0, r):
            c = data_frame['App Version'][i].split(".")
            if int(c[0]) >= int(d[0]):
                if int(c[0]) == int(d[0]) and len(c) > 1 and len(d)>1:
                    if int(c[1]) >= int(d[1]):
                        if int(c[1]) == int(d[1]) and len(c) > 2 and len(d)>2:
                            if int(c[2]) >= int(d[2]):
                                data_frame['apkfraud'][i] = 0
                            else:
                                data_frame['apkfraud'][i] = 1
                        else:
                            data_frame['apkfraud'][i] = 0
                    else:
                        data_frame['apkfraud'][i] = 1
                else:
                    data_frame['apkfraud'][i] = 0
            else:
                data_frame['apkfraud'][i] = 1
    except:
        err=True
        return data_frame,err


    return data_frame,err

def sdkversioncheck(data_frame,sdkv):
    data_frame['sdkfraud']=1
    err=False
    r = data_frame.shape[0]
    d = sdkv.split(".")
    if d[0]=='4':
        d[0]='v4'
    try:
        for i in range(0, r):
            c = data_frame['SDK Version'][i].split(".")
            if c[0] == d[0]:
                if c[0] == d[0] and len(c) > 1 and len(d)>1:
                    if int(c[1]) >= int(d[1]):
                        if int(c[1]) == int(d[1]) and len(c) > 2 and len(d)>2:
                            if int(c[2]) >= int(d[2]):
                                data_frame['sdkfraud'][i] = 0
                            else:
                                data_frame['sdkfraud'][i] = 1
                        else:
                            data_frame['sdkfraud'][i] = 0
                    else:
                        data_frame['sdkfraud'][i] = 1
                else:
                    data_frame['sdkfraud'][i] = 0
            else:
                data_frame['sdkfraud'][i] = 1
    except:
        err=True
        return data_frame,err


    return data_frame,err


def osversioncheck(data_frame,osv,type):
    data_frame['osfraud']=1
    err=False
    r = data_frame.shape[0]
    d = osv.split(".")
    try:
        for i in range(0, r):
            if type==1:
                ce = data_frame['Os'][i].split(" ")
                c=ce[1].split(".")
            if type==0:
                try:
                    c = data_frame['OS Version'][i].split(".")
                except:
                    ce=data_frame['OS Version'][i]
                    c=[ce]
            if type==3:
                i=i+1
                ce = data_frame['Version'][i].split('=')
                c = ce[1].split('.')

            try:
                if int(c[0]) >= int(d[0]):
                    if int(c[0]) == int(d[0]) and len(c) > 1 and len(d) > 1:
                        if int(c[1]) >= int(d[1]):
                            if int(c[1]) == int(d[1]) and len(c) > 2 and len(d) > 2:
                                if int(c[2]) >= int(d[2]):
                                    data_frame['osfraud'][i] = 0
                                else:
                                    data_frame['osfraud'][i] = 1
                            else:
                                data_frame['osfraud'][i] = 0
                        else:
                            data_frame['osfraud'][i] = 1
                    else:
                        data_frame['osfraud'][i] = 0
                else:
                    data_frame['osfraud'][i] = 1
            except:
                pass
    except:
        err=True
        return data_frame,err


    return data_frame,err

def clickinject2(df,citime):
    df['ITd-CTd'] = 0
    df['IT-CT'] = 0
    df['CI'] = 0
    try:
        ti=int(citime[0][0])
    except:
        ti=15
        pass
    r = df.shape[0]
    for i in range(1, r + 1):
        try:
            df['ITd-CTd'][i] = (parser.parse(str(df['Inst DT'][i])) - parser.parse(str(df['Click DT'][i]))).days
            if int(df['ITd-CTd'][i]) == 0:
                dateTimeA = parser.parse(str(df['Install Time'][i]))
                dateTimeB = parser.parse(str(df['Attributed Touch Time'][i]))
                df['IT-CT'][i] = (dateTimeB - dateTimeA).seconds
                if df['IT-CT'][i] <= ti:
                    print("inside")
                    df['CI'][i] = 1
        except:
            pass
    return df
def clickspam2(df):
    data=df['Site ID'].value_counts()
    r = df.shape[0]
    count = 0
    df['CS'] = 0
    for i in range(1, r+1):
        if df['Site ID'][i] == 'NaN':
            df['CS'][i] = 1
        if data[df['Site ID'][i]] >= 30 and df['ITd-CTd'][i] == 0 and df['CS'][i]==0:
            d = math.floor(0.75 * data[df['Site ID'][i]])
            seriesObj = df.apply(lambda x: True if x['IT-CT'] < 7200 and x['Site ID'] == df['Site ID'][i] and x[
                'ITd-CTd'] == 0 else False, axis=1)
            numOfRows = len(seriesObj[seriesObj == True].index)
            if numOfRows < d:
                for j in range(1,r+1):
                    if df['Site ID'][i]==df['Site ID'][j]:
                        df['CS'][j] = 1
    return df
def summary(df,c):
    data=df['Site ID'].value_counts()
    dff = pd.DataFrame(data.keys())
    dff.rename(columns={0: 'Site ID'},inplace=True)
    dff['Total Installs']=0
    dff['CI count'] = 0
    dff['CS count']=0
    dff['osfraud total']=0
    dff['apkfraud total']=0
    dff['sdkfraud total']=0
    dff['Country Mismatches']=0

    j = 0
    for i in data.keys():
        de = df['CI'][df['Site ID'] == i].value_counts()
        dee=df['CS'][df['Site ID'] == i].value_counts()
        deee=df['osfraud'][df['Site ID'] == i].value_counts()
        if c==0:
            dec = df['Country Mismatch'][df['Site ID'] == i].value_counts()
            deef=df['apkfraud'][df['Site ID'] == i].value_counts()
            deeff=df['sdkfraud'][df['Site ID'] == i].value_counts()
        cv = df[df['Site ID'] == i].shape[0]
        dff['Total Installs'][j]=cv
        try:
            dff['CI count'][j] = de[1]
        except:
            pass
        try:
            dff['CS count'][j] = dee[1]
        except:
            pass
        try:
            dff['Country Mismatches'][j] = dec[1]
        except:
            pass
        try:
            dff['osfraud total'][j] = deee[1]
        except:
            pass
        try:
            dff['apkfraud total'][j] = deef[1]
        except:
            pass
        try:
            dff['sdkfraud total'][j] = deeff[1]
        except:
            pass
        j=j+1
    return dff

def countrycheck(df,ccode):
    try:
        countryy=ccode[0][0].split(" ")
        r = df.shape[0]
        df['Country Mismatch'] = 0
        for i in range(0, r):
            if df['Country Code'][i] not in countryy:
                df['Country Mismatch'][i] = 1
        return df
    except:
        df['Country Mismatch'] = 0
        return df
