import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='origamibot',
    version='0.1.0',
    author='Crystal Melting Dot',
    author_email='stresspassing@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cmd410/OrigamiBot',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
