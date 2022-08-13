import tkinter
from tkinter import filedialog
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import datetime
import seaborn as sns
from matplotlib import pyplot as plt
import math
import random

# ask to chose file from your PC.
root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
'''############################################################################################'''
#                                             Load File and Check Format
'''############################################################################################'''
# Get file extention (format).
file_format = file_path.split('.')[-1]
# Check about file format if csv, xlsx, xls or other.
if file_format == "csv":
    df = pd.read_csv(file_path)
elif file_format == "xlsx" or file_format == "xls":
    df = pd.read_excel(file_path)
else:
    print('File format must be csv or excel')
    quit()
'''############################################################################################'''
#                                             Show Data Information
'''############################################################################################'''
print("--------------------------------")
# Show information about your data.
print("Show data information:")
print(df.info())
print("--------------------------------")
# To show all columns.
pd.options.display.max_columns = 12
print("Show some data:")
print(df.head())
print("--------------------------------")
'''############################################################################################'''
#                                             Handling Missing Values
'''############################################################################################'''
if df.isnull().values.any():
    # print Shape of Data.
    print("Main data shape:")
    print(df.shape)
    print("--------------------------------")
    # Create dataframe that display info about missing values
    print("Show number of missing values and percentage")
    missing_info = pd.DataFrame()
    missing_info["Missing"] = df.isnull().sum().sort_values(ascending = False)
    missing_info["Percentage % "] = df.isna().mean().sort_values(ascending = False) * 100
    print(missing_info)
    print("--------------------------------")
    # Drop Columns where percentage of missing values is greater than 50%
    df.drop(df.columns[df.isna().mean() >= 0.50], axis=1, inplace=True)
    # Handling of missing values.
    for i in range(len(df.columns)):
        if df[df.columns[i]].dtype in [np.int64, np.int32, np.int]:
            df[df.columns[i]].fillna(int(df[df.columns[i]].median()), inplace=True)
        elif df[df.columns[i]].dtype in [np.float64, np.float32, np.float]:
            df[df.columns[i]].fillna(df[df.columns[i]].mean(), inplace=True)
        elif df[df.columns[i]].dtype == bool:
            df[df.columns[i]].fillna(df[df.columns[i]].mode(), inplace=True)
        else:
            df[df.columns[i]].dropna(inplace=True)

    print('Check about missing values after handling:')
    print(df.isnull().sum())
    print(df.head())
    print("--------------------------------")
    # print Shape of Data after droping.
    print("data shape after drop columns that have 50% missing values:")
    print(df.shape)
    print("--------------------------------")
'''############################################################################################'''
#     Check if dataframe has column of date type and create columns for day,month and year.
'''############################################################################################'''
try:
    # List for most common date formats.
    fmts = ('%Y','%b %d, %Y','%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y','%m/%d/%y','%b %Y','%B%Y','%b %d,%Y','%d/%m/%Y',
            "EEE, dd MMM yyyy HH:mm:ss z", #RFC_822
            "EEE, dd MMM yyyy HH:mm zzzz", "yyyy-MM-dd'T'HH:mm:ssZ",
            "yyyy-MM-dd'T'HH:mm:ss.SSSzzzz", #Blogger Atom feed has millisecs also
            "yyyy-MM-dd'T'HH:mm:sszzzz", "yyyy-MM-dd'T'HH:mm:ss z",
            "yyyy-MM-dd'T'HH:mm:ssz", #ISO_8601
            "yyyy-MM-dd'T'HH:mm:ss", "yyyy-MM-dd'T'HHmmss.SSSz",
            "yyyy-MM-dd"
            )
    for i in range(len(df.columns)):
        if df[df.columns[i]].dtype not in [np.float64,np.float32,np.float,np.int,np.bool]:
            for fmt in fmts:
                for j in range(0,df.shape[0],25):
                    try:
                        datetime.datetime.strptime(str(df[df.columns[i]][j]), fmt)
                        my_fmt = fmt
                    except:
                        pass
            df[df.columns[i]] = pd.to_datetime(df[df.columns[i]], format=my_fmt)
            df['Day'] = df[df.columns[i]].dt.day
            df['Month'] = df[df.columns[i]].dt.month
            df['Year'] = df[df.columns[i]].dt.year
            df.drop(df.columns[i], axis = 1, inplace = True)
            # print Shape of Data after Splitting.
            print("data shape after splitting date column:")
            print(df.shape)
            print(df.head())
            print("--------------------------------")
except:
    pass
'''############################################################################################'''
#                                         Data Visualization
'''############################################################################################'''
int_columns = df.select_dtypes(include = ['int','int32','int64']).columns
float_columns = df.select_dtypes(include = ['float','float32','float64']).columns
objects_value = df.select_dtypes(exclude = ['int','int32','int64','float','float32','float64']).columns
numeric_data = pd.concat([df[int_columns],df[float_columns]],axis = 1)
categorical_data = df[objects_value]
'''                                      Numeric-Numeric Analysis                               '''
'''
                                    Univariate Analysis

'''
try:
    num_plots_x = 3   # No. of plots in every row.
    num_plots_y = math.ceil(len(numeric_data.columns)/num_plots_x) # No. of plots in every column.
    # distribution plot for all numerical columns.
    figure, axis = plt.subplots(num_plots_y,num_plots_x)
    figure.set_size_inches(10, 8)
    figure.suptitle('Features Distplots')
    count = 0
    for i in range(num_plots_y):
        for j in range(num_plots_x):
            if count >= numeric_data.shape[1]:
                axis[i,j].set_visible(False)
                continue
            sns.distplot(numeric_data[numeric_data.columns[count]],ax = axis[i,j])
            count = count + 1
    if len(numeric_data[numeric_data.columns] != 0):
        plt.show()
except:
    plt.close()
try:
    # box plot plot for all numerical columns.
    figure, axis = plt.subplots(num_plots_y,num_plots_x)
    figure.set_size_inches(10, 8)
    figure.suptitle('Features Boxplots')
    count = 0
    for i in range(num_plots_y):
        for j in range(num_plots_x):
            r = random.random()
            b = random.random()
            g = random.random()
            if count >= numeric_data.shape[1]:
                axis[i,j].set_visible(False)
                continue
            sns.boxplot(data = numeric_data[numeric_data.columns[count]],ax = axis[i,j], color = (r,g,b))
            axis[i,j].set_title(numeric_data.columns[count])
            count = count + 1
    plt.show()
except:
    plt.close()
'''
                                       Bivariate Analysis

'''
# Show Correlation Matrix.
plt.title('Correlation Matrix')
sns.heatmap(numeric_data.corr(), annot = True, fmt = '.2f', cmap = 'Reds')
plt.show()
# pair plotting.
sns.pairplot(numeric_data[numeric_data.columns], kind = 'reg')
plt.title('Features Pairplots')
plt.tight_layout()
plt.show()
'''                                      Numeric-Categorical Analysis                               '''
print('some categorical analysis: ')
print("--------------------------------")
for i in range(len(categorical_data.columns)):
    for j in range(len(numeric_data.columns)):
        print(df.groupby(categorical_data.columns[i])[numeric_data.columns[j]].mean().sort_values(ascending = False))
        print("--------------------------------")
