from utils import plot_and_save,read_data_from_csv


file_path = "D:\kulin\mouse-movement-detection\\results/2022_06_08_12_32_11_PM.csv"


#run the function
file_name = file_path.split('/')[-1]
file_name = file_name.split('.')[0]
print(f'{file_name=}')


data = read_data_from_csv(file_name)
plot_and_save(data, file_name)

