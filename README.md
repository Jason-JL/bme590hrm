# This is a Heart Rate Monitor

### Usage:
the program provides a dialog to choose the interested ECG singal file. The file should contains and only contains two column data. The first column is time, the second colum is voltage value.

To program provides methods to get voltage_extremes, duration, numb_beats, beats, mean_hr_bpm from the selected file. To get them, just using pandas read the csv file and gives the column name: time, volt. Then call the process methods given in hbAnalysis module. The main module gives an example of the whole process. From Choosing file, reading data, data analysis and writing out to file. 
