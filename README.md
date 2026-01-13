# 2025-Cosmic-Motor-Power-Analysis

I did some analysis of the power used while competing at 2025 CoSMiC.
All data from the `lance_log_data_2025_05_24-13_24_51` rosbag. 
At this time we were operating on 4S Lipos at ~14-16 VDC

## Methodology

I dumped the data from the rosbag into CSV files stored in `raw`
The raw data was taken in approximately 0.05 second intervals

For each motor, I calculated an equivalent windowed VRMS value using the Discrete Time Sliding Window calculation method with a window size of 0.1, 1, 3, 5, 10, and 60 seconds. After this is calculated I may or may not drop any zero terms.

For each motor I looked at output / stator current, and supply current to the motor controller. 

## Output Spec

### XLSX Files
There is one XLSX file per motor. It contains the raw data, then one page of calculated RMS values for each window size at both the input and output current sensor. Each page of calculated RMS values also contains the calculated means with and without zeros included, and calculated Q0, Q1, Q2, Q3, andQ4 points for the data set with the zeros dropped.

### Box Plots
There are 4 sets of box plots for each motor. 

|                | Zeros Included                        | Zeros Dropped                            |
|----------------|---------------------------------------|------------------------------------------|
| Output Current | *.info.csv_output_current_boxplot.png | *.info.csv_output_current_nz_boxplot.png |
| Input Current  | *.info.csv_input_current_boxplot.png  | *.info.csv_input_current_nz_boxplot.png  |

The Y axis has units of Amps
The X axis is spaced by Raw Data, then each of the sliding window sizes in order from least to greatest.