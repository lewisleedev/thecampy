import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thecampy", # Replace with your own username
    version="3.0.1",
    author="lewisleedev",
    author_email="lewislee@lewislee.net",
    description="더 캠프 인터넷편지 비공식 라이브러리",
    url="https://github.com/lewisleedev/thecampy",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],
    python_requires='>=3.6',
)
