
# Recruitment Needs Prediction

## Use Case

### Recruitment Needs Forecasting
- **Description**: This project aims to build models to predict future recruitment needs based on organizational growth and historical turnover data.
- **Benefit**: Enables more efficient planning and reduces the workload on the HR team.

---

## Project Setup and Usage

### Prerequisites
Ensure you have Python installed on your system. You can download it [here](https://www.python.org/downloads/).

### Setting Up the Environment

#### 1. Install `venv`
For Linux and Windows, `venv` is included with Python 3.3 and later. If not available, install Python or ensure the `venv` module is included.

#### 2. Create a Virtual Environment
Run the following commands depending on your operating system:

- **Linux**:
  ```bash
  python3 -m venv env
  ```

- **Windows**:
  ```cmd
  python -m venv env
  ```

#### 3. Activate the Virtual Environment

- **Linux**:
  ```bash
  source env/bin/activate
  ```

- **Windows**:
  ```cmd
  .\env\Scripts\activate
  ```

#### 4. Install Dependencies
After activating the virtual environment, install the required libraries:
```bash
pip install -r requirements.txt
```

---

## Running the Project

### 1. Train the Model
Run the script to train the recruitment needs prediction model:
```bash
python train_model.py
```

### 2. Predict Headcounts for Next Year
After training, execute the prediction script to forecast the recruitment needs:
```bash
python predict_model.py
```

---

## Notes
- Make sure your datasets are formatted correctly and placed in the designated folder before running the scripts.
- Prediction results will be saved in the specified output directory.
- The dataset in the project is too short. Feel comfortable using longer variables or data
---

## Support
For any questions or issues, feel free to open an issue in this repository.