FROM kbase/sdkbase2:python
MAINTAINER KBase Team
# -----------------------------------------

# RUN apt-get update
RUN pip install --upgrade pip

# Install MEGAHIT
WORKDIR /kb/module
ARG filename=MEGAHIT-1.2.8-Linux-x86_64-static
RUN cd /opt && \
  curl -L -O https://github.com/voutcn/megahit/releases/download/v1.2.8/${filename}.tar.gz && \
  tar -xvf ${filename}.tar.gz && \
  rm ${filename}.tar.gz && \
  ln -s /opt/${filename}/bin/megahit /usr/bin/megahit && \
  chmod +x /usr/bin/megahit

# copy local wrapper files, and build
COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
