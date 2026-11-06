import os
import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.max_colwidth = None

file_path = "machine_condition_dataset.csv"

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
    print("The CSV file has been succesfully loaded.")
else:
    print("The CSV file does not exist. Please check the file path and try again.")
    raise SystemExit

print(data.head())

num_rows, num_cols = data.shape
print("Number of columns =", num_cols)
print("Number of rows =", num_rows)

data['Status'] = None
data['Recommended_Action'] = None

def classify_condition(test_num):
    row = data.iloc[test_num - 1].values
    temperature = row[2]
    pressure = row[3]
    vibration = row[4]
    current = row[5]
    rpm = row[6]

    if temperature > 50 or pressure > 6 or vibration > 6 or current > 5 or rpm < 1350 or rpm > 1550:
        status = "CRITICAL"
    elif temperature >= 40 or pressure < 2 or vibration >= 3 or current >= 4 or rpm < 1400 or rpm > 1500:
        status = "WARNING"
    else:
        status = "NORMAL"

    return status

def determine_action(status):
    if status == "CRITICAL":
        Recommended_Action = "Stop operation in the simulation and request supervisor/technician inspection."
    elif status == "WARNING":
        Recommended_Action = "Continue monitoring and arrange inspection."
    else:
        Recommended_Action = "Continue normal monitoring in the simulation."
    return Recommended_Action

def add_column():
    test_num = 1    
    while test_num <= 30:
        data.loc[test_num-1, 'Status'] = classify_condition(test_num)
        data.loc[test_num-1, 'Recommended_Action'] = determine_action(data.loc[test_num-1, 'Status'])
        test_num+=1

def print_summary():
    value_set = data.iloc[:, [2,3,4,5,6]]
    mean_set = value_set.mean()
    max_set = value_set.max()
    min_set = value_set.min()
    print("Mean Temperature =", round(mean_set.iloc[0], 2), "°C")
    print("Mean Pressure =", round(mean_set.iloc[1], 2), "bar")
    print("Mean Vibration =", round(mean_set.iloc[2], 2), "mm/s")
    print("Mean Current =", round(mean_set.iloc[3], 2), "A")
    print("Mean RPM =", round(mean_set.iloc[4], 2), "RPM")
    print("Max Temperature =", max_set.iloc[0], "°C")
    print("Max Pressure =", max_set.iloc[1], "bar")
    print("Max Vibration =", max_set.iloc[2], "mm/s")
    print("Max Current =", max_set.iloc[3], "A")
    print("Max RPM =", max_set.iloc[4], "RPM")
    print("Min Temperature =", min_set.iloc[0], "°C")
    print("Min Pressure =", min_set.iloc[1], "bar")
    print("Min Vibration =", min_set.iloc[2], "mm/s")
    print("Min Current =", min_set.iloc[3], "A")
    print("Min RPM =", min_set.iloc[4], "RPM")

    status_list = data.iloc[:, [7]]
    status_count = status_list.value_counts()
    print("No. of NORMAL =", status_count.iloc[1])
    print("No. of WARNING =", status_count.iloc[0])
    print("No. of CRITICAL =", status_count.iloc[2])
    status = 1
    status_percentage = pd.Series()
    while status <= 3:
        status_percentage[status - 1] = (status_count.iloc[status - 1] / status_count.sum()) * 100
        status+=1
    print("% NORMAL =", round(status_percentage[1], 2),"%")
    print("% WARNING =", round(status_percentage[0], 2),"%")
    print("% CRITICAL =", round(status_percentage[2], 2),"%")

def graph_plot():
    figure_1, axis_1 = plt.subplots()
    plt.plot(data["Time_s"], data["Temperature_C"], marker='o')
    axis_1.axhline(y=40, color='yellow', linestyle='--', label='Warning Treshold')
    axis_1.axhline(y=50, color='red', linestyle='--', label='Critical Boundary')
    axis_1.set_xlabel("Time (s)")
    axis_1.set_ylabel("Temperature (°C)")
    axis_1.set_title("Temperature-Versus-Time Graph")
    axis_1.legend()
    axis_1.grid(True)

    figure_2, axis_2 = plt.subplots()
    plt.plot(data["Time_s"], data["Vibration_mm_s"], marker='o')
    axis_2.set_xlabel("Time (s)")
    axis_2.set_ylabel("Vibration (mm/s)")
    axis_2.set_title("Vibration-Versus-Time Graph")
    axis_2.grid(True)

    plt.show()

add_column()
print_summary()
print(data)
graph_plot()