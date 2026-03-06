# imgviewer

## Setup
```
python -m venv venv
source venv/bin/activate.bash
pip install -r requirements.txt
```

## Run
Bridge network:
```
ssh -N -L 8080:127.0.0.1:8080 HOSTNAME
```

Run GUI:
```
venv/bin/python main.py
```

In your web browser:
```
http://127.0.0.1:8080
```
