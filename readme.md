# CS175 Minecraft Project

This GitHub repository is required for CS175 to keep track of the process.
This repo only works for Mac.
## set up
### install Malmo

https://github.com/Microsoft/malmo

Launch client in Malmo minecraft before running python files if you want to test the performance in minecraft. 


### project configuration

[PyCharm](https://www.jetbrains.com/pycharm/) is preferred.

- Open the whole project as a Pycharm project.

- mark Python_Examples in Malmo directory as a source directory: 

   in preference->project structure: press add content root: Python_Example, click on this root, and mark it as a source 

### use VirtualEnv
We can only use the system version Python. It is better for us to create a virtual env  
- install virtual env:
    ```
    $ sudo /usr/bin/python -m pip install virtualenv  
    ```
- in project root directory:
    ```
    $ /usr/bin/python -m virtualenv ./MCpython --clear 

    ```
    press  `y` to create the virtualenv  
    ```
    $ source ./MCpython/bin/activate
    (MCpython) $ python --version

    ```
    it should show 
    ```
    Python 2.7.10
    ```
- We have to install some additional packages for this group project.
  We can install packages from requirments.txt in groupProject directory.
    ```
    (MCpython) $ pip install -r ./requirements.txt
    ```
- in pycharm preferences configure project interpreter
    to be `projectroot/MCpython/bin/python`