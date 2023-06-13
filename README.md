# About
The model that has been built were then served to our mobile application through a REST API. We served the model by first building a python server using Flask. And then it was dockerized and deployed to GCP CLoud Run. The model is now ready to be used by our mobile application
# How to build
```bash
# on windows
git clone https://github.com/Confidentz-C23-PS334/confidentz-flask.git
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
flask run --host=0.0.0.0
```
