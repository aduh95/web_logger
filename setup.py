import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web_logger",
    version="0.6.0",
    author="Antoine du Hamel",
    author_email="duhamelantoine1995@gmail.com",
    description="Logger from python to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.7",
    url="https://github.com/aduh95/web_logger",
    packages=["web_logger"],
    install_requires=["websockets"],
    project_urls={
        "Bug Tracker": "https://github.com/aduh95/web_logger/issues",
        "Source Code": "https://github.com/aduh95/web_logger",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
