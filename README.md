# Web-scraping-tab.com
Create A Webscrapping Project for Football Matches

1. First you need to create a virtual environment 


  a) if you don't have virtual env library first install
  ```
  pip install virtualenv
  ```
  b) now use the code below to create a vitual environment
  ```
  python3 -m venv venv
  ```
2. activate your venv


  a)for mac-user 
  ```
  source venv/bin/activate
  ```
  b)for windows
  ```
  venv/Scripts/activate
  ```
  
3. after Clone this repository in to your local machine
```
git clone https://github.com/SoroushZiaee/Web-scraping-tab.com.git
```

4. now install requirements
```
pip install -r requirments.txt
```


5. now you run the program

League name
- english premier league
- french ligue 1
- german bundesliga
- italian serie a
- spanish primera division

```
python3 main.py --nameleague 'spanish primera division' --verbose True
```

<h3>
  V2
</h3>

- on this version we add the previous record of each game
- create a UI with pygame or pyqt4
- use PhantomJS() instead chrome driver to make application faster (It's not Efficient)
- Create a method to iterate over url and capture all data

<h3>
How Get Historical Data
</h3>

League name
- english premier league -> (2020-2021, 2019-2020, 2018-2019, 2017-2018, 2016-2017)
- french ligue 1 -> (2020-2021, 2019-2020, 2018-2019, 2017-2018, 2016-2017)v
- german bundesliga -> (2020-2021, 2019-2020, 2018-2019, 2017-2018, 2016-2017)
- italian serie a -> (2020-2021, 2019-2020, 2018-2019, 2017-2018, 2016-2017)
- spanish primera division -> (2020-2021, 2019-2020, 2018-2019, 2017-2018, 2016-2017)

```
python main.py --nameleague 'english premier league' --verbose True --history True --season '2020-2021'
```












