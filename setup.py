import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# See https://github.com/pybuilder/pybuilder/issues/56
del os.link

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

def version():
    with open(os.path.abspath(__file__).replace('setup.py', 'version.meta'), 'r') as v:
        return v.read()

setup(name='kubernetes-py',
      version=version(),
      description='A python module for Kubernetes.',
      long_description=read_md('README.md'),
      author='mnubo inc.',
      author_email='scoutu@mnubo.com',
      url='https://github.com/mnubo/kubernetes-py',
      download_url='https://github.com/mnubo/kubernetes-py/releases',
      packages=[
          'kubernetes',
          'kubernetes.exceptions',
          'kubernetes.models',
          'kubernetes.models.v1',
          'kubernetes.utils'
      ],
      install_requires=[
          'importlib>=1.0.3',
          'uuid>=1.30'
      ],
      scripts=[],
      test_suite='nose.collector',
      tests_require=[
          'nose', 
          'nose-cover3'
      ],
      include_package_data=True,
      zip_safe=False)

