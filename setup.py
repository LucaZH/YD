from setuptools import setup, find_packages

setup(
    name="yd",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp>=2023.12.30",
        "click>=8.1.7",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "yd=yd.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A YouTube video downloader CLI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LucaZH/YD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)