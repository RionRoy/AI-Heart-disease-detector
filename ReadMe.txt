CARDIO-AI: HEART DISEASE DETECTION SYSTEM

WHAT IS THIS? This is an Artificial Intelligence application that analyzes heart scans (ECGs). It uses a "Deep Learning Brain" trained on over 21,000 patient records to detect 50+ specific heart conditions--including Heart Attacks, Bundle Branch Blocks, and Arrhythmias--in seconds.

PRE-REQUISITES (WHAT YOU NEED INSTALLED) You only need one piece of software to run this application.

Software: Python (Version 3.10)

Note: Newer versions like 3.13 may not work. Please use 3.10.

Download Link: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

CRITICAL INSTALLATION STEP: When installing Python, you MUST check the box at the bottom of the first screen that says: "Add Python 3.10 to PATH".

If you do not check this box, the app will not start.

HOW TO START THE APP (SEQUENTIAL STEPS)

Step 1: Unzip Extract the "Cardio_AI_Project" zip file to your Desktop.

Step 2: Launch Open the folder and look for the file named "Start.bat" (It might just be named "Start"). Double-click it.

First Run: You will see a black window appear. It is installing the necessary AI tools (TensorFlow, Streamlit). This takes 1-3 minutes. Please be patient.

Future Runs: It will open instantly.

Step 3: Usage Once the installation finishes, your web browser will automatically open the CardioAI Dashboard.

Look for the "AI Engine Online" indicator.

Drag and drop your ECG file (in .npy format) into the upload box.

Click the red "RUN DIAGNOSIS" button.

Read the medical diagnosis and confidence score displayed on the screen.

RE-RUNNING THE TRAINING (IMPORTANT) The AI Model included in this folder (final_heart_model.keras) is already trained and ready to use. You do NOT need to re-run the training notebook to use the app.

However, if you decide to re-run the Google Colab notebook to re-train the model or process new data, you must do the following:

Download the PTB-XL Dataset from the link below.

Upload the dataset folder to your personal Google Drive.

Ensure the folder is named "PTBXL" inside your Drive so the code can find it.

Dataset Name: PTB-XL (PhysioNet)

Direct Download Link: https://physionet.org/content/ptb-xl/1.0.3/

TROUBLESHOOTING

Issue: "Pip is not recognized" error. Solution: You likely did not check the "Add to PATH" box when installing Python. Uninstall Python and reinstall it, ensuring that specific box is checked.

Issue: The black window closes immediately. Solution: You might have the wrong version of Python installed. Ensure you have installed Python 3.10 using the link provided above.

Issue: The browser does not open automatically. Solution: Check the black command window. If it displays "Local URL: http://localhost:8501", open your web browser and type that address into the bar.

(c) 2025 CardioAI Diagnostics