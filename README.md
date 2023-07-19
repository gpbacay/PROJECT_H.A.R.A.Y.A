# HARAYA (High-functioning Autonomous Responsive Anthropomorphic Yielding Assistant)

![HARAYA Logo](ai.png)

**HARAYA**, an acronym for **H**igh-functioning **A**utonomous **R**esponsive **A**nthropomorphic **Y**ielding **A**ssistant, is an exceptional leap in AI virtual assistants, meticulously developed by the visionary mind of [*Gianne P. Bacay*](https://www.facebook.com/giannebacay). Seamlessly integrating cutting-edge technologies in artificial intelligence, computer vision, web data scraping, computer automation, and natural language processing, HARAYA offers an unparalleled personalized and remarkably human-like virtual assistant experience. With an unwavering commitment to excellence, HARAYA outperforms traditional virtual assistants, effortlessly excelling in executing complex tasks, making informed decisions, and providing unparalleled user support.

Embodying true autonomy, HARAYA operates independently and intelligently, continuously adapting and evolving through advanced machine learning techniques like unsupervised learning, semi-supervised learning, and reinforcement learning. This unique level of autonomy empowers HARAYA to respond with unmatched efficiency, offering quick and accurate reactions to user interactions and inquiries. Its intuitive responsiveness fosters a natural and engaging communication experience, akin to interacting with a human assistant.

Further enhancing user engagement, HARAYA boasts anthropomorphic characteristics in appearance, behavior, and mannerisms, artfully designed to establish a sense of familiarity and emotional connection with users. The result is an enriched and fulfilling user experience, reflecting the very essence of human-like interactions.

Moreover, HARAYA's yielding nature allows it to dynamically generate personalized and coherent responses, effortlessly tailoring its assistance to meet the diverse needs and preferences of individual users. By encompassing these extraordinary qualities, HARAYA stands tall as a high-functioning, autonomous, responsive, anthropomorphic, and yielding virtual assistant, shattering the boundaries of conventional AI technology. With a relentless drive for innovation, HARAYA redefines the landscape of virtual assistant interactions, marking a new era of user-centric and technologically advanced AI experiences.

## Features

- **Speech Recognition**: HARAYA can understand voice commands, allowing for seamless and intuitive user interactions.

- **Face and Pose Recognition**: HARAYA is equipped with the ability to recognize faces and poses through computer vision, enabling applications in image analysis and identification.

- **Computer Automation**: HARAYA can automate various computer tasks, streamlining workflows and enhancing productivity.

- **Question Answering**: HARAYA utilizes Google's advanced Large language model PaLM2 chat-bison foundation model to provide accurate answers to a diverse array of questions and engage in informative discussions. This large language model (LLM) is renowned for its outstanding proficiency in language understanding, generation, and conversational skills. Specifically fine-tuned for natural multi-turn dialogues, the model proves to be an excellent option for text-based tasks related to code, where interactive back-and-forth conversations are essential.

- **Web Data Scraping**: HARAYA has the capability to scrape data from the internet, facilitating automated data extraction and analysis.

- **Web Search**: HARAYA can perform searches on the internet, providing relevant information and assisting users in finding desired content.

- **Information Provision**: HARAYA is a valuable source of information, leveraging AI capabilities and online resources to provide insights on various topics.

## Getting Started

To get started with HARAYA, follow the instructions below:

### Prerequisites

- Python: Ensure that you have Python installed on your system. You can download the latest version of Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

1. Clone or download the HARAYA repository to your local machine:

        https://github.com/gpbacay/PROJECT_H.A.R.A.Y.A.git

   Alternatively, you can download the repository as a ZIP file and extract it to a directory of your choice.

2. Navigate to the project directory:

        C:\Users\Gianne Bacay\Desktop\PROJECT_H.A.R.A.Y.A\haraya.py

3. Install the required dependencies using `pip`, the Python package manager. Execute the following command:

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

Thank you for choosing HARAYA as your AI virtual assistant. We hope HARAYA enhances your productivity, provides valuable information, and delivers a personalized experience.

