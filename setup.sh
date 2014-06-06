# Setup a basic project (DEVELOPMENT ONLY)

read -p "Developer? " dev

read -p "Remove previous directories? " yn
if [ $yn = "y" ]; then
    rm -fr csci1200
    rm -fr site
fi

echo "Creating new directory structure"

# Setup csci1200 "data and code" directory
mkdir csci1200
mkdir csci1200/bin
mkdir csci1200/code
mkdir csci1200/code/hwconfig
if [ dev = "y" ]; then
    git clone -b develop-Grader git@github.com:JFrei86/HWserver.git csci1200/code/rcos
else
    git clone -b develop-Grader https://git@github.com/JFrei86/HWserver.git csci1200/code/rcos
fi

# Create default class.json
mkdir csci1200/results
cp csci1200/code/rcos/Sample_Files/sample_data/class.json csci1200/results/class.json

# Setup Site
if [ $dev = "y" ]; then
    echo "Creating site..."
    git clone -b develop-site git@github.com:JFrei86/HWserver.git site
else
    echo "Creating site..."
    git clone -b develop-site https://git@github.com/JFrei86/HWserver.git site
fi

# Create Sample Assignment
read -p "Create a sample assignment? " yn
if [ $yn = "y" ]; then
	echo "Creating sample assignment"
	cp -r csci1200/code/rcos/Sample_Files/sampleConfig/HW1 csci1200/code/hwconfig/HW1
	#cd csci1200/code/hwconfig/HW1 && make assignment
fi

if [ $dev = "y" ]; then
    read -p "Add symlink to /var/www? (for apache)" yn
    if [ $yn = "y" ]; then
        sudo rm "/var/www/hws"
        sudo ln -s "$(pwd)/site/public" "/var/www/hws"
    fi
    echo "You can now access the site at 127.0.0.1/hws"
fi
