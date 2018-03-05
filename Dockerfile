FROM jenkins/jnlp-slave
USER root
RUN apt-get update -qq &&  \
    apt-get install -qq python-apt python-pycurl git python-pip ruby ruby-dev \
                        build-essential autoconf ruby-bundler sshpass
ARG ansible_version
RUN pip install ansible==$ansible_version
