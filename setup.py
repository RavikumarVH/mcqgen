#to install local pakcages in virutal environment

from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author="Ravikumar",
    author_email="rvhattikal92@gmail.com",
    install_requires=["openai","langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages(),

)