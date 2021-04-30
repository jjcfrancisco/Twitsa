# Twitssa

Twitssa is a <b>Twit</b>ter <b>S</b>crapper <b>S</b>entiment <b>A</b>nalysis app that searches a given word on Twitter and gives an in depth sentiment analysis.

Twitssa allows users to search for specific public tweets, scrape them off Twitter and clean the extracted tweets to use them sentiment analysis.

<br>

![](examples/exampleTwitssa.gif)

<br>

* [Getting Started](#getting-started)
* [Methods](#methods)
* [Troubleshooting](#troubleshooting)
* [References](#references)

<br>

## Getting Started
Twitssa requires Python 3 installed as well as the chrome webdriver - the latter can be easily downloaded from the [Chrome website](https://chromedriver.chromium.org/downloads). The app is written in Python using [mini-forge](https://conda-forge.org/) via Homebrew and the main packages used are Selenium for scraping, Pandas for manipulating data and Tkinter for creating the GUI. This app was developed using an Apple laptop with the M1 chip and some Python libraries are simply not available using the Conda package manager. Please note, the provided YAML file installs libraries using both Conda and Pip.

<br>

To use Twitssa follow the next steps in the terminal:

<br>

* Create a new directory and clone the GitHub repository:

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

* Activate the Conda environment

```bash
conda activate [name_environment]
```
* Launch Twitssa
```bash
python3 twitssa.py
```

<br>

## Methods
Twitssa has four main components: the web scrapper, a text transformer to prepare the data, the sentiment analysis and the Graphical User Interphase (GUI).

A web scrapper such as Selenium - the one used in Twitssa - can programmatically parse and extract data from a given website due to its ability to understand HTML syntax. Twitssa, for example, scrapes public tweets when given a word, a language and a location. In this particular case, [Twitter has its own API](https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits#:~:text=Standard%20API%20v1.&text=You%20can%20only%20post%20300,id%20endpoint%20during%20that%20period.) to extract its tweets but there are several limitations such as the amount of data that can be extracted. More importantly, it allows users to obtain vast amounts of data very quickly. As Mitchell describes it:

> <i>"If the only way you access the internet is through a browser, you’re missing out on a
huge range of possibilities."</i>



<br>

## Expected Output

<br>

<img src="https://i.ibb.co/G229k37/after.png" width="400">

<br>
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
["Rate limits: Standard v1.1"](https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits#:~:text=Standard%20API%20v1.&text=You%20can%20only%20post%20300,id%20endpoint%20during%20that%20period.), Twitter, viewed 30 April 2021.


<br>

## License & copyright

© Frank Jimenez

Licensed under the [MIT Licence](LICENSE).