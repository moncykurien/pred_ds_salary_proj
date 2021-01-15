# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 13:17:38 2021

@author: moncy
"""
import pandas as pd
import datetime

df = pd.read_csv('X:/LAB/MachineLearning/KenLee/pred_ds_salary_proj/apps/data/training_data/raw_training_data.csv')

#salary parsing
df1 = df[df['Salary Estimate'] != '-1']
salary = df1['Salary Estimate'].apply(lambda x: x.split('(')[0].replace('$','').replace('K',''))

df1['hourly'] = df1['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

salary = salary.apply(lambda x: x.lower().replace('per hour',''))
df1['min_salary'] = salary.apply(lambda x: x.split('-')[0])
df1['max_salary'] = salary.apply(lambda x: x.split('-')[1])
df1[['min_salary', 'max_salary']]=df1[['min_salary', 'max_salary']].astype('int64')

df1['avg_salary'] = (df1['min_salary']+df1['max_salary'])/2

#Company name text only
df1['company_txt'] = df1.apply(lambda x: x['Company Name'] if x['Rating'] == -1 else x['Company Name'][:-3], axis = 1)

#State
df1['state'] = df1['Location'].apply(lambda x: x.split(',')[1].strip())

#Age of the company
curr_year = datetime.datetime.now().year
df1['age_of_company'] = df1['Founded'].apply(lambda x: x if x == -1 else curr_year - x)

#Tools
"""
python
sql
r studio
spark
excel
aws
"""
df1['python_skill'] = df1['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df1['sql_skill'] = df1['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df1['r_studio_skill'] = df1['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() else 0)
df1['spark_skill'] = df1['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df1['excel_skill'] = df1['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df1['aws_skill'] = df1['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df1['azure_skill'] = df1['Job Description'].apply(lambda x: 1 if 'azure' in x.lower() else 0)
df1['gcp_skill'] = df1['Job Description'].apply(lambda x: 1 if (('google cloud' in x.lower()) or ('gcp' in x.lower())) else 0)

df1.to_csv('X:/LAB/MachineLearning/KenLee/pred_ds_salary_proj/apps/data/training_data_cleaned/cleaned_training_data.csv')