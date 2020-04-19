# Imports
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px
from urllib.request import urlopen
import json
import warnings
import os
pio.templates.default = "plotly_dark"

# Dataset
path='data/'
opath='outputs/'
country_csv=path+'cov_country.csv'
time_csv=path+'cov_day.csv'
cov_state=path+'cov_state.csv'
cov_county=path+'cov_county.csv'
fips_path=path+'county_fips_master.csv'
country_pd=pd.read_csv(country_csv)
time_pd=pd.read_csv(time_csv,parse_dates=['Last_Update'])
n_state_pd=pd.read_csv(cov_state)
county_pd=pd.read_csv(cov_county,dtype={"FIPS": str})
fips_pd=pd.read_csv(fips_path,dtype={"fips":str},encoding = "ISO-8859-1")
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
warnings.filterwarnings("ignore")
print("Please Wait....")


#Preprocessing
# The Country names are changed according to norms so that Plotly Express is able to use them to plot correctly.
def change_country_name(dataframe):
  for a in range(len(dataframe['Country_Region'])):
    if(dataframe['Country_Region'][a]=="US"):
      dataframe['Country_Region'][a]="USA"
    if(dataframe['Country_Region'][a]=="Taiwan*"):
      dataframe['Country_Region'][a]="Taiwan"
    if(dataframe['Country_Region'][a]=="Korea, South"):
      dataframe['Country_Region'][a]="South Korea"
    if(dataframe['Country_Region'][a]=="Congo (Kinshasa)"):
      dataframe['Country_Region'][a]="Democratic Republic of the Congo"
    if(dataframe['Country_Region'][a]=="Congo (Brazzaville)"):
      dataframe['Country_Region'][a]="Repubic of the Congo"
    if(dataframe['Country_Region'][a]=="Bahamas, The"):
      dataframe['Country_Region'][a]="Bahamas"
    if(dataframe['Country_Region'][a]=="Cote d'Ivoire"):
      dataframe['Country_Region'][a]="Côte d'Ivoire"
    if(dataframe['Country_Region'][a]=="Gambia, The"):
      dataframe['Country_Region'][a]="Gambia"
    if(dataframe['Country_Region'][a]=="Reunion"):
      dataframe['Country_Region'][a]="Réunion"
  return dataframe
country_pd=change_country_name(country_pd)
time_pd=change_country_name(time_pd)
country_df=country_pd.copy()
del country_df['Last_Update']
del country_df['Lat']
del country_df['Long_']

#Function1
def calc_day_increase():
    flag="Afghanistan"
    inc=[]
    for i in range(len(time_pd)):
        if(time_pd["Country_Region"][i]==flag):
            if(i!=0):
                if(time_pd["Country_Region"][i-1]==flag):
                    inc.append(time_pd.loc[i,"Confirmed"]-time_pd.loc[i-1,"Confirmed"])
                else:
                    inc.append(time_pd.loc[i,"Confirmed"])
            else:
                inc.append(time_pd.loc[i,"Confirmed"])
        else:
            inc.append(time_pd.loc[i,"Confirmed"])
            flag=time_pd["Country_Region"][i]
    inc=pd.DataFrame(inc)
    inc=inc.rename(columns={0:"Daily Increase"})
    return inc
inc=calc_day_increase()
new_time_pd=pd.concat([time_pd,inc],axis=1)

#Function2
def vis_process(df_data):
    df_data = df_data.groupby(['Last_Update', 'Country_Region','Daily Increase','Deaths'])['Confirmed'].max()
    df_data=df_data.reset_index()
    df_data["Last_Update"] = pd.to_datetime(df_data["Last_Update"]).dt.strftime('%d/%m/%Y')
    mod=np.sqrt(df_data["Confirmed"])
    mod=pd.DataFrame(mod).rename(columns={"Confirmed":"Square Root(Confirmed Cases)"})
    mod2=np.log10(df_data["Confirmed"]+1)
    mod2=pd.DataFrame(mod2).rename(columns={"Confirmed":"Log(Confirmed Cases)"})
    df_data=pd.concat([df_data,mod,mod2],axis=1)
    return df_data
df_data=vis_process(new_time_pd)
df_data.head()

#Visualisation 1
fig = px.scatter_geo(df_data, locations="Country_Region", locationmode='country names',
                     color="Square Root(Confirmed Cases)" ,
                     size= "Square Root(Confirmed Cases)",
                     hover_name="Country_Region",
                     hover_data=["Confirmed"],
                     range_color= [0, max(df_data["Square Root(Confirmed Cases)"])],
                     projection="natural earth", animation_frame="Last_Update",
                     color_continuous_scale="Viridis",
                     title='Coronavirus- Total Confirmed Cases as of April 07 2020.',
                     size_max=50
                    )
fig.update(layout_coloraxis_showscale=True)
print("Processed Visualisation 1.")


#Visualisation 2
df_data2 = new_time_pd.groupby(['Country_Region'])['Confirmed'].max()
max_df=df_data2.nlargest(10,keep="first")
top10countries=list(max_df.index.values)
new_list=[]
for a in range(len(time_pd)):
    if time_pd['Country_Region'][a] in top10countries:
        new_list.append(new_time_pd.iloc[a,:])
top10=pd.DataFrame(new_list)
top10['Confirmed']=top10['Confirmed']+1
df_small_data=vis_process(top10)
df_small_data.head()
fig2=px.scatter(df_small_data, x="Last_Update", y="Square Root(Confirmed Cases)", animation_frame="Last_Update", animation_group="Country_Region",
            size="Confirmed",color="Country_Region", hover_name="Country_Region",
           log_x=False, size_max=65, range_x=[0,90], range_y=[-10,700],
               title="Top 10 Countries (as of April 07 2020)- Cases over Time.",color_continuous_scale="Viridis")
fig2.update_xaxes(showticklabels=False)
fig2.update(layout_coloraxis_showscale=True)
print("Processed Visualisation 2.")

#Visualisation 3
df_data3 = new_time_pd.groupby(['Country_Region'])['Confirmed'].max()
max_df=df_data3.nlargest(10,keep="first")
top20countries=list(max_df.index.values)
new_list=[]
for a in range(len(time_pd)):
    if time_pd['Country_Region'][a] in top20countries:
        new_list.append(new_time_pd.iloc[a,:])
top20=pd.DataFrame(new_list)
top20['Confirmed']=top20['Confirmed']+1
df_med_data=vis_process(top20)
df_med_data.head()
fig3=px.scatter(df_med_data, x="Deaths", y="Daily Increase", animation_frame="Last_Update", animation_group="Country_Region",
            size="Confirmed",color="Country_Region", hover_name="Country_Region",
           log_x=False, size_max=65, range_x=[0,20000], range_y=[-10,32000],
               title="Top 10 Countries- Daily Increase vs Total Deaths",color_continuous_scale="Viridis")
fig3.update_xaxes(showticklabels=True)
fig3.update(layout_coloraxis_showscale=True)
print("Processed Visualisation 3.")

#Visualisation 4
state_pd=n_state_pd[n_state_pd["Country_Region"]=="US"]
state_pd=state_pd.reset_index()
final_df=county_pd.groupby(['Admin2', 'Province_State','FIPS'])['Confirmed','Deaths'].max()
final_df=final_df.reset_index()
final_df=final_df.rename(columns={"Confirmed":"Confirmed_County","Deaths":"Deaths_County"})
new_tot_conf=[]
new_tot_death=[]
data_abs=[]
for index1 in range(final_df.shape[0]):
    for index2 in range(state_pd.shape[0]):
        if(final_df['Province_State'][index1]==state_pd['Province_State'][index2]):
            new_tot_conf.append(state_pd['Confirmed'][index2])
            new_tot_death.append(state_pd['Deaths'][index2])
            data_abs.append("False")
new_tot_conf=pd.DataFrame(new_tot_conf).rename(columns={0:"Confirmed_State"})
new_tot_death=pd.DataFrame(new_tot_death).rename(columns={0:"Deaths_State"})
data_abs=pd.DataFrame(data_abs).rename(columns={0:"Data Absent?"})
new_cols=[final_df,new_tot_conf,new_tot_death,data_abs]
final_df=pd.concat(new_cols,axis=1)
final_df=final_df.rename(columns={"Admin2":"County"})
final_df['Ratio']=round(final_df['Confirmed_County']/final_df['Confirmed_State'],2)
datalist=[]
intermediate_dataframe=fips_pd[~fips_pd['fips'].isin(final_df['FIPS'])]
intermediate_dataframe=intermediate_dataframe.reset_index(drop=True)
for index1 in range(intermediate_dataframe.shape[0]):
    datalist.append([intermediate_dataframe['county_name'][index1][:-7],intermediate_dataframe['state_name'][index1],intermediate_dataframe['fips'][index1],0,0,0,0,"True",-0.5])
missed_data=pd.DataFrame(datalist)
missed_data=missed_data.rename(columns={0:"County",1:"Province_State",2:"FIPS",3:"Confirmed_County",4:"Deaths_County",5:"Confirmed_State",6:"Deaths_State",7:"Data Absent?",8:"Ratio"})
final_df=final_df.append(missed_data,ignore_index=True)

fig4 = px.choropleth(final_df, geojson=counties, locations='FIPS', color='Ratio',
                           color_continuous_scale="Viridis",
                           range_color=(-0.4, 0.4),
                           scope="usa",hover_name="County", hover_data=["Province_State","Confirmed_State", "Confirmed_County","Deaths_County","Deaths_State","Data Absent?"]
                          )
fig4.update_layout(margin={"r":0,"l":0,"b":10})
fig4.update_layout(title_text='County Hotspots within every States in USA (as of April 08 2020)')
fig4.update(layout_coloraxis_showscale=True)
print("Processed Visualisation 4.")

#Visualise All
fig.show()
fig2.show()
fig3.show()
fig4.show()

#Save all visualisations as HTML files
fig.write_html(opath+"vis1.html")
fig2.write_html(opath+"vis2.html")
fig3.write_html(opath+"vis3.html")
fig4.write_html(opath+"vis4.html")
print('Outputs are opened in Browser and also store in output directory.')
