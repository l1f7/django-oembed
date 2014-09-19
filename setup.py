from setuptools import setup, find_packages
 
setup(
    name='django-oembed',
    version='0.1.6',
    description='A collection of Django tools which make it easy to change'
        'text filled with oembed links into the embedded objects themselves.',
    author='Lift Interactive and Eric Florenzano',
    author_email='aaron@liftinteractive.com',
    url='https://github.com/l1f7/django-oembed',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
