Welcome to our "Guess Who" Game! 

To start our game with streamlit, please make sure you have downloaded the following things: 
Relevant files: 
    - page-orga.py: needed to navigate between pages
    - game-page.py: this is where the main logic behind the game lies 
    - stats-page.py: here you can see how many games you played, how many guesses you needed and how good your guess was based on the number of questions you asked beforehand 
    - character.csv: stores the characters and their characteristics. This is needed for the LLM to know how to answer the questions asked by the user
    - README.txt 
    - pictures folder: stores the .png files of the characters that are displayed on the game page 
Needed libraries: 
    - streamlit 
    - pandas
    - numpy
    - openai

To open the website in the browser, please run the "page-orga.py" file with streamlit run "page-orga.py" 

In order for the LLM to work you need to enter a valid API key.
If you switched pages from the game page to the stats page, you need to reenter the API key, but don't worry your statistics and games are saved either way. 

Sometimes the Website and the LLM take a few seconds to respond and update, so please wait paitently until the process is finished :)

Have fun with our Guessing Game!
