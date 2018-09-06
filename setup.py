import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pansys",
    version="0.1.3",
    url="https://github.com/idling-mind/pansys",
    author="Najeem Muhammed",
    author_email="najeem@gmail.com",
    description="Work with Ansys through python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering",
    ),
    install_requires=[
        "pexpect" ,"pandas"
    ]
)