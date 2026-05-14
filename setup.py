from setuptools import find_packages,setup
setup(

    name="mcqgenerator",
    version="0.0.1",
    author="yasir",
    author_email="syedyashyasir420@gmail.com",
    install_requires=["langchain",
                      "langchain-community",
                      "langchain-core",
                      "langchain-groq",
                      "langchain-xai",
                      "xai-sdk",
                      "streamlit",
                      "python-dotenv",
                      "PyPDF2"],
    packages=find_packages()
)