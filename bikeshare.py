import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Ask user to input for city
    while True:
        try:
            city = input('Enter the name of the city (chicago, new york city, washington): ').lower()
            if city in CITY_DATA:
                break
            else:
                raise ValueError('Invalid input. Please enter a valid city name.')
        except ValueError as e:
            print(e)

    # Ask user to input for month
    while True:
        try:
            month = input('Enter the month to filter by (all, january, february, march, april, may, june): ').lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                raise ValueError('Invalid input. Please enter a valid month.')
        except ValueError as e:
            print(e)

    # Ask user to input for day of week
    while True:
        try:
            day = input('Enter the day of the week to filter by (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ').lower()
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                raise ValueError('Invalid input. Please enter a valid day of the week.')
        except ValueError as e:
            print(e)

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
    
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from the "Start Time" column to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new DataFrame
        df = df[df['Month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new DataFrame
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    # Display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print('Most Frequent Trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_rounded = round(mean_travel_time, 1)
    print(f'Mean Travel Time: {mean_travel_time_rounded} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_counts)
    else:
        print('Gender data is not available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('Earliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', common_year)
    else:
        print('Birth year data is not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Displays 5 rows of individual trip data from the DataFrame based on user input.

    Args:
        df (DataFrame): Pandas DataFrame containing the trip data
    """
    print('\n')

    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()