### QuintUber

* Provides simple service to book ride and reach destination
* Built using Python Django web framework

#### Requirements
- Python 3.5+
- Linux / MacOSx / Windows
- Tested in MacOsx

#### Usage

```
git clone https://github.com/R3DDY97/quintUber
cd quintuber
pip3 install -r requirements.txt

python manage.py migrate

python3 manage.py runserver

or

python3 manage.py runserver "0.0.0.0:8000"


```

#### Front End

- To get list of available users

    Open the link "http://0.0.0.0:8000/ride/drivers/"

- To visualise the driver cabs location on map

    Open the link "http://0.0.0.0:8000/ride/cars/"

![Available Cars/Drivers Map Visualisation](https://github.com/R3DDY97/quintUber/blob/main/pics/map.png)


#### Testing
For testing driver, ride, distance, driver assignment services

```
python3 manage.py test

```


![Project Structure](https://github.com/R3DDY97/quintUber/blob/main/pics/file_tree.png)
