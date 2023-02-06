<h1>Medication Tracker</h1>

A Python 3.11 GUI application that keeps track of medication deliveries and doses using tkinter and csv.

This is a medication tracker for the UKMedicalCannabis community however could be easily modified to track other medication too!

It requires Python3.11 and can run without any external packages.


<h2>Installation</h2>

	To install Python 3.11, follow the instructions below based on your operating system:

	MacOS
		Go to https://www.python.org/downloads/
		Download the latest stable version of Python for macOS
		Follow the instructions to install Python on your computer.

		Alternatively, you can use the package manager `Homebrew` which allows for the install of well known packages with ease.
		To install Homebrew on macOS, follow these steps:
			Open Terminal (you can find it in Applications > Utilities)
			Copy and paste the following command into Terminal: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
			Press enter and follow the instructions to install Homebrew.
		
		When python is installed, to confirm the installation, open the Terminal and run python3 -V. This should output the version of Python installed, which should be Python 3.11.

	Linux
		Open terminal
		Run the following command based on your distribution:
			Debian/Ubuntu: sudo apt-get install python3.11
			Fedora: sudo dnf install python3.11
			Arch Linux: sudo pacman -S python3.11
			
		To confirm the installation, run python3 -V. This should output the version of Python installed, which should be Python 3.11.

	Windows
		Go to the Python website and download the latest version of Python 3.11 for Windows.
		Run the installer and follow the instructions.
		To confirm the installation, open the Command Prompt and run python3 -V. This should output the version of Python installed, which should be Python 3.11.

	Running the Script
		Clone the repository to your local machine using git clone https://github.com/danny137/medicationtracker.git.
		Navigate to the repository using the Command Prompt or Terminal.
		Run the script using python3 main.py.

<h2>Usage</h2>
	To run, execute `python main.py` in Command Prompt or Terminal, respective of operating system, from within the `medicationtracker` directory.
	
	The Medication Tracker application has 4 tabs:
	
	New Delivery: Allows the user to add a new medication delivery and its quantity. The delivery will be added to the medication.csv file.
	
	Dose: Allows the user to take a dose of a medication and records the date and time in the doses.csv file.
	
	View Medications: Shows a list of all the medications and their respective quantities stored in the medication.csv file.
	
	View Doses: Shows a list of all the doses taken and their respective dates and times stored in the doses.csv file.
	
