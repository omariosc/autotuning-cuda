# Flamingo CUDA Autotuning System - Multi-stage Docker Build
# This Dockerfile creates optimized containers for different use cases

# ==============================================================================
# Base Python Image with CUDA Support
# ==============================================================================
FROM nvidia/cuda:12.0-devel-ubuntu22.04 as base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    gcc \
    g++ \
    make \
    pkg-config \
    libnuma-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# ==============================================================================
# Development Image with Full Toolchain
# ==============================================================================
FROM base as development

LABEL maintainer="Flamingo Development Team <team@flamingo-autotuner.org>"
LABEL description="Flamingo CUDA Autotuning System - Development Environment"
LABEL version="1.0.0"

# Install additional development tools
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    htop \
    tree \
    tmux \
    gdb \
    valgrind \
    strace \
    && rm -rf /var/lib/apt/lists/*

# Install Python development dependencies
RUN pip install \
    pytest \
    pytest-cov \
    black \
    isort \
    mypy \
    flake8 \
    pre-commit \
    jupyter \
    ipython

# Create working directory
WORKDIR /workspace

# Copy source code
COPY . /workspace/

# Install Flamingo in development mode
RUN pip install -e ".[dev,docs]"

# Set up git (for development containers)
RUN git config --global --add safe.directory /workspace

# Create non-root user for development
RUN useradd -m -s /bin/bash flamingo && \
    chown -R flamingo:flamingo /workspace
USER flamingo

# Default command for development
CMD ["/bin/bash"]

# ==============================================================================
# Production Runtime Image
# ==============================================================================
FROM base as production

LABEL maintainer="Flamingo Development Team <team@flamingo-autotuner.org>"
LABEL description="Flamingo CUDA Autotuning System - Production Runtime"
LABEL version="1.0.0"

# Create application directory
WORKDIR /app

# Create non-root user
RUN useradd -m -s /bin/bash flamingo && \
    chown flamingo:flamingo /app

# Copy only necessary files
COPY pyproject.toml README.md LICENSE.txt /app/
COPY flamingo/ /app/flamingo/
COPY tuner/ /app/tuner/
COPY utilities/ /app/utilities/
COPY examples/ /app/examples/

# Install Python dependencies
RUN pip install /app

# Switch to non-root user
USER flamingo

# Create directories for data and results
RUN mkdir -p /app/data /app/results /app/configs

# Set default environment variables
ENV FLAMINGO_CONFIG_DIR=/app/configs
ENV FLAMINGO_PLUGIN_DIR=/app/plugins
ENV FLAMINGO_DATA_DIR=/app/data
ENV FLAMINGO_RESULTS_DIR=/app/results

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD flamingo --version || exit 1

# Default command
ENTRYPOINT ["flamingo"]
CMD ["--help"]

# ==============================================================================
# Jupyter Notebook Image for Interactive Analysis
# ==============================================================================
FROM production as notebook

LABEL description="Flamingo CUDA Autotuning System - Jupyter Notebook Environment"

# Switch back to root to install additional packages
USER root

# Install Jupyter and scientific packages
RUN pip install \
    jupyterlab \
    notebook \
    matplotlib \
    seaborn \
    plotly \
    pandas \
    numpy \
    scipy \
    scikit-learn

# Install Jupyter extensions
RUN pip install \
    jupyterlab-git \
    jupyterlab-lsp \
    python-lsp-server

# Create Jupyter configuration
RUN mkdir -p /home/flamingo/.jupyter

# Copy Jupyter configuration
COPY docker/jupyter_notebook_config.py /home/flamingo/.jupyter/

# Copy example notebooks
COPY examples/notebooks/ /app/notebooks/

# Set ownership
RUN chown -R flamingo:flamingo /home/flamingo/.jupyter /app/notebooks

# Switch back to flamingo user
USER flamingo

# Expose Jupyter port
EXPOSE 8888

# Set working directory to notebooks
WORKDIR /app/notebooks

# Default command for notebook
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# ==============================================================================
# CI/CD Testing Image
# ==============================================================================
FROM development as testing

LABEL description="Flamingo CUDA Autotuning System - CI/CD Testing Environment"

# Install additional testing tools
RUN pip install \
    pytest-xdist \
    pytest-benchmark \
    pytest-mock \
    coverage \
    codecov \
    tox

# Copy test configuration
COPY pytest.ini tox.ini .coveragerc /workspace/

# Run tests by default
CMD ["pytest", "--cov=flamingo", "--cov=tuner", "--cov=utilities", "-v"]

# ==============================================================================
# Documentation Building Image
# ==============================================================================
FROM base as docs

LABEL description="Flamingo CUDA Autotuning System - Documentation Builder"

# Install documentation dependencies
RUN pip install \
    sphinx \
    sphinx-rtd-theme \
    sphinx-autodoc-typehints \
    myst-parser \
    sphinx-copybutton

WORKDIR /docs

# Copy documentation source
COPY docs/ /docs/
COPY flamingo/ /docs/../flamingo/

# Build documentation
RUN make html

# Serve documentation
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000", "--directory", "_build/html"]