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

## Results

### Hopper Linear Actuators
![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_act.info.csv_output_current_boxplot.png)

![img2](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_act.info.csv_output_current_nz_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_act.info.csv_supply_current_boxplot.png)

![img2](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_act.info.csv_supply_current_nz_boxplot.png)

### Hopper Belt
![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_belt.info.csv_output_current_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_belt.info.csv_output_current_nz_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_belt.info.csv_supply_current_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/hopper_belt.info.csv_supply_current_nz_boxplot.png)

### Left Track

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_left.info.csv_output_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_left.info.csv_output_current_nz_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_left.info.csv_supply_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_left.info.csv_supply_current_nz_boxplot.png)

### Right Track

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_right.info.csv_output_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_right.info.csv_output_current_nz_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_right.info.csv_supply_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/track_right.info.csv_supply_current_nz_boxplot.png)

### Trencher


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/trencher.info.csv_output_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/trencher.info.csv_output_current_nz_boxplot.png)

![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/trencher.info.csv_supply_current_boxplot.png)


![img](https://raw.githubusercontent.com/Cardinal-Space-Mining/2025-Cosmic-Motor-Power-Analysis/refs/heads/main/out/trencher.info.csv_supply_current_nz_boxplot.png)

## Conclusion

We are not in the realm of steady state DC or AC electronics that the 2017 NEC covers. The vast majority of the time, the motors are off or at very low current draws, however they have brief transient events up to and exceeding 140A. As a result, I will spec everything to a FOS of 1.5 with respect to the Q3 value the non-zero supply current at a RMS window of 1 Second, and will rely on the high heat capacitance of copper to handle the short duration high current pulses.

|                 | Supply Current, Nz, 1s IRMS, Q3 (A-RMS) | Ampacity at FOS of 1.5 | Suggested NEC Wire Gauge | Chosen Wire Gauge |
|-----------------|-----------------------------------------|------------------------|--------------------------|-------------------|
| Hopper Actuator | 0.83                                    | 1.245                  | 14                       | 14                |
| Hopper Belt     | .4                                      | .6                     | 14                       | 14                |
| Trencher        | 3.5                                     | 5.25                   | 14                       | 14                |
| Right Track     | 5.04                                    | 7.56                   | 14                       | 12                |
| Left Track      | 8.13                                    | 12.195                 | 14                       | 12                |

I will spec the track wires a gauge higher for greater efficiency. The mass cost of this decision is low as the track motors are the closest motors to the electrical box, and because the tracks consume the majority of power used by the system from a mechanical perspective. According to my calculations this will earn us ~0.4 of a point.
