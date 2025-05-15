from setuptools import setup, find_packages

setup(
    name="kubsu_astro_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15',
        'numpy>=1.24',
        'matplotlib>=3.7',
    ],
    entry_points={
        'gui_scripts': [
            'astro_app=app.frontend.front_v2:main',
        ],
    },
)