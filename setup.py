import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="tubee",
    version="0.0.1",
    author="Vitaliy Pisnya",
    author_email="vitaliy.pisnya@gmail.com",
    description="Simple youtube-dl wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weezybusy/tubee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)
