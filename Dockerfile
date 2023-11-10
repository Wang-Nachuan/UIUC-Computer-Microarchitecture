FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependences
RUN apt-get update
RUN apt-get install -y build-essential bison flex software-properties-common curl
RUN apt-get install -y libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev vim default-jdk default-jre
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
RUN apt-get update
RUN apt-get install -y sbt
RUN apt-get install -y texinfo gengetopt
RUN apt-get install -y libexpat1-dev libusb-dev libncurses5-dev cmake
# deps for poky
RUN apt-get install -y python3.8 patch diffstat texi2html texinfo subversion chrpath wget
# deps for qemu
RUN apt-get install -y libgtk-3-dev gettext
# deps for firemarshal
RUN apt-get install -y python3-pip python3.8-dev rsync libguestfs-tools expat ctags
# install DTC
RUN apt-get install -y device-tree-compiler
RUN apt-get install -y python
# install git >= 2.17
RUN add-apt-repository ppa:git-core/ppa -y
RUN apt-get update
RUN apt-get install git -y
# install verilator
RUN apt-get install -y autoconf
RUN git clone http://git.veripool.org/git/verilator && \
    cd verilator && \
    git checkout v4.034 && \
    autoconf && ./configure && make -j$(nproc) && make install

WORKDIR /workspace

CMD ["/bin/bash"]