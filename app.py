import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

st.title("Sentiment Analysis dari Social Media Angkasa Pura 2 ")
st.sidebar.title("Sentiment Analysis")
st.markdown("Analisa Sentimen terkait Pelayanan Bandara-Bandara di bawah naungan Angkasa Pura 2 ✈️")
st.sidebar.markdown("Analisa Sentimen terkait Pelayanan Bandara-Bandara di bawah naungan Angkasa Pura 2 ✈️")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv("tweet_trial.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


data = load_data()
st.sidebar.subheader("Social Media Comment")
random_tweet = st.sidebar.radio("Sentiment Type", ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])
st.sidebar.markdown("### Comment dan Sentiment")
select = st.sidebar.selectbox('Visual Type', ['Histogram', 'piechart'], key=1)

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Jumlah Comment terhadap sentimen")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="sentiment", y="Comment", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("Waktu dan Lokasi Comment")
hour = st.sidebar.slider('Jam per hari', 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('close', True, key=1):
    st.markdown('Lokasi Comment dan Sentimen berdasarkan waktu')
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Pembagian comment dan sentimen")
choice = st.sidebar.multiselect("Pilih Bandara",
                                ('Soekarno Hatta', 'Kualanamu', 'Supadio'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count',
                              color='airline_sentiment',
                              facet_col='airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600,
                              width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word Cloud for picked sentiment', ('positive', 'negative', 'neutral'))

if not st.sidebar.checkbox("close", True, key='3'):
    st.header("word cloud for %s sentiment" % word_sentiment)
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join(
        [word for word in words.split() if 'http' not in word and not (word.startswith('@') and (word != 'RT'))])
    word_cloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(
        processed_words)
    # plt.imshow(word_cloud)
    # plt.xticks([])
    # plt.yticks([])
    # st.pyplot()
    fig, ax = plt.subplots()
    plt.imshow(word_cloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig)
