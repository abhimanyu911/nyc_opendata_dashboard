sudo apt-get update

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda

echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc

source ~/.bashrc

pip install -r requirements.txt

git clone https://github.com/abhimanyu911/nyc_opendata_dashboard.git

wget https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD -O ./data.csv

cd nyc_opendata_dashboard

streamlit run app.py