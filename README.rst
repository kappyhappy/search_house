pip install -r requirements.txt

download phantomjs from web
phantomjs.org/download.html

tar -xf phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin

git clone https://github.com/kappyhappy/house_price

python house_price/search_house.py
