import conf, json, time, math, statistics
from boltiot import Sms, Bolt

//The math and statistics libraries will be required for calculating the Z-score and the threshold boundaries.

//The following lies code helps define a function which calculates the Z-score and the using the Z-score calculates the boundaries required for anomaly detection.

def compute_bounds(history_data,frame_size,factor): //Here is a function, which takes 3 input variables: hisotry_data, frame_size and factor.
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size] // Here code checks whether enough data has been accumulated to calculate the Z-score, and if there is too much data, then the code deletes the older data.
    Mn=statistics.mean(history_data) //this line calculates the mean (Mn) value of the collected data points.
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2) //This code helps to calculate the Variance of the data points.
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1]+Zn
    Low_bound = history_data[frame_size-1]-Zn
    return [High_bound,Low_bound] 
    //Here we calculate the Z score (Zn) for the data and use it to calculate the upper and lower threshold bounds required to check if a new data point is normal or anomalous.

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
history_data=[] 
//Here we initialize the Bolt and SMS variables, which we will use to collect data and send SMS alerts. Here we also initialize an empty list with the name 'history_data' which we will use to store older data, so that we can calculate the Z-score.


//The following while loop contains the code required to run the algorithm of anomaly detection.
while True:
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    if data['success'] != 1:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(10)
        continue

    print ("This is the value "+data['value'])
    sensor_value=0
    try:
        sensor_value = int(data['value'])
    except e:
        print("There was an error while parsing the response: ",e)
        continue

    bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
    if not bound:
        required_data_count=conf.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(int(data['value']))
        time.sleep(10)
        continue

    try:
        if sensor_value > bound[0] :
            print ("The light level increased suddenly. Sending an SMS.")
            response = sms.send_sms("Someone turned on the lights")
            print("This is the response ",response)
        elif sensor_value < bound[1]:
            print ("The light level decreased suddenly. Sending an SMS.")
            response = sms.send_sms("Someone turned off the lights")
            print("This is the response ",response)
        history_data.append(sensor_value);
    except Exception as e:
        print ("Error",e)
    time.sleep(10) 
