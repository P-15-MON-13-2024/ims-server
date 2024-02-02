# IMS-Server
The backend codebase for the **RFID-based Wireless Inventory Management System**. 

This project was developed as a part of the Electronic Design Lab (EE344) course of Electrical Engineering Department, IIT-Bombay by group **MON-13**. 
# Installation instruction
## 1. Setup virtual env
**WINDOWS**
```bat
pip install virtualenv
virtualenv venv
```
To activate the virtualenv
```bat
./venv/Scripts/activate
```
To get dependencies
```bat
pip install -r requirements.txt
```
**LINUX**
```bash
./getdependencies.sh
```

## 2. Running the debug server
On making database related changes. Might have to perform it before the first run.
```bat
python manage.py makemigrations
python manage.py migrate
```

**WINDOWS**
```bat
python manage.py runserver
```
**LINUX**
```bash
./runserver.sh
```
### Note
To make the `.sh` scripts executatable
```bash
chmod +x <filename.sh>
```


### Group Members
1. Abhijat Bharadwaj (@Keymii)
1. Ananya Chinmaya (@ananyachinmaya)
1. Animesh Kumar (@KeeengPin)
1. Shounak Das (@shounakd56)

