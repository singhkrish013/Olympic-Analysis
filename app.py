import streamlit as st
import pandas as pd
import preprocessor,helper

import altair as alt


import matplotlib.pyplot as plt
import seaborn as sns

import plotly.figure_factory as ff
import plotly.express as px


df = pd.read_csv('Datasets/athlete_events.csv')
region_df = pd.read_csv('Datasets/noc_regions.csv')


df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://www.freepnglogos.com/uploads/olympic-rings-png/olympic-rings-logos-download-0.png')
user_menu=st.sidebar.radio(
    'SELECT AN OPTION',('MEDAL TALLY','OVERALL ANALYSIS','COUNTRY-WISE ANALYSIS','ATHLETE-WISE ANALYSIS')
)


if user_menu=='MEDAL TALLY':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " +str(selected_year) + " Olympics")
    
    st.table(medal_tally)

if user_menu == 'OVERALL ANALYSIS':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')

    
    # Define the hover selection parameter (Altair 5 syntax)
    hover = alt.param(
        name="hover",
        select={
            "type": "point",
            "on": "mouseover",
            "fields": ["Edition"],
            "nearest": True
        }
    )

    # Base line chart
    base = alt.Chart(nations_over_time).mark_line(point=True).encode(
        x="Edition",
        y="region"
    )

    # Invisible points to trigger selection
    points = base.mark_point(opacity=0).add_params(hover)

    # Highlighted points on the line
    highlight_points = alt.Chart(nations_over_time).mark_point(color="red", size=100).encode(
        x="Edition",
        y="region",
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    nations_over_time["label"] = (
        "Edition: " + nations_over_time["Edition"].astype(str) +
        ", region: " + nations_over_time["region"].astype(str)
    )


    # Labels near points
    labels = alt.Chart(nations_over_time).mark_text(align="left", dx=5, dy=-5).encode(
        x="Edition",
        y="region",
        text=alt.condition(hover, "label:N", alt.value("")),
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    # Vertical rule at selected Edition
    rule = alt.Chart(nations_over_time).mark_rule(color="gray", strokeDash=[5, 5]).encode(
        x="Edition"
    ).transform_filter(hover)

    # Final chart with all layers
    chart = alt.layer(base, points, highlight_points, labels, rule).properties(
        title="Number of Participating Countries Over Editions",
        width=700,
        height=400
    )
    st.title("Participation Nations Over The Years")
    st.altair_chart(chart, use_container_width=True)
   

    Events_over_time = helper.data_over_time(df,'Event')

    
    # Define the hover selection parameter (Altair 5 syntax)
    hover = alt.param(
        name="hover",
        select={
            "type": "point",
            "on": "mouseover",
            "fields": ["Edition"],
            "nearest": True
        }
    )

    # Base line chart
    base = alt.Chart(Events_over_time).mark_line(point=True).encode(
        x="Edition",
        y="Event"
    )

    # Invisible points to trigger selection
    points = base.mark_point(opacity=0).add_params(hover)

    # Highlighted points on the line
    highlight_points = alt.Chart(Events_over_time).mark_point(color="red", size=100).encode(
        x="Edition",
        y="Event",
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    Events_over_time["label"] = (
        "Edition: " + Events_over_time["Edition"].astype(str) +
        ", Event: " + Events_over_time["Event"].astype(str)
    )


    # Labels near points
    labels = alt.Chart(Events_over_time).mark_text(align="left", dx=5, dy=-5).encode(
        x="Edition",
        y="Event",
        text=alt.condition(hover, "label:N", alt.value("")),
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    # Vertical rule at selected Edition
    rule = alt.Chart(Events_over_time).mark_rule(color="gray", strokeDash=[5, 5]).encode(
        x="Edition"
    ).transform_filter(hover)

    # Final chart with all layers
    chart = alt.layer(base, points, highlight_points, labels, rule).properties(
        title="Number of Events Over Editions",
        width=700,
        height=400
    )
    st.title("Events Over The Years")
    st.altair_chart(chart, use_container_width=True)





    athletes_over_time = helper.data_over_time(df,'Name')

    
    # Define the hover selection parameter (Altair 5 syntax)
    hover = alt.param(
        name="hover",
        select={
            "type": "point",
            "on": "mouseover",
            "fields": ["Edition"],
            "nearest": True
        }
    )

    # Base line chart
    base = alt.Chart(athletes_over_time).mark_line(point=True).encode(
        x="Edition",
        y="Name"
    )

    # Invisible points to trigger selection
    points = base.mark_point(opacity=0).add_params(hover)

    # Highlighted points on the line
    highlight_points = alt.Chart(athletes_over_time).mark_point(color="red", size=100).encode(
        x="Edition",
        y="Name",
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    athletes_over_time["label"] = (
        "Edition: " + athletes_over_time["Edition"].astype(str) +
        ", Name: " + athletes_over_time["Name"].astype(str)
    )


    # Labels near points
    labels = alt.Chart(athletes_over_time).mark_text(align="left", dx=5, dy=-5).encode(
        x="Edition",
        y="Name",
        text=alt.condition(hover, "label:N", alt.value("")),
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    # Vertical rule at selected Edition
    rule = alt.Chart(athletes_over_time).mark_rule(color="gray", strokeDash=[5, 5]).encode(
        x="Edition"
    ).transform_filter(hover)

    # Final chart with all layers
    chart = alt.layer(base, points, highlight_points, labels, rule).properties(
        title="Number of Athletes Over Editions",
        width=700,
        height=400
    )
    st.title("Athletes Over The Years")
    st.altair_chart(chart, use_container_width=True)




    st.title("Number of Events Over Time--[Every Sport]")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    msa=helper.most_successful(df,selected_sport)
    st.table(msa)
#-------------------------------------------------------

if user_menu == 'COUNTRY-WISE ANALYSIS':

    st.sidebar.title('COUNTRY-WISE ANALYSIS')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    

    country_df = helper.yearwise_medal_tally(df,selected_country)


# Define the hover selection parameter (Altair 5 syntax)
    hover = alt.param(
        name="hover",
        select={
            "type": "point",
            "on": "mouseover",
            "fields": ["Edition"],
            "nearest": True
        }
    )

    # Base line chart
    base = alt.Chart(country_df).mark_line(point=True).encode(
        x="Year",
        y="Medal"
    )

    # Invisible points to trigger selection
    points = base.mark_point(opacity=0).add_params(hover)

    # Highlighted points on the line
    highlight_points = alt.Chart(country_df).mark_point(color="red", size=100).encode(
        x="Year",
        y="Medal",
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    country_df["label"] = (
        "Year: " + country_df["Year"].astype(str) +
        ", Medal: " + country_df["Medal"].astype(str)
    )


    # Labels near points
    labels = alt.Chart(country_df).mark_text(align="left", dx=5, dy=-5).encode(
        x="Year",
        y="Medal",
        text=alt.condition(hover, "label:N", alt.value("")),
        opacity=alt.condition(hover, alt.value(1), alt.value(0))
    )
    # Vertical rule at selected Edition
    rule = alt.Chart(country_df).mark_rule(color="gray", strokeDash=[5, 5]).encode(
        x="Year"
    ).transform_filter(hover)

    # Final chart with all layers
    chart = alt.layer(base, points, highlight_points, labels, rule).properties(
        title="Number of Medals Over Years",
        width=700,
        height=400
    )
    st.title(selected_country + " Medal Tally Over The Years")
    st.altair_chart(chart, use_container_width=True)


    st.title(selected_country + " Excels in the Following Sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 15 Athletes of "+selected_country)
    top15_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top15_df)
#========================================================


if user_menu=='ATHLETE-WISE ANALYSIS':
    athlete_df=df.drop_duplicates(subset=['Name','region'])

    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()


    fig=ff.create_distplot([x1,x2,x3,x4],['Overall_Age','Gold_Medalist','Silver_Medalist','Bronze_Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age ")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War','Athletics','Swimming', 'Badminton', 'Sailing', 'Gymnastics','Art Competitions','Handball', 'Weightlifting', 'Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing','Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing','Tennis','Golf', 'Softball', 'Archery','Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball','Rhythmic Gymnastics', 'Rugby Sevens','Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)


    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    t4_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=t4_df['Weight'],y=t4_df['Height'],hue=t4_df['Medal'],style=t4_df['Sex'],s=60)
    st.pyplot(fig)

    
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)




    
    

    