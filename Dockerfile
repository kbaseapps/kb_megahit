FROM kbase/kbase:sdkbase.latest
MAINTAINER Michael Sneddon
# -----------------------------------------

WORKDIR /kb/module

# Make sure SSL certs are properly installed
RUN apt-get install python-dev libffi-dev libssl-dev \
    && pip install pyopenssl ndg-httpsclient pyasn1 \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade

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
