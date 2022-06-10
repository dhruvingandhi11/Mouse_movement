
from time import time,sleep
import subprocess
import csv





def record_concurrent_applications(closing_event, expected_run_duration,time_steps_for_app_log,file_name, t1_status= True, t2_status=True):
    print('application log started...')
   
    #Overall recording times
    record_start_time = time()
    expected_end_time = record_start_time + expected_run_duration
    print(f'applicatrion {record_start_time=}')
    print(f'application log {time_steps_for_app_log=}')
    
    #for loging application
    applicatios = []
    last_set = set()        # initialise empty set for comparision
    
    #loop initialise parameters
    counter = 0
    #last_event_start_time = time() - time_steps_for_app_log

    #define writer to write current applications to csv file
    csvfile = open(f'results/{file_name}_applog.csv', 'w', newline='\n')
    writer = csv.writer(csvfile)
    
    while time() < expected_end_time:
        loop_start_time = time()
        if closing_event.is_set():
            print('Received closing_event flag. Closing recording of the logs of current application')
            break

        # #Check if certain time is lapsed as per 'time_steps_for_app_log' (based on fps)
        # if loop_start_time - last_event_start_time >= time_steps_for_app_log:

        #last_event_start_time = loop_start_time
        counter +=1 
        #print(f"------{counter}-------")
        print(f'\n-----{counter}-------')
        

        #Get current running applications at this time
        current_app = [0]
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
        # cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for j,line in enumerate(proc.stdout):
            if line.rstrip() and j>2:
                # only print lines that are not empty
                # decode() is necessary to get rid of the binary string (b').... # rstrip() to remove `\r\n`
                current_app.append(line.decode().rstrip())
            
        current_set = set(current_app)
        print(f'{current_set=}')
        print(f'{last_set=}')
        if "Slack" not in current_set:
            print("'Slack' is closed or not started yet. Closing recording of the logs of current application")
            print('Also, Enabling Flag for closing_event')
            closing_event.set()
            break

        if current_set != last_set:
            print("Not same")
            current_app[0] = loop_start_time - record_start_time
            applicatios.append([current_app])
            #write in csv file
            writer.writerows([current_app])
        last_set = current_set 
        
 
        pause_time = loop_start_time + time_steps_for_app_log - time()
        sleep(pause_time)
            
             
    # return applicatios 
    print('Application logging closed.')


# #saving data to csv file       
# with open(f'application_log.csv', 'w', newline='\n') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(applicatios)