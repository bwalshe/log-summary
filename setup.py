import setuptools


setuptools.setup(
    name="log-summary", # Replace with your own username
    version="0.0.1",
    author="Brian Walshe",
    author_email="walshe.brian@gmail.com",
    description="Summarised logs",
    long_description="This package will parse logs against a regex and provide a summary table of the counts of each message level. In addition it will create time series graphs of when each type of messaage occured.",
    #long_description_content_type="text/markdown",
    url="https://github.com/bwalshe/logsummary",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "pandas",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "log_info = log_summary.run:run"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)