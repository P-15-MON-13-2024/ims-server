env_folder="./venv/"

if [ -d "$env_folder" ]; then
    echo "Dependencies folder exists."
else
    pip3 install virtualenv
    virtualenv venv
fi

source ./venv/bin/activate
pip3 install -r requirements.txt