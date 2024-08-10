import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f.readlines()]

setuptools.setup(
    name="image_webshell",
    version="0.0.3",
    author="Marven11",
    author_email="marven11@example.com",
    description="Embed webshell and other text into a png",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marven11/ImageWebshell",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_data={},
    entry_points={
        "console_scripts": [
            "image_webshell=image_webshell.__main__:main",
        ]
    },
)
