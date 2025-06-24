from setuptools import setup, find_packages

setup(
    name='webhdfs-client',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'api-tool @ git+https://github.com/andreynetrebin/api-tool.git'
    ],
    description='A WebHDFS client using a custom API tool',
    author='Andrey Netrebin',
    author_email='netrebin.a89@gmail.com',
    url='https://github.com/andreynetrebin/webhdfs-client',
)
