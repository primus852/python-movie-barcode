FROM ubuntu:18.04
MAINTAINER Torte <findnibbler@gmail.com>

# Set openCV Enviroment
ENV OPENCV_VERSION="3.4.1"

# Update Apt
RUN apt-get update

# Build tools
RUN apt-get install -y build-essential cmake unzip pkg-config python3-dev python3-pip wget

# Image Codecs
RUN apt-get install -y libjpeg-dev libpng-dev libtiff-dev

# Image/Video processing tools
RUN apt-get install -y \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    ffmpeg

# GTK Gui
RUN apt-get install -y libgtk-3-dev

# Optimization Tools for openCV
RUN apt-get install -y libatlas-base-dev gfortran

# Upgrade PIP #
RUN pip3 install --upgrade pip

# Install Packages
RUN pip3 install numpy
RUN pip3 install tqdm
RUN pip3 install daemoniker
RUN pip3 install python_dateutil
RUN pip3 install scipy
RUN pip3 install scikit_learn

WORKDIR /

# Build openCV
RUN wget -O opencv-${OPENCV_VERSION}.zip https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip opencv-${OPENCV_VERSION}.zip \
&& wget -O opencv_contrib-${OPENCV_VERSION}.zip https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.zip \
&& unzip opencv_contrib-${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/build \
&& cd /opencv-${OPENCV_VERSION}/build \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_NEW_PYTHON_SUPPORT=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DENABLE_AVX=ON \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-${OPENCV_VERSION}/modules \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DBUILD_EXAMPLES=ON \
  -DCMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python3) \
  -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
&& make -j $(nproc) \
&& make install \
&& rm /opencv-${OPENCV_VERSION}.zip \
&& rm -r /opencv-${OPENCV_VERSION} \
&& rm /opencv_contrib-${OPENCV_VERSION}.zip \
&& rm -r /opencv_contrib-${OPENCV_VERSION}