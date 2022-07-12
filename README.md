## Read before running the code


#### You need to create an account and fill out the application form on - https://ais.usvisa-info.com/. To do this you would need DS-160 Number.


#### Assumes chrome web driver , if you use firefox, change the `driver` to `FirefoxDriver`

#### I only check for dates until February, if you need to check beyond, find and change the logic `if month == 'February' `. Send a PR if you generalize it. (Thanks in advance! ;) )

#### Create ssl cert if you want email sending capability -  https://support.google.com/a/answer/6180220?hl=en


## Running the script

#### IMPORTANT: Before running the script, search for `os.getenv` in the script and add all those env vars to your bash or zsh.

```
python3 main.py

```


## Debug Errors

#### ModuleNotFoundError: No module named 'selenium'

This is a good resource: https://bobbyhadz.com/blog/python-no-module-named-selenium

```
pip3.10 install selenium

pip3.10 install webdriver-manager

```


#### main.py:30: DeprecationWarning: executable_path has been deprecated, please pass in a Service object driver = webdriver.Chrome(executable_path=chrome_web_driver_exec_path)

You are most likely missing `chrome_web_driver_exec_path` environment variable in your bash or zsh.

Or you can do the following:

Comment out the line that uses `chrome_web_driver_exec_path` and do the following instead:
  
This is a good resource: https://bobbyhadz.com/blog/python-no-module-named-selenium

```

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


```

