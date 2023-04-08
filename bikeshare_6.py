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
    while True:
        city = input("Please enter a city (Chicago, New York City, or Washington): ")
        if city.lower() in CITY_DATA.keys():
            break
        else:
            print("Invalid input. Please enter one of the three cities specified.")


    while True:
        month = input("Please enter a month (January, February, March, April, May, June), or type 'all' for all months: ")
        if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")



    while True:
        day = input("Please enter a day of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday), or type 'all' for all days: ")
        if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")


    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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

    file_name = CITY_DATA.get(city.lower())
    if file_name is None:
        print("Invalid city name. Please try again.")
        return None

    df = pd.read_csv(file_name)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['Start Time'].dt.month == month_index]

    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = days.index(day)
        df = df[df['Start Time'].dt.dayofweek == day_index]

    if df.empty:
        print("No data available for the selected filters.")
        return pd.DataFrame()

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {popular_start_station}")


    popular_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {popular_end_station}")


    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print(f"The most frequent combination of start station and end station trip: {popular_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")


    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)


    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_count)
    else:
        print("\nNo gender data available for the selected city and filters.")


    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print("\nEarliest birth year:", int(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print("Most recent birth year:", int(most_recent_birth_year))

        most_common_birth_year = df['Birth Year'].mode()[0]
        print("Most common birth year:", int(most_common_birth_year))
    else:
        print("\nNo birth year data available for the selected city and filters.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Displays raw data upon request from user.
    Args:
    (df) df - Pandas DataFrame containing city data filtered by month and day
    Returns:
        None
    """
    start = 0
    end = 5
    display_raw_data = input("Would you like to see 5 lines of raw data? (yes or no)").lower()

    while True:
        if display_raw_data == "yes":
            print(df.iloc[start:end])
            start += 5
            end += 5
            display_raw_data = input("Would you like to see more raw data? (yes or no)").lower()
        else:
            break

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
