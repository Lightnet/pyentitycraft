# pyentitycraft

# License: MIT

# Created By: Lightnet

# Status:
 * Prototype.
 * Testing...

# Information:
  To build minecraft clone in Python 3.11.x with Panda3D and other packages.
  
  By using the pipenv to isolated environment. So it act like any local machine computer for fixed version control. To prevent break packages and python version.

# Programs:
 * Python 3.11
 * toolchain for binary build for OS
 * 
 
# Packages:
 * panda3d==1.10.13
 * panda3d-gltf==1.0.0
 * pyinstaller==5.13.0
 * Cython==3.0.0
 * Pipenv (https://pipenv.pypa.io/en/latest)
 
# Set up:

Note that pip3 vs pip is different in install those packages.

```
pip3 install --user pipenv
```
Note this will install virtual environment to deal with python and packages different versions. In case of build error.

Create folder current project dir:
```
.venv
```
By default it will not create current project folder. It goes to user folder virtual env folder with name prefixed.

## pipenv others:
  Note in case not working.
```
set PIPENV_VENV_IN_PROJECT=1
unset PIPENV_VENV_IN_PROJECT
```
# run pipenv:
```
pipenv shell
```
It will run in virtual isolated.

# Install package:
```
pipenv install -r requirements.txt
```
Install packages in from requirements.txt need to run and build application.

```
pipenv install <package_name>
pipenv install <package_name>==<version>
```

# Run Application:
```
python src/main.py
```

# Build Lib:
```
python src/setup.py build_ext --inplace
```
This from Cython package.

# Build Application Binary:
```
pyinstaller --onefile src/main.py
```

# Notes:
 * Launching Panda3D tends to crash window application.
 * Window application error not showing top.
 * It might be incorrect set up to close when run.

# Links and notes:
 * https://stackoverflow.com/questions/52540121/make-pipenv-create-the-virtualenv-in-the-same-folder
 * https://pipenv-fork.readthedocs.io/en/latest/advanced.html

# Credits:
 * https://www.youtube.com/watch?v=xV3gH1JZew4  How to Create Minecraft in Python and Panda3D
    * https://github.com/shaunwa/cbt-panda3d-minecraft
 * https://www.youtube.com/watch?v=Ab8TOSFfNp4  Creating a Voxel Engine (like Minecraft) from Scratch in Python
    * https://github.com/StanislavPetrovV/Minecraft


 