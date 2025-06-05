# Base image
FROM zenika/alpine-chrome

# Expose port 8080
EXPOSE 8080

# Disable interactive prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PATH="/root/OpenEFT/nbis/nfseg/bin:/root/OpenEFT/nbis/nfiq/bin:$PATH"

# Update and install required packages, including cmake, X11 development libraries, and openjpeg
RUN apt-get update && apt-get install -y \
    git \
    sudo \
    build-essential \
    cmake \
    chromium-browser \
    chromium-bsu \
    libopenjp2-7-dev \
    libgl1-mesa-glx \
    libx11-dev \
    libxext-dev \
    python3 \
    python3-pip \
    bash

# Clone the OpenEFT repository
RUN git clone https://github.com/lbussy/OpenEFT.git /root/OpenEFT && \
    cd /root/OpenEFT && git pull

# Set working directory to the cloned repo
WORKDIR /root/OpenEFT

# Clone and set up NBIS in the repo directory
RUN mkdir /root/build && \
    echo "Setting Up NBIS" && \
    git clone https://github.com/lbussy/nbis /root/OpenEFT/nbis && \
    cd /root/OpenEFT/nbis && \
    ./setup.sh /root/build && \
    echo "Configuring NBIS" && \
    make config && \
    echo "Making NBIS" && \
    make it && \
    echo "Installing NBIS" && \
    make install LIBNBIS=no

# Add NBIS binaries to PATH
RUN echo 'export PATH="/root/OpenEFT/nbis/nfseg/bin:$PATH"' >> ~/.bashrc && \
    echo 'export PATH="/root/OpenEFT/nbis/nfiq/bin:$PATH"' >> ~/.bashrc

# Install Python dependencies from the requirements.txt in the OpenEFT repo
RUN pip3 install -r requirements.txt

# Run Django migrations
RUN python3 manage.py migrate

# Run the build_linux.sh script
RUN chmod +x build_docker.sh && ./build_docker.sh

# Set the default command to run the application
CMD ["python3", "openeft.py"]
