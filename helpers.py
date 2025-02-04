from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    # 1. No of Messages
    num_messages = df.shape[0]
    # 2. No of Messages
    words = []
    for word in df['message']:
        words.extend(word.split())
    # 3. No of media
    not_of_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    # 4. No of links
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    # 5. No of emojis
    # 6. No of characters

    return num_messages, words, not_of_media, links


def fetch_most_busy_user(df):
    x = df['users'].value_counts().head()
    df = round(df['users'].value_counts()/df.shape[0]*100,
               2).reset_index().rename(columns={'users': 'user', 'count': 'percentage'})
    return x, df


def create_word_cloud(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    temp_df = df[df['users'] != 'group_notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']
    stop_words = []
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = file.read()

    def remove_stop_words(message):
        return ' '.join([word for word in message.lower().split() if word not in stop_words])
    temp_df['message'] = temp_df['message'].apply(remove_stop_words)
    word_cloud = WordCloud(width=800, height=800,
                           background_color='white', random_state=21, max_font_size=110)
    df_wc = word_cloud.generate(temp_df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    temp_df = df[df['users'] != 'group_notification']
    temp_df = temp_df[temp_df['message'] != '<Media omitted>\n']
    stop_words = []
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = file.read()
    words = []
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in words and word not in [' ', ' "" ', 'omitted']:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))


def fetch_emoji(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend(
            [em for em in message if em in emoji.UNICODE_EMOJI["en"]])
    emojis = set(emojis)
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'message'].reset_index()
    times = []
    for i in range(timeline.shape[0]):
        times.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time'] = times
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    df['day_name'] = df['date'].dt.day_name()
    week_day_timeline = df.groupby('day_name').count()['message'].reset_index()
    return week_day_timeline


def month_activity_map(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()


def activity_heat_map(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    periods = []
    for i in df['hour']:
        if i >= 24:
            periods.append(i+'- 1')
        else:
            periods.append(str(i)+'-'+str(int(i)+1))
    df['periods'] = periods
    pv_table = df.pivot_table(
        index="day_name", columns="periods", values="message", aggfunc="count").fillna(0)
    return pv_table
