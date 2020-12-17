import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

requires = ['requests']

setuptools.setup(
    name='origamibot',
    version='2.0.20',
    author='Crystal Melting Dot',
    author_email='stresspassing@gmail.com',
    description='Library for creating bots for telegram with Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    url='https://github.com/cmd410/OrigamiBot',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
