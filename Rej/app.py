from flask import Flask,render_template,request
res=""


import pandas as pd
import numpy as np


import numpy as np
xls = pd.ExcelFile('Sports news (1).xlsx')

tnassocric = pd.read_excel(xls, 'TNAssoCricket')


cricongoing = pd.read_excel(xls, 'CricketOngoing',names=['Status', 'Name', 'Date','Location'])


cricupcoming = pd.read_excel(xls, 'CricketUpcoming',names=['Status', 'Name', 'Date','Location'])


ind = pd.read_excel('in.xlsx')


ind.drop(['lat','lng','iso2','population','population_proper'], axis =1, inplace=True)



cricongoing['Location'].value_counts()

cricupcoming['Location'].value_counts()


ind.rename(columns = {'city':'Location'}, inplace = True)


def change_column_order(df, col_name, index):
    cols = df.columns.tolist()
    cols.remove(col_name)
    cols.insert(index, col_name)
    return df[cols]

def split_df(dataframe, col_name, sep):
    orig_col_index = dataframe.columns.tolist().index(col_name)
    orig_index_name = dataframe.index.name
    orig_columns = dataframe.columns
    dataframe = dataframe.reset_index()  # we need a natural 0-based index for proper merge
    index_col_name = (set(dataframe.columns) - set(orig_columns)).pop()
    df_split = pd.DataFrame(
        pd.DataFrame(dataframe[col_name].str.split(sep).tolist())
        .stack().reset_index(level=1, drop=1), columns=[col_name])
    df = dataframe.drop(col_name, axis=1)
    df = pd.merge(df, df_split, left_index=True, right_index=True, how='inner')
    df = df.set_index(index_col_name)
    df.index.name = orig_index_name
    # merge adds the column to the last place, so we need to move it back
    return change_column_order(df, col_name, orig_col_index)
cricongoingsplit = split_df(cricongoing , 'Location', ',')
cricongoingsplit = pd.DataFrame(cricongoingsplit)

cricongoingsplit= cricongoingsplit.sort_values('Location')

cricupcomingsplit = split_df(cricupcoming , 'Location', ',')
cricupcomingsplit = pd.DataFrame(cricupcomingsplit)

cricupcomingsplit= cricupcomingsplit.sort_values('Location')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Bengaluru (Bangalore)'], 'Bangalore')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Ambikapur (Chhattisgarh)'], 'Ambikapur')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Ara (Bihar)'], 'Ara')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Ara (Jharkhand)'], 'Ara')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Ashta (Madhya Pradesh)'], 'Ashta')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Aurangabad (Bihar)'], 'Aurangabad')

cricongoingsplit['Location'] = cricongoingsplit['Location'].replace(['Aurangabad (Maharashtra)'], 'Aurangabad')

cricongoingmerge = cricongoingsplit.merge(ind[['Location', 'admin_name','country']], on = 'Location', how = 'left')

cricongoingmerge[cricongoingmerge['country'].isna()]
cricongoingmerge = cricongoingmerge[cricongoingmerge['country'].notna()]

cricongoingmerge.reset_index()





cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Bengaluru (Bangalore)'], 'Bangalore')


cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Ambikapur (Chhattisgarh)'], 'Ambikapur')

cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Ara (Bihar)'], 'Ara')

cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Ara (Jharkhand)'], 'Ara')

cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Ashta (Madhya Pradesh)'], 'Ashta')

cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Aurangabad (Bihar)'], 'Aurangabad')

cricupcomingsplit['Location'] = cricupcomingsplit['Location'].replace(['Aurangabad (Maharashtra)'], 'Aurangabad')

cricupcomingmerge = cricupcomingsplit.merge(ind[['Location', 'admin_name','country']], on = 'Location', how = 'left')

cricupcomingmerge[cricupcomingmerge['country'].isna()]
cricupcomingmerge = cricupcomingmerge[cricupcomingmerge['country'].notna()]

cricupcomingmerge.reset_index()

def ret(location): 
 df2 = cricupcomingmerge[cricupcomingmerge["Location"]==location]
 df2.iloc[:,[0,1,2,3,4,5]]
 df1 = cricongoingmerge[cricongoingmerge["Location"]==location]
 df1.iloc[:,[0,1,2,3,4,5]]
 frames = [df1, df2]
 result = pd.concat(frames)
 print(result)
 data = tuple(result.itertuples(index=False,name =None))
 
 return data
 

 

from flask import Flask,render_template

app=Flask(__name__,template_folder='template',static_folder='static')

@app.route("/")

def hello():
  
   return render_template('register.html')



@app.route("/",methods=['POST'])
def info():
   global res
   if request.method=="POST":
     location = request.form['Location']
     headingss=("Status","Name","Date","Location","State","Country")
     result = ret(location)
     res=result
     
     
   return render_template('register.html',data=res,headings = headingss)
if __name__ == '__main__':
    app.run(port=3000,debug=True)





