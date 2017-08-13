# pypi

## Purpose
To demonstrate how to exploit PyPI's lack of security practices by creating an automated process to spread a malicious payload.

## Run
1. Write your payload and put it in `setup.template`.
2. Get a gmail account and set `$email` and `$password` environment variables to your account credentials. Run `python pypi.py`.
 Gmail allows you to send mail to "sub domains" i.e. `<string>+<your_email>@gmail.com`. PyPI considers all of these email addresses as unique.
3. Run `pypi.py`

## How?
Automating the entire PyPI process
1. Create a new account on PyPI
2. Verify your account
3. Create a new Python package
4. Upload to PyPI
