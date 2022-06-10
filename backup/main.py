from datetime import datetime
from utils import record_mouse_events, save_data_to_csv, plot_and_save, read_data_from_csv
from current_programs import record_concurrent_applications
import threading
from threading import Event

#inpout parameters
fps =  100
expected_run_duration = 30     # In seconds
max_idle_time = 100             # In seconds
time_steps_for_app_log = 5    # in seconds. eg. after every 10 seconds


#define file name
file_name = f'{datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")}'


# create a shared event object
# closing_event.is_set() will give False. Untile closing_event.set().
closing_event = Event()


t1 = threading.Thread( target = record_mouse_events, 
                       args = (closing_event,fps, expected_run_duration, max_idle_time, file_name))
t2 = threading.Thread( target = record_concurrent_applications, 
                       args = (closing_event, expected_run_duration, time_steps_for_app_log, file_name))
t1.start()
t2.start()
t1.join()
t2.join()


#Collect data and save to csv file
# record_mouse_events(fps, expected_run_duration, max_idle_time, file_name)

# #Collect concurrent applications and save to csv file
# record_concurrent_applications(expected_run_duration,time_steps_for_app_log,file_name)

# #Save data to csv
# save_data_to_csv(data, file_name)

# read data from csv
data = read_data_from_csv(file_name)

#Plot and save data: 3D animation, 3D plot image
plot_and_save(data, file_name)


