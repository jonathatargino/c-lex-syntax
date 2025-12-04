from setuptools import setup, find_packages

setup(
    name="meu_projeto",
    version="0.1.0",
    description="Meu projeto Python",
    author="Seu Nome",
    packages=find_packages(where="."), 
    include_package_data=True,
)