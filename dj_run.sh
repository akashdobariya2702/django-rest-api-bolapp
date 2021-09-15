pip3 install --upgrade virtualenv
virtualenv -p python3 bol_env
source bol_env/bin/activate
pip3 install -r requirements.txt
python3 manage.py runserver
