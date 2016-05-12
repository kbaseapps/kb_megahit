FROM kbase/kbase:sdkbase.latest
MAINTAINER Michael Sneddon
# -----------------------------------------

WORKDIR /kb/module

# Install MEGAHIT
RUN \
  git clone https://github.com/voutcn/megahit.git && \
  cd megahit && \
  git checkout tags/v1.0.3 && \
  make

# copy local wrapper files, and build
COPY ./ /kb/module
RUN mkdir -p /kb/module/work

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
