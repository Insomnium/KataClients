from distutils.core import setup

setup(name='kataclient',
      version='1.0',
      description='Cleent for CodeEnjoy',
      author='Konstantin Ilyashenko',
      author_email='kx13@ya.ru',
      packages=['kataclient'],
      install_requires=['websocket-client', 'click'],
      entry_points={
          'console_scripts': [
              'kataclient=kataclient.CodeBattlePython:main']})
