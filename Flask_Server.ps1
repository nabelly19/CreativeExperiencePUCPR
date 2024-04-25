cd $PWD
deactivate

$server = "$PWD\server"
python -m venv "$server\.venv"

cd $server

& "$server\.venv\Scripts\Activate.ps1"

pip install flask
pip install tensorflow
pip install numpy
pip install opencv-python
pip install joblib

flask --app App run --debug

cd $PWD

# ".\$server\.venv\Scripts\deactivate"