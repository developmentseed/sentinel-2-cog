FROM lambci/lambda:build-python3.6

WORKDIR /tmp

ENV PACKAGE_PREFIX /tmp/python

COPY sentinel2_to_cog sentinel2_to_cog
COPY setup.py setup.py

# Install Python dependencies
RUN CFLAGS="--std=c99" pip3 install . --no-binary numpy -t $PACKAGE_PREFIX -U
