"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = recaptcha_solver.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
from typing import KeysView
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import chromedriver_binary
import string
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
import datetime, calendar
import multiprocessing
import concurrent.futures
import requests
import json
from selenium.webdriver.chrome.options import Options
import time
import os
from random import randint
import urllib
import pydub
from speech_recognition import Recognizer, AudioFile
from selenium.webdriver.common.keys import Keys

from recaptcha_solver import __version__

__author__ = "DmitrievichLevin"
__copyright__ = "DmitrievichLevin"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from recaptcha_solver.skeleton import solveCap`,
# when using this Python module as a library.


def solveCap():
    
    path = os.path.abspath(os.getcwd())
    url = "http://democaptcha.com/demo-form-eng/recaptcha-2.html"
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    driver = webdriver.Chrome(options=chrome_options);
    driver.get(url)

    frames = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(frames)
    time.sleep(randint(2,4))

    driver.find_element_by_class_name("recaptcha-checkbox-border").click()

    time.sleep(randint(2, 4))

    driver.switch_to_default_content()

    frames = driver.find_element_by_tag_name("iframe")

    driver.switch_to.frame(frames)

    try:
        driver.find_element_by_xpath("//span[contains(@class, 'recaptcha-checkbox goog-inline-block')][@checked=\"true\"]")
        print("No need to solve")

    except:

        driver.switch_to_default_content()
        frames = driver.find_element_by_xpath("//*[@title='recaptcha challenge']")
        
        driver.switch_to_frame(frames)

        driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button").click()

        driver.switch_to_default_content()

        frames = driver.find_element_by_xpath("//*[@title='recaptcha challenge']")

        driver.switch_to.frame(frames)

        time.sleep(randint(2, 4))

        driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

        try:
            driver.switch_to_default_content()

            frames = driver.find_element_by_xpath("//*[@title='recaptcha challenge']")

            driver.switch_to_frame(frames)

            src = driver.find_element_by_xpath("//*[@id=\"audio-source\"]").get_attribute("src")
            print(src)
            urllib.request.urlretrieve(src, path+"\\audio.mp3")

            sound = pydub.AudioSegment.from_mp3(
                path+"\\audio.mp3").export(path+"\\audio.wav", format="wav")
            
            recognizer = Recognizer()

            recaptcha_audio = AudioFile(path+"\\audio.wav")

            with recaptcha_audio as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio, language = "en-US")

            print(text)

            driver.switch_to_default_content()

            frames = driver.find_element_by_xpath("//*[@title='recaptcha challenge']")

            driver.switch_to_frame(frames)

            inputfield = driver.find_element_by_id("audio-response")
            inputfield.send_keys(text.lower())

            inputfield.send_keys(Keys.ENTER)

            time.sleep(10)
            print("success")
            driver.quit()

        except:
            print("failed")
            driver.quit()




# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="ReCaptcha Solver")
    parser.add_argument(
        "--version",
        action="version",
        version="recaptcha_solver {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Solving captcha...")
    solveCap()
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m recaptcha_solver.solver
    #
    run()
