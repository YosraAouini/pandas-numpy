# population.py
# AUTHOR NAME
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 5 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library, including numpy and pandas.
# Remember to include docstrings and comments.

## Import librairies
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)

import warnings
warnings.filterwarnings("ignore")

def main():

    # Stage 1: Import data


    ## Import data
    codes = pd.read_excel("UN Population Datasets/UN Codes.xlsx",sheet_name="world_data")
    population_dataset1 = pd.read_excel("UN Population Datasets/UN Population Dataset 1.xlsx",sheet_name="Pop Growth Stats")
    population_dataset2 = pd.read_excel("UN Population Datasets/UN Population Dataset 2.xlsx",sheet_name="Pop Growth Cities")
    # Data pre-processing
    data1=pd.pivot_table(population_dataset1, values='Value', index=['Region/Country/Area','Year'],columns=['Series'], aggfunc=np.sum)
    data1=data1.reset_index(level=['Region/Country/Area','Year'],drop=False)
    data1.dropna(subset=['Year'])

    data2=pd.pivot_table(population_dataset2, values='Value', index=['Region/Country/Area','Year'],columns=['Series'], aggfunc=np.sum)
    data2=data2.reset_index(level=['Region/Country/Area','Year'],drop=False)
    data2.dropna(subset=['Year'])

    # Merge datasets
    print("codes shape",codes.shape[0])
    print("data1 shape",data1.shape[0])
    print("data2 shape",data2.shape[0])
    countries_stats1=pd.merge(codes, data1, left_on='Country',right_on='Region/Country/Area', how='inner', suffixes=('', '_drop'))
    countries_stats1=countries_stats1.drop(['Region/Country/Area'], axis=1)
    print("countries_stats1 shape",countries_stats1.shape[0])
    countries_stats=pd.merge(countries_stats1, data2, left_on=['Country','Year'],right_on=['Region/Country/Area','Year'], how='inner', suffixes=('', '_drop'))
    countries_stats=countries_stats.drop(['Region/Country/Area'], axis=1)
    countries_stats.dropna(subset=['Year'])
    print("countries_stats shape",countries_stats.shape[0])
    # set hierarchical  index 'UN Region', 'UN Sub-Region','Year'
    index = pd.MultiIndex.from_frame(countries_stats[['UN Region', 'UN Sub-Region','Year']])
    countries_stats.set_index(index,inplace=True)
    idx = pd.IndexSlice
    countries_stats=countries_stats.sort_index()

    # Describe combined dataset
    print("\n Description of dataset: \n")
    print(countries_stats.describe())

    # Print Average statistics per region and year using aggregation with the mean function
    print("\n Average statistics per region and year: \n ")
    countries_stats_=countries_stats.drop(['Year','UN Region'], axis=1)
    print(countries_stats_.groupby(['UN Region', 'Year']).mean())


    # Plot Population annual rate of increase (percent) for each region
    p1 = pd.pivot_table(countries_stats_, values='Population annual rate of increase (percent)', index=['UN Region', 'Year'],
                            aggfunc=np.mean)
    p1=p1.reset_index()
    print(p1)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar( p1['UN Region'], p1['Population annual rate of increase (percent)'], color='b')
    ax.set_ylabel('Annual Rate')
    ax.set_title('Population annual rate of increase (percent)')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.savefig('books_read.png',bbox_inches='tight')

    # Count Missing values per columns of the combined dataset
    print("\n Count Missing Values per columns \n ")
    print(countries_stats.isnull().sum())

    # Add new variable popo_decrease to define countries that have  negatif Population annual rate of increase (percent)
    countries_stats['pop_decrease']= countries_stats.eval('`Population annual rate of increase (percent)`<0').astype(int)
    # Add new variable females_lives_more_than_males  to define countries that have  negatif Life expectancy at birth for females (years)`>`Life expectancy at birth for males (years)
    countries_stats['females_lives_more_than_males']= countries_stats.eval('`Life expectancy at birth for females (years)`>`Life expectancy at birth for males (years)`').astype(int)

    # Liste of countries where their population decrease per region and year
    print('Number of countries where their population decrease')
    countries_stats_=countries_stats.drop(['Year','UN Region'], axis=1)
    print(countries_stats_[countries_stats_['pop_decrease']==1].groupby(['UN Region','Year']).count()['pop_decrease'])

    # Liste of countries where males lives than females per region and year
    print('Number of countries where males lives than females')
    print(countries_stats_[countries_stats_['females_lives_more_than_males']==0].groupby(['UN Region', 'Year']).count()['females_lives_more_than_males'])


    #Define function region_valid to raise error when the sub-region doesn't exist
    def region_valide(sub_region):
       if sub_region not in countries_stats['UN Sub-Region'].unique():
           raise ValueError("You must enter a valid UN sub-region name")

    #Using the while functionality, the user can enter many time the sub-region name until he enter a valid name
    sub_region = None
    while sub_region  is None:
        input_value = str(input("Please enter a sub-region name: "))
        try:
            # try and convert the string input to a number
            region_valide(input_value)
            sub_region=input_value
        except ValueError:
            # tell the user off
            print("You must enter a valid UN sub-region name".format(input=input_value))

    print("\n")
    print("The dataset contain informations of these years: " ,countries_stats['Year'].unique())
    # Define function year_valid to raise error when the year s not valid doesn't exist or not integer type
    def year_valide(user_year):
        if int(user_year) not in countries_stats['Year'].unique() or not isinstance(user_year,int):
            raise ValueError("You must enter a valid year")

    # Using the while functionality, the user can enter many time the year until he enter a valid name

    year = None

    while year is None:
        input_year = input("Please enter a year: ")
        try:
            input_year=int(input_year)
            year_valide(input_year)
            year = input_year
        except ValueError:
            # tell the user off
            print("You must enter a valid year".format(input=input_year))

    ## Select data concerning the sub region and the chosen year
    regions_stats=countries_stats.loc[idx[:,sub_region,year],:]

    # Print average statistics of the sub_region in the chosen year
    print('\n')
    print("Average Statistics of sub region {} in {}:".format(sub_region,year))
    print("\n")
    print(regions_stats.iloc[:,4:].mean())

    # Print 3 countries with the lower rate fertility  in the region
    print("\n 3 countries with the lower rate fertility  in the region  \n")
    regions_stats_ = regions_stats.drop(['Year', 'UN Region'], axis=1)
    print(regions_stats_.nsmallest(3, 'Total fertility rate (children per women)')[['Country','Total fertility rate (children per women)']])

    # Print Top 3 countries with the best rate fertility  in the region
    print("\n Top 3 countries with the best Life expectancy at birth  in the region  \n")
    regions_stats_ = regions_stats.drop(['Year', 'UN Region'], axis=1)
    print(regions_stats_.nlargest(3, 'Life expectancy at birth for both sexes (years)')[['Country','Life expectancy at birth for both sexes (years)']])


    # Export countries_stats dataframe
    countries_stats.to_excel("countries_stats.xlsx")



if __name__ == '__main__':
    main()


