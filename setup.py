from setuptools import setup, find_packages

setup(
    name='PR_CYBR_SECURITY_AGENT',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add dependencies from requirements.txt
    ],
    author='PR-CYBR',
    author_email='support@pr-cybr.com',
    description='PR-CYBR-SECURITY-AGENT',
    url='https://github.com/PR-CYBR/PR-CYBR-SECURITY-AGENT',
)
