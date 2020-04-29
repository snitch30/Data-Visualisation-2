# Data-Visualisation-2
### CS7DS4- COVID19- Visualisation

## Introduction 

COVID-19 has become a pandemic. The outbreak has affected millions of people directly by infection and almost everyone indirectly through their livelihoods, how people work, country’s GDP and growth rate amongst thousands of other factors. One of the key things required to beat this pandemic and to return back to normalcy is public awareness and people following WHO guidelines. This study/project hopes to increase the public awareness, by trying to answer few hypotheses as mentioned below using data visualisation with exploratory visualisations.

## Hypotheses

These hypotheses are what the readers of this visualisation can expect to find answers to.

1. What are the current Hotspot Countries (area with very high number of confirmed covid cases)? 
2. What are the current Hotspot Counties within USA?
(USA being the country with highest confirmed cases -as of 07/04/2020)
3. How fast did the cases in top 10 countries with highest confirmed cases? 
4. How fast the cases increased with the respect to increase in deaths?

All of these hypotheses are answered in the visualisation, with data as of 07-April-2020. First two hypothesis hopes to let the readers know the regions to be careful in. The next hypothesis hopes the reader to understand the speed and nature of the outbreak with respect to confirmed cases and deaths.

## Dataset

The main dataset used for this study is from CSSEGISandData- Data from Johns Hopkins Centre for Systems Science and Engineering. Due to the huge amount of data and different features/attributes the data has been split into different parts. In this study, four of them *cases*, *country*, *cases_time*, and *cases_state* were used.

*country* data has attributes like Country, Last Updated Time, Coordinates, Confirmed Cases, Deaths, Recovered and Active cases with 184 data points. cases_time data is similar to country however it has 14165 data points updates for two months. cases_state data and cases data are for specific to USA and has attributes like FIPS (Unique County Codes), Case Data, Province State amongst others.

In this project, all data used were those that were obtained on 07-April-2020 and stored offline.

In this project, we also use support dataset that supports the main dataset in a consistent visualisation. This includes *County Fips* dataset which accounts for all the counties and its FIPS codes in US. As the main dataset is live, this means there could be instances where the data is not present for some counties, which can be presented to the viewer with the help of this support dataset.

## Tools

This project is completely built on Python 3. We have used libraries on top Python to visualise. Libraries like Numpy and Pandas were used for handling data. Libraries like Plotly and Plotly Express were used for visualising the data.

## Running the Project

There are three ways of going through the visualisation.

- #### TO INTERACT WITH LARGE SIZED VISUALISATION

*The "outputs" Directory has four separate visualisation without any code, and the visualisation is large and very clear and can be accessed with any browser. The files need to be downloaded as **.html** files.*

- #### TO VIEW CODE AND INTERACT WITH MEDIUM SIZED VISUALISATION

*"Notebook.html" shows the code used as well as the output as medium sized, similar to a Jupiter notebook output and can be accessed with any browser. The file need to be downloaded as **.html** file.*

- #### TO RUN CODE AND INTERACT WITH LARGE SIZED VISUALISATION

To run the code and then see the visualisation, follow the below instructions.
The prerequisite for this run is **Python3**.

***STEP 1 IS IMPORTANT- FOR RELATIVE PATH TO WORK***
1. CHANGE DIRECTORY OF TERMINAL INTO PROJECT DIRECTORY (WORKING DIRECTORY)

2. INSTALL REQUIRED LIBRARY USING PYTHON

```
pip install -r requirements.txt
```

3. RUN CODE

```
python code/vis_code.py 
```
4. VISUALISATIONS ARE OPENED IN BROWSER AS WELL AS STORED IN OUTPUT FOLDER.
