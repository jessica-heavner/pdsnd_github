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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city
    city = input("Enter a city (chicago, new york city, washington): ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Enter a city (chicago, new york city, washington): ").lower()

    # get user input for month
    month = input("Enter a month (all, january, february, ... , june): ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                        'november', 'december']:
        month = input("Enter a month (all, january, february, ... , june): ").lower()

    # get user input for day of week
    day = input("Enter a day (all, monday, tuesday, ... sunday): ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Enter a day (all, monday, tuesday, ... sunday): ").lower()

    print('-' * 40)
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
    # read in data from appropriate csv
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # set month if not all
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # set day if not all
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    # ask user if they want to see 5 lines of raw data
    response = input("Would you like to see 5 lines of the data? (yes or no)").lower()
    row_index = 0
    while response not in ['yes', 'no']:
        response = input("Incorrect input. Would you like to see 5 lines of the data? (yes or no)").lower()
        print(response)
    while response == 'yes':
        print(df[row_index:row_index + 5])
        row_index += 5
        response = input("Would you like to see 5 more lines of the data? (yes or no)").lower()
        while response not in ['yes', 'no']:
            response = input("Incorrect input. Would you like to see 5 lines of the data? (yes or no)").lower()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("\nMost popular month: %s" % popular_month)

    # display the most common day of week
    popular_week_day = df['day_of_week'].mode()[0]
    print("\nMost popular day of week: %s" % popular_week_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost popular hour: %s" % popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nMost popular start station: %s" % popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nMost popular end station: %s" % popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_combo = (df['Start Station'] + ' ' + df['End Station']).mode()[0]
    print("\nMost popular start/end station combination: %s" % popular_start_end_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration for the city selected."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time: %s" % total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time: %s" % mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. This includes, user tyope, gender, and birth year"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user_types = df['User Type'].value_counts()
    print("\nCounts of user types: \n%s" % count_of_user_types)

    # Display counts of gender (only chicago + new york city)
    if city == "new york city" or city == "chicago":
        count_of_genders = df['Gender'].value_counts()
        print("\nCount of genders: \n%s" % count_of_genders)
    else:
        print("Gender data not available for Washington")

    # Display earliest, most recent, and most common year of birth (only chicago + new york city)
    if city == "new york city" or city == "chicago":
        earliest_year_of_birth = df['Birth Year'].min()
        print("\nEarliest Year of Birth: %s" % earliest_year_of_birth)
        most_recent_year_of_birth = df['Birth Year'].max()
        print("\nMost Recent Year of Birth: %s" % most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("\nMost Common Year of Birth: %s" % most_common_year_of_birth)
    else:
        print("Birth year data not available for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

# sources:
# slicing: https://datacarpentry.org/python-ecology-lesson/03-index-slice-subset/index.html
# mode for two columns: https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe