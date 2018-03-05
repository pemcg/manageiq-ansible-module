FROM manageiq/manageiq:gaprindashvili-1
# Initialize SSH
ENV container docker
RUN yum clean all
RUN yum install -y sudo openssh-server openssh-clients which curl
RUN [ -f "/etc/ssh/ssh_host_rsa_key" ] || ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN [ -f "/etc/ssh/ssh_host_dsa_key" ] || ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''

RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys && \
    for key in /etc/ssh/ssh_host_*_key.pub; do echo "localhost $(cat ${key})" >> /root/.ssh/known_hosts; done && \
    echo "root:smartvm" | chpasswd && \
    chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/*

#RUN sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN systemctl enable sshd
RUN systemctl disable evmserverd evminit evm-watchdog miqvmstat miqtop
RUN rm -rf /var/www/miq/vmdb/certs/*


EXPOSE 22
