import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def isInAlphabeticalOrder(word):
    for i in range(len(word) - 1):
        if word[i] > word[i + 1]:
            return False
    return True
    

    
def downword(word):
    # convert to lowercase 
    lword = word.lower();
    # iterate through length of string
    for i in range(len(lword) - 1):
        # if current char is less than char to the right, it is not a downword
        if lword[i] < lword[i + 1]:
            return False
    return True

def upworda(word):
    return not downword(word)