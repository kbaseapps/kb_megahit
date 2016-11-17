FROM kbase/kbase:sdkbase.latest
MAINTAINER Michael Sneddon
# -----------------------------------------

WORKDIR /kb/module

RUN pip install --upgrade ndg-httpsclient

# Install MEGAHIT
RUN \
  git clone https://github.com/voutcn/megahit.git && \
  cd megahit && \
  git checkout tags/v1.0.6 && \
  make

# copy local wrapper files, and build
COPY ./ /kb/module
RUN mkdir -p /kb/module/work

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
