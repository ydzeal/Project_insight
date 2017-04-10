#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import re
import csv
import pandas as pd
import date_to_seconds as ds
import numpy as np
import time
import datetime
import operator


def read_log(fileName):
    # read log.txt as a dataframe
    df = pd.read_csv(fileName, encoding='utf-8', sep =' ', \
            quoting=csv.QUOTE_NONE, error_bad_lines=False, \
            header=None, usecols=[0, 3, 4, 5, 6, 7, 8, 9]) 
            
    # name each column
    df.columns = ['Host', 'Timestamp', 'Timezone', 'Method', \
                    'Request', 'Version', 'HttpCode', 'Bytes']
    return df
    
def feature1(df, n):
    # count the most active hosts
    active_hosts = df['Host'].value_counts()[:n] 
    
    # output with hosts.txt
    with open('./log_output/hosts.txt', 'w', encoding='utf-8') as lines:
        for index, count in active_hosts.iteritems(): 
            lines.write('%s,%s\n' % (index, count))
            
def feature2(df, n):
    # str to int, replace '-' with '0' 
    df['Bytes'] = pd.to_numeric(df['Bytes'], errors='coerce', downcast='integer').fillna(0)

	#group by the request, return the top 10 resources 
    most_resource = df[['Request', 'Bytes']].groupby('Request').sum().\
                    sort_values(by='Bytes', ascending=False).head(n)
    
    # output with resources.txt
    with open('./log_output/resources.txt', 'w', encoding='utf-8') as lines:
        for request, _ in most_resource.iterrows():
            url = request.split(' ')[1] if ' ' in request else request
            lines.write('%s\n' % url)
            
def feature3(fileName):
    # create a list to store time stamps
    timeSeq = []
    
    # sort the time stamps
    with open(fileName, 'r') as lines:
        for line in lines:
            time_stamp = re.search('\[.*\]', line).group(0)
            time_stamp = time_stamp[1:]
            pieces = time_stamp.split('/')
            days = int(pieces[0])
            month = ds.month2Num[pieces[1]]
            tmp = pieces[2].split(':')
            year = int(tmp[0])
            hours = int(tmp[1])
            minutes = int(tmp[2])
            seconds = int(tmp[3][0:2])
            std_time = datetime.datetime(year, month, days, hours, minutes, seconds)
            
            # store sorted time stamps with ascending order
            timeSeq.append(std_time)
            
    # dictionary, [key, value] = [current second, count for visit]
    countDict = {}
    
    # iterate by seconds, (better than by raw rows)
    first_sec = ds.datetime_to_timestamp(timeSeq[0])
    last_sec = ds.datetime_to_timestamp(timeSeq[-1])
    
    # for current second, total visit times during 1 hour = prev visit times + end - head
    head, end, count = 0, 0, 0
    for cur_sec in range(first_sec, last_sec):
    
        # visit sum for 1 hour period extends to a new second
        while end < len(timeSeq) and ds.datetime_to_timestamp(timeSeq[end]) <= cur_sec + 3600:
            count += 1
            end += 1
        countDict[cur_sec] = count
        
        # visit sum for 1 hour period removes the oldest second
        while head < len(timeSeq) and ds.datetime_to_timestamp(timeSeq[head]) == cur_sec:
            count -= 1
            head += 1
    
    #correspond the visit times with the seconds        
    countList = [(key, value) for key, value in countDict.items()]    
    countList.sort(key=operator.itemgetter(1), reverse=True)
    
    # output the hours.txt
    with open('./log_output/hours.txt', 'w', encoding='utf-8') as lines:
        for i in range(0, min(10, len(countList))):
            std_time = ds.timestamp_to_datetime(countList[i][0])
            timeStr = ds.time2str(std_time.day, std_time.month, std_time.year, std_time.hour, std_time.minute, std_time.second)
            lines.write(timeStr  + " -0400" + ',' + str(countList[i][1]) + '\n')

            
def feature4(df):
    # format Timestamp so that can apply math operation
	df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.replace('[', ''), \
                        format='%d/%b/%Y:%H:%M:%S')
      
	blocked_hosts = {} 
	blocked_starts = {} 
	blocked_results = [] 

	for _, row in df.iterrows():

		http_code = row['HttpCode']
		host = row['Host']
		time_stamp = row['Timestamp']
        
        # get block start time by host
		blocked_start = blocked_starts.get(host, None)
		blocked = False 

		if pd.to_numeric(http_code, errors='ignore') == 401:
        
            # if first time failure
			if blocked_start is None:      
                # record failure time stamp
				blocked_starts[host] = time_stamp 
                # count the fail times for the host
				blocked_hosts[host] = 1 
			else:
                # if not the first time fail to log in, then is interval < 20s ? 
				time_delta =  (time_stamp - blocked_start).total_seconds()
				if time_delta <= 20: 
					blocked_hosts[host] += 1 
				else:
                    # if interval > 20s, treat it as first failure
					blocked_starts[host] = time_stamp 
					blocked_hosts[host] = 1
                    
            # failure times more than 3, block
			if blocked_hosts.get(host, 0) > 3:
				blocked = True
                
		else: 
            # already blocked but log in successfully after 5 min, then unblock
			if blocked_start is not None and (time_stamp - blocked_start).total_seconds() > 300:
				blocked_starts.pop(host)
				blocked_hosts.pop(host)
            
			if blocked_hosts.get(host, 0) >= 3: 
				blocked = True

        # add the info into results if get blocked
		if blocked: 
			blocked_results.append('%s - - [%s %s %s %s %s %s %s\n' % \
                (host, time_stamp.strftime('%d/%b/%Y:%H:%M:%S'), \
                row['Timezone'], row['Method'], row['Request'], row['Version'],\
                row['HttpCode'], row['Bytes']))
                
    # output the blocked.txt
	with open('./log_output/blocked.txt', 'w',encoding='utf-8') as lines:
		for line in blocked_results:
			lines.writelines(line)

# feature 5 identify the 10 hosts which use resources the most.
def feature5(df, n):
    # str to int, replace '-' with '0' 
    df['Bytes'] = pd.to_numeric(df['Bytes'], errors='coerce', downcast='integer').fillna(0)

	#group by the Host, return the top 10 resources 
    most_resource = df[['Host', 'Bytes']].groupby('Host').sum().\
                    sort_values(by='Bytes', ascending=False).head(n)
    
    # output with resources_host.txt
    with open('./log_output/resources_host.txt', 'w', encoding='utf-8') as lines:
        for request, _ in most_resource.iterrows():
            url = request.split(' ')[1] if ' ' in request else request
            lines.write('%s\n' % url)            

            
def main():
    fileName = './log_input/log.txt' 
    df = read_log(fileName)
    
    feature1(df, 10)
    feature2(df, 10)
    feature3(fileName)
    feature4(df)
    feature5(df, 10)

if __name__ == "__main__":
    main()

