from setuptools import setup
packages = [
    'pykitsu',
    'pykitsu.core',
    'pykitsu.utils'
]
setup(
    name='pykitsu',
    version='0.2.0',
    description='kitsu.io python api wrapper',
    long_description='an asynchronous and fast api wrapper for kitsu.io',
    author='Ore',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='asynchronous fast kitsu wrapper',
    install_requires=[
        'aiohttp',
        'asyncio',
        'colorama'
    ],
)