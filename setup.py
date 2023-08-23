from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = [line.strip() for line in f.readlines() if not line.startswith("-f")]

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="dr-cardio-sonix",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sonix-run=⭐️_Home",
        ],
    },
    author="Kotov Daniil",
    author_email="entertomerci@gmail.com",
    description="Dr. Cardio Sonix is a website "
                "that gives absolutely everyone a neural network "
                "to monitor your heart condition.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cardio-Sonix/cardio-sonix-website",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "License :: GNU GENERAL PUBLIC LICENSE",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ai website cardiovascular streamlit streamlit-component",
    python_requires=">=3.10",
)
