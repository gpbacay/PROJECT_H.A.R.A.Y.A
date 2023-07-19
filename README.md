# HARAYA (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)

![HARAYA Logo](ai.png)

HARAYA is a high-functioning autonomous responsive anthropomorphic yielding assistant developed by Gianne P. Bacay. It is designed to provide a personalized and intelligent AI virtual assistant experience, leveraging cutting-edge technologies in artificial intelligence and natural language processing.

## Features

- Speech Recognition: HARAYA can understand voice commands, allowing for seamless and intuitive user interactions.

- Face and Pose Recognition: HARAYA is equipped with the ability to recognize faces and poses, enabling applications in image analysis and identification.

- Computer Automation: HARAYA can automate various computer tasks, streamlining workflows and enhancing productivity.

- Question Answering: Powered by Google's Larage language model PaLM2 bison model, HARAYA can answer a wide range of questions and engage in informative conversations.

- Web Scraping: HARAYA has the capability to scrape data from the internet, facilitating automated data extraction and analysis.

- Web Search: HARAYA can perform searches on the internet, providing relevant information and assisting users in finding desired content.

- Information Provision: HARAYA is a valuable source of information, leveraging AI capabilities and online resources to provide insights on various topics.

## Getting Started

To get started with HARAYA, follow the instructions below:

### Prerequisites

- Python: Ensure that you have Python installed on your system. You can download the latest version of Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

1. Clone or download the HARAYA repository to your local machine:

        $ git clone https://github.com/gpbacay/PROJECT_H.A.R.A.Y.A.git

Alternatively, you can download the repository as a ZIP file and extract it to a directory of your choice.

2. Navigate to the project directory:

        $ cd PROJECT_H.A.R.A.Y.A

3. Install the required dependencies using `pip`, the Python package manager. Execute the following command:

        $ pip install -r requirements.txt

This will install all the necessary packages and dependencies required by the HARAYA program.

### Usage

Upon running HARAYA, the program will first use the web data scraping system to gather data such as the current time, date, location, and weather through the internet. After collecting this information, HARAYA will initialize the face recognition system to recognize the person she is interacting with.

To use the face recognition system, please follow these steps:

1. Ensure that your system has a default camera configured.

2. Place the images of people you want HARAYA to recognize in the [faces](./faces) directory. Each image file should correspond to a person's face, and the name of the file (excluding the extension) will be used as the person's name.

3. Run the `haraya.py` script in your preferred Python environment, such as the terminal, command prompt, or IDE:

        $ python haraya.py

   Alternatively, if you are using Windows, you can double-click the [H.A.R.A.Y.A.exe](H.A.R.A.Y.A.exe) executable file located in the project directory.

4. HARAYA will utilize your system's default camera for face detection and pose estimation.

5. When HARAYA detects a known face, it will log the time and the name of the person in a CSV file named [database.csv](database.csv).

6. After recognizing your face, HARAYA will greet you and ask how she can assist you.

Please note that the successful operation of the face recognition system relies on appropriate lighting conditions and clear images of the faces in the [faces](./faces) directory.


## Contributing

Thank you for your interest in contributing to the HARAYA project! Contributions are welcome and encouraged. Please contact Gianne P. Bacay through the following channels to discuss potential contributions:

- Facebook: [Gianne Bacay](https://www.facebook.com/giannebacay)
- TikTok: [gpbacay](https://www.tiktok.com/@gpbacay)
- Email: giannebacay2004@gmail.com

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

If you have any questions, suggestions, or feedback, please feel free to reach out to Gianne P. Bacay, the creator of HARAYA.

- Creator's GitHub profile: [https://github.com/gpbacay](https://github.com/gpbacay)

Thank you for choosing HARAYA as your AI virtual assistant. We hope HARAYA enhances your productivity, provides valuable information, and delivers a personalized experience.

