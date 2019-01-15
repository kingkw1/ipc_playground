from setuptools import setup

setup(
    name='mindx_ipc',
    version='0.0.0',
    description='Communicates messages between 2 processes running on the same pc.',
    url='https://github.com/kingkw1/mindx_ipc',
    author='Kevin King',
    license='MIT',
    packages=['mindx_ipc',
              'mindx_ipc.core',
              'mindx_ipc.transfer_protocols'],
    install_requires=['pandas',
                      'numpy'],
)
