import pandas as pd
import numpy as np
import datetime as dt
import numpy as np
import glob
import scipy
import scipy.odr as odr
from scipy import stats
from statistics import mean
from dateutil.relativedelta import relativedelta
from Common_Constants import *


def df_timeloc_func(df, start_time, end_time, df_time_col='time'):
    """
    Crops DF's into specified time intervals

    Parameters
    ----------
    df : object
        Pass in your DF
    start_time : str
        Start time as a string in datetime format (EX '2020-01-22 00:00:00')
    end_time : str
        End time as a string in datetime format (EX '2020-08-28 05:00:00')
    df_time_col : str
        Time column header name as string Default('time')

    Returns
    -------
    object
        DF object cropped by specified start and end time bounds
    """
    start = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = dt.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    df = df.loc[(df[df_time_col] >= start) & (df[df_time_col] < end)]
    return df


def to_denver_tz_func(df, time_column_header='time'):
    """
    Converts DF['time'] column data timezone from UTC to local(Denver) time

    Parameters
    ----------
    df : object
        Pass in your DF
    time_column_header: str
        name of time column as string (default 'time')
    Returns
    -------
    object
        DF object with time column converted to local (Denver) timezone
    """
    try:
        df[time_column_header] = df[time_column_header].dt.tz_localize('UTC').dt.tz_convert('America/Denver')
        df[time_column_header] = df[time_column_header].dt.tz_localize(None)
        return df
    except:
        raise Exception('to_denver_tz_func takes two arguments (df, time column header (default "time"))')


def time_title_func(start_time, end_time):
    """
    Convert the start and end times time to a title format

    Parameters
    ----------
    start_time : str
        Start time as a string in datetime format (EX '2020-01-22 00:00:00')
    end_time : str
        End time as a string in datetime format (EX '2020-08-28 05:00:00')

    Returns
    -------
    str
        A title string in (m/d/y-m/d/y) format
    """
    start = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = dt.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    time_title = str(start.month) + '/' + str(start.day) + '/' + str(start.year)[-2:] + '-' + str(end.month) + '/' + \
                 str(end.day) + '/' + str(end.year)[-2:]
    return time_title


def site_title_string_func(sites_name_list):
    """
    Convert a site list to a title string format

    Parameters
    ----------
    sites_name_list : str
        A list of site abbreviations:

    Returns
    -------
    str
        A title string in (m/d/y-m/d/y) format
    """
    if len(sites_name_list) > 1:
        title_string = ''
        for site_name in sites_name_list:
            if site_name != sites_name_list[-1]:
                title_string += site_name + ', '
            else:
                title_string += '& ' + site_name
        return title_string
    else:
        return sites_name_list[0]


def interval_binning_func(df, bin_time_interval):
    """
    Converts time column to binned frequency

    Parameters
    ----------
    df : object
        Your data frame must have 'time' column in datetime format
    bin_time_interval : str
        datetime binging string (EX: 'month', 'week', 'day', 'year', or 'all time')

    Returns
    -------
    object
        DF with binned time column on specified time interval
    """
    if bin_time_interval == 'year':  # setting up bin intervals ex every month, every year, ect...
        df['time'] = df['time'].dt.year
    elif bin_time_interval == 'month':
        df['time'] = df['time'].dt.month
        df.sort_values(by='time', inplace=True)
        df['time'].replace(
            {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
             11: "Nov", 12: "Dec"}, inplace=True)
    elif bin_time_interval == 'week':
        df['time'] = df['time'].dt.week
    elif bin_time_interval == 'day':
        df['time'] = df['time'].dt.day
    elif bin_time_interval == 'all time':
        df['time'] = ''
    else:
        try:
            1 + bin_time_interval
        except:
            print('Error! bin_time_interval not recognized')
    return df


def concat_with_site_func(sites_list, df_list):
    """
    Concatenates multiple DF's into one and adds a column (df['site]) with site names as values.

    Parameters
    ----------
    sites_list : list of str
        List of sites there is data for
    df_list : list of object
        list of site dataframes

    Returns
    -------
    object
        Single combine df with new site column
    """
    for i in range(len(sites_list)):
        df_list[i]['site'] = sites_list[i]
        # creating a site column for plotting
    data = pd.concat(df_list)
    # combing df list into single df for plotting
    return data


def get_quarters_and_years_func(start_time, end_time):
    """
    get relevant quarters and years as a list of strings from user supplied start_time and end_time stings.

    Parameters
    __________
    start_time : str
        Start time as a string in datetime format (EX '2020-01-22 00:00:00')
    end_time : str
        End time as a string in datetime format (EX '2020-08-28 05:00:00')

    Returns
    _______
    list of str
        list of strings with all years and quarters between the start and end times. The strings look like this:
        ('2020_Q2')

    """
    start = dt.datetime.strptime((start_time[:7]), '%Y-%m')
    end = dt.datetime.strptime((end_time[:7]), '%Y-%m')
    num_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
    dates_list = [start + relativedelta(months=m) for m in range(num_months)]

    quarters_list = []
    for date in dates_list:
        if date.month == 1 or date.month == 2 or date.month == 3:
            quarters_list.append(str(date.year) + '_' + 'q1')
        elif date.month == 4 or date.month == 5 or date.month == 6:
            quarters_list.append(str(date.year) + '_' + 'q2')
        elif date.month == 7 or date.month == 8 or date.month == 9:
            quarters_list.append(str(date.year) + '_' + 'q3')
        else:
            quarters_list.append(str(date.year) + '_' + 'q4')
    quarters_list = list(set(quarters_list))

    return quarters_list


def file_path_generator_func(file_path, sites, species, start_time, end_time):
    """
    Constructs a list of relevant file_paths

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

    Returns
    -------
    list
        List of file path names to be imported
    """
    path_species = None
    if species in MET_LIST or species == 'met':
        path_species = 'met'
    elif species == 'ch4' or species == 'co2' or species == 'co2_ppm' or species == 'co' or species == 'co2':
        path_species = 'ch4'
    elif species == 'o3':
        path_species = 'ozone'
    elif species == 'pm2_5' or species == 'pm10':
        path_species = 'pm'
    elif species in VOC_LIST:
        path_species = 'voc'
    elif species == 'no' or species == 'nox':
        path_species = 'nox'
    elif species == 'h2s' or species == 'so2':
        path_species = 'met'
    elif species == 'radon':
        path_species = 'radon'
    else:
        print('species not recognized')

    if path_species == 'nox':
        file_paths = []
        for site in sites:
            if site == 'BSE' or site == 'CCF' or site == 'ESF' or site == 'CCM' or site == 'LUR':
                file_paths.append(file_path + '/' + site + '/' + 'met/')
            else:
                file_paths.append(file_path + '/' + site + '/' + path_species + '/')
    else:
        file_paths = [(file_path + '/' + site + '/' + path_species + '/') for site in sites]

    all_files = []
    for file_path in file_paths:
        file = glob.glob(r'' + file_path + "/*.csv")
        all_files.append(file)
    for file in all_files:
        if file == all_files[0]:
            combined_files = file
        else:
            combined_files += file

    quarters = get_quarters_and_years_func(start_time, end_time)
    good_file_paths = []
    for path in combined_files:
        year_q_position = path.find('_20')
        date_info = path[(year_q_position + 1): (year_q_position + 8)]
        if date_info in quarters:
            good_file_paths.append(path)

    return good_file_paths


def wind_file_path_generator_func(file_path, sites, start_time, end_time):
    """
    Constructs a list of relevant file_paths

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

    Returns
    -------
    list
        List of file path names to be imported
    """

    wind_paths = []
    for site in sites:
        wind_paths.append(file_path + '/' + site + '/met')

    all_files = []
    for file_path in wind_paths:
        file = glob.glob(r'' + file_path + "/*.csv")
        all_files.append(file)
    for file in all_files:
        if file == all_files[0]:
            combined_files = file
        else:
            combined_files += file

    quarters = get_quarters_and_years_func(start_time, end_time)
    good_file_paths = []
    for path in combined_files:
        year_q_position = path.find('_20')
        date_info = path[(year_q_position + 1): (year_q_position + 8)]
        if date_info in quarters:
            good_file_paths.append(path)

    return good_file_paths


def csv_import_func(file_paths, sites, header_num=1):
    """
    Constructs a list of relevant file_paths

    Parameters
    ----------
    file_paths : str
        Your base file path to Boulder AIR CSV data (EX: 'E:\IDAT')
    sites : list of str
        List of site(s) codes as strings (EX: ['LUR', 'BSE'])
    header_num : int
        String of species as it appears in the data column (EX: 'ethane')

    Returns
    -------
    list of objects

    """
    count = 0
    active_site = sites[0]
    df_list = []
    data_list = []
    for path in file_paths:
        data = pd.read_csv(path, header=header_num)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data['time'] = data['time'].dt.round('1min')
        if active_site in path and path != file_paths[-1]:
            df_list.append(data)
        elif active_site not in path and path != file_paths[-1]:
            data_list.append(df_list)
            df_list = []
            df_list.append(data)
            count += 1
            active_site = sites[count]
        elif active_site in path and path == file_paths[-1]:
            df_list.append(data)
            data_list.append(df_list)
        else:
            data_list.append(df_list)
            df_list = []
            df_list.append(data)
            data_list.append(df_list)

    combine_data_list = []
    for lst in data_list:
        # data = lst[0]
        count = 0
        data_list_1 = []
        data_list_2 = []
        two_sets_of_data = False
        for df in lst:
            if count == 0:
                data_list_1.append(df)
                count += 1
            elif df.columns[1] in data_list_1[0].columns:
                data_list_1.append(df)
                count += 1
            else:
                two_sets_of_data = True
                data_list_2.append(df)
                count += 1

        if len(data_list_1) == 1:
            data1 = data_list_1[0]
        else:
            data1 = pd.concat(data_list_1)

        if two_sets_of_data:
            if len(data_list_2) == 1:
                data2 = data_list_2[0]
            else:
                data2 = pd.concat(data_list_2)
            data = pd.merge(data1, data2, on='time', how='outer')
        else:
            data = data1

        data = data.sort_values(by=['time'])

        combine_data_list.append(data)

    return combine_data_list


def voc_wind_pairing_func(met_df,
                          voc_df):
    """
    This function is meant to pair met and VOC data together (can also add methane data if needed)

    The function averages the met data over the 10 minute GC VOC sampling interval and places the data point in the
    middle of the interval.  Wind direction data is averaged using a special method since it has a circular scale
    (0 to 360).  Methane may also be included in the averaged interval if it is present in the met data.

    Parameters
    __________
    met_df : object
        dataframe containing met data
    voc_df : object
        dataframe containing VOC data

    Returns
    -------
    object
        returns a dataframe with merged voc and met data
    """
    # imput met df and voc df returns merged df with average windspeed and durection over voc sampaling interval
    voc_df['time'] = voc_df['time'].dt.round('1min')
    bool_list = met_df['time'].isin(voc_df['time'])
    met_df['bool'] = bool_list
    data = pd.merge(voc_df, met_df, on='time', how='outer')
    data = data.set_index(['time'])  # sorting index by date
    data = data.sort_index()
    data = data.reset_index()
    ind_bool = data.loc[data['bool'] == True]
    goodind = ind_bool.index.tolist()
    ch4_bool = False

    reallygoodind = []
    for i in goodind:  # getting index values within 9 mins of voc data colection
        reallygoodind.append(i - 4)
        reallygoodind.append(i - 3)
        reallygoodind.append(i - 2)
        reallygoodind.append(i - 1)
        reallygoodind.append(i)
        reallygoodind.append(i + 1)
        reallygoodind.append(i + 2)
        reallygoodind.append(i + 3)
        reallygoodind.append(i + 4)
    data['index'] = data.index
    data2 = [data['index'].isin(reallygoodind)]
    data['bool2'] = np.transpose(data2)
    data = data.loc[data['bool2'] == True]
    if 'wsp_avg_ms' in list(data.columns) or 'wdr_avg' in list(data.columns):
        data = data.rename(columns={'wsp_avg_ms': 'wsp', 'wdr_avg': 'wdr'})

    if 'ch4' in data.columns:
        data['ch4'] = data['ch4'].astype(float)
        ch4_bool = True
    data['wdr'] = data['wdr'].astype(float)  # converting wdr and wsp into floating point values for later functions
    data['wsp'] = data['wsp'].astype(float)
    data['x'] = np.sin((data['wdr'] * np.pi / 180))  # converting wdr into east-west and north-south components
    data['y'] = np.cos((data['wdr'] * np.pi / 180))

    avg_wsp_list = []
    avg_list = []
    fixedind = []
    last_ind = None

    if ch4_bool is True:
        avg_ch4_list = []
        for ind, row in data.iterrows():
            if ind - 1 == last_ind:
                xlist.append(row['x'])
                ylist.append(row['y'])
                last_ind = ind
                avgwsplist.append(row['wsp'])
                avgch4list.append(row['ch4'])
            elif ind == reallygoodind[0]:
                avgch4list = []
                avgwsplist = []
                xlist = []
                ylist = []
                xlist.append(row['x'])
                ylist.append(row['y'])
                avgwsplist.append(row['wsp'])
                avgch4list.append(row['ch4'])
                last_ind = ind
            else:
                centerind = (last_ind - 4)
                fixedind.append(centerind)
                xtot = sum(xlist)
                ytot = sum(ylist)
                dev = (xtot / ytot)
                ark = (np.arctan(dev))
                avg = (ark * 57.2958)
                if xtot > 0 and ytot > 0:  # if loop used to determin which quadrent wind direction data fit in
                    avg_list.append(avg)
                elif xtot > 0 and ytot < 0:
                    avg2nd = (avg + 180)
                    avg_list.append(avg2nd)
                elif xtot < 0 and ytot < 0:
                    avg3rd = (avg + 180)
                    avg_list.append(avg3rd)
                elif xtot < 0 and ytot > 0:
                    avg4th = (avg + 360)
                    avg_list.append(avg4th)
                else:
                    avg_list.append(np.nan)
                wsp = mean(avgwsplist)
                ch4 = mean(avgch4list)
                avg_wsp_list.append(wsp)
                avg_ch4_list.append(ch4)
                xlist = []
                ylist = []
                avgwsplist = []
                avgch4list = []
                avgwsplist.append(row['wsp'])
                avgch4list.append(row['ch4'])
                xlist.append(row['x'])
                ylist.append(row['y'])
                last_ind = ind
    else:
        for ind, row in data.iterrows():
            if ind - 1 == last_ind:
                xlist.append(row['x'])
                ylist.append(row['y'])
                last_ind = ind
                avgwsplist.append(row['wsp'])
            elif ind == reallygoodind[0]:
                avgwsplist = []
                xlist = []
                ylist = []
                xlist.append(row['x'])
                ylist.append(row['y'])
                avgwsplist.append(row['wsp'])
                last_ind = ind
            else:
                centerind = (last_ind - 4)
                fixedind.append(centerind)
                xtot = sum(xlist)
                ytot = sum(ylist)
                dev = (xtot / ytot)
                ark = (np.arctan(dev))
                avg = (ark * 57.2958)
                if xtot > 0 and ytot > 0:  # if loop used to determin which quadrent wind direction data fit in
                    avg_list.append(avg)
                elif xtot > 0 and ytot < 0:
                    avg2nd = (avg + 180)
                    avg_list.append(avg2nd)
                elif xtot < 0 and ytot < 0:
                    avg3rd = (avg + 180)
                    avg_list.append(avg3rd)
                elif xtot < 0 and ytot > 0:
                    avg4th = (avg + 360)
                    avg_list.append(avg4th)
                else:
                    avg_list.append(np.nan)
                wsp = mean(avgwsplist)
                avg_wsp_list.append(wsp)
                xlist = []
                ylist = []
                avgwsplist = []
                avgwsplist.append(row['wsp'])
                xlist.append(row['x'])
                ylist.append(row['y'])
                last_ind = ind

    avgdata = pd.DataFrame(fixedind, columns=['index'])
    avgdata['avg_wdr'] = avg_list
    avgdata['avg_wsp'] = avg_wsp_list
    if ch4_bool is True:
        avgdata['avg_ch4'] = avg_ch4_list
    data = pd.merge(data, avgdata, on=['index'], how='outer')  # merging data frames
    check = data
    data = data.loc[data['bool'] == True]
    if ch4_bool is True:
        data = data.drop(
            columns=['x', 'y', 'wsp', 'wdr', 'bool', 'bool2', 'index', 'ch4'])  # removed co2 from this list
    else:
        data = data.drop(columns=['x', 'y', 'wsp', 'wdr', 'bool', 'bool2', 'index'])
    if ch4_bool is True:
        data = data.rename(columns={'avg_wdr': 'wdr', 'avg_wsp': 'wsp', 'avg_ch4': 'ch4'})
    else:
        data = data.rename(columns={'avg_wdr': 'wdr', 'avg_wsp': 'wsp'})
    return data

def radon_wind_pairing_func(met_df, radon_df):
    """
    This function is meant to pair met and VOC data together (can also add methane data if needed)

    The function averages the met data over the 10 minute GC VOC sampling interval and places the data point at the
    end of the interval.  Wind direction data is averaged using a special method since it has a circular scale
    (0 to 360).  Methane may also be included in the averaged interval if it is present in the met data.

    Parameters
    __________
    met_df : object
        dataframe containing met data
    voc_df : object
        dataframe containing VOC data

    Returns
    -------
    object
        returns a dataframe with merged radon and met data
    """
    # imput met df and voc df returns merged df with average windspeed and durection over voc sampaling interval
    radon_df['time'] = radon_df['time'].dt.round('1min')
    bool_list = met_df['time'].isin(radon_df['time'])
    met_df['bool'] = bool_list
    data = pd.merge(radon_df, met_df, on='time', how='outer')
    data = data.set_index(['time'])  # sorting index by date
    data = data.sort_index()
    data = data.reset_index()
    ind_bool = data.loc[data['bool'] == True]
    goodind = ind_bool.index.tolist()
    data['wdr'] = data['wdr'].astype(float)  # converting wdr and wsp into floating point values for later functions
    data['wsp'] = data['wsp'].astype(float)

    if 'wsp_avg_ms' in list(data.columns) or 'wdr_avg' in list(data.columns):
        data = data.rename(columns={'wsp_avg_ms': 'wsp', 'wdr_avg': 'wdr'})

    data['wdr_x'] = np.sin((data['wdr'] * np.pi / 180))  # converting wdr into east-west and north-south components
    data['wdr_y'] = np.cos((data['wdr'] * np.pi / 180))

    # creating list of lists with each nested list comprised of index values for averaging
    avg_inds_list = []
    for ind in goodind:
        num = 0
        ind_buffer_list = []
        while num < 10:
            ind_buffer_list.append(ind-num)
            num += 1
        avg_inds_list.append(ind_buffer_list)

    # grabbing relivant wsp, wdr, and time data to do averaging
    avg_wsp_list = []
    avg_wdr_list = []
    time_interval_list = []
    for lst in avg_inds_list:
        wdr_x_list = []
        wdr_y_list = []
        wsp_list = []
        for ind in lst:
            wdr_x_list.append(data.iloc[ind]['wdr_x'])
            wdr_y_list.append(data.iloc[ind]['wdr_y'])
            wsp_list.append(data.iloc[ind]['wsp'])
            if ind == lst[0]:
                time_interval_list.append(data.iloc[ind]['time'])

        avg_wsp_list.append(mean(wsp_list))
        # getting avg wsp for each interval_group

        # calculating wdr average for each group
        wdr_x_tot = sum(wdr_x_list)
        wdr_y_tot = sum(wdr_y_list)
        dev = (wdr_x_tot / wdr_y_tot)
        ark = (np.arctan(dev))
        avg = (ark * 57.2958)
        if wdr_x_tot > 0 and wdr_y_tot > 0:  # if loop used to determin which quadrent wind direction data fit in
            avg_wdr_list.append(avg)
        elif wdr_x_tot > 0 and wdr_y_tot < 0:
            avg2nd = (avg + 180)
            avg_wdr_list.append(avg2nd)
        elif wdr_x_tot < 0 and wdr_y_tot < 0:
            avg3rd = (avg + 180)
            avg_wdr_list.append(avg3rd)
        elif wdr_x_tot < 0 and wdr_y_tot > 0:
            avg4th = (avg + 360)
            avg_wdr_list.append(avg4th)
        else:
            avg_wdr_list.append(np.nan)

    # created a combine df and merging it with the radon df
    combine_df = pd.DataFrame()
    combine_df['wdr'] = avg_wdr_list
    combine_df['wsp'] = avg_wsp_list
    combine_df['time'] = time_interval_list

    combine_df = pd.merge(combine_df, radon_df, on='time', how='outer')

    return combine_df


def met_methane_combine_func(data_parameters, wind_list, methane_list):
    """
    combines met and methane data into a single df then adds df to list of df(s).

    Parameters
    ----------
    data_parameters : object
        class object storing parameters and constants for making windrose ready files.
    wind_list : list of objects
        list of met df's (1 df per site being run)
    methane_list : list of objects
        list of met df's (1 df per site being run)

    Returns
    --------
    list of objects
        list of combine met and methane df's
    """
    met_list = []
    for i in range(len(data_parameters.sites)):
        combine_data = pd.merge(wind_list[i], methane_list[i], on='time', how='outer')
        met_list.append(combine_data)
    return met_list


def met_methane_voc_combine_func(data_parameters, wind_list, data_list):
    """
    met and methane data are already combine and then combine voc data with that. (returns list with combined df's)

    uses voc_wind_pairing_func to combine voc's with met and methane data on VOC sampling interval.
    adds benz_tol, pro_eth, in_pent, in_bute, and eth_meth columns.

    Parameters
    ----------
    data_parameters : object
        class object storing parameters and constants for making windrose ready files
    wind_list : list of objects
        list of met df's
    data_list : list of objects
        list of VOC df's

    Returns
    --------
    list of objects
        list of combine data frames with voc's, methane, and met data
    """
    combine_data = []
    for i in range(len(data_parameters.sites)):  # makeing voc ratio columns
        data_list[i]['benz_tol'] = data_list[i]['benzene'] / data_list[i]['toluene']
        data_list[i]['pro_eth'] = data_list[i]['propane'] / data_list[i]['ethane']
        data_list[i]['in_pent'] = data_list[i]['i-pentane'] / data_list[i]['n-pentane']
        data_list[i]['in_bute'] = data_list[i]['i-butane'] / data_list[i]['n-butane']
        data = voc_wind_pairing_func(wind_list[i], data_list[i])
        data['eth_meth'] = (data['ethane'] / data['ch4'])
        combine_data.append(data)
    return combine_data


def met_voc_combine_func(data_parameters, wind_list, data_list):
    """
    combine voc data with met data (returns list with combened df's)

    uses voc_wind_pairing_func to combine voc's with met data on VOC sampling interval.
    adds benz_tol, pro_eth, in_pent, and in_bute  columns.

    Parameters
    ----------
    data_parameters : object
        class object storing parameters and constants for making windrose ready files
    wind_list : list of objects
        list of met df's
    data_list : list of objects
        list of VOC df's

    Returns
    --------
    list of objects
        list of combine data frames with voc's and met data
    """
    combine_data = []
    for i in range(len(data_parameters.sites)):  # makeing voc ratio columns
        data_list[i]['benz_tol'] = data_list[i]['benzene'] / data_list[i]['toluene']
        data_list[i]['pro_eth'] = data_list[i]['propane'] / data_list[i]['ethane']
        data_list[i]['in_pent'] = data_list[i]['i-pentane'] / data_list[i]['n-pentane']
        data_list[i]['in_bute'] = data_list[i]['i-butane'] / data_list[i]['n-butane']
        data = voc_wind_pairing_func(wind_list[i], data_list[i])
        combine_data.append(data)
    return combine_data

def met_radon_combine_func(data_parameters, wind_list, data_list):
    """
    combine voc data with met data (returns list with combened df's)

    uses voc_wind_pairing_func to combine voc's with met data on VOC sampling interval.
    adds benz_tol, pro_eth, in_pent, and in_bute  columns.

    Parameters
    ----------
    data_parameters : object
        class object storing parameters and constants for making windrose ready files
    wind_list : list of objects
        list of met df's
    data_list : list of objects
        list of VOC df's

    Returns
    --------
    list of objects
        list of combine data frames with voc's and met data
    """
    combine_data = []
    for i in range(len(data_parameters.sites)):  # makeing voc ratio columns
        data = radon_wind_pairing_func(wind_list[i], data_list[i])
        combine_data.append(data)
    return combine_data

def met_non_voc_combine_func(data_parameters, wind_list, data_list):
    """
    combine non-voc data with met data (returns list with combened df's)

    Parameters
    ----------
    data_parameters : object
        class object storing parameters and constants for making windrose ready files
    wind_list : list of objects
        list of met df's
    data_list : list of objects
        list of non-VOC df's

    Returns
    --------
    list of objects
        list of combine data frames with non-voc and met data
    """
    combine_data = []
    for i in range(len(data_parameters.sites)):  # makeing voc ratio columns
        if 'wdr' in data_list[i].columns or 'wdr_avg' in data_list[i].columns:
            data = wind_list[i]
            combine_data.append(data)
        else:
            data = pd.merge(data_list[i], wind_list[i], on='time', how='outer')
            combine_data.append(data)
    return combine_data


def zero_filter_func(combine_data):
    """
    Used to replace all 0 and negative values in a dataframe with NaN's

    Parameters
    __________
    combine_data : list of objects
        list of dataframes you want to replace 0 and negative vales in.

    Returns
    ________
    list of objects
         returns list of df's with 0 and negative values replaced with NaN's
    """
    filtered_combine_data = []
    for df in combine_data:
        df = df.set_index(df['time'])
        df = df.drop(columns=['time'])
        df = df.mask(df <= 0)
        df = df.reset_index()
        filtered_combine_data.append(df)
    return filtered_combine_data


def box_zero_filter_func(combine_data):
    """
    Used to replace all 0 and negative values in a dataframe with NaN's

    Parameters
    __________
    combine_data : objects
        a combine site dataframes you want to replace 0 and negative vales in.

    Returns
    ________
    object
         returns df with 0 and negative values replaced with NaN's
    """
    for col in combine_data.columns:
        try:
            combine_data[col] = combine_data[col].mask(combine_data[col] <= 0)
        except:
            continue
    return combine_data


def wind_ready_export_func(data_parameters, combine_data):
    """
    Used to export R OpenAir ready data

    Parameters
    __________
    data_parameters : object
        class object storing parameters and constants for making windrose ready files
    combine_data : list of objects
        data frame containing combined met and species data ready for export

    Returns
    ________
    None
         exports the data to out directory specified in the data_parameters object.  With wsp data removed above filter
         value
    """
    num = 0
    for df in combine_data:
        df = df.loc[df['wsp'] > data_parameters.wsp_filter]
        df.to_csv(data_parameters.export_dir + '\\' + data_parameters.sites[num] + '_' +
                  data_parameters.species + '_' + data_parameters.start_time[:10] + '__' +
                  data_parameters.end_time[:10] + '_Wind_Plot_Ready.csv', index=False, encoding='utf-8')
        num += 1


def quarter_loc_func(quarter_year):
    """
    this function makes a list of all relivant quarters and years between your start_time and end_time it also returns
    the quarter for your title

    Parameters
    __________
    quarter_year : list of str
        list of all quarter year strings inside user specified start and end dates.

    Returns
    ________
    list of ints, str
        returns list of wanted months for the quarter you are using and a title string of that quarter
    """

    quarter = quarter_year[:2]
    if quarter == 'Q1':
        good_months = [1, 2, 3]
    elif quarter == 'Q2':
        good_months = [4, 5, 6]
    elif quarter == 'Q3':
        good_months = [7, 8, 9]
    else:
        good_months = [10, 11, 12]
    return good_months, quarter


def wind_column_correction_func(wind_list):
    """
    this function replaces 'wsp_avg_ms' & 'wdr_avg' headers with 'wsp' & 'wdr' for all df's in a list of df's

    Parameters
    __________
    wind_list : list of objects
        list of all met df's imported

    Returns
    ________
    list of objects
        returns list of df's with unwanted header names replaced
    """
    header_correction_list = []
    for df in wind_list:
        if 'wsp_avg_ms' in df.columns and 'wdr_avg' in df.columns:
            df = df.rename(columns={"wsp_avg_ms": "wsp", "wdr_avg": "wdr"})
            header_correction_list.append(df)
        else:
            header_correction_list.append(df)
    return header_correction_list


def lat_lon_column_func(combine_data, data_parameters):
    """
    this function adds latitude "lat" and longitude "lon" columns to each df based on site

    Parameters
    __________
    combine_data : list of objects
        list of all combine df's (one for each site)
    data_parameters : object
        class object storing parameters and constants for making windrose ready files

    Returns
    ________
    list of objects
        returns list of df's with lat and lon columns added specific to each site's combine df
    """
    for i in range(len(data_parameters.sites)):
        combine_data[i]['lat'] = LAT_LON_DICT.get(data_parameters.sites[i])[0]
        combine_data[i]['lon'] = LAT_LON_DICT.get(data_parameters.sites[i])[1]
    return combine_data