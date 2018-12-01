FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer [Dylan Chivian (DCChivian@lbl.gov)]
# -----------------------------------------

# RUN apt-get update
RUN pip install --upgrade pip

# Install MEGAHIT
WORKDIR /kb/module
RUN \
  git clone https://github.com/voutcn/megahit.git && \
  cd megahit && \
  git checkout tags/v1.1.1 && \
  make

# copy local wrapper files, and build
COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
