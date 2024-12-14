1. Enable 2-Step Verification on your Google Account
2. Create a new project or select an existing one
Enable the Gmail API:

3. In the navigation menu, go to "APIs & Services" > "Library"
Search for "Gmail API" and click on it
Click "Enable"


4. [Create credentials:](https://myaccount.google.com/apppasswords)

5. Setup alertmanager config file:
    1. Copy the config file to right path
        ```
        cp alertmanager.config.example.yml config/alertmanager/config.yml
        ```
    2. Fill the file with your email credentials and related data.
    
