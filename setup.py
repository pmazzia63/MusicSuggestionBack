from setuptools import setup, find_packages

setup(
    name="music-suggestion-api",
    version="0.1.0",
    author="mazziap",
    description="Music suggestion API using FastAPI and scikit-learn",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/votre_username/mon_projet",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas",
        "scikit-learn",
        "pydantic"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
