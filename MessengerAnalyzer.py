from datetime import datetime
from datetime import timezone
import matplotlib.pyplot as plt  # library for plotting data
import operator  # to convert dictionary to list
from tkinter import filedialog  # for file selection UI
from tkinter import *  # for UI
import json  # for handling json
import os  # library for handling paths
from collections import Counter  # for counting words
from collections import OrderedDict
import csv  # for exporting data
import numpy as np

# keeps root window closed
root = Tk()
root.withdraw()

# ask user to select file
folder = filedialog.askdirectory(title="Select Folder")
folder_name = os.path.basename(os.path.normpath(folder)).split("_")[0]

# sets data range for results
start_datetime = 'Jul 12 2019  12:00AM'
end_datetime = 'Jul 12 2020  12:59PM'

# set color of charts
primary_color = '#343837'
secondary_color = '#001146'
tertiary_color = 'white'

# people you want to exclude from your data
exclude_list = []

# words you want to exclude from you word count data
word_exclude_list = ["I", "You", "the", "to", "a", "is", "and", "of", "that", "you", "in", "it", "so", "for", "my",
                     "this", "are", "on", "just", "have", "was", "like", "we", "be", "Oh", "at", "with", "but", "he",
                     "all", "And", "about", "me", "So", "not", "not", "one", "they", "what", "The", ".", "get", "I",
                     "from", "will", "up", "I'm", "an", "your", "do", "really", "out", "it's", "as", "Hahahahaha",
                     "his", "or", "if", "i", "going", "We", "there", "Hahahaha", "has", "our", "when",
                     "some", "can", "Ha", "oh", "had", "see", "that's", "Hahaha", "This", "would", "ha", "no",
                     "got", "That", "how", "What", "But", "were", "him", "more", "now", "did", "right", "been", "Yeah",
                     "don't", "It", "them", "by", "It's", "too", "ha!", "HAHAHAHA", "because", "That's", "her", "who",
                     "Haha", "haha", "He", "go", "Just", "I've", "Iâm", "it.", "she", "HAHAHA", "where", "very",
                     "HAHAHAHAHA", "into", "these", "than", "A", "They", "can't", "am", "Also"]


# write a function that takes the file name as a parameter
def get_textual_messages():
    mess_dict = {}
    x = 0
    # finds all files in selected folder that have json extensions
    for file in os.listdir(folder):
        if file.endswith(".json"):
            # add file name to location to create full path
            file_path = os.path.realpath(folder) + "\\" + str(file)
            # open json file in read mode
            with open(file_path, "r") as read_file:
                data = json.load(read_file)
            # starting number for dictionary
            for message in data['messages']:
                # if message is a generic textual message
                if 'content' in message:
                    # find content of message
                    message_content = message['content']

                    # find time of message
                    message_timestamp = message['timestamp_ms']

                    # find message sender
                    message_sender = message['sender_name']

                message_tuple = message_timestamp, message_sender, message_content
                mess_dict[x] = message_tuple
                x += 1
    return mess_dict


def get_all_messages():
    mess_dict = {}
    x = 0
    # finds all files in selected folder that have json extensions
    for file in os.listdir(folder):
        # add file name to location to create full path
        if file.endswith(".json"):
            file_path = os.path.realpath(folder) + "\\" + str(file)
            # open json file in read mode
            with open(file_path, "r") as read_file:
                data = json.load(read_file)
            # starting number for dictionary
            for message in data['messages']:
                # find time of message
                message_timestamp = message['timestamp_ms']

                # find message sender
                message_sender = message['sender_name']

                message_tuple = message_timestamp, message_sender
                mess_dict[x] = message_tuple
                x += 1
    return mess_dict


def find_sender_count_date_range(start, end):
    mess_dict = get_all_messages()
    count_dict = {}

    # convert start date+time to datetime, then timestamp as integer
    start_datetime_dt = datetime.strptime(start, '%b %d %Y %I:%M%p')
    start_datetime_ts = int(start_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # convert end date+time to datetime, then timestamp as integer
    end_datetime_dt = datetime.strptime(end, '%b %d %Y %I:%M%p')
    end_datetime_ts = int(end_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        if start_datetime_ts <= mess_dict[x][0] <= end_datetime_ts:
            count_dict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Messages Sent in " + folder_name + '\n' + " from " + start + " to " + end
    # set x axis
    keys = formatted_count.keys()
    print(keys)
    # set y axis
    values = formatted_count.values()
    print(values)

    # create chart
    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_sender_count_total():
    mess_dict = get_all_messages()
    count_dict = {}

    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        count_dict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Messages Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_character_count_total():
    mess_dict = get_textual_messages()
    count_dict = {}

    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        count_dict[y] += len(mess_dict[x][2])

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Characters Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_character_count_date_range(start, end):
    mess_dict = get_textual_messages()
    count_dict = {}

    # convert start date+time to datetime, then timestamp as integer
    start_datetime_dt = datetime.strptime(start, '%b %d %Y %I:%M%p')
    start_datetime_ts = int(start_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # convert end date+time to datetime, then timestamp as integer
    end_datetime_dt = datetime.strptime(end, '%b %d %Y %I:%M%p')
    end_datetime_ts = int(end_datetime_dt.replace(tzinfo=timezone.utc).timestamp()) * 1000

    # put names here that you want to exclude
    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
            # check if message is in date range
        if start_datetime_ts <= mess_dict[x][0] <= end_datetime_ts:
            count_dict[y] += len(mess_dict[x][2])

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Number of Characters Sent in " + folder_name + '\n' + " from " + start + " to " + end
    # set x axis
    keys = formatted_count.keys()
    print(keys)
    # set y axis
    values = formatted_count.values()
    print(values)

    # create chart
    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_most_used_words(most_common_count):
    mess_dict = get_textual_messages()
    count_dict = {}
    # get unique names in messages
    all_words = []
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            split_words = mess_dict[x][2].split()
            for w in split_words:
                if "âs" in str(w):
                    w = w.replace("â", "'")
                all_words.append(w)

    # count words in word list
    counted_words = Counter(all_words)

    # remove words that are in teh exclude list
    for w in word_exclude_list:
        if w in counted_words:
            del counted_words[w]

    # get top (specified number) of most common words
    most_occur = counted_words.most_common(most_common_count)

    # convert to standard dict
    most_occur = dict(most_occur)

    # set default file to csv
    file_types = [('CSV', '*.csv')]
    # open dialog to safe file
    csv_file = filedialog.asksaveasfile(type='a', filetypes=file_types, defaultextension=csv)
    # set file path to variable
    csv_file = csv_file.name
    # write dictionary of words to csv file
    with open(csv_file, 'w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in most_occur.items():
            print(key, value)
            writer.writerow([key, value])


def single_word_usage(chosen_word):
    mess_dict = get_textual_messages()
    count_dict = {}

    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in count_dict:
            count_dict[y] = 0
        if chosen_word.lower() in mess_dict[x][2].lower():
            count_dict[y] += 1

    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in count_dict.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = count_dict[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Total Usage of the Word " + '"' + chosen_word + '"' + " in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def find_average_message_length():
    mess_dict = get_textual_messages()
    character_count_dict = {}
    message_count_dict = {}
    # get unique names in messages
    for x in mess_dict:
        if mess_dict[x][1] not in exclude_list:
            y = mess_dict[x][1]
        # if name is not in name list, add it and set the value to 0
        if y not in character_count_dict:
            character_count_dict[y] = 0
            message_count_dict[y] = 0
            # check if message is in date range
        character_count_dict[y] += len(mess_dict[x][2])
        message_count_dict[y] += 1
    print(character_count_dict)
    print(message_count_dict)
    average_character_count = {}
    for c in character_count_dict.keys():
        average_key = c
        average_value = character_count_dict[c] / message_count_dict[c]
        average_value = round(average_value, 2)
        average_character_count[average_key] = average_value
    print(average_character_count)
    # creates nwe formatted dict with first name and last initial
    formatted_count = {}
    for x in average_character_count.keys():
        name_split = x.split(" ")
        formatted_name = name_split[0] + " " + name_split[-1][:1]
        formatted_count[formatted_name] = average_character_count[x]

    # sort dictionary by descending order
    formatted_count = dict(sorted(formatted_count.items(), key=operator.itemgetter(1), reverse=True))

    chart_title = "Average Length of Message Per Person in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = formatted_count.keys()
    # set y axis
    values = formatted_count.values()

    # set width of bars
    bar_width = .4
    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    bars = plt.bar(keys, values, color=secondary_color, width=bar_width)

    # get height of largest bar
    highest_bar = max(values)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)

    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        bar_height = bar.get_height()
        label_height = bar_height - (.1 * bar_height)
        # if label would not fit in axis, put label above it
        if bar_height < label_height - (bar_height - (bar_height * .1)):
            label_height = bar_height + (.1 * bar_height)
        plt.text(bar.get_x() + (bar_width / 2), label_height, bar_height, color=tertiary_color,
                 horizontalalignment='center')
    plt.show()


def message_count_by_month():
    mess_dict = get_all_messages()
    month_list = []

    for x in mess_dict:
        # get timestamp from message
        timestamp = int(mess_dict[x][0]) / 1000
        # convert time stamp to date time
        dt = datetime.fromtimestamp(timestamp)
        # get month and year from time stamp, and combine them
        message_year = int(dt.year)
        message_month = int(dt.month)
        message_date = str(message_year) + "-" + str(message_month)
        # add month and year combo to month list if they are not in there already
        if message_date not in month_list:
            month_list.append(message_date)

    # the month_list will miss months that had no messages sent, so we need to add them in

    # sort list by year, then month
    month_list = sorted(month_list, key=lambda x: (int(x.split("-")[0]), int(x.split("-")[-1])))

    # get the last and first month
    first_month = month_list[0]
    # add all months in range
    last_month = month_list[-1]

    # get first/last month/year as integers, to be used for conditionals
    first_month_only = int(first_month.split("-")[-1])
    last_month_only = int(last_month.split("-")[-1])
    first_year_only = int(first_month.split("-")[0])
    last_year_only = int(last_month.split("-")[0])

    year_iter = first_year_only
    month_iter = first_month_only

    # new month list that will have all months, even ones where no messages are sent
    new_month_list = []
    while year_iter <= last_year_only:
        # need to find way to break on last year and month
        added_date = str(year_iter) + "-" + str(month_iter)
        new_month_list.append(added_date)
        month_iter += 1
        if month_iter > 12:
            year_iter += 1
            month_iter = 1
        if month_iter > last_month_only and year_iter >= last_year_only:
            break

    month_counts = []

    # create list with as many entries as there are months in the new month list
    for m in new_month_list:
        month_counts.append(0)

    # for each message, find the month/year and add it to the month counts relative to where it is in the month list
    for x in mess_dict:
        # get timestamp from message
        timestamp = int(mess_dict[x][0]) / 1000
        # convert time stamp to date time
        dt = datetime.fromtimestamp(timestamp)
        # get month and year from time stamp, and combine them
        message_year = int(dt.year)
        message_month = int(dt.month)
        message_date = str(message_year) + "-" + str(message_month)
        month_counts[(new_month_list.index(message_date))] += 1

    # we want the counts to be the total up to that point, not just the total for the month
    # so for each month count after the first, we need to add the value from the previous month
    u = 0
    for m, s in enumerate(month_counts):
        if u > 0:
            month_counts[m] += month_counts[m - 1]
        u = 1

    chart_title = "Messages Sent in " + folder_name + '\n' + " All Time"
    # set x axis
    keys = new_month_list
    # set y axis
    values = month_counts

    # create chart
    fig, ax = plt.subplots()
    # set background color
    fig.patch.set_facecolor(primary_color)
    ax.set_facecolor(primary_color)

    # change color of chart borders
    ax.spines['bottom'].set_color(tertiary_color)
    ax.spines['top'].set_color(tertiary_color)
    ax.spines['left'].set_color(tertiary_color)
    ax.spines['right'].set_color(tertiary_color)

    # set color of labels
    ax.xaxis.label.set_color(tertiary_color)
    ax.yaxis.label.set_color(tertiary_color)

    # set color of ticks
    ax.tick_params(axis='x', colors=tertiary_color)
    ax.tick_params(axis='y', colors=tertiary_color)

    # set title and styling of title
    plt.title(chart_title, fontsize=20, color=tertiary_color)

    # set bars to variable
    plt.plot(keys, values, color=tertiary_color)

    # assign your bars to a variable so their attributes can be accessed
    plt.xticks(fontsize=20)
    plt.xticks(rotation=-90)
    plt.xticks(size=15)
    plt.yticks(fontsize=20)
    plt.subplots_adjust(bottom=0.3)
    plt.xticks(np.arange(0, len(keys), 3))

    # access the bar attributes to place the text in the appropriate location
    plt.show()


# uncomment a function below to run it

# find_sender_count_date_range(start_datetime, end_datetime)

# find_sender_count_total()

# find_character_count_total()

# find_character_count_date_range(start_datetime, end_datetime)

# find_most_used_words(100)

# single_word_usage()

# find_average_message_length()

message_count_by_month()
