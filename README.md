## QuintUber

* Provides simple service to book ride and reach destination
* Built using Python Django web framework

---

### Project Structure

![Project Structure](https://github.com/R3DDY97/quintUber/blob/main/pics/file_tree.png)

- quintproject directory is the project created using django which contains settings and configurations
- uber directory is the applications developed under the quintproject
- urls.py => api endpoints routes logic
- views.py => routes processing controller and handler functions
- binary_search_tree.py => Has binary search tree class and related methods required for nearest Driver assignment
- *service.py* => Main service file having Ride_Service, Driver_Service, Distance_Service classes that provide functionality to find distance, ride processing, Driver processing methods

- constants.py => Constants used
- driver_dist.json => driver distance file helps in creating memory data, key: distance, value: driverId
- sample_driver_data.csv =>  Driver data - driverId, latitude, longitude, cab_color, vehicle regd number......
- tests.py => Test Case Functions file

---

### Requirements
- Python 3.5+
- Linux / MacOSx / Windows
- Tested in MacOsx

----

### Usage

```
git clone https://github.com/R3DDY97/quintUber
cd quintuber
pip3 install -r requirements.txt

python3 manage.py runserver
```

---

### Front End

- To get list of available users

    Open the link http://127.0.0.1:8000//ride/drivers

- To visualise the driver cabs location on map

    Open the link http://127.0.0.1:8000//ride/cars

![Available Cars/Drivers Map Visualisation](https://github.com/R3DDY97/quintUber/blob/main/pics/map.png)

---

### Testing
For testing driver, ride, distance, driver assignment services

```
python3 manage.py test

```

---
