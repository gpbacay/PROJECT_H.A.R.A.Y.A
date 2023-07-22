# HARAYA (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)

![HARAYA Logo](ai.png)

**HARAYA**, an acronym for **H**igh-functioning **A**utonomous **R**esponsive **A**nthropomorphic **Y**ielding **A**ssistant, represents a groundbreaking advancement in the realm of AI virtual assistants, solely developed by [*Gianne P. Bacay*](https://www.facebook.com/giannebacay). It seamlessly integrates cutting-edge technologies in artificial intelligence, including computer vision, web data scraping, automation, natural language processing (NLP), and large language model (LLM) utilization, to deliver a personalized and remarkably human-like user experience. Operating autonomously and continuously adapting through advanced machine learning and deep learning techniques, HARAYA excels in handling complex tasks, making informed decisions, and providing unparalleled user support. Its anthropomorphic characteristics foster engaging communication, while its generative or yielding nature enables tailored assistance for individual users, setting a new standard for virtual assistant interactions and marking a new era of user-centric AI virtual assistant experiences.

## Features

- **Speech Recognition**: HARAYA can understand speeches or voice commands, allowing for seamless and intuitive user interactions.

- **Text to Speech**: HARAYA utilizes a Text to Speech module, allowing her to convert text-based data into spoken words. This allows HARAYA to provide information audibly, enhancing user interactions and making her even more intuitive and user-friendly.

- **Face and Pose Recognition**: HARAYA is equipped with the ability to recognize faces and poses through computer vision, enabling applications in image analysis and identification.

- **Computer Automation**: HARAYA can automate various computer tasks, streamlining workflows and enhancing productivity.

- **Question Answering**: HARAYA uses Google AI's PaLM2 LLM, a renowned language model known for its exceptional proficiency in language understanding, generation, and conversational skills. Specifically fine-tuned for natural multi-turn dialogues, it excels in providing accurate answers to a diverse range of questions and is ideal for text-based tasks involving coding, advanced reasoning, mathematics, and supports over 100 languages.

- **Web Search**: HARAYA can perform searches on the internet, providing relevant information and assisting users in finding desired content.

- **Web Data Scraping**: HARAYA has the capability to scrape data from any website in the internet, facilitating automated data extraction and analysis.

- **Information Provision**: HARAYA is a valuable source of information, leveraging AI capabilities and online resources to provide insights on various topics.

## Getting Started

To get started with HARAYA, follow the instructions below:

### Prerequisites

Before getting started with HARAYA, ensure that you meet the following prerequisites:

- **Internet**: Ensure that you are connected to the internet with a strong connection.

- **Microphone**: Ensure that you have a microphone, preferably with noise cancelation, as HARAYA can only be activated or utilize through speech or voice commands.

- **Camera**: Ensure that you also have a camera or a webcam on your computer for face recognition and computer vision capabilities of HARAYA.

- **Python**: Ensure that you have Python installed on your system. You can download the latest version of Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Python pip**: Ensure that you have the Python package manager or `pip` installed on your system. It is usually included by default when installing Python, but if for any reason it's not available, you can refer to the official Python documentation for installation instructions: [https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Installation

1. Clone or download the HARAYA repository to your local machine:

        https://github.com/gpbacay/PROJECT_H.A.R.A.Y.A.git

   Alternatively, you can download the repository as a ZIP file and extract it to a directory of your choice.

2. Navigate to the project directory, for example:

        C:\Users\Gianne Bacay\Desktop\PROJECT_H.A.R.A.Y.A\haraya.py

3. Open `haraya.py` in integrated terminal and install the required dependencies using `pip`, the Python package manager. Execute the following command in the integrated terminal:

        pip install -r requirements.txt

This will install all the necessary packages and dependencies required by the HARAYA program.

### Usage

1. Run the `haraya.py` script in your preferred Python environment, such as the integrated terminal, command prompt, or IDE:

        python haraya.py

   Alternatively, if you are using Windows, you can run or double-click the [H.A.R.A.Y.A.exe](H.A.R.A.Y.A.exe) executable file located in the project directory in order to run `haraya.py`.

Upon running HARAYA, the program will initially utilize the web data scraping system to gather data, such as the current time, date, location, and weather, from the internet. After collecting real time data, HARAYA will proceed to initializing the face recognition system and subsequently recognize the face of the person with whom it is interacting.

To fully utilize the face recognition system, please follow these steps:

1. Ensure that your system has a default camera or webcam configured.

2. Place the images of people you want HARAYA to recognize in the [faces](./faces) directory. Each image file should correspond to a person's face, and the name of the file (excluding the extension) will be used as the person's name.

HARAYA will utilize your system's default camera for face detection and pose estimation. When HARAYA detects a known face, it will log the time and the name of the person in a CSV file named [database.csv](database.csv). After recognizing your face, HARAYA will greet you and ask how she can assist you.

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

Thank you for choosing HARAYA as your AI virtual assistant. I hope HARAYA enhances your productivity, provides valuable information, and delivers a personalized experience.

