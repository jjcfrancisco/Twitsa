# Twitsa

<img src="https://i.ibb.co/VB5Pbdr/after.png" width="300">


Twitsa app allows users to easily scrape public Tweets off Twitter and give an in depth sentiment analysis of the extracted data.

The provided Jupyter Notebook allows users to search for specific public tweets, scrape them off Twitter and clean the extracted tweets to use them sentiment analysis. 

* [Getting Started](#getting-started)
* [Methods](#methods)
* [Troubleshooting](#troubleshooting)
* [References](#references)

<br>

## Getting Started
Twitsa requires Python 3 installed as well as the chrome webdriver - the latter can be easily downloaded from the [Chrome website](https://chromedriver.chromium.org/downloads). The app is written in Python using [mini-forge](https://conda-forge.org/) via Homebrew and the main packages used are Selenium for scraping and and Pandas for manipulating data. This app was developed using an Apple laptop with the M1 chip and some Python libraries are simply not available using Conda package manager. Please note, the provided YML file installs libraries using both Conda and Pip.

To use the Twitter Sentiment Analysis notebook follow the next steps:

<br>

* From the terminal, clone the directory:

```bash
git clone https://github.com/jjcfrank/twitter-sentiment-analysis.git
```

* Install the needed libraries by updating the environment. The code below creates a new Conda environment **(recommeded**).

```bash
conda env update -n [name_environment] --file environment.yaml
```

* If you prefer to install the libraries in the base environment.

```bash
conda env update -n base --file environment.yaml
```

<br>

## Methods

<br>

## Expected Output
The notebook should output:
<ol>
<li>A scatter plot graph with the sentiment polarity and subjectivity from the scrapped tweets
<li>A bar plot graph with the number of positive, negative and neutral tweets
<li>A word cloud image with the most used words from the scrapped tweets
<li>Percentages of positive, negative and neutral tweets in the form of a string
</ol>

<br>

## Troubleshooting

Symptoms | Possible Solutions
--------- | ------------------
Cannot install environment.yaml | Make sure you have activated conda
PermissionError: [Errno 13] Permission denied | Make sure the chrome webdriver is inside the app folder

<br>

## References

<br>

## License & copyright

© Frank Jimenez

Licensed under the [MIT Licence](LICENSE).