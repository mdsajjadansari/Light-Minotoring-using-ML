# Light Monitoring using ML

Here I have written a code using `z-score analysis` along with json, time, math, statistics and boltiot library to find out whether someone turned on or off the lights in the room, and send an SMS when this happens.

`To send SMS alert I have used Twilio (https://www.twilio.com)`

First of All change credentials of `conf.py` according to your `Mailgun` Account.
Here the circuit connection will be something like this:

##### Hardware Required

* 1 x Bolt IoT Module
* 1 x Micro USB Cable
* 1 x LDR (2 legged devicewith a red wave pattern disk on top)
* 1 x 10k Ohm Resistor (brown black orange color code)

The resistance of an LDR varies inversely with light, i.e., the resistance decreases as the intensity of light falling on the LDR increases. Connecting the LDR Circuit to the Bolt

Connect the LDR to Bolt as shown in image below. Note: There is no positive or negative for this and the 10k Ohm resistor. Also, make sure the Bolt module is not powered on while making connections. Always make it a habit to power off the circuit while making connections for your own and the circuit's safety. Double-check all connections before turning it on.

Here are the steps for making the hardware connections:

Step 1: Insert one lead of the LDR into the Bolt Module's 3v3 Pin.
![](https://camo.githubusercontent.com/3c0bd34c9aa78c0e99c1b5feeff7f4a0c78398da/68747470733a2f2f63646e2e66732e746561636861626c6563646e2e636f6d2f41444e75704d6e577952376b435752766d37364c617a2f726573697a653d77696474683a313530302f68747470733a2f2f7777772e66696c657069636b65722e696f2f6170692f66696c652f4f4e53346c506e68526e6d52484e437368444456)

Step 2: Insert other lead of the LDR into the A0 pin
![](https://camo.githubusercontent.com/b482b689aa0b4a9d360cf56aacdf882184171728/68747470733a2f2f63646e2e66732e746561636861626c6563646e2e636f6d2f41444e75704d6e577952376b435752766d37364c617a2f726573697a653d77696474683a313530302f68747470733a2f2f7777772e66696c657069636b65722e696f2f6170692f66696c652f4c79754c41344a4d545379394e53783371414739)

Step 3: Insert one leg of the 10k Ohm resistor into the GND pin
![](https://camo.githubusercontent.com/a30db117169caaa72980afc6ad01b2afe87964f1/68747470733a2f2f63646e2e66732e746561636861626c6563646e2e636f6d2f41444e75704d6e577952376b435752766d37364c617a2f726573697a653d77696474683a313530302f68747470733a2f2f7777772e66696c657069636b65722e696f2f6170692f66696c652f57364e4a44455a4b524e4b3843345236776a4438)

Step 4: Insert the other leg of the resistor also into the A0 pin
![](https://camo.githubusercontent.com/acf916c0ff9c734a40f6c708908c42434c492311/68747470733a2f2f63646e2e66732e746561636861626c6563646e2e636f6d2f41444e75704d6e577952376b435752766d37364c617a2f726573697a653d77696474683a313530302f68747470733a2f2f7777772e66696c657069636b65722e696f2f6170692f66696c652f344a49663957524a57764d785a76486157415a41)

Warning!! Make sure that at no point do the 3.3V (or even 5V) and GND pins or wires coming out of them touch each other. If you short power to Ground without a resistor even accidentally, the current drawn might be high enough to destroy the Bolt module 

![](https://camo.githubusercontent.com/9877f98f7ded2327f89c5d68fc61ab668d635d8c/68747470733a2f2f63646e2e66732e746561636861626c6563646e2e636f6d2f41444e75704d6e577952376b435752766d37364c617a2f726573697a653d77696474683a313530302f68747470733a2f2f7777772e66696c657069636b65722e696f2f6170692f66696c652f4d4833507936704b51704f7541694e476f6b6167)
Thus, we are effectively measuring the voltage across the 10k Ohm Resistor and the final circuit should look like the image below:

Now connect your module with power source and Run

    python3 Light_Prediction.py



# FAQ : 

The algorithm for the code can be broken down into the following steps:

1) Fetch the latest sensor value from the Bolt device.

2) Store the sensor value in a list, that will be used for computing z-score.

3) Compute the z-score and upper and lower threshold bounds for normal and anomalous readings.

4) Check if the sensor reading is within the range for normal readings.

5) If it is not in range, send the SMS.

6) Wait for 10 seconds.

7) Repeat from step 1.

> The code will initially start printing the following.

![](https://cdn.fs.teachablecdn.com/resize=width:1500/Zo31Dq0YR3Wh9ZekEUFP)

After about 100 seconds (10 seconds delay with a frame size of 10), the system will start printing the light intensity values, as per the following image.

#### Note: The values may change depending on the lighting conditions.
![](https://cdn.fs.teachablecdn.com/resize=width:1500/3DOd07uCQz6600VdXMql)

If we try to move a lit light source, like the torch on mobile close to the LDR.If we start from far away and move the torch close to the LDR slowly, the system will not send an alert. Similarly, if we move the light source away slowly no alert will be sent. But if we suddenly move the light source close to or away from the LDR, then the system will send an alert.

Note: If you are not getting these results, try changing the `FRAME_SIZE` and `MUL_FACTOR` values in the `conf.py` file.

So, what is happening here?

Well in the case of the projects in the 'Interfacing sensor over VPS' section, we set the bounds for the temperature sensor. But in this project, we are using the `Z-score algorithm` to dynamically change the bounds at which an alert is sent.

So when we move the light source close to or away from the LDR slowly, the bounds also start changing slowly.

But when we move the light source close to or away from the LDR very fast, the bounds do not change fast enough, and the system detects an anomaly and sends an SMS alert.

### So how does this system help us know if someone turned on or off the lights?

Well throughout the day, the light in the room will change with the rising and setting of the sun. This change will be slow, and the bounds for the system will change to match this change. But when someone turns on or turns off the lights in the room, the intensity of light in the room will change suddenly. Because of this, the system will detect an anomaly and quickly alert you that someone is in your room.
