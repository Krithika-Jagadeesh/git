import pandas as pd
import json
import os
from mysql.connector import connect 
from sqlalchemy import create_engine


# Creating the path for aggregated insurance state list to verify working good or not.

# In[58]:


path_agg_in = r"E:\guvi\Project_2\pulse\data\aggregated\insurance\country\india\state"
agg_in_state_list = os.listdir(path_agg_in)
agg_in_state_list


# Creating rest 8 paths till state.

# In[59]:


path_agg_tr = r"E:\guvi\Project_2\pulse\data\aggregated\transaction\country\india\state"

path_agg_us = r"E:\guvi\Project_2\pulse\data\aggregated\user\country\india\state"

path_map_in = r"E:\guvi\Project_2\pulse\data\map\insurance\hover\country\india\state"

path_map_tr = r"E:\guvi\Project_2\pulse\data\map\transaction\hover\country\india\state"

path_map_us = r"E:\guvi\Project_2\pulse\data\map\user\hover\country\india\state"

path_top_in = r"E:\guvi\Project_2\pulse\data\top\insurance\country\india\state"

path_top_tr = r"E:\guvi\Project_2\pulse\data\top\transaction\country\india\state"

path_top_us = r"E:\guvi\Project_2\pulse\data\top\user\country\india\state"


# Creating state list for rest 8 paths.

# In[60]:


agg_tr_state_list = os.listdir(path_agg_tr)
print(agg_tr_state_list)

agg_us_state_list = os.listdir(path_agg_us)
print(agg_us_state_list)

map_in_state_list = os.listdir(path_map_in)
print(map_in_state_list)

map_tr_state_list = os.listdir(path_map_tr)
print(map_tr_state_list)

map_in_state_list = os.listdir(path_map_in)
print(map_in_state_list)

map_us_state_list = os.listdir(path_map_us)
print(map_us_state_list)

top_in_state_list = os.listdir(path_top_in)
print(top_in_state_list)

top_tr_state_list = os.listdir(path_top_tr)
print(top_tr_state_list)

top_us_state_list = os.listdir(path_top_us)
print(top_us_state_list)


# Creating 9 dataframes by extracting data from all 9 files.

# In[61]:


# Extracting data from aggregated insurance json file

agg_in_clm = {'State':[], 'Year':[],'Quarter':[],'Insurance_Type':[], 'Insurance_Count':[], 'Insurance_Amount':[]}

for state in agg_in_state_list:
    p1_state = os.path.join(path_agg_in, state)
    agg_in_yr = os.listdir(p1_state)

    for year in agg_in_yr:
        p1_year = os.path.join(p1_state, year)
        agg_in_yr_list = os.listdir(p1_year)

        for quarter in agg_in_yr_list:
            p1_quarter = os.path.join(p1_year, quarter)
            data_1 = open(p1_quarter, 'r')
            d1 = json.load(data_1)

            for z in d1['data']['transactionData']:
                name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                agg_in_clm['Insurance_Type'].append(name)
                agg_in_clm['Insurance_Count'].append(count)
                agg_in_clm['Insurance_Amount'].append(amount)
                agg_in_clm['State'].append(state)
                agg_in_clm['Year'].append(year)
                agg_in_clm['Quarter'].append(int(quarter.strip('.json')))

agg_in_df = pd.DataFrame(agg_in_clm)
agg_in_df


# In[62]:


# Extracting data from aggregated transaction json file

agg_tr_clm = {'State':[], 'Year':[],'Quarter':[],'Transaction_Type':[], 'Transaction_Count':[], 'Transaction_Amount':[]}

for state in agg_tr_state_list:
    p2_state = os.path.join(path_agg_tr, state)
    agg_tr_yr = os.listdir(p2_state)

    for year in agg_tr_yr:
        p2_year = os.path.join(p2_state, year)
        agg_tr_yr_list = os.listdir(p2_year)

        for quarter in agg_tr_yr_list:
            p2_quarter = os.path.join(p2_year, quarter)
            data_2 = open(p2_quarter, 'r')
            d2 = json.load(data_2)

            for z in d2['data']['transactionData']:
                name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                agg_tr_clm['Transaction_Type'].append(name)
                agg_tr_clm['Transaction_Count'].append(count)
                agg_tr_clm['Transaction_Amount'].append(amount)
                agg_tr_clm['State'].append(state)
                agg_tr_clm['Year'].append(year)
                agg_tr_clm['Quarter'].append(int(quarter.strip('.json')))

agg_tr_df = pd.DataFrame(agg_tr_clm)
agg_tr_df


# In[63]:


# Extracting data from aggregated user json file

agg_us_clm = {'State':[], 'Year':[],'Quarter':[],'User_Brand':[], 'User_Count':[], 'User_Percentage':[]}

for state in agg_us_state_list:
    p3_state = os.path.join(path_agg_us, state)
    agg_us_yr = os.listdir(p3_state)

    for year in agg_us_yr:
        p3_year = os.path.join(p3_state, year)
        agg_us_yr_list = os.listdir(p3_year)

        for quarter in agg_us_yr_list:
            p3_quarter = os.path.join(p3_year, quarter)
            data_3 = open(p3_quarter, 'r')
            d3 = json.load(data_3)

            users = d3.get('data', {}).get('usersByDevice')
            if users:
                for z in users:
                    brand = z.get('brand', 'Unknown')
                    count = z.get('count', 0)
                    percentage = z.get('percentage', 0.0)
                    agg_us_clm['User_Brand'].append(brand)
                    agg_us_clm['User_Count'].append(count)
                    agg_us_clm['User_Percentage'].append(percentage)
                    agg_us_clm['State'].append(state)
                    agg_us_clm['Year'].append(year)
                    agg_us_clm['Quarter'].append(int(quarter.replace('.json', '')))

agg_us_df = pd.DataFrame(agg_us_clm)
agg_us_df


# In[64]:


# Extracting data from map insurance json file

map_in_clm = {'State':[], 'Year':[],'Quarter':[],'Insurance_Place':[], 'Insurance_Count':[], 'Insurance_Amount':[]}

for state in map_in_state_list:
    p4_state = os.path.join(path_map_in, state)
    map_in_yr = os.listdir(p4_state)

    for year in map_in_yr:
        p4_year = os.path.join(p4_state, year)
        map_in_yr_list = os.listdir(p4_year)

        for quarter in map_in_yr_list:
            p4_quarter = os.path.join(p4_year, quarter)
            data_4 = open(p4_quarter, 'r')
            d4 = json.load(data_4)

            for z in d4['data']['hoverDataList']:
                name = z['name']
                count = z['metric'][0]['count']
                amount = z['metric'][0]['amount']
                map_in_clm['Insurance_Place'].append(name)
                map_in_clm['Insurance_Count'].append(count)
                map_in_clm['Insurance_Amount'].append(amount)
                map_in_clm['State'].append(state)
                map_in_clm['Year'].append(year)
                map_in_clm['Quarter'].append(int(quarter.strip('.json')))

map_in_df = pd.DataFrame(map_in_clm)
map_in_df


# In[65]:


# Extracting data from map transaction json file

map_tr_clm = {'State':[], 'Year':[],'Quarter':[],'Transaction_Place':[], 'Transaction_Count':[], 'Transaction_Amount':[]}

for state in map_tr_state_list:
    p5_state = os.path.join(path_map_tr, state)
    map_tr_yr = os.listdir(p5_state)

    for year in map_tr_yr:
        p5_year = os.path.join(p5_state, year)
        map_tr_yr_list = os.listdir(p5_year)

        for quarter in map_tr_yr_list:
            p5_quarter = os.path.join(p5_year, quarter)
            data_5 = open(p5_quarter, 'r')
            d5 = json.load(data_5)

            for z in d5['data']['hoverDataList']:
                name = z['name']
                count = z['metric'][0]['count']
                amount = z['metric'][0]['amount']
                map_tr_clm['Transaction_Place'].append(name)
                map_tr_clm['Transaction_Count'].append(count)
                map_tr_clm['Transaction_Amount'].append(amount)
                map_tr_clm['State'].append(state)
                map_tr_clm['Year'].append(year)
                map_tr_clm['Quarter'].append(int(quarter.strip('.json')))

map_tr_df = pd.DataFrame(map_tr_clm)
map_tr_df


# In[66]:


# Extracting data from map user json file

map_us_clm = {'State':[], 'Year':[],'Quarter':[],'District_Title':[], 'Registered_Users':[], 'App_Opens':[]}

for state in map_us_state_list:
    p6_state = os.path.join(path_map_us, state)
    map_us_yr = os.listdir(p6_state)

    for year in map_us_yr:
        p6_year = os.path.join(p6_state, year)
        map_us_yr_list = os.listdir(p6_year)

        for quarter in map_us_yr_list:
            p6_quarter = os.path.join(p6_year, quarter)
            data_6 = open(p6_quarter, 'r')
            d6 = json.load(data_6)

            for district, z in d6['data']['hoverData'].items():
                registeredUsers = z['registeredUsers']
                appOpens = z['appOpens']
                map_us_clm['District_Title'].append(district.title())
                map_us_clm['Registered_Users'].append(registeredUsers)
                map_us_clm['App_Opens'].append(appOpens)
                map_us_clm['State'].append(state)
                map_us_clm['Year'].append(year)
                map_us_clm['Quarter'].append(int(quarter.strip('.json')))

map_us_df = pd.DataFrame(map_us_clm)
map_us_df


# In[67]:


# Extracting data from top insurance json file

top_in_clm = {'State':[], 'Year':[], 'Quarter':[], 'District':[], 'Pincode':[], 'Insurance_Count':[], 'Insurance_Amount':[]}

for state in top_in_state_list:
    p7_state = os.path.join(path_top_in, state)
    top_in_yr = os.listdir(p7_state)

    for year in top_in_yr:
        p7_year = os.path.join(p7_state, year)
        top_in_yr_list = os.listdir(p7_year)

        for quarter in top_in_yr_list:
            p7_quarter = os.path.join(p7_year, quarter)
            data_7 = open(p7_quarter, 'r')
            d7 = json.load(data_7)

            for z in d7['data']['pincodes']:
                name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                top_in_clm['District'].append(None)
                top_in_clm['Pincode'].append(name)
                top_in_clm['Insurance_Count'].append(count)
                top_in_clm['Insurance_Amount'].append(amount)
                top_in_clm['State'].append(state)
                top_in_clm['Year'].append(year)
                top_in_clm['Quarter'].append(int(quarter.strip('.json')))

            for z in d7['data']['districts']:
                name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                top_in_clm['District'].append(name)
                top_in_clm['Pincode'].append(None)
                top_in_clm['Insurance_Count'].append(count)
                top_in_clm['Insurance_Amount'].append(amount)
                top_in_clm['State'].append(state)
                top_in_clm['Year'].append(year)
                top_in_clm['Quarter'].append(int(quarter.strip('.json')))

top_in_df = pd.DataFrame(top_in_clm)
top_in_df


# In[68]:


# Extracting data from top transaction json file

top_tr_clm = {'State':[], 'Year':[], 'Quarter':[], 'District':[], 'Pincode':[], 'Transaction_Count':[], 'Transaction_Amount':[]}

for state in top_tr_state_list:
    p8_state = os.path.join(path_top_tr, state)
    top_tr_yr = os.listdir(p8_state)

    for year in top_tr_yr:
        p8_year = os.path.join(p8_state, year)
        top_tr_yr_list = os.listdir(p8_year)

        for quarter in top_tr_yr_list:
            p8_quarter = os.path.join(p8_year, quarter)
            data_8 = open(p8_quarter, 'r')
            d8 = json.load(data_8)

            for z in d8['data']['pincodes']:
                name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                top_tr_clm['District'].append(None)
                top_tr_clm['Pincode'].append(name)
                top_tr_clm['Transaction_Count'].append(count)
                top_tr_clm['Transaction_Amount'].append(amount)
                top_tr_clm['State'].append(state)
                top_tr_clm['Year'].append(year)
                top_tr_clm['Quarter'].append(int(quarter.strip('.json')))

            for z in d8['data']['districts']:
                name = z['entityName']
                count = z['metric']['count']
                amount = z['metric']['amount']
                top_tr_clm['District'].append(name)
                top_tr_clm['Pincode'].append(None)
                top_tr_clm['Transaction_Count'].append(count)
                top_tr_clm['Transaction_Amount'].append(amount)
                top_tr_clm['State'].append(state)
                top_tr_clm['Year'].append(year)
                top_tr_clm['Quarter'].append(int(quarter.strip('.json')))

top_tr_df = pd.DataFrame(top_tr_clm)
top_tr_df


# In[69]:


# Extracting data from top user json file

top_us_clm = {'State':[], 'Year':[], 'Quarter':[], 'District':[], 'Pincode':[], 'Registered_Users':[]}

for state in top_us_state_list:
    p9_state = os.path.join(path_top_us, state)
    top_us_yr = os.listdir(p9_state)

    for year in top_us_yr:
        p9_year = os.path.join(p9_state, year)
        top_us_yr_list = os.listdir(p9_year)

        for quarter in top_us_yr_list:
            p9_quarter = os.path.join(p9_year, quarter)
            data_9 = open(p9_quarter, 'r')
            d9 = json.load(data_9)

            for z in d9['data']['pincodes']:
                name = z['name']
                count = z['registeredUsers']
                top_us_clm['District'].append(None)
                top_us_clm['Pincode'].append(name)
                top_us_clm['Registered_Users'].append(count)
                top_us_clm['State'].append(state)
                top_us_clm['Year'].append(year)
                top_us_clm['Quarter'].append(int(quarter.strip('.json')))

            for z in d9['data']['districts']:
                name = z['name']
                count = z['registeredUsers']
                top_us_clm['District'].append(name)
                top_us_clm['Pincode'].append(None)
                top_us_clm['Registered_Users'].append(count)
                top_us_clm['State'].append(state)
                top_us_clm['Year'].append(year)
                top_us_clm['Quarter'].append(int(quarter.strip('.json')))

top_us_df = pd.DataFrame(top_us_clm)
top_us_df


# Connecting with SQL

# In[70]:


connection = connect(
    host = 'localhost',
    port = '3306',
    user = 'root',
    password = '123456',
    database = 'phonepe'
)

print(connection.is_connected())


# In[71]:


cursor = connection.cursor()


# Inserting all 9 dataframes into SQL

# In[76]:


engine = create_engine('mysql+pymysql://root:123456@localhost:3306/phonepe')

agg_in_df.to_sql(name = 'aggregated_insurance', con = engine, if_exists = 'replace', index = False)
agg_tr_df.to_sql(name = 'aggregated_transaction', con = engine, if_exists = 'replace', index = False)
agg_us_df.to_sql(name = 'aggregated_user', con = engine, if_exists = 'replace', index = False)

map_in_df.to_sql(name = 'map_insurance', con = engine, if_exists = 'replace', index = False)
map_tr_df.to_sql(name = 'map_transaction', con = engine, if_exists = 'replace', index = False)
map_us_df.to_sql(name = 'map_user', con = engine, if_exists = 'replace', index = False)

top_in_df.to_sql(name = 'top_insurance', con = engine, if_exists = 'replace', index = False)
top_tr_df.to_sql(name = 'top_transaction', con = engine, if_exists = 'replace', index = False)
top_us_df.to_sql(name = 'top_user', con = engine, if_exists = 'replace', index = False)

