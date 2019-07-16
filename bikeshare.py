import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Check Lists to check that input from user is correct
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    dow = ['All', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please enter a city. Available Cities: Chicago, New York City, Washington.')
    #error handling for city proper input from user
    while True:
        city = input('City: ').lower()
        try:
            CITY_DATA[city]
            break
        except KeyError as e:
            print("Invalid City. Try again.\nKeyError occured:{}".format(e))

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Please enter a month. If all months are wanted, type all.')
    #error handling for month proper input from user
    while True:
        month = input('Month: ').lower()
        if month in months:
            break
        else:
            print("Invalid Month. Try again.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please enter a day of the week (in full). If all days are wanted, type all.')
    #error handling for day of the week proper input from user
    while True:
        day = input('Day of the Week: ').title()
        if day in dow:
            break
        else:
            print("Invalid Day of the Week. Try again.")

    print('-'*40)
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

    # Load data
    df = pd.read_csv(CITY_DATA[city])
    # Fix timestamps
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    df['End Time'] = pd.to_datetime(df["End Time"])
    # Start filtering
    if month != 'all':
        # using the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Start Time'].dt.month == month]

    # filter by day of week if applicable. if filtered, return string day of the week rather than integer
    if day != 'All':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['Start Time'].dt.weekday == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    print("Most Common Month: {}".format(months[df['Start Time'].dt.month.mode()[0]-1]).title())

    # TO DO: display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print("Most Common Day of Week: {}".format(days[df['Start Time'].dt.weekday.mode()[0]-1]))

    # TO DO: display the most common start hour
    print("Most Common Hour: {}".format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most Commonly Used Start Station: {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most Commonly Used End Station: {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    station_counts = df['Start Station'].value_counts()+df['End Station'].value_counts()
    print("Most Commonly Used Station: {}".format(station_counts.dropna().sort_values(ascending=False).index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    years, total_time = total_time//31557600, total_time%31557600
    months, total_time = total_time//2592000, total_time%2592000
    days, total_time = total_time//86400, total_time%86400
    hours, total_time = total_time//3600, total_time%3600
    minutes, total_time = total_time//60, total_time%60
    seconds = total_time
    print("Total Travel Time: {} years, {} months, {} days, {} hours, {} minutes, {} seconds.".format(years, months, days, hours, minutes, seconds))
   # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()
    hours, avg_time = avg_time//3600, avg_time%3600
    minutes, avg_time = avg_time//60, avg_time%60
    seconds = avg_time
    print("Average Travel Time: {} hours, {} minutes, {} seconds.".format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        print("Type of Users:\n{}".format(df['User Type'].value_counts()))
    except KeyError as e:
        print("No data to analyze.")

    # TO DO: Display counts of gender
    try:
        print('Gender Split:\n{}'.format(df['Gender'].value_counts()))
    except KeyError as e:
        print("No data to analyze.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("Earliest Birth Year: {}".format(df['Birth Year'].min()))
        print("Most Recent Birth Year: {}".format(df['Birth Year'].max()))
        print("Most Frequent Birth Year: {}".format(df['Birth Year'].mode()[0]))
    except KeyError as e:
        print("No data to analyze.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
