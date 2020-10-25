from setuptools import setup

setup(
    name="Trajectory_Gomes_Yune",
    version="0.1",
    author="Raphael GOMES CARDOSO & Richard YUNE",
    author_email="raphael.gomes-cardoso@grenoble-inp.org  or richardyune@hotmail.com",
    description="Trajectories of take off and landing flights in Paris",
    long_description=open("README.md").read(),
    license="",
    install_requires=[
        'pathlib',
        'pandas',
	    'numpy',
	    'matplotlib',
        'libproj-dev',
        'proj-data',
        'proj-bin',
        'libgeos-dev',
        'cython',
	    'pyproj',
	    'cartopy'
    ],
    packages=["Trajectory_Gomes_Yune"],  
    python_requires='>=3.8',
)
