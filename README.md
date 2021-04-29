# Twitssa

Twitssa is a Twitter Scrapper Sentiment Analysis app that searches a given word on Twitter and gives an in depth sentiment analysis.

The provided Jupyter Notebook allows users to search for specific public tweets, scrape them off Twitter and clean the extracted tweets to use them sentiment analysis.

<br>

![](examples/exampleTwitssa.gif)

<br>
<br>

* [Getting Started](#getting-started)
* [Methods](#methods)
* [Troubleshooting](#troubleshooting)
* [References](#references)

<br>

## Getting Started
Twitssa requires Python 3 installed as well as the chrome webdriver - the latter can be easily downloaded from the [Chrome website](https://chromedriver.chromium.org/downloads). The app is written in Python using [mini-forge](https://conda-forge.org/) via Homebrew and the main packages used are Selenium for scraping and and Pandas for manipulating data. This app was developed using an Apple laptop with the M1 chip and some Python libraries are simply not available using Conda package manager. Please note, the provided YML file installs libraries using both Conda and Pip.

To use Twitssa follow the next steps:

<br>

* From the terminal, create a new directory and clone the GitHub repository:

```bash
mkdir twitssa && cd twitssa && git clone https://github.com/jjcfrank/twitter-sentiment-analysis.git
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

<br>

<img src="https://i.ibb.co/G229k37/after.png" width="400">

<br>

After executing the app Twitssa should:
<ol>
<li>Display several descriptive statistics based on the used word</li>
<li>Create in the root directory a scatter plot graph with the sentiment polarity and subjectivity from the scrapped tweets</li>
<li>Create in the root directory a bar plot graph with the number of positive, negative and neutral tweets</li>
<li>Create in the root directory a word cloud image with the most used words from the scrapped tweets</li>
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