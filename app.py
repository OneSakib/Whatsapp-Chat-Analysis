import streamlit as st
# import preprocess
import preprocess
import helpers
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    df = preprocess.process_data(data)
    # st.dataframe(df)
    usersList = list(df['users'].unique().tolist())
    usersList.remove('group_notification')
    usersList.sort()
    usersList.insert(0, 'All Users')
    selected_user = st.sidebar.selectbox('Select User', usersList)
    if selected_user != 'All Users':
        df = df[df['users'] == selected_user]
    if st.sidebar.button('Show Analysis'):
        num_messages, words, not_of_media, links = helpers.fetch_stats(
            selected_user, df)
        st.title("Top Stastics")
        col1, col2, col3, colo4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(len(words))
        with col3:
            st.header('Total Media')
            st.title(not_of_media)
        with colo4:
            st.header('Total Links')
            st.title(len(links))
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helpers.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helpers.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color="red")
        st.pyplot(fig)
        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            # Week Day Timeline
            st.title("Week Day Activity")
            week_day_timeline = helpers.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(week_day_timeline['day_name'], week_day_timeline['message'])
            st.pyplot(fig)
        with col2:
            # Week Day Timeline
            st.title("Monthly Activity")
            bus_month = helpers.month_activity_map(
                selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(bus_month.index,
                   bus_month.values, color='orange')
            st.pyplot(fig)
        st.title("Activity Heat Map")
        activity_heat_map = helpers.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heat_map)
        st.pyplot(fig)
        # finding the busiest user in the group
        if selected_user == 'All Users':
            st.header('Busiest User')
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('User')
                x, new_df = helpers.fetch_most_busy_user(df)
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='skyblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # Word Cloud
        df_wc = helpers.create_word_cloud(selected_user, df)
        st.header('Word Cloud')
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        st.pyplot(fig)
        # Most common words
        most_common_df = helpers.most_common_words(selected_user, df)
        st.header('Most Common Words')
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='skyblue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # EMOJI
        emojis_df = helpers.fetch_emoji(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.header("EMOJI")
            st.dataframe(emojis_df)
        with col2:
            st.header("PIE Chart")
            fig, ax = plt.subplots()
            ax.pie(emojis_df[1], labels=emojis_df[0], autopct="%0.2f")
            st.pyplot(fig)
