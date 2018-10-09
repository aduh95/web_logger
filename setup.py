import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhtmllogger",
    version="0.2",
    author="Antoine du Hamel",
    author_email="duhamelantoine1995@gmail.com",
    description="Logger from python to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aduh95/pyhtmllogger",
    packages=["pyhtmllogger"],
    install_requires=["websockets"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

