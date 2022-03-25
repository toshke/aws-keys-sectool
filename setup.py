from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='aws-keys-sectool', version='0.3.0', author='Nikola Tosic',
      author_email='nikola@toshke.me',
      url='https://github.com/toshke/aws-keys-security',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='aws security credentials',
      packages=['aws_keys_sectool'],
      install_requires=['boto3'],
      python_requires='>=3.6',
      description='List active aws profiles and protect their conusmption via IP condition IAM policies',
      entry_points={
          'console_scripts': ['aws-keys-sectool = aws_keys_sectool.__main__:main'],
      })