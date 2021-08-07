# school_data.py
# Ateeb Goraya
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 git repository.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
from decimal import Decimal

import numpy as np


def main():
    print("ENSF 592 School Enrollment Statistics")
    
    """ 
launches a program, with the statement
CSV list data is taken for unique years numpy .np CSV
CSV list data takes all values contained from numpy.npgenfromtext
3d array is created and data is stored using school_codes .Len()
numpy array np.array is generated
condition statement is then executed
finding the max and min value in array using min() max()
mean calculated using .len() method

    """
    # getting unique years list from csv
    years = np.unique(np.genfromtxt('Assignment4Data.csv', delimiter=',', dtype='str', skip_header=1, usecols=0))
    # getting unique school codes list from csv
    school_codes = np.unique(np.genfromtxt('Assignment4Data.csv', delimiter=',', dtype='str', skip_header=1, usecols=2))
    # getting all values from csv
    all_values = np.genfromtxt('Assignment4Data.csv', delimiter=',', dtype='str', skip_header=1,
                               usecols=(0, 1, 2, 3, 4, 5))
    # generating a 3d array for storing data
    number = np.zeros(
        (years.__len__(), school_codes.__len__(), 3))  # [[[0] * 3] * school_codes.__len__()] * years.__len__()
    # generating school name array with empty string
    school_name = ["" for x in range(school_codes.__len__())]
    # processing data in a format
    for value in all_values:
        index_of_years = np.where(years == value[0])[0][0]
        index_of_school_codes = np.where(school_codes == value[2])[0][0]
        number[index_of_years][index_of_school_codes][0] = value[3]
        number[index_of_years][index_of_school_codes][1] = value[4]
        number[index_of_years][index_of_school_codes][2] = value[5]
        school_name[index_of_school_codes] = str(value[1])

    # generating  NumPy array
    array_of_number = np.array(number)
    # printing dimension and shape
    print('Shape of full data array: ' + str(array_of_number.shape).replace('L', ''))
    print('Dimensions of full data array: ' + str(array_of_number.ndim))

    # Prompt for user input
    index_of_school = -1
    # taking input from user until valid input
    while True:
        school_name_or_code = input("Please enter the high school name or school code: ")
        # finding value in school codes
        if str(school_name_or_code) in school_codes:
            index_of_school = np.where(school_codes.__eq__(str(school_name_or_code)))[0][0]
            break
        # finding value in school names
        elif str(school_name_or_code) in school_name:
            for i in range(school_name.__len__()):
                if school_name[i].__eq__(school_name_or_code):
                    index_of_school = i
                    break
            break
        else:
            print ('You must enter a valid school name or code')

    #print (index_of_school)

    # Print Stage 2 requirements here
    print("\n***Requested School Statistics***\n")
    print ("School Name: " + school_name[index_of_school] + ", " + school_codes[index_of_school] + "\n")
    grade10_mean = 0  # grade 10 mean
    grade11_mean = 0  # grade 11 mean
    grade12_mean = 0  # grade 12 mean
    highest_enrollment = 0
    lowest_enrollment = array_of_number[0][0][0]
    total_enrollment_by_year = np.zeros(years.__len__())
    index_of_total = 0;
    grade10_over500 =[]
    grade11_over500 =[]
    grade12_over500 =[]
    for i in array_of_number:
        # adding all the value for calculating mean
        grade10_mean += Decimal(i[index_of_school][0])
        grade11_mean += Decimal(i[index_of_school][1])
        grade12_mean += Decimal(i[index_of_school][2])
        if Decimal(i[index_of_school][0])>500:
            grade10_over500.append(i[index_of_school][0])

        if Decimal(i[index_of_school][1])>500:
            grade11_over500.append(i[index_of_school][1])

        if Decimal(i[index_of_school][2])>500:
            grade12_over500.append(i[index_of_school][2])
        # finding max value from all the value
        highest_enrollment = max(Decimal(i[index_of_school][0]), Decimal(i[index_of_school][1]),
                                 Decimal(i[index_of_school][2]), highest_enrollment)

        # finding min value from all the value
        lowest_enrollment = min(Decimal(i[index_of_school][0]), Decimal(i[index_of_school][1]),
                                Decimal(i[index_of_school][2]), lowest_enrollment)
        total_enrollment_by_year[index_of_total] = Decimal(i[index_of_school][0]) + Decimal(
            i[index_of_school][1]) + Decimal(i[index_of_school][2])
        index_of_total = index_of_total + 1

    # calculating mean
    grade10_mean = grade10_mean / years.__len__()
    grade11_mean = grade11_mean / years.__len__()
    grade12_mean = grade12_mean / years.__len__()


    # print the outputs
    print ("Mean enrollment for grade 10: " + str(grade10_mean))
    print ("Mean enrollment for grade 11: " + str(grade11_mean))
    print ("Mean enrollment for grade 12: " + str(grade12_mean))
    print("\n")
    print ("Highest enrollment for single grade: " + str(highest_enrollment))
    print ("Lowest enrollment for single grade: " + str(lowest_enrollment))
    for i in range(years.__len__()):
        print ("Total enrollment for : " + str(years[i]) + ': ' + str(total_enrollment_by_year[i]))
    # Print Stage 3 requirements here

    # Enrollment numbers were over 500
    print("\nEnrollment numbers over 500:")
    if len(grade10_over500)==0 :
        print("No enrollments over 500 for Grade 10")
    else:
        print("Grade 10 over 500: ",grade10_over500)
    if len(grade11_over500)==0 :
        print("No enrollments over 500 for Grade 11")
    else:
        print("Grade 11 over 500: ",grade11_over500)

    if len(grade12_over500)==0 :
        print("No enrollments over 500 for Grade 12")
    else:
        print("Grade 12 over 500: ",grade12_over500)


    print ("\n***General Statistics for All Schools***\n")

    mean_enrollment_first_value = 0
    mean_enrollment_second_value = 0
    total_graduating_class = 0
    count = 0

    # calculating total mean enrollment of 2013
    for i in array_of_number[0]:
        for j in i:
            mean_enrollment_first_value += Decimal(j)
            count = count + 1

    # calculating total mean enrollment of 2020
    for i in array_of_number[array_of_number.__len__() - 1]:
        total_graduating_class += i[2] # calculating graduating student
        for j in i:
            mean_enrollment_second_value += Decimal(j)

    all_school_max = 0
    all_school_min = array_of_number[0][0][0]

    for i in array_of_number:
        for j in i:
            all_school_max = max(Decimal(j[0]), Decimal(j[1]), Decimal(j[2]), all_school_max)
            all_school_min = min(Decimal(j[0]), Decimal(j[1]), Decimal(j[2]), all_school_min)

    # printing outputs
    print ("Mean enrollment in " + str(years[0]) + ": " + str(mean_enrollment_first_value / count))
    print ("Mean enrollment in " + str(years[years.__len__() - 1]) + ": " + str(mean_enrollment_second_value / count))
    print ("Total graduating class of " + str(years[years.__len__() - 1]) + ": " + str(total_graduating_class))
    print ("Highest enrollment for single grade: " + str(all_school_max))
    print ("Lowest enrollment for single grade: " + str(all_school_min))


if __name__ == '__main__':
    main()
