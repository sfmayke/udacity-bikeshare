import time
import pandas as pd
import calendar
from datetime import datetime, timedelta

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """

    while True:
        try:
            city: str = input("Select the CITY you would like to check: Chicago, New York, "
                              "or Washington)\n")
            if city.lower() not in ['chicago', 'new york', 'washington']:
                raise ValueError
            break
        except ValueError:
            print(f"Results cannot be filtered by \"{city}\". Please select a valid city!\n")
            continue

    return city.lower()


def check_prompt(prompt_text: str):
    """
    Asks user a yes or no question to continue or end the flow.

    Args:
        (str) prompt_text - The question to be displayed to the user
    Returns:
        (bool) answer - User answer as boolean
    """
    while True:
        try:
            answer = input(prompt_text)
            if answer.lower() in ['y', 'yes', 'ye']:
                return True
            if answer.lower() in ['n', 'no']:
                return False
            raise Exception
        except Exception:
            print("Invalid response!\n")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for month (all, january, february, ... , june)
    month: str = ""
    if check_prompt(f"Would you like to filter by MONTH? y/n\n"):
        while True:
            try:
                month = input("What MONTH would you like to filter by? (january, february, march, april, may, "
                              "or june')\n")
                if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    raise Exception
                break
            except Exception:
                print(f"Results cannot be filtered by \"{month}\", please select a valid month!\n")
                continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day: str = ""
    if check_prompt("Would you like to filter by DAY OF WEEK? y/n\n"):
        while True:
            try:
                day = input("What day of week would you like to filter by? (Monday, Tues...')\n")
                if day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'sunday']:
                    raise Exception
                break
            except Exception:
                print(f"Results cannot be filtered by \"{day}\", select a valid day!\n")
                continue

    print('-' * 60)
    return month.lower(), day.lower()


def load_data(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    return df


def filter_data(df, filters: tuple):
    """
    Filters the data based on selected filters.

    Args:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and/or day
    """

    month, day = filters
    # filter by month if applicable
    if month:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, filters: tuple):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # this assumes there is only one most common value
    month, day = filters
    if not month:
        month = df['month'].mode().values[0]
        print(f"Most common month: {calendar.month_name[month]}")

    # display the most common day of week
    if not day:
        day = df['day_of_week'].mode().values[0]
        print(f"Most common day of week: {day}")

    # display the most common start hour
    hour = df['hour'].mode().values[0]
    hour_str = datetime.strptime(str(f"{hour}:00"), '%H:%M')
    localized_hour = datetime.strftime(hour_str, '%I:%M %p')
    print(f"Most common hour: {localized_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode().values
    print(f"Most commonly used start station: {start_station}")

    # display most commonly used end station
    end_station = df['End Station'].mode().values
    print(f"Most commonly used end station: {end_station}")

    # display most common trip from start to end
    common_trip = df[['Start Station', 'End Station']].mode().values[0]
    print(f"Most common trip from start to end: {common_trip[0]} TO {common_trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print(f"Total travel time was: {timedelta(seconds=int(total))}")

    # display mean travel time
    total_mean = df['Trip Duration'].mean()
    print(f"Average travel time was: {timedelta(seconds=int(total_mean))}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def user_stats(df, city: str):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())

    print("\n")

    # Display counts of gender
    if city in ['chicago', 'new york']:
        user_types = df['Gender'].value_counts()
        print(user_types.to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def display_data(df):
    """ Display trip data on demand """
    print('-' * 60)
    curr_loc = 0
    while True:
        if check_prompt("\nWould you like to view 5 rows of trip data? y/n\n"):
            print(df.iloc[curr_loc:curr_loc+5])
            curr_loc += 5
            continue
        break


def main():
    while True:
        print('-' * 60)
        print('Hello! Let\'s explore some US bikeshare data!')
        print('-' * 60)

        city = get_city()
        month, day = get_filters()
        df = load_data(city)
        df = filter_data(df, (month, day))

        time_stats(df, (month, day))
        station_stats(df)
        if check_prompt("Would you like to see info about trip duration and users? y/n\n"):
            trip_duration_stats(df)
            user_stats(df, city)

        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() in ['n', 'no']:
            input('\nExiting the program...\n')
            break


if __name__ == "__main__":
    main()
