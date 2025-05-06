from flask import Flask, render_template, send_file
import subprocess

from serpapi import GoogleSearch

params = {
  "q": "Coffee",
  "api_key": "a2a1474b2e6ba99d36ae610c49bb60d13f3cc56025adf403882509320f517bcd"
}

search = GoogleSearch(params)
results = search.get_dict()
print(results)