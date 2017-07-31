# TestingResumizeMe
A Selenium script to test [resumize.me](http://resumize.me/)

## Details
The script runs on Python 2.7.6 and relies on a bunch of libraries that need to be installed:
- selenium
- hashlib
- loremipsum
- random
- radar

## How to
Clone the repository, then
```
$> cd TestingResumizeme
$> python Tester.py
```

A Chrome browser will open and start creating fake CVs.
By default the script will try create 100 CVs. To change this number, modify the variable TESTS in the script.

Final note, Selenium may be blocked by some antivirus when trying to connect to Internet.

## Licensing
MIT License (https://opensource.org/licenses/MIT)
