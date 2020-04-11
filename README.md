# (VUE) Green IoT impacts calculator

 <img src="/readme-images/IotLandscape.png" alt="BootstrapVue"/>

Green IoT is defined as energy-efficient procedures adopted by IoT either to reduce the GHGE of existing applications or to reduce the impact of IoT itself. In the literature there are many strategies that allow to reduce the impact of these devices at each stage of their lifecycle but what is missing is a way to estimate how green an IoT solution is.

The model proposed in my thesis work is one of the first attempts to assess the energy required and waste produced by the devices employed in an IoT solution focused on outdoor application equipped with an energy harvesting solution.

The following project represents the backend of the web service developed as part of my master thesis work.

The aim of the web service is to estimate the energy impact (expressed in MJ) and the waste impact (expressed in Kg) of the user's IoT solution. The web service, in addition, calculates a green proposal. In this way it is possible to understand how far an IoT solution is from a greener ideal one.

This part of the project provides the RESTful API with which it is possible to calculate the impacts of each IoT system component (device, battery, solar panel and maintenance). In particular, maintenance requires information on the other components and returns not only its energy and waste impact, but also the analysis of the green proposal which is computed by resizing the energy harvesting system components (solar panel and battery). 

Maintenance is formulated as a multi-objective-binary linear programming problem. To solve it, Gurobi Optimizer has been used and you can get it for free for a certain period of time.

To clearly understand how the web service works, a simple frontend has been impelemented exploiting VUE.js.

Further information on the frontend is available in the dedicated repository: https://github.com/edoBaldini/vue-g-iot-calc

![](/readme-images/home.png)
![](/readme-images/chart.png)

## Installing	

```
git clone https://github.com/edoBaldini/Rest-G-IoT-Calc-API
cd Rest-G-IoT-Calc-API
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python setup.py develop
```

Change in the following three files:

```from werkzeug import cached_property```

 with

 ```from werkzeug.utils import cached_property```

```
nano env/lib/python3.7/site-packages/flask_restplus/fields.py
nano env/lib/python3.7/site-packages/flask_restplus/model.py
nano env/lib/python3.7/site-packages/flask_restplus/api.py
```

It is assumed that you have installed Gurobi version 9 on you pc, but it is necessary to make it available in the venv:

```
cd /<Gurobi-install-directory>
python setup.py build -b /tmp/gurobi install
```

we can run the server

```
cd ~/<Web-service-directory>/iot_green_calculator
python app.py
```

to stop it

```control + c ```

to deactivate the venv

``` 
deactivate
```



## Build with

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

- <a href="https://flask-restplus.readthedocs.io/en/stable//">Flask-RESTPlus</a>

- <a href="https://flask-cors.readthedocs.io/en/latest/api.html">Flask-CORS</a>

- <a href="https://www.gurobi.com/documentation/9.0/quickstart_mac/py_python_interface.html">Gurobi</a>

  
