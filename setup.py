from distutils.core import setup

setup(
    name='pysyne',
    version='0.0.1',
    packages=['pysyne'],
    url='https://github.com/phantamanta44/pysyne',
    license='MIT License',
    author='Evan Geng',
    author_email='evandalong@gmail.com',
    description='Python audio visualization',
    entry_points={
        'console_scripts': [
            'pysyne=pysyne:main'
        ]
    }
)
