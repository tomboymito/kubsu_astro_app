from setuptools import setup, find_packages

setup(
    name="astro_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'numpy',
        'astropy',
        'scipy',
        'pandas',
        'python-multipart',
        'python-dotenv',
        'pytest',
        'pytest-cov',
        'locust'
    ],
)