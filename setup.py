from setuptools import setup

setup(
    name='ipc_playground',
    version='0.0.0',
    description='Communicates messages between 2 processes running on the same pc.',
    url='https://github.com/kingkw1/ipc_playground',
    author='Kevin King',
    license='MIT',
    packages=['ipc_playground',
              'ipc_playground.core',
              'ipc_playground.transfer_protocols'],
    install_requires=['pandas',
                      'numpy'],
)
