# `Automation` folder

## 1. Description ✍️

This folder contains files necessary for conducting Cybersickness research.

The research primarily uses two programs – scenarios created with 'Unity' and 'AcqKnowledge'. However, it's also necessary to take notes during the experiment, so automation scripts have been created to reduce manual clicking.

Currently, the research setup requires two computers.

> [!WARNING]
> 
> Programs don’t save files from Acqknowledge automatically

## 2. The structure of the folder 🧱
```
📦Automation
 ┣ 📂unity_data
 ┃ ┣ 📜unity_data.csv
 ┃ ┗ 📜unity_data.xlsx
 ┣ 📜Acqknowledge_listener.py
 ┣ 📜Automation.md
 ┣ 📜Cube_vis.png
 ┣ 📜ExperimentData.py
 ┣ 📜MainGUIcybersickness.py
 ┗ 📜unity_notifier.py
 ```

## 3. Description of files in folder 📁

Below is a diagram showing which files and folders are used on each computer.<br>

![obraz](https://github.com/user-attachments/assets/7dcb821d-e592-4a4d-b4dc-239fb8593daf)


### 3.1 Computer 1 🖥️

#### **MainGUICybersickness.py** 

This is the main GUI program that controls the entire experiment.

**Features**:
* Allows you to choose a scenario
* Sends requests to `Acqknowledge_listener.py`
* Send the scenario to Unity
* Add time marks to a csv file - `experiment_log.csv`

**Appearance:**

![obraz](https://github.com/user-attachments/assets/fc4f5906-c3ee-49f4-bac4-453deff3afe5)

**What's included?**
* Information about the current scenario number
* Grid setting
* Type of movement and rotation on the right side
* three buttons with text - `Start Experiment` , `Stop Experiment` and `Hard Stop`
* two buttons with symbols - `-` and `+`

`Start Experiment` - starts the scenario <br>
`Stop Experiment` - interupts the scenario if necessary <br>
`Hard stop` - ends the experiment and closes all programs <br>

#### **ExperimentData.py** 🐍

> A helper script for MainGUICybersickness.py. It helps load scenarios from the unity_data folder.

#### **ExperimentData.py** 🐍

> Another helper for MainGUICybersickness.py. It sends requests to AcqKnowledge and Unity.

#### **unity_notifier.py** 🐍

> It's a helper for `MainGUICybersickness.py` . It helps to send requests to Acqknowledge and Unity.

#### **Cube_vis.png**

> Used by `MainGUICybersickness.py` for visualizing how cubes will spawn. Shown in the GUI image above.

### 3.2 Computer 2 🖥️

This computer runs a listener to help create time markers in AcqKnowledge.

#### `Acqknowledge_listener.py`

> This background script logs incoming requests and scenarios. 
> When it receives a request from the Start Experiment button, it automatically creates a time marker in AcqKnowledge. 
> It is given the experiment duration, and after the experiment ends, it also creates a marker.

## 4. Running experiment 👩‍🔬

The order of starting programs isn't strict, but I recommend the following sequence:

#### 4.1 **Computer 1** 🖥️:

##### 4.1.1 Run `Cybersickness.exe` in **Unity** 🎮

> The file is in the `Unity_simulator` folder

##### 4.1.2 Run `MainGUIcybersickness.py` in **VS Code** 👩🏻‍💻

> [!CAUTION]
> Make sure that you are in the correct folder with `MainGUIcybersickness.py` in terminal.

Run program with 
```bash
python MainGUIcybersickness.py
```

> [!CAUTION]
> Don't click `Start Experiment` yet

#### 4.2 **Computer 2** 🖥️ :

##### 4.2.1 Run `Acqknowledge_listener.py` in **VS Code** 👩🏻‍💻

> [!CAUTION]
> Make sure that you are in the correct folder with `Acqknowledge_listener.py` in terminal.

> [!TIP]
> Use `cd` and the folder name or the full path to navigate.

Run program with 
```bash
python MainGUIcybersickness.py
```

##### 4.2.2 Run `Acqknowledge` 🫀

> Prepare the experiment, calibrate all signals and press Run ▶️

#### 4.3 **Computer 1** 🖥️: [come back]

##### 4.3.1 `Start Experiment` button

## 5. Recommendation

> [!TIP]
> Use `VS Code` for using these python files
>
> Make sure you have installed all necessary libraries and required programs.
