# Le Chant des Plantes

# What is this?

This is a little software that makes sounds with plants. You need to install thison a raspberry.
Then put one electrode at the top of the plant and one at the root. The software get the voltage measure and the variations, it makes sound with it.

# How to use?

1. Clone this repo.

    ```terminal
    git clone https://github.com/seevoid/Le-Chant-des-plantes.git

1. Activate virtual env.
    - on Windows :
        ```terminal
        ./plants_env/Scripts/activate

3. Install the required libraries.

    - using pip :

        ```terminal
        pip install -r requirements.txt

4. Put the programm on your rpi and put the electrodes in the pins you choosed. Then edit the script with the good pins. You can also edit the notes and so on...

5. Start the script.

    ```terminal
    python app.py

# Video demo


https://user-images.githubusercontent.com/17503183/216373792-a10d7d40-6f0f-46ee-9731-4a3b946c56d2.mp4


# License 

MIT
