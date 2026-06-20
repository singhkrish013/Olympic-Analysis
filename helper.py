import numpy as np
import pandas as pd

def fetch_medal_tally(df,years,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','City','Year','Sport','Event','Medal'])
    flag=0
    if years=='Overall' and country=='Overall':
        temp_df=medal_df
    if years=='Overall' and country!='Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if years!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(years)]
    if years!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(years)) & (medal_df['region']==country)]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total']=x['Gold']+x['Silver']+x['Bronze']
    print(x)
    return x




def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':col},inplace=True)
    return nations_over_time



def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    count_df = temp_df['Name'].value_counts().reset_index().head(15)
    count_df.columns = ['Name', 'Medals']
    count_df['Medals'] = count_df['Medals'].astype(str)

    merged_df = pd.merge(count_df, df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result_df = merged_df[['Name', 'Medals', 'Sport', 'region']]
    result_df.rename(columns={'Name': 'Athlete'}, inplace=True)

    return result_df



def yearwise_medal_tally(df,country):
    t2_df=df.dropna(subset=['Medal'])
    t2_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    nt2_df=t2_df[t2_df['region']==country]
    final_nt2_df=nt2_df.groupby('Year').count()['Medal'].reset_index()

    #pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return final_nt2_df

def country_event_heatmap(df,country):
    t3_df=df.dropna(subset=['Medal'])
    t3_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    nt3_df=t3_df[t3_df['region']=='India']

    pt = nt3_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    
    temp_df = temp_df[temp_df['region'] == country]

    count_df = temp_df['Name'].value_counts().reset_index().head(15)
    count_df.columns = ['Name', 'Medals']
    count_df['Medals'] = count_df['Medals'].astype(str)

    merged_df = pd.merge(count_df, df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result_df = merged_df[['Name', 'Medals', 'Sport']]
    result_df.rename(columns={'Name': 'Athlete'}, inplace=True)

    return result_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        t4_df = athlete_df[athlete_df['Sport'] == sport]
        return t4_df
    else:
        return athlete_df
    

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
