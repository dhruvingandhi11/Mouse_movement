from pynput import mouse
from time import time,sleep
import csv
import numpy as np
import matplotlib.pyplot as plt


def record_mouse_events(closing_event,
                        fps=100, 
                        expected_run_duration=30, 
                        max_idle_time=10,
                        file_name = 'test',
                        ):
    ''' this function records mouse events. and returns the data in a list of lists. (optionally returns the data, commented code below)
        It also saves the data to a csv file.
    fps                     : frames per second that we want to record.
    expected_run_duration   : how long we want to record the mouse event.
    max_idle_time           : how long we want to continue recording if there is no mouse event.
    data                    : list of lists. each list contains the mouse event data.
                            - Each sub-list contains the following data: timestamp, x, y, left_click, right_click
                            - Right_click is 1 if right click is pressed, 0 otherwise. same for left_click.
                            - x and y are the mouse position on the screen.
                            - timestamp is the time in seconds since the start of the recording.
    '''

    #Overall recording
    record_start_time = time()
    print('type of time =',type(record_start_time ), record_start_time)
    # exit()
    expected_end_time = record_start_time + expected_run_duration
    print(f'{record_start_time=}')
    
    time_steps = 1/fps # seconds. 1/fps = time between frames
    print(f'{time_steps=}')
    data =  []
    
    #loop initialise parameters
    idle_time = False
    counter = 0
    #last_event_start_time = time()
    x,y,left,right = 0,0,0,0
    
    with mouse.Events() as events:
        #define writer to write events to csv file
        csvfile= open(f'results/{file_name}.csv', 'w', newline='\n')
        writer = csv.writer(csvfile)
        loop_start_time = time()
        f_time = 0
        
        # run while loop till [Condition] i.e [counter number of frames] or  [expected_run_duration]
        # or 'idle_time' is reached to 'max_idle_time'
        while time() < expected_end_time:
        #while True:
            loop_start_time = time()

            if closing_event.is_set():
                print('Received closing_event flag. Closing record_mouse_events')
                break

            counter +=1 
            print(f"------{counter}-------")
            
            #Get mouse event
            event = events.get(0)
            if event is None:       #idle time
                left,right = 0,0    # x,y remains same
                #Check of max idle time is reached
                if idle_time == False:
                    #initialise idle time
                    idle_time_start = time()
                    idle_time = True
                    #print('waiting for mouse event...')
                if time() - idle_time_start > max_idle_time:
                    #break loop if max idle time is reached
                    print(f'You did not interact with the mouse since last {max_idle_time} seconds. Have a good day!')
                    print('Activating Flag for closing_event as True after inactivity.')
                    closing_event.set()
                    break 
            
            else:
                idle_time = False
                #print(f'Received event {event}')
                
                #Mouse moved to new position
                if str(type(event)) == "<class 'pynput.mouse.Events.Move'>": #Change it later
                    x,y = event.x, event.y
                    left,right = 0,0
                
                #Press mouse button   
                elif str(type(event)) == "<class 'pynput.mouse.Events.Click'>":
                    x,y  = event.x, event.y
                    if event.pressed:
                        if event.button == mouse.Button.left:
                            left,right = 1,0
                      
                        if event.button == mouse.Button.right:
                            left,right = 0,1



            #data.append([loop_start_time - record_start_time,x,y,left,right])

            writer.writerow([loop_start_time - record_start_time,x,y,left,right,time() - loop_start_time  ])
  
            # pause_time =  time_steps  - (time() -loop_start_time )
            # pause_time = loop_start_time + time_steps - time() - f_time
            pause_time =  + record_start_time  + (counter * time_steps) - time()
            if pause_time>0:
                print(pause_time)
                sleep(pause_time)
            # print(f'{time_steps =  }, {now - loop_start_time =}, {pause_time = }, {f_time= },') 
            
            #s_time = time()
            #f_time = time() -s_time - pause_time
        record_end_time = time()
    #Summary
    duration = record_end_time - record_start_time      
    print(f'{duration=}')
    print('fps = ', counter/duration) 
    #print(f'{len(data)} events collected')
    
    # return data

def plot_and_save(data, file_name, save_3D_plot=True, save_animation= True):
    ''' this function plots the data and saves it to 
                - a png file for 3D plot image. 
                - a mp4 file for animation. 3D rotating animation.
        data                    : list of lists. each list contains the mouse event data.
        file_name               : name of the file to save the animation and image.
        save_3D_plot            : True if we want to save the 3D plot.
        save_animation          : True if we want to save the animation.
    
    '''
    print('Plotting data...')
    #Convert to numpy arrays. Convert to float if strings from csv.
    data = np.array(data)
    
    x = data[:,1]
    y = data[:,2]
    z = data[:,0]
    #left, right click points
    l_data =  data[data[:,3] == 1]
    r_data = data[data[:,4] == 1]
    xl,yl,zl = l_data[:,1] , l_data[:,2], l_data[:,0]
    xr,yr,zr = r_data[:,1] , r_data[:,2], r_data[:,0]

    #Visualize
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot(x, y, z)
    ax.scatter3D(xl,yl,zl, color = 'red')
    ax.scatter3D(xr,yr,zr, color = 'blue')

    ax.set_xlabel('x-position')
    ax.set_ylabel('y-position')
    ax.set_zlabel('time (seconds)')
    ax.legend(['Movement over time' ,'left_click', 'right_click'],loc ="upper left")
    if save_3D_plot:
        plt.savefig(f'results/{file_name}.png')
        print('plot image saved')
    #plt.show()


    # # 3D visualizerotate the axes and update
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)

    ''' Saving 3d animation  '''
    if save_animation:
        print('inside save_animation')
        from matplotlib import animation
        def init():
            return fig,
        def animate(i):
            ax.view_init(elev=10., azim=i)
            return fig,
        # Animate
        print('animating...')
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=360, interval=20, blit=True)
        # Save
        print('Saving 3d animation...')
        #anim.save(f'results/animation{datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")}.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
        anim.save(f'results/{file_name}.gif', fps=30)
        print('Animation Saved!')

def save_data_to_csv(data, file_name):
    ''' this function saves the data to a csv file.
    data                    : list of lists. each list contains the mouse event data.
                              - Each sub-list contains the following data: timestamp, x, y, left_click, right_click
                              - Right_click is 1 if right click is pressed, 0 otherwise. same for left_click.
                              - x and y are the mouse position on the screen.
                              - timestamp is the time in seconds since the start of the recording.
    file_name               : name of the file to save the data.
    '''
    print('Saving data to csv file...')
    with open(f'results/{file_name}.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f'Data saved to csv file at results/{file_name}.csv')



def read_data_from_csv(file_name):
    ''' this function reads the data from a csv file.
    file_name               : name of the file to read the data.
    '''
    print("reading data from csv file")
    data = []
    with open(f'results/{file_name}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) #read as numbers, not strings
        for row in reader:
            data.append(row)
    return data


