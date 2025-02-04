import re
import pandas as pd


def process_data(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[a-zA-Z]{2}\s-\s"
    message = re.split(pattern, data)
    pattern2 = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}"
    dates = re.findall(pattern, data)
    message = message[1:]
    df = pd.DataFrame({'user_messages': message, 'message_date': dates})
    df['message_date'] = df['message_date'].str.replace(
        '\u202f', ' ', regex=True)
    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=True)
    df['message_date'] = pd.to_datetime(
        df['message_date'], format='%d/%m/%y, %I:%M %p', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_messages']:
        pattern3 = r"([\w\W]+?):\s"
        data = re.split(pattern3, message)
        if data[1:]:
            users.append(data[1])
            messages.append(data[2])
        else:
            users.append('group_notification')
            messages.append(data[0])
    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df
