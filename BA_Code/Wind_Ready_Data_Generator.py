from Common_Functions import *
from Plotting_Objects import *
from Common_Constants import *


class WindReadyConstants:
    """
    Object storing user defined constants for generating R Open AIR figures from BA CSV data.

    Parameters
    ----------
    file_path : str
        Your base file path to Boulder AIR CSV data (EX: 'E:\IDAT')
    sites : list of str
        List of site(s) codes as strings (EX: ['LUR', 'BSE'])
    species : str
        String of species as it appears in the data column (EX: 'ethane')
    start_time : str
        Start time as a string in datetime format (EX '2020-01-22 00:00:00')
    end_time : str
        End time as a string in datetime format (EX '2020-08-28 05:00:00')
    wsp_filter: int or float
        Number used as the wind speed cut-off value (only include wsp > value)
    methane_match: bool
        (True or False) used to specify weather or not to combine methane and voc data together
    zero_filter: bool
        (True or False) used to specify weather or not to replace all negative and zero values in df with NAN's
    export_dir: str
        File path to out directory
    """

    def __init__(self, file_path, sites, species, start_time, end_time, wsp_filter, methane_match, zero_filter,
                 export_dir):
        self.file_path = file_path
        self.sites = sites
        self.species = species
        self.start_time = start_time
        self.end_time = end_time
        self.wsp_filter = wsp_filter
        self.methane_match = methane_match
        self.zero_filter = zero_filter
        self.export_dir = export_dir


def main():
    """
    main function for running Wind_Ready_Data_Generator script.  Script instanciates WindReadyConstants class.

    This script takes BA quarterly CSV_out files as inputs and produces CSV files ready to be used by R studios OpenAir
    package to make heat plots and pollution rose figures.  It does this by reading in combining met data with
    BA species data.  It also has a built in filtering function that can be applied or not as needed.  Multiple site
    outputs can be produced at the same time.
    """
    data_parameters = WindReadyConstants(file_path=r'E:/IDAT', sites=['LUR'],
                                         species='ethane', start_time='2022-01-01 00:00:00',
                                         end_time='2022-03-31 23:59:00', wsp_filter=1, methane_match=True,
                                         zero_filter=True, export_dir='E:\Ready for wind plot dir')
    # ending dates of each quarter: q1: 03-31 23:59:00, q2: 06-30 23:59:00,
    # q3: 09-30 23:59:00, q4: 12-31 23:59:00,

    wind_file_paths = wind_file_path_generator_func(data_parameters.file_path, data_parameters.sites,
                                                    data_parameters.start_time, data_parameters.end_time)
    # getting file paths to nessisary met data
    data_file_paths = file_path_generator_func(data_parameters.file_path, data_parameters.sites,
                                               data_parameters.species, data_parameters.start_time,
                                               data_parameters.end_time)
    # getting file paths to nessisary species data

    wind_list = csv_import_func(wind_file_paths, data_parameters.sites)
    # importing met data as a list of df's one per site
    data_list = csv_import_func(data_file_paths, data_parameters.sites)
    # importing species data as a list of df's one per site

    data_list = [df_timeloc_func(df, data_parameters.start_time, data_parameters.end_time) for df in data_list]
    # slicing the df's to the correct time interval
    wind_list = [df_timeloc_func(df, data_parameters.start_time, data_parameters.end_time) for df in wind_list]
    # slicing the df's to the correct time interval

    if data_parameters.methane_match is True and data_parameters.species in VOC_LIST:
        # trigger this statment if you want to combine VOC and Methane data
        methane_file_paths = file_path_generator_func(data_parameters.file_path, data_parameters.sites, 'ch4',
                                                      data_parameters.start_time, data_parameters.end_time)
        # getting file paths to nessisary methane data.

        methane_list = csv_import_func(methane_file_paths, data_parameters.sites)
        methane_list = [df_timeloc_func(df, data_parameters.start_time, data_parameters.end_time) for df in
                        methane_list]
        # read in methane data as list of dataframes (one per site)

        wind_list = met_methane_combine_func(data_parameters, wind_list, methane_list)
        # combin methane and met df's and place them back in list

        combine_data = met_methane_voc_combine_func(data_parameters, wind_list, data_list)
        # make combine VOC data with met and methane data and place into list of df's

    elif data_parameters.methane_match is False and data_parameters.species in VOC_LIST:
        # make combine VOC data with met but not methane data
        combine_data = met_voc_combine_func(data_parameters, wind_list, data_list)

    else:
        # combine non-voc species with met data
        combine_data = met_non_voc_combine_func(data_parameters, wind_list, data_list)

    if data_parameters.zero_filter is True:
        # if True filiter zero and negative values by replacing them with NAN values
        combine_data = zero_filter_func(combine_data)
        # function that does the filtering

    wind_ready_export_func(data_parameters, combine_data)
    # export wind ready CSV files to you out dir


if __name__ == "__main__":
    main()
