from distutils.core import setup

setup(name='simplepipe',
      version='0.0',
      description="""Simplepipe. Metrics gathering utility using the
                  prometheus push gateway.""",
      author='Christian Boin',
      install_requires=[
            "prometheus-client==0.13.1",
            "requests==2.27.1",
            "beautifulsoup4==4.9.0",
            "requests-html==0.3.4",
            "pydantic==1.9.0",
            "python-dotenv==0.19.2"
      ],
     )