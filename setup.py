from setuptools import setup

setup(
    name='mindx_ipc',
    version='0.0.0',
    description='Communicates messages between 2 processes running on the same pc.',
    packages=['mindx_ipc'],
    install_requires=['pandas',
                      'numpy'],
)
