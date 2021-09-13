FROM ubuntu:18.04
RUN apt-get update -y

# tzdata asks for input on timezone, which isn't possible in docker build
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y qemu-kvm libvirt-daemon-system libvirt-dev
# 5.4.0-84 wasn't available at the time of writing

# RUN apt-cache search linux-image-5.4
# RUN apt-get install -y -f linux-image-5.4.0-84-generic

RUN uname -r
RUN apt-get install -y linux-image-$(uname -r)
# RUN apt-get install -y iptables
RUN apt-get install -y curl net-tools jq
RUN apt-get autoclean
RUN apt-get autoremove
RUN curl -O https://releases.hashicorp.com/vagrant/$(curl -s https://checkpoint-api.hashicorp.com/v1/check/vagrant  | jq -r -M '.current_version')/vagrant_$(curl -s https://checkpoint-api.hashicorp.com/v1/check/vagrant  | jq -r -M '.current_version')_x86_64.deb
RUN dpkg -i vagrant_$(curl -s https://checkpoint-api.hashicorp.com/v1/check/vagrant  | jq -r -M '.current_version')_x86_64.deb
RUN vagrant plugin install vagrant-libvirt
RUN vagrant box add --provider libvirt peru/windows-server-2019-standard-x64-eval 
RUN vagrant init peru/windows-server-2019-standard-x64-eval 

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]







