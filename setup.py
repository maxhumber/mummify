from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mummify",
    version="1.3.0",
    description="Version control for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["git", "logging", "version control", "machine learning"],
    url="https://github.com/maxhumber/mummify",
    author="Max Humber",
    author_email="max.humber@gmail.com",
    license="MIT",
    packages=["mummify"],
    entry_points={"console_scripts": ["mummify=mummify.cli:cli"]},
    zip_safe=False,
    python_requires=">=3.7",
    setup_requires=["setuptools>=38.6.0"],
)
