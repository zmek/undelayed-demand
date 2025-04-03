# undelayed-demand: A streamlit app for visualising patterns of emergency demand by hour of day. 

Welcome to the undelayed-demand repository, which is designed to support hospital bed management through predictive modelling. I'm Zella King, a health data scientist in the Clinical Operational Research Unit (CORU) at University College London. Since 2020, I have worked with University College London Hospital (UCLH) NHS Trust on practical tools to improve patient flow through the hospital.

## What is this repository for? 

One reason why Emergency Departments (EDs) fail to meet admissions targets is because beds are not available at the time patients need to be admitted. UCLH wanted to understand their "undelayed" demand over the course of a day - that is, when beds would be needed if patients were processed within the 4-hour target time for ED. 

I created an application for an improvement project for UCLH, which was focused on their emergency patient pathway. The app show operations managers when they need to have bed ready for incoming patients.

The app itself is available on Streamlit Community [here](https://undelayed-demand-2jlyfpul5sawfbxd9tgz5n.streamlit.app/). You can upload a file of arrival datetimes of patients later admitted to your ED, and specify your ED targets. The app will generate a series of charts showing your patterns of demand. 

Follow the instructions below to set up a locally hosted version of the same Streamlit app. 



# Undelayed-Demand Setup Instructions

## Setup Options

### Option 1: Using Conda (Recommended)
1. **Install Conda** 
   - Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download)

2. **Clone the repository**
   ```bash
   git clone https://github.com/zmek/undelayed-demand.git
   cd undelayed-demand
   ```

3. **Create and activate the conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate undelayed-demand
   ```

### Option 2: Using Python venv
1. **Clone the repository**
   ```bash
   git clone https://github.com/zmek/undelayed-demand.git
   cd undelayed-demand
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Streamlit App

After completing either setup option above:

```bash
streamlit run app.py
```

The app should automatically open in your default web browser at http://localhost:8501. If it doesn't, you can manually open this URL.

## Running the Jupyter Notebooks

### For Conda Setup (Option 1)

1. **Register your environment as a Jupyter kernel** (only needed first time)
   ```bash
   python -m ipykernel install --user --name=undelayed-demand --display-name="Python (undelayed-demand)"
   ```

2. **Launch Jupyter Notebook or JupyterLab**
   ```bash
   # For Jupyter Notebook
   jupyter notebook
   
   # For JupyterLab
   jupyter lab
   ```

3. **Navigate to the notebooks directory and open the notebook**
   ```
   notebooks/Visualise_un-delayed_demand.ipynb
   ```

4. **Select the kernel**
   - In the Jupyter interface, make sure to select the "Python (undelayed-demand)" kernel from the kernel dropdown menu

### For Python venv Setup (Option 2)

1. **Register your environment as a Jupyter kernel** (only needed first time)
   ```bash
   python -m ipykernel install --user --name=venv --display-name="Python (venv)"
   ```

2. **Launch Jupyter Notebook or JupyterLab**
   ```bash
   # For Jupyter Notebook
   jupyter notebook
   
   # For JupyterLab
   jupyter lab
   ```

3. **Navigate to the notebooks directory and open the notebook**
   ```
   notebooks/Visualise_un-delayed_demand.ipynb
   ```

4. **Select the kernel**
   - In the Jupyter interface, make sure to select the "Python (venv)" kernel from the kernel dropdown menu

## Data Requirements

The notebook expects:
- A data directory structure with a `data-raw` folder
- A file named `ed_sdec_ct_5.csv` in this directory, or update the code accordingly
- The CSV file should contain Emergency Department arrival data with an `arrival_datetime` column

You may need to create this directory structure and place your data file accordingly to run the notebook successfully.

## Troubleshooting

- If you encounter errors with the patientflow package, check out its GitHub repository for specific installation instructions: https://github.com/UCL-CORU/patientflow.git
- Make sure you have Git installed for the package installation from GitHub
- If you face issues with data paths, check the path settings in the notebook where `set_file_paths` is called
