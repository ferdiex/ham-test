# 📡 FCC Technician Exam Simulator (Streamlit) v1.0.0

⚠️ **Important note about the exam timer:**  
When you switch sections (e.g., from Exam Mode to Practice or Study), the exam timer continues running in the background. This behavior mirrors the official FCC exam.

## Overview  
This is a Streamlit-based web application designed to help users study, practice, and simulate the FCC Technician exam (2022–2026 question pool). The app supports images in questions, dynamic practice settings, and pass/fail thresholds for the exam simulation.

---

## Features  
- **Study Mode**: Review all questions from the question pool with correct answers visible.
- **Practice Mode**: Flexible number of questions, weak area reports.
- **Exam Mode**: Timed official-like 35-question exam simulation.

---

## Prerequisites  

Ensure you have **Python 3.11.14** installed on your system. You can check your Python version by running:

```bash
python --version
```

If you don't have Python installed, visit: [Python Downloads](https://www.python.org/downloads/)  

---

## Installation and Usage  

To run the FCC Technician Exam Simulator on your machine:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourname/HamTest.git
   cd HamTest
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows, use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run ham_test.py
   ```

5. The interface will open in your browser. Enjoy the simulator!

---

## Project Structure  

```
HamTest/
├── ham_test.py               # Main Streamlit app file
├── Elemento-2-2022-2026.json # Question pool (Spanish, under CC-BY 4.0)
├── images/                   # Images for the questions
├── LICENSE                   # Licensing of the repository
├── README.md                 # Documentation for the project
└── requirements.txt          # Python dependencies for the application
└── .gitignore                # Git ignore rules
```

---

## Contributing  

Contributions are welcome! Please adhere to the following guidelines:

- Ensure all questions added or changed follow the JSON format strictly.
- Add new images to the `images` folder and reference them using relative paths.
- Test your contributions in all modes: Study, Practice, and Exam.

To contribute:  
1. Fork the repository and clone it locally.  
2. Create a new branch (`git checkout -b feature-name`).  
3. Commit and push your changes.  
4. Open a pull request for review.  

---

## Timer Behavior and Known Issues  

The exam timer continues counting if sections are switched, mimicking the official exam. To pause the timer when switching sections, proper state management logic is needed to prevent freezes.

---

## License  

The FCC Technician question pool (Spanish translation) and JSON file are distributed under the Creative Commons **CC-BY 4.0 License**:  
[View License](https://creativecommons.org/licenses/by/4.0/).

Original English content is in the public domain as provided by the FCC.

---

## Ham Test App
Try out the app here: [https://ham-test.streamlit.app/](https://ham-test.streamlit.app/)

---

## Version History

### v1.0.0
- Unified behavior between Study and Practice Modes.
- Improved filtering and dynamic selection across all modes.
- Enhanced clarity in the user interface.
