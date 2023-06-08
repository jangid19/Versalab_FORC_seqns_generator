# -*- coding: utf-8 -*-
'''Functions for generating FORC sequence files
    Some fctns are used to process the FORC .data files to 'generic FORC files'
    11-2022: Written by Rahul Jangid for use by R. Kukreja's group
'''
from sys import platform
import pandas as pd
import numpy as np
from pathlib import Path
import os

def concat_type():
    """Function returns concat type depending on OS

    Returns:
        concat (string): returns concat type depending on OS
    """
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        concat_3 = "{0}/{1}/{2}"
        concat_2 = "{0}/{1}"
        concat_1 = "/"
    elif platform == "win64" or platform == "win32":
        concat_3 = "{0}\\{1}\\{2}"
        concat_2 = "{0}\\{1}"
        concat_1 = "\\"
    else:
        concat_3 = "{0}\\{1}\\{2}"
        concat_2 = "{0}\\{1}"
        concat_1 = "\\"
    return concat_1, concat_2, concat_3

def seqns_comment(comment = str):
    """Adds a comment line in FORC sqence file given the comment

    Args:
        comment (type = string): String to be inserted as comment. Defaults to str.

    Returns:
        String: returns the comment line
    """
    line = f"REM ##{comment}"
    return line

def seqns_set_field(field = float, ramp_rate = 100, apprach_type = 0):
    """Generates a set field line in sequence files

    Args:
        field (float): _description_. Defaults to float.
        ramp_rate (float): _description_. Defaults to 100 Oe.
        apprach_type (int): set approach type. 0 = linear, 2 = oscillate. Defaults to linear approach 

    Returns:
        String: returns the set field line
    """
    line = f"FLD FIELD {field} {ramp_rate} {apprach_type} 0"
    return line

def seqns_set_temp(temp = float, rate = 10, mode = 0):
    """Generates the line to set temp in seqns files

    Args:
        temp (float, 50<T<400): Set temperature. Defaults to float.
        rate (float, 0<rate<10): rate of temp change. Defaults to 10 K/min.
        mode (int, 0 or 1): mode for approaching the temp (0 = Fast settle, 1 = No overshoot). Defaults to 0/Fast settle.

    Returns:
        str: returns the set temp line
    """
    line = f"TMP TEMP {temp} {rate} {mode}"
    return line
    

def seqns_wait_for_settle(wait_time = 100, temp_bool = 1, field_bool = 1):
    """Generates a wait for field, temp or both in sequence files

    Args:
        wait_time (int >= 0): wait time in sec. Defaults to int.
        temp_bool (int = 0 or 1): wait for temp = 1, no wait for temp = 0. Defaults to 1.
        field_bool (int = 0 or 1): wait for field = 1, no wait for temp = 0. Defaults to 1.

    Returns:
        String: returns line for seq file to set wait time for field or temp or both
    """
    line = f"WAI WAITFOR {wait_time} {temp_bool} {field_bool} 0 0 0"
    return line

def seqns_add_cmmt_in_data(comment = str):
    """Generates a comment line inside the datafile

    Args:
        comment (str): Comment to be added. Defaults to str.

    Returns:
        string: line in seq for adding comment to data file
    """
    line = f"VSMCM \"{comment}\""
    return line
    
def seqns_create_data_file(file_directory = str, file_name = str):
    """Generates a line in sequence to create a new datafile

    Args:
        file_directory (str): directory for saving the data. Defaults to str.
        file_name (str): file name. Defaults to str.

    Returns:
        str: string with the command for generating a new data file in seq file
    """
    # if platform == "linux" or platform == "linux2" or platform == "darwin":
    #     concat_1 = "/"
    # elif platform == "win64":
    #     concat_1 = "\\"
    # else:
    #     concat_1 = "\\"
    concat_1, _, _ = concat_type()
        
    line = f"VSMDF \"{file_directory}{concat_1}{file_name}\""
    return line
        
def seqns_add_touchdown():
    """Generates a command for centering the sample

    Returns:
        str: center sample command
    """
    line = "VSMLS 1 0 0 0 0 0"
    return line

def seqns_adv_measurement(freq = 39.7, amp = 2, avg_time = 1, start_stop_bool = 0, measuremet_type = 1):
    # 0 = start, 1 = stop for start stop measurement
    # measurement type:single measuremtn = 1, continuous measuremnt = 0
    """Generate a line for advanced manual measurement in seqns files

    Args:
        freq (float): Sample oscillation freq. Defaults to 39.7 Hz.
        amp (int): Sample oscillation amplitude. Defaults to 2 mm.
        avg_time (int): Avging time for measurement. Defaults to 1 sec.
        start_stop_bool (int, 0 or 1): start (=0) or stop (=1) measurement. Defaults to 0/start measurement.
        measuremet_type (int, 0 or 1): single (=1) or continuous (=0) measurement. Defaults to 1/single measurement.

    Returns:
        str: advanced measurement command line
    """
    psudo_time = avg_time*40 - 1
    line = f"VSMCO {psudo_time} 0 0 {measuremet_type} {start_stop_bool} {amp} {freq} {avg_time} 0 2 0 \"A/C,0,10,10,0\""
    return line

def seqns_MvsH_sweep_measurement(freq = 39.7, amp = 2, min_field = -400, mid_field = 0, max_field = 400,  step_size = 1, avging_time = 1):
    """_summary_

    Args:
        freq (float): Sample oscillation freq. Defaults to 39.7 Hz.
        amp (int): Sample oscillation amplitude. Defaults to 2 mm.
        avg_time (int): Avging time for measurement. Defaults to 1 sec.
        min_field (int, optional): _description_. Defaults to -400 Oe.
        mid_field (int, optional): _description_. Defaults to 0 Oe.
        max_field (int, optional): _description_. Defaults to 400 Oe.
        step_size (int, optional): _description_. Defaults to 1 Oe.

    Returns:
        str: MvsH in sweep mode without autocentering command line
    """
    line = f"VSMMH 1 0 0 0 0 {amp} {freq} {avging_time} 0 2 0 1 2 {min_field} {mid_field} {max_field} {step_size} 0 10000 {step_size} 0 2 1 0 1 0 \"A/C,0,10,10,0\" "
    return line

def seqns_FORC_measurements_V1(set_temp = 50, temp_rate = 10, ampli = 2, freq = 39.7, H_sat = 1000, max_field = 300, min_field = -300, max_reversal_field = 100,\
    min_reversal_field = -300, N_FORCs = 200, step_size = 0.5, avging_time = 1, N_repeat = 1, seq_file_path_n_name = str, data_file_path = str, data_file_name = str):
    """Generates a seqns file to do FORC measurements for Quantum Design VSM

    Args:
        set_temp (int, 50 < T < 400): Set temp for FORC measurements in K. Defaults to 50 K.
        temp_rate (int, 0 < dT < 10): Set temp ramp rate in K/min. Defaults to 10 K/min.
        ampli (int, 1 < A < 4): Set the amplitude of sample viberation in mm. Defaults to 2 mm.
        freq (float, optional): Freq to viberate the sample at in Hz. Defaults to 39.7 Hz.
        H_sat (int, optional): Saturating field in Oe. Defaults to 1000 Oe.
        max_field (int, optional): _description_. Defaults to 300 Oe.
        min_field (int, optional): _description_. Defaults to -300 Oe.
        max_reversal_field (int, optional): _description_. Defaults to 100 Oe.
        N_FORCs (int, optional): _description_. Defaults to 200.
        step_size (float, optional): _description_. Defaults to 0.5 Oe.
        avging_time (int, optional): _description_. Defaults to 1 sec.
        N_repeat (int, optional): _description_. Defaults to 1. #### Still working on this!!!
        seq_file_path_n_name (_type_, optional): path/name of the seqns file. Defaults to str.
        data_file_path (_type_, optional): data file path. Defaults to str.
        data_file_name (_type_, optional): data file name. Defaults to str.
    """
    # Calculating the step size in reversal field
    field_range = max_reversal_field - min_reversal_field
    dHa = field_range/N_FORCs
    
    with open(seq_file_path_n_name, 'w') as f:
        for idx in range(N_FORCs-1):
            # Chaning the Ha field
            Ha_field = max_reversal_field-(idx+1)*dHa
            FORC_number = str(idx+1).zfill(3)
            if idx == 0:
                # Initial temp setup
                f.write(seqns_set_field(field = 0, ramp_rate = 100, apprach_type = 0))
                f.write('\n')
                f.write(seqns_set_temp(temp = set_temp, rate = temp_rate, mode = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 3600, temp_bool = 1, field_bool = 1))
                f.write('\n')
                f.write(seqns_add_touchdown())
                f.write('\n')
                
                # Start saturation measurement
                f.write(seqns_comment(f"FORC_{FORC_number}"))
                f.write('\n')
                f.write(seqns_create_data_file(file_directory = data_file_path, file_name = data_file_name))
                f.write('\n')
                f.write(seqns_set_field(field = H_sat, ramp_rate = 50, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 0, measuremet_type = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 1, measuremet_type = 1))
                f.write('\n')
                
                # Start FORC measurement
                f.write(seqns_add_cmmt_in_data(comment = "start_data_FORC"))
                f.write('\n')
                f.write(seqns_set_field(field = Ha_field, ramp_rate = dHa, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_MvsH_sweep_measurement(freq = freq, amp = ampli, min_field = min_field, mid_field = Ha_field,\
                    max_field = max_field,  step_size = step_size, avging_time = avging_time))
                f.write('\n')
                f.write(seqns_add_cmmt_in_data(comment = "end_data_FORC"))
                f.write('\n')
            elif idx > 0 and idx < (N_FORCs-2):
                # Start saturation measurement
                f.write(seqns_comment(f"FORC_{FORC_number}"))
                f.write('\n')
                f.write(seqns_set_field(field = H_sat, ramp_rate = 50, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 0, measuremet_type = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 1, measuremet_type = 1))
                f.write('\n')
                
                # Start FORC measurement
                f.write(seqns_add_cmmt_in_data(comment = "start_data_FORC"))
                f.write('\n')
                f.write(seqns_set_field(field = Ha_field, ramp_rate = dHa, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_MvsH_sweep_measurement(freq = freq, amp = ampli, min_field = min_field, mid_field = Ha_field,\
                    max_field = max_field,  step_size = step_size, avging_time = avging_time))
                f.write('\n')
                f.write(seqns_add_cmmt_in_data(comment = "end_data_FORC"))
                f.write('\n')
            elif idx == (N_FORCs-2):
                # Start saturation measurement
                f.write(seqns_comment(f"FORC_{FORC_number}"))
                f.write('\n')
                f.write(seqns_set_field(field = H_sat, ramp_rate = 50, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 0, measuremet_type = 1))
                f.write('\n')
                f.write(seqns_adv_measurement(freq = freq, amp = 2, avg_time = 2, start_stop_bool = 1, measuremet_type = 1))
                f.write('\n')
                
                # Start FORC measurement
                f.write(seqns_add_cmmt_in_data(comment = "start_data_FORC"))
                f.write('\n')
                f.write(seqns_set_field(field = Ha_field, ramp_rate = dHa, apprach_type = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 0, field_bool = 1))
                f.write('\n')
                f.write(seqns_MvsH_sweep_measurement(freq = freq, amp = ampli, min_field = min_field, mid_field = Ha_field,\
                    max_field = max_field,  step_size = step_size, avging_time = avging_time))
                f.write('\n')
                f.write(seqns_add_cmmt_in_data(comment = "end_data_FORC"))
                f.write('\n')
                
                # Ending seqns with setting 300 K and 0 Oe field
                f.write(seqns_set_field(field = 0, ramp_rate = 100, apprach_type = 0))
                f.write('\n')
                f.write(seqns_set_temp(temp = 300, rate = temp_rate, mode = 0))
                f.write('\n')
                f.write(seqns_wait_for_settle(wait_time = 5, temp_bool = 1, field_bool = 1))
                f.write('\n')

            # f.write('\n')
            
    print("Done generating the sequence file!!!")
    print("Seqence exported at:")
    print(seq_file_path_n_name)
    
def import_first_n_lines(file_path, n):
    """_summary_

    Args:
        file_path (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, 'r', encoding='cp1252') as f:
        lines = []
        for i, line in enumerate(f):
            lines.append(line)
            if i == n - 1:
                break
    return lines

def n_row_avg(df, N_rows = int):
    """Averages N_rows of a df and returns a new_df of size df/N_row

    Args:
        df (_type_): _description_
        N_rows (_type_, optional): _description_. Defaults to int.

    Returns:
        _type_: _description_
    """
    new_df = df.groupby(df.index//N_rows).mean()
    return new_df

def find_string_index(string_list, string_to_find):
    """_summary_

    Args:
        string_list (_type_): _description_
        string_to_find (_type_): _description_

    Returns:
        _type_: _description_
    """
    for i, s in enumerate(string_list):
        if s == string_to_find:
            return i
    return -1


def find_substring_index(string_list, substring):
    """_summary_

    Args:
        string_list (_type_): _description_
        substring (_type_): _description_

    Returns:
        _type_: _description_
    """
    for i, s in enumerate(string_list):
        if s.find(substring) != -1:
            return i
    return False

def delete_rows_with_substring(df, column, substring):
    #Find the index of the substring in the specified column
    index = df[column].apply(lambda x: x.find(substring) if type(x) == str else -1)
    #Find the rows that contain the substring
    rows_to_delete = df[index >= 0].index
    #Delete the rows
    return df.drop(rows_to_delete)


def delete_rows_with_number(df, column, number):
    # Find the rows that contain the number
    mask = df[column].round(0) == number
    # Delete the rows
    return df[~mask]

def get_files_from_dir(directory, extension):
    """_summary_

    Args:
        directory (str): Directory in which to search for files
        extension (str): extensition of files to look for

    Returns:
        data_files(list): returns a list containing both file names and full file path
    """
    # Initialize an empty list to store the file names and paths
    dat_files = []

    # Get the list of files in the directory
    files = os.listdir(directory)

    # Iterate through the list of files
    for file in files:
    # Check if the file is a .extension file
        if file.endswith(extension):
            # Get the file name and path
            file_name = file
            file_path = os.path.join(directory, file)
            # Add the file name and path to the list
            dat_files.append((file_name, file_path))
        
    # Return the list of file names and paths
    return dat_files

def gen_PMC_FORC_file(path_PMC_header, path_data_file_dir, path_final_PMC_file, avging_time = 0.5):
    """Generates a PMC .forc file from single .DAT file from VSM  

    Args:
        path_PMC_header (str): path to the sample PMC FORC file to steal headers from.
        path_data_file_dir (str): path to the dir storing the single .DAT data file.
        path_final_PMC_file (str): path and name of the final file. example: "path/NN9_FORCs_PMC_try_6_1.forc"
    """
    # Getting all files from the dir
    path_data_file = get_files_from_dir(path_data_file_dir, ".DAT")[0][1]
    
    # Importing data
    data = pd.read_csv(path_data_file, skiprows=30)
    
    # Calculating number of data points
    num_data_points = len(data) - data['Magnetic Field (Oe)'].isna().sum()
    
    # Select the column you want to count the string in
    column = data['Comment']

    # Select the string you want to count
    string = 'START_DATA_FORC'

    # Count the number of times the string appears in the column
    num_FORCs = column.str.count(string).sum()
    
    # Importing the header lines to use for PMC files
    header_lines = import_first_n_lines(path_PMC_header, 86)
    
    # Finding index of the NForcs and NSegments line
    list_rplace_header_lines = ['NForc', 'segments', 'Averaging time', 'Number of data']
    index_header_replace = []
    for idx in list_rplace_header_lines:
        temp_index = find_substring_index(header_lines, idx)
        index_header_replace.append(temp_index)
        
    # index_NForcs_PMC = find_substring_index(header_lines, 'NForc')
    # index_NSegments_PMC = find_substring_index(header_lines, 'segments')
    # index_Avging_time_PMC = find_substring_index(header_lines, 'Averaging time')
    # index_Num_Data_Points = find_substring_index(header_lines, 'Number of data')
    
    # Replacing the real NForcs and Nsegments in the line
    list_rplace_lines = [f'NForc                           {int(num_FORCs)}\n', 
                         f'Number of segments              {int(num_FORCs*2)}\n',
                         f'Averaging time                 +{int(avging_time*10)}00.0000E-03\n',
                         f'Number of data                  {int(num_data_points)}\n']
    
    for idx, _ in enumerate(list_rplace_header_lines):
        header_lines[index_header_replace[idx]] = list_rplace_lines[idx]

    # header_lines[index_NForcs_PMC] = f'NForc                           {int(num_FORCs)}\n'
    # header_lines[index_NSegments_PMC] = f'Number of segments              {int(num_FORCs*2)}\n'
    # header_lines[index_Avging_time_PMC] = f'Averaging time                 +{int(avging_time*10)}00.0000E-03\n'
    # header_lines[index_Num_Data_Points] = f'Number of data                  {int(num_data_points)}\n'
    
    # Parameters to plot
    x_param = 'Magnetic Field (Oe)'
    y_param = 'Moment (emu)'
    
    # # Empty row at the end of each dataset
    # empty_row = pd.Series([None, None], index=['Field', 'Moment'])

    # Adding "END" in the last line
    end_line = pd.Series(['MicroMag 2900/3900 Data File ends', np.NAN], index=['Field', 'Moment'])

    # Creating the pd.DataFrame
    df = pd.DataFrame(columns=['Field', 'Moment'])

    # Changing to SI units
    x = ((data[x_param]*10**-4).tolist())
    y = ((data[y_param]*10**-3).tolist())

    # Creating a temp dataframe
    temp_df = pd.DataFrame(list(zip(x, y)), columns = ['Field', 'Moment'])

    # # Appending the data and the last line
    # df = df.append(temp_df, ignore_index=True)
    # df = df.append(end_line, ignore_index=True)
    
    # Appending the data and the last line
    df = pd.concat([df, temp_df])
    df = pd.concat([df, end_line])
    
    # Exporting the pd dataframe as .forc
    with open(Path.cwd().joinpath(path_final_PMC_file), "w", encoding='cp1252') as f:
        f.write(''.join(str(e) for e in header_lines))
        
    # Appending the data to created file with headers. Exporting the pd dataframe as .forc
    with open(Path.cwd().joinpath(path_final_PMC_file), "a", encoding='cp1252') as f:
        f.write("\n".join([l.strip(",\n") for l in df.to_csv(index=False, header=None, float_format='%.15f', line_terminator = '\n').split("\n")]))
        
    print('Done generating a PMC file from the VSM measurement file!!')
    

def gen_generic_FORC_file_from_PMC_data(path_data_file_dir, path_final_PMC_file, generic_type = 'FORCinel', saturating_field = 500):
    """Generates a generic forc file from PMC type single .DAT file from VSM  

    Args:
        path_PMC_header (str): path to the sample PMC FORC file to steal headers from.
        path_data_file_dir (str): path to the dir storing the single .DAT data file.
        path_final_PMC_file (str): path and name of the final file. example: "path/NN9_FORCs_PMC_try_6_1.forc"
    """
    # Getting all files from the dir
    path_data_file = get_files_from_dir(path_data_file_dir, ".DAT")[0][1]
    
    # Importing data
    data = pd.read_csv(path_data_file, skiprows=30)
    
    # Delete rows that contain the substring 'de' in the 'col1' column of the dataframe
    data = delete_rows_with_substring(data, 'Comment', 'START_DATA_FORC')
    data = delete_rows_with_number(data, 'Magnetic Field (Oe)', saturating_field)
    
    # Parameters to plot
    x_param = 'Magnetic Field (Oe)'
    y_param = 'Moment (emu)'
    
    # # Empty row at the end of each dataset
    # empty_row = pd.Series([None, None], index=['Field', 'Moment'])

    # Adding "END" in the last line
    end_line = pd.Series(['END', np.NAN], index=['Field', 'Moment'])

    # Creating the pd.DataFrame
    df = pd.DataFrame(columns=['Field', 'Moment'])

    # Changing to SI units
    x = ((data[x_param]*10**-4).tolist())
    y = ((data[y_param]*10**-3).tolist())

    # Creating a temp dataframe
    temp_df = pd.DataFrame(list(zip(x, y)), columns = ['Field', 'Moment'])

    # # Appending the data and the last line
    # df = df.append(temp_df, ignore_index=True)
    # df = df.append(end_line, ignore_index=True)
    
    # # Appending the data and the last line
    # df = pd.concat([df, temp_df])
    # df = pd.concat([df, end_line])
    
    if generic_type == 'FORCinel':
        # Appending the data and the last line
        df = pd.concat([df, temp_df])
        df = pd.concat([df, end_line])
        
        with open(Path.cwd().joinpath(path_final_PMC_file), "w") as f:
            f.write("\n".join([l.strip(",\n") for l in df.to_csv(index=False, header=None, float_format='%.15f', line_terminator = '\n').split("\n")]))
            
        # Removing the empty last line
        with open(path_final_PMC_file) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace('\r','').replace('\n','')
        with open(path_final_PMC_file, 'w') as wr:
            wr.writelines(lines)
        print('Done generating a FORCinel file from the VSM measurement file!!')
        
    elif generic_type == 'doFORC':
        # Appending the data and the last line
        df = pd.concat([df, temp_df])
        
        with open(Path.cwd().joinpath(path_final_PMC_file), "w") as f:
            f.write("\n".join([l.strip(",\n") for l in df.to_csv(index=False, header=None, float_format='%.15f', line_terminator = '\n').split("\n")]))
            
        # Removing the empty last line
        with open(path_final_PMC_file) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace('\r','').replace('\n','')
        with open(path_final_PMC_file, 'w') as wr:
            wr.writelines(lines)
        print('Done generating a doFORC file from the VSM measurement file!!')
        