import version_query

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

my_version = version_query.query_version_str()

setup(
    name="kubernetes-py",
    version=my_version,
    description="A python module for Kubernetes.",
    author="mnubo inc.",
    author_email="it-admin@mnubo.com",
    url="https://github.com/mnubo/kubernetes-py",
    download_url="https://github.com/mnubo/kubernetes-py/tarball/{}".format(my_version),
    keywords=["kubernetes_py", "k8s", "kubernetes"],
    packages=[
        "kubernetes_py",
        "kubernetes_py.models",
        "kubernetes_py.models.unversioned",
        "kubernetes_py.models.v1",
        "kubernetes_py.models.v1alpha1",
        "kubernetes_py.models.v1beta1",
        "kubernetes_py.models.v2alpha1",
        "kubernetes_py.utils",
    ],
    install_requires=["six>=1.10.0", "PyYAML>=3.13", "requests>=2.10.0", "uuid>=1.30", "python-dateutil>=2.6.0"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    scripts=[],
    test_suite="nose.collector",
    tests_require=["nose", "nose-cover3"],
    include_package_data=True,
    zip_safe=False,
)
