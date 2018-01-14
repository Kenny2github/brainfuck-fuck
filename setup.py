from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name='brainfuck-fuck',
      version='2018.1.14',
      description='Just a nice little brainfuck interpreter in Python.',
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Interpreters',
      ],
      keywords='brainfuck interpreter brainfuck-fuck',
      url='https://github.com/Kenny2github/brainfuck-fuck',
      author='Ken Hilton',
      author_email='kenny2minecraft@gmail.com',
      license='MIT',
      packages=['brainfuck_fuck'],
      entry_points={
          'console_scripts': [
              'bf=brainfuck_fuck.bf:main',
          ],
      },
)
