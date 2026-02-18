"""
StateManifoldEngine - Setup Script

메타 엔진: 여러 난제가 동시에 겹쳐진 상태 공간
"""

from setuptools import setup, find_packages
import os

# 버전 정보 읽기
version = "0.2.0"
version_file = os.path.join(os.path.dirname(__file__), "src", "state_manifold_engine", "__init__.py")
if os.path.exists(version_file):
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

setup(
    name="state-manifold-engine",
    version=version,
    description="State Manifold Engine - 메타 상태 공간 엔진",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="GNJz",
    author_email="",
    url="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

