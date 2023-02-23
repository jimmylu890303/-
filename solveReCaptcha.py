import site
import sys
import os
from twocaptcha import TwoCaptcha

def solveRecaptcha(sitekey,url):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from twocaptcha import TwoCaptcha

    api_key = os.getenv('APIKEY_2CAPTCHA', '13c3f87cf9d469356fc54713a6140639')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)

    except Exception as e:
        print(e)

    else:
        return result