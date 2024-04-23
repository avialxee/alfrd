from setuptools import setup

with open("README.md", "r") as rdme:
    desc = rdme.read()

setup(
    name = 'alfred',
    version = '0.0.1',
    url='https://gitlab.ia.forth.gr/smile/alfred/',
    author='Avinash Kumar',
    author_email='avialxee@gmail.com',
    description='Automated Logical FRamework for Executing scripts Dynamically (ALFRED)',
    py_modules = ["alfred"],
    package_dir={'':'src'},
    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "License :: OSI Approved :: BSD License",
                 "Intended Audience :: Science/Research",
                 ],
    long_description=desc,
    long_description_content_type = "text/markdown",
    install_requires=[ "google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib", "gspread",
                        "pandas", "numpy", "psutil",
                        "protobuf==3.19.6"
                      ],
    extras_require = {
        "dev" : ["pytest>=3.7",
        ]
    },
     entry_points={ 
        "console_scripts": [
            "alfred=alfred:cli"
        ],
    },

)