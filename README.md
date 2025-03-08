## Approach

I created an RAG Agent using chatgpt 4.0 with langchain openIA integration to manage the collect data from the tools functions. To simplify the logic, I separeted the functions into 3 files, using duckduckgo for web search, Cinemagoer for idmb and the YouTube Api. For the gui I use PyQt6

## Setup & Installation

### Run the Setup Script

This will create a virtual environment, activate it, and install all dependencies:

```sh
setup_env.bat
```

Or, if running manually:

```sh
python -m venv .venv
call .\.venv\Scripts\activate  #  Windows
source .venv/bin/activate      #  Mac/Linux
pip install -r requirements.txt
```

### Running the Agent

Run the following commands in the terminal while been located on the root folder, u only need the GUI to run the full code

To start the main process:

```sh
python -m ml.main_runner
```

To start the GUI:

```sh
python -m gui.app
```

## Challenges

While trying to approach the tool selection section of the project I run into a few problems with the logic involved. I dont think the result is bad, but maybe the response acomplished isn't the best optimized one

Another problem I found is the rate limit for DuckDuckGoSearch. Apparently, because the API is free, it has a limited number of daily uses
