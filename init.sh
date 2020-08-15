
GOOGLE_CHROME=`which google-chrome`

if [ -z "$GOOGLE_CHROME" ]; then
    # for ubuntu 18.04
    # Google Chrome をインストール
    wget -P /tmp https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i /tmp/google-chrome-stable_current_amd64.deb

    # 依存モジュールをインストール
    sudo apt update
    sudo apt -f install -y

fi

# Seleniumをインストール
sudo apt install python3-selenium

pip3 install -r requirements.txt

# generate config.json
cp config.template.json config.json
