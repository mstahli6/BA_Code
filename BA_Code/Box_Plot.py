from Common_Functions import *
from Plotting_Objects import *
from Common_Constants import *


class BoxPlotConstants:
    """
    Object storing user defined constants for constructing box plots from BA CSV data.

    Parameters
    ----------
    file_path : str
        Your base file path to Boulder AIR CSV data (EX: 'E:\IDAT')
    sites : list of str
        List of site(s) codes as strings (EX: ['LUR', 'BSE'])
    species : str
        String of species as it appears in the data column (EX: 'ethane')
    plot_type : str
        String of Box Plot Type (must be one of the options) Options: 'quarterly report', 'diurnal comparison',
        'custom time comparison', or 'year quarter comparison'.
    bin_time_interval : str
        Time interval as string in which the box plots are binned (must be one of the options) Options: 'year',
        'month', 'week', 'day', or 'all time'
    start_time : str
        Start time as a string in datetime format (EX '2020-01-22 00:00:00')
    end_time : str
        End time as a string in datetime format (EX '2020-08-28 05:00:00')
    """

    def __init__(self, file_path, sites, species, plot_type, bin_time_interval, start_time, end_time):
        self.file_path = file_path
        self.sites = sites
        self.species = species
        self.plot_type = plot_type
        self.bin_time_interval = bin_time_interval
        self.start_time = start_time
        self.end_time = end_time


def diurnal_comparison_func(data_list, data_parameters):
    """
    Creates a Diurnal Box Plot over a user specified time interval

    The data is prepared in a number of stages (view comments under each function)
    Then the data is plotted using the Seaborn module
    Day is 8am through 8pm Night is 9pm till 8am

    Parameters
    ----------
    data_list : list of object
        List of sites data frames
    data_parameters : object
        class object storing parameters essential for constructing the box plot

    Returns
    -------
    None
        Plots
    """
    data = concat_with_site_func(data_parameters.sites, data_list)
    # converts data list into single df with a site column

    data = df_timeloc_func(data, data_parameters.start_time, data_parameters.end_time)
    # locks data into specified time interval

    data = to_denver_tz_func(data)
    # converts UTC data to Denver (MST or MDT) timezone

    data['hour'] = data['time'].dt.hour
    # creates an hour column from time data

    hour_list = data['hour'].tolist()
    # convert hour column to list for quicker iteration
    night_day_list = ['Day' if ((hour >= 8) and (hour < 20)) else 'Night' for hour in hour_list]
    # create list with 'night' or 'day' values. day == 8am-8pm (inclusive), night == 9pm to 7am (inclusive)
    data['diurnal'] = night_day_list
    # add new diurnal list to df as a column

    TITLE_TIME = time_title_func(data_parameters.start_time, data_parameters.end_time)
    # formats time interval to be used in title

    PALETTE = [COLOR_DICT[site] for site in data_parameters.sites]
    # sets box colors to site colors

    SPECIES_NAME = NAME_DICT[data_parameters.species]
    # get name of species for title and y_axis label

    SPECIES_UNIT = UNIT_DICT[data_parameters.species]
    # get units of species for y_axis label

    SITE_TITLE_STRING = site_title_string_func(data_parameters.sites)
    # creats a site string to be used in the plot title

    # data = data.loc[data[data_parameters.species] > 0]

    box_plot = GeneralBoxPlot(data, data['diurnal'], data[data_parameters.species], data['site'])
    box_plot.plotting_func(x_label='',
                           y_label=(SPECIES_NAME + ' ' + SPECIES_UNIT), title=(SITE_TITLE_STRING + ' ' + SPECIES_NAME +
                                                                               ' ' + TITLE_TIME), palette=PALETTE)


def custom_time_comparison_func(data_list, data_parameters):
    """
    Creates a Box Plot over a user specified time interval

    The data is prepared in a number of stages (view comments under each function)
    Then the data is plotted using the Seaborn module

    Parameters
    ----------
    data_list : list of object
        List of sites data frames
    data_parameters : object
        class object storing parameters essential for constructing the box plot

    Returns
    -------
    None
        Plots
    """
    data = concat_with_site_func(data_parameters.sites, data_list)
    # converts data list into single df with a site column

    data = df_timeloc_func(data, data_parameters.start_time, data_parameters.end_time)
    # locks data into specified time interval

    data = interval_binning_func(data, data_parameters.bin_time_interval)
    # bins data['time'] column into new time interval EX: months

    TITLE_TIME = time_title_func(data_parameters.start_time, data_parameters.end_time)
    # formats time interval to be used in title

    SPECIES_NAME = NAME_DICT[data_parameters.species]
    # get name of species for title and y_axis label

    SPECIES_UNIT = UNIT_DICT[data_parameters.species]
    # get units of species for y_axis label

    SITE_TITLE_STRING = site_title_string_func(data_parameters.sites)
    # creats a site string to be used in the plot title

    PALETTE = [COLOR_DICT[site] for site in data_parameters.sites]
    # sets box colors to site colors

    # data = data.loc[data[data_parameters.species] > 0]

    box_plot = GeneralBoxPlot(data, data['time'], data[data_parameters.species], data['site'])
    # instantiate box plot class
    box_plot.plotting_func(x_label=data_parameters.bin_time_interval.title(),
                           y_label=(SPECIES_NAME + ' ' + SPECIES_UNIT), title=(SITE_TITLE_STRING + ' ' + SPECIES_NAME +
                                                                               ' ' + TITLE_TIME), palette=PALETTE,
                           showfliers=False, hue_order=data_parameters.sites)
    # plots the data as box_box


def quarterly_report_box_plot_func(data_list, data_parameters):
    """
    Creates two boxplots one standard with the quarterly title and a second quarter year comparison boxplot

    This function uses the first site int eh data_parameters list to make the quarter year comparison boxplot
    note that to get the correct quarter data use the last day and hour of the month as your end_time variable
    (EX: 06-30 23:59:00 for q2)

    Parameters
    ----------
    data_list : list of objects
        list of df's
    data_parameters
        class object used to store user specified constants and parameters used to make boxplots

    Returns
    -------
    None
        two boxplots are produced (one standared with quarter header and one quarter year comparison)
    """
    data = concat_with_site_func(data_parameters.sites, data_list)
    # converts data list into single df with a site column

    data = df_timeloc_func(data, data_parameters.start_time, data_parameters.end_time)
    # locks data into specified time interval

    data = interval_binning_func(data, data_parameters.bin_time_interval)
    # bins data['time'] column into new time interval EX: months

    quarter_year = get_quarters_and_years_func(data_parameters.start_time, data_parameters.end_time)
    # gets the quarter and year for the title

    quarter_year = quarter_year[0].title()
    quarter_year = quarter_year[-2:] + ' ' + quarter_year[:4]
    # format quarter year to be ready for the title

    SPECIES_NAME = NAME_DICT[data_parameters.species]
    # get name of species for title and y_axis label

    SPECIES_UNIT = UNIT_DICT[data_parameters.species]
    # get units of species for y_axis label

    SITE_TITLE_STRING = site_title_string_func(data_parameters.sites)
    # creats a site string to be used in the plot title

    PALETTE = [COLOR_DICT[site] for site in data_parameters.sites]
    # sets box colors to site colors

    box_plot = GeneralBoxPlot(data, data['time'], data[data_parameters.species], data['site'])
    # instantiate box plot class
    box_plot.plotting_func(x_label=data_parameters.bin_time_interval.title(),
                           y_label=(SPECIES_NAME + ' ' + SPECIES_UNIT), title=(SITE_TITLE_STRING + ' ' + SPECIES_NAME +
                                                                               ' ' + quarter_year), palette=PALETTE,
                           showfliers=False, hue_order=data_parameters.sites)
    # plots the data as box_box

    ###
    # Yearly Quarter Comparison Box-plots Section
    ###

    data_file_paths = file_path_generator_func(data_parameters.file_path, [data_parameters.sites[0]],
                                               data_parameters.species, ('2017' + data_parameters.start_time[4:]),
                                               data_parameters.end_time)
    # get file paths for first site's full historical data

    data_list = csv_import_func(data_file_paths, [data_parameters.sites[0]])
    # import all historic data for first site in data_parameters site list

    data = concat_with_site_func([data_parameters.sites[0]], data_list)
    # converts data list into single df with a site column

    data['dt'] = data['time']
    # duplicate the time column as 'dt'
    data['year'] = data['dt'].dt.year
    # create year column
    data['month'] = data['dt'].dt.month
    # create month column

    good_months, quarter = quarter_loc_func(quarter_year)
    # create a list of wanted months from quarter_year string and get the quarter title sting
    data = data.loc[(data['month'] >= good_months[0]) & (data['month'] <= good_months[-1])]
    # loc the data frame to only include months in the wanted quarter

    PALETTE = [COLOR_DICT[data_parameters.sites[0]]]
    # sets box colors to site colors

    box_plot = GeneralBoxPlot(data, data['year'], data[data_parameters.species], data['site'])
    # instantiate box plot class
    box_plot.plotting_func(x_label=data_parameters.bin_time_interval.title(),
                           y_label=(SPECIES_NAME + ' ' + SPECIES_UNIT), title=(data_parameters.sites[0] + ' ' +
                                                                               SPECIES_NAME +
                                                                               ' ' + quarter + ' Yearly Comparison'),
                           palette=PALETTE, showfliers=False)
    # plots the data as box_box


def main():
    """
    Main fucntion for running Box_Plot script instanciates BoxPlotConstants Class

    Fill in data_parameters with your file path (r'file_path_str') sites as a list of strings ['BSE', 'LUR'],
    species as str 'ch4', plot_type as string (different plot types are specified in BoxPlotConstants doc string)
    Options: 'quarterly report', 'diurnal comparison', or 'custom time comparison'.
    Time interval as string in which the box plots are binned (must be one of the options) Options: 'year',
    'month', 'week', 'day', or 'all time'.  Lastly imput your start_time and end_time as a str:
    start_time='2022-02-01 00:00:00', end_time='2022-06-06 00:00:00'.
    """
    data_parameters = BoxPlotConstants(file_path=r'E:/IDAT', sites=['LUR', 'ECC'],
                                       species='benzene', plot_type='quarterly report', bin_time_interval='month',
                                       start_time='2022-01-01 00:00:00', end_time='2022-03-31 23:59:00')
    # ending dates of each quarter: q1: 03-31 23:59:00, q2: 06-30 23:59:00,
    # q3: 09-30 23:59:00, q4: 12-31 23:59:00,

    data_file_paths = file_path_generator_func(data_parameters.file_path, data_parameters.sites,
                                               data_parameters.species, data_parameters.start_time,
                                               data_parameters.end_time)
    # constructing list of file_paths
    print(data_file_paths)

    data_list = csv_import_func(data_file_paths, data_parameters.sites)
    # importing relivent files from file_paths list as a list of Data Frames

    if data_parameters.plot_type == 'custom time comparison':
        # calls plotting function based on plot_type parameter
        custom_time_comparison_func(data_list, data_parameters)
        # plots data
    elif data_parameters.plot_type == 'diurnal comparison':
        diurnal_comparison_func(data_list, data_parameters)
        # plots data
    elif data_parameters.plot_type == 'quarterly report':
        quarterly_report_box_plot_func(data_list, data_parameters)
        # makes plots for quarterly reports (the first one is a standared quarerly box plot and the second is a month-
        # year boxplot that uses the firs site in the list as its input.


if __name__ == "__main__":
    main()
