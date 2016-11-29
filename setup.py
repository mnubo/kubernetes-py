import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# See https://github.com/pybuilder/pybuilder/issues/56
del os.link


def version():
    with open(os.path.abspath(__file__).replace('setup.py', 'version.meta'), 'r') as v:
        return v.read()

setup(
    name='kubernetes-py',
    version=version(),
    description='A python module for Kubernetes.',
    author='mnubo inc.',
    author_email='scoutu@mnubo.com, francis@mnubo.com',
    url='https://github.com/mnubo/kubernetes-py',
    download_url='https://github.com/mnubo/kubernetes-py/tarball/' + version(),
    keywords=['kubernetes', 'k8s'],
    packages=[
        'kubernetes',
        'kubernetes.models',
        'kubernetes.models.unversioned',
        'kubernetes.models.v1',
        'kubernetes.models.v1beta1',
        'kubernetes.utils'
    ],
    install_requires=[
        'importlib>=1.0.3',
        'uuid>=1.30',
        'PyYAML>=3.11',
        'requests>=2.10.0',
    ],
    scripts=[],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'nose-cover3'
    ],
    include_package_data=True,
    zip_safe=False
)
