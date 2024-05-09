from setuptools import setup

with open("README.md", "r") as rdme:
    desc = rdme.read()

setup(
    name = 'alfrd',
    version = '0.0.2',
    url='https://github.com/avialxee/alfrd/',
    author='Avinash Kumar',
    author_email='avialxee@gmail.com',
    description='Automated Logical FRamework for script execution Dynamically(ALFRD)',
    py_modules = ["alfrd"],
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
    install_requires=[ "google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib", "gspread", "gspread-formatting",
                        "pandas", "numpy", "psutil",
                        "protobuf==3.19.6"
                      ],
    extras_require = {
        "dev" : ["pytest>=3.7",
        ]
    },
     entry_points={ 
        "console_scripts": [
            "alfrd=alfrd:cli"
        ],
    },

)