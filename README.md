<img src='data/img/carbonara header.png' width='600px'>

Carbonara 🍝 is a Windows tool to compare the energy consumption of Python code using Intel Power Gadget (3.6). Hopefully, this can lead to insights into how we can reduce carbon emissions as a community. This project is not actively maintained and did not have a focus on proper code quality, merely the effectiveness of the tool for realising quick academic research.

<img src='https://img.shields.io/badge/version-v1.0.0-yellow'>
<img src='https://img.shields.io/badge/release%20date-march%202023-red'>
<img src='https://img.shields.io/badge/platform-Intel--based%20Windows-blue'>

As an example, popular and compatible Python packages for common data operations, e.g. Pandas, Vaex, Polars and Dask, have been compared for academic purposes and a simple run of the experiment can be visualized by checking out `results/results-experiment.csv`. In addition, the experiments are still displayed in `/experiments` and set up in `index.py` to serve as an example, although changes are required for your own experiment.

*For any questions or issues, please reach out.*

---------------------------

## Running experiments

* Set up experiments in `/experiments` and run in `index.py`:
    ```
    python index.py
    ```

> Important: For valid results of experiments, please refer to [this scientific guide](https://luiscruz.github.io/2021/10/10/scientific-guide.html) by Luís Cruz, such that the experiment environment of measuring energy consumption is fully understood or adjusted to your intentions.

* Start the Streamlit app for visualisation of results.
    ```
    streamlit run gui.py
    ```

Or, manually:

* Connect the results of the experiment with PowerGadget logs in `parsinator.py`:
    ```
    python src/parsinator.py
    ```

* Read the results (stored in `/results`) by using `readinator.py`:
    ```
    python src/readinator.py
    ```

---------------

## Installation



To use this project, you need to have Python 3.9 installed on your Intel-based Windows machine.

1. Clone the repository to your local machine.
    ```
    git clone https://github.com/philippedeb/carbonara.git
    ```


2. Navigate to the project directory.
    ```
    cd your-repository
    ```

3. Create a virtual environment using `venv` or `conda`.
3.1. Using venv:

    ```
    python3 -m venv venv
    ```

     - Activate the virtual environment:
        ```
        venv\Scripts\activate
        ```

    3.2. Using conda:
    ```
    conda create --name myenv python=3.9
    ```

    - Activate the conda environment:
        ```
        conda activate myenv
        ```

4. Install the required packages.

    ```
    pip install -r requirements.txt
    ```

    Or using conda:

    ```
    conda install --file requirements.txt
    ```

*Note: if you do not plan on checking out existing `/experiments`, only `streamlit`, `scipy`, `plotly`, `psutil` and `wmi` are needed.*
