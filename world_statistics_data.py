# world_data.py
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 5 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library, including numpy and pandas.
# Remember to include docstrings and comments.

## Import librairies
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def main():

    # Stage 1: Import data

    print("ENSF 592 World Data")

    ## Import data 
    data=pd.read_csv('Assign5Data.csv',header=0, delimiter=";")
    ## Set index
    index = pd.MultiIndex.from_frame(data[['UN Region', 'UN Sub-Region','Country']])
    data.set_index(index,inplace=True)

    ##
    #Define function region_valid to raise error when the sub-region doesn't exist     
    def region_valide(sub_region):
       if sub_region not in data['UN Sub-Region'].unique():
           raise ValueError("You must enter a valid UN sub-region name")

    #Using the while functionality, the user can enter many time the sub-region name until he enter a valid name   
    sub_region  = None
    while sub_region  is None:
        input_value = str(input("Please enter a sub-region name: "))
        try:
            # try and convert the string input to a number
            region_valide(input_value)
            sub_region=input_value
        except ValueError:
            # tell the user off
            print("You must enter a valid UN sub-region name".format(input=input_value))


    ## Select data concerning the sub region
    data_r=data[data['UN Sub-Region']==sub_region ]

    ## Define  the find_null()` to determine whether any area data is missing for the chosen sub-region.

    def find_null(sub_region_name):
        data_km=data_r['Sq Km']
        if len(data_km[data_km.isnull()])!=0:
            return data_km[data_km.isnull()]
        else: 
            print("There are no missing sq km values for this sub-region.")

    print("Sq Km measurements are missing for:") 
    print(find_null(sub_region ))


    print("Calculating change in population and latest density")
    ## Calculate change in population
    data_r['change_pop']=data_r['2020 Pop'] - data_r['2000 Pop']
    ## Calculate population density 
    data_r["population_density"]=data_r['2020 Pop']/data_r['Sq Km']
    print(data_r.iloc[:,3:])

    print("Number of threatened species in each country of the sub-region:")
    species =data_r[['Plants (T)','Fish (T)','Birds (T)','Mammals (T)']]
    data_r["species_number"] = species.sum(axis=1)
    print(data_r[['Plants (T)','Fish (T)','Birds (T)','Mammals (T)','species_number']])


    print("The calculated sq km area per umber of threatened species in each country is:")
    data_r['species_density']=data_r['Sq Km']/data_r['species_number']
    print(data_r['species_density'])


if __name__ == '__main__':
    main()


