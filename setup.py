from setuptools import setup  # type: ignore


setup(
    name="askai",
    version="1.0.0",
    author="Max Fischer",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/maxvfischer/askai",
    py_modules=["entrypoint_askai"],
    install_requires=[
        "click==8.1.3",
        "openai==0.25.0",
        "PyYAML==6.0",
    ],
    entry_points="""
        [console_scripts]
        askai=entrypoint_askai:askai
    """
)
