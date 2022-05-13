from animality import __version__
from setuptools import setup

setup(
  name='animality-py',
  packages=['animality'],
  version=__version__,
  license='MIT',
  description='A python API wrapper for https://animality.xyz/',
  long_description=open('README.md', 'r', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author='vierofernando',
  entry_points={
    'console_scripts': [
      'animality = animality.cli'
    ]
  },
  author_email='vierofernando9@gmail.com',
  url='https://github.com/animality-xyz/animality-py',
  download_url=f'https://github.com/animality-xyz/animality-py/archive/{__version__}.tar.gz',
  keywords=['animal', 'api', 'animality', 'animality-api'],
  install_requires=[
    'aiohttp',
    'halo'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  python_requires='>=3.7'
)
