pyflightdata
============

[![Build Status](https://travis-ci.org/supercoderz/pyflightdata.svg?branch=master)](https://travis-ci.org/supercoderz/pyflightdata)

A simple library to get flight data from flightradar24 from within Python code.
This is not an offical API and does not use any undocumented API from flightradar24.
This code simply automates what you would do from a browser and extracts the flight history by aircraft registration or by the flight number.

The idea is to use this in cases where you want to exatract flight information for analysis, in a reasonable manner without bombarding the site with lot of requests and without having to manually do the recording of data by hand.

The API does not provide any mass request mechanism and does not recommend such usage or take responsibility for any such usage by anyone.
