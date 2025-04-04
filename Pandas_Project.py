import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def print_s(s):
    print(s)
    time.sleep(1)
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print_s('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('What city would you like to get data from? (Chicago, New York City, Washington, or All)\n').lower()
        if city == 'all' or city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print_s("That is not a valid city.\n")
        
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month would you like to filter by? (From January to June or All) \n').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month in months or month == 'all':
            break
        else:
            print_s("That is not a valid month.\n")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day would you like to filter by? (From Monday to Sunday or All)\n)').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day in days or day == 'all':
            break
        else:
            print_s("That is not a valid day.")

    print_s('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load the data file into a dataframe either by one city or all cities.
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        df_merge = []
        for city, filename in CITY_DATA.items():
            #read the csv file into the df
            df = pd.read_csv(filename)
            # add a column to identify the source city
            df['city'] = city
            # append the df to the list df_merge
            df_merge.append(df)
        #combine all the data into one
        df = pd.concat(df_merge, ignore_index=True)



    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_s('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print_s("Most common month is {}.".format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print_s("Most common day of the week is {}.".format(popular_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print_s("Most popular Start Hour: {}.".format(popular_hour))

    print_s("\nThis took %s seconds." % (time.time() - start_time))
    print_s('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_s('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print_s("Most popular Start Station : {}.".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print_s("Most popular End Station : {}.".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(by=['Start Station', 'End Station']).size().idxmax()
    print_s("Most frequent combination of Start Station and End Station: {}.".format(popular_start_end))

    print_s("\nThis took %s seconds." % (time.time() - start_time))
    print_s('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_s('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print_s('Total travel time: {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print_s('Average travel time: {}'.format(mean_travel_time))

    print_s("\nThis took %s seconds." % (time.time() - start_time))
    print_s('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_s('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_value = df['User Type'].value_counts()
    print_s("Counts of User Types: {}.".format(user_value))

    # TO DO: Display counts of gender
    try:
        gender_value = df['Gender'].value_counts()
        print_s("Counts of Gender: {}.".format(gender_value))
    except KeyError:
        print_s("There is no data on gender")
    

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        early_year = df['Birth Year'].min()
        print_s("Earliest Birth Year: {}.".format(early_year))

        most_recent_year = df['Birth Year'].max()
        print_s("Most recent Birth Year: {}.".format(most_recent_year))

        most_common_year = df['Birth Year'].mode()
        print_s("Most common Birth Year: {}.".format(most_common_year))
    except KeyError:
        print_s("There is no data on birth year")

    print_s("\nThis took %s seconds." % (time.time() - start_time))
    print_s('-'*40)

# raw data 
def raw_data_request(df):
    count = 0
    while True:
        raw_data = input("Would you like to see 5 lines of raw data? (Enter yes or no)\n").lower()
        if raw_data == "yes":
            print_s(df[count:count+5]) #displays the lines of raw data
            count += 5
        elif raw_data == "no":
            break
        else:
            print_s("That is not a valid input.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_request(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()