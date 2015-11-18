FROM kbase/sdkbase:latest
MAINTAINER Michael Sneddon
# -----------------------------------------

# Install the SDK (should go away eventually)
RUN \
  . /kb/dev_container/user-env.sh && \
  cd /kb/dev_container/modules && \
  rm -rf jars && \ 
  git clone https://github.com/kbase/jars && \
  rm -rf kb_sdk && \
  git clone https://github.com/kbase/kb_sdk -b develop && \
  cd /kb/dev_container/modules/jars && \
  make deploy && \
  cd /kb/dev_container/modules/kb_sdk && \
  make && make deploy

# Update Transform (should go away eventually)
RUN \
  . /kb/dev_container/user-env.sh && \
  cd /kb/dev_container/modules && \
  rm -rf transform && \ 
  git clone https://github.com/kbase/transform -b develop

# setup the transform, but ignore errors because sample data cannot be found!
RUN \
  . /kb/dev_container/user-env.sh; \
  cd /kb/dev_container/modules/transform/t/demo; \
  python setup.py; \
  exit 0;


WORKDIR /kb/module

# Install megahit
RUN \
  git clone https://github.com/voutcn/megahit.git && \
  cd megahit && \
  make

# copy local wrapper files, and build
COPY ./ /kb/module
RUN mkdir -p /kb/module/work

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
