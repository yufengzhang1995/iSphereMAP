import setuptools
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_requirements(path):
    with open(path, "r") as fh:
        content = fh.read()
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


install_requires = get_requirements('requirements.txt')

setuptools.setup(
    name = "iSphereMAP",
    version = "0.0.1",
    author = "Yufeng Zhang",
    author_email = "chloezh@umich.edu",
    description = "Python-based common computational tools for spherical regression under mismatch corruption",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/yufengzhang1995/iSphereMAP",
    packages = setuptools.find_packages(),
    install_requires = install_requires,
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)