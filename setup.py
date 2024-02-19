from setuptools import find_packages, setup

setup(
    name="simple-salesforce-extends",
    version="0.1.0",
    url="https://github.com/shinsaka/simple-salesforce-extends",
    author="shinsaka",
    author_email="shinx1265@gmail.com",
    maintainer="shinsaka",
    maintainer_email="shinx1265@gmail.com",
    packages=find_packages(),
    python_requires=">=3.11",
    description="simple-salesforce extends library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["simple-salesforce~=1.12"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
