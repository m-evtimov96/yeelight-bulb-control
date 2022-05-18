# yeelight-bulb-control
Simple GUI project for controling yeelight led bulbs

## 1. Configuration
* First you need to enable "Lan Control" for the bulb, so it can be controlled in your local network (use the yeelight phone app).
* If you just want to use the program download the "standalone_app" folder and run "YeelightApp.exe" (must add the "YeelightApp.exe" to the firewall exception list).
* If you want to edit and run the code install yeelight library via `pip install yeelight` or using the requirements.txt file.
* One of the functions uses the match-case syntax so you will need python >= 3.10.

## 2. Usage
* Enter the bulb's ip address and click connect.
* Use the provided on/off button and brigthness, color temp, saturation and hue sliders to change the bulb state.
* Change the bulb to one of the presets by clicking on the "scenes" buttons.

![image](https://user-images.githubusercontent.com/59535105/165339515-eba19f51-58c9-40d9-b8d1-10fb47be099e.png)

## 3. Common errors
* `a socket error occurred when sending the command` - make sure that the bulb is on with enabled Lan Control and you are using the correct ip adress.
* `code: -5001 message: invalid params` - Add the YeelightApp.exe file to your firewall exceptions list and restart the program.

## 4. Contacts
You can contact me for any questions or recommendations at: m.evtimov196@gmail.com.
