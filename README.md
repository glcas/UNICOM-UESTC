# UNICOM-UESTC
In UESTC, we can use WiFi suppoerted by information center in teaching area, which needs signing in only once.

However, the WiFi in dorm are offered by China Unicom & China Telecom, and the Unicom's need to sign in each time, keeping the signing in page open.

So I hope this automatic signing in program can relax myself:)
### Attention
Suppose you're living in University of Electronic Science and Technology of China, I'm sure you've solved the problem of surfing Github in your dormitory without cellular.  
However, if you're visiting the page with cellular, please do not download and run the script immediately. Please use your username and password(If you don't have, you can get one), and avoid tolerating a slow network for both you and me.
### About Prompt
If you're using Windows 10, it will pump the login prompt when you connect a login-needed AP. However, you do NOT need the notice any more with this script.  
This is the way to say Goodbye to him:  
* Keydown **Win+R**
* Input **regedit** and **Enter** (If your UAC is on, choose **Yes** in the window.)
* Input **Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet** in the location bar
* Double click **EnableActiveProbing**
* Change value from **1** to **0**  
  
Then enjoy your peaceful time!
