from setuptools import setup, find_packages

setup(
    name="STATQAGenerator",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["openai", 
                       "langchain_core", 
                       "langchain_groq",
                       "streamlit", 
                       "python-dotenv", 
                       "PyPDF2"
    ],

    # Metadata
    author="Ze Wang",
    author_email="zewang@gmail.com",
    description="Generate and evaluate a quiz on a topic in statistics.",
    license="MIT",
)
