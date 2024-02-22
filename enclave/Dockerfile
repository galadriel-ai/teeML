FROM amazonlinux

# Install python for running the server and net-tools for modifying network config
RUN yum update -y
RUN yum groupinstall "Development Tools" -y
RUN yum install openssl-devel bzip2-devel libffi-devel  libffi-devel bzip2-devel wget net-tools git -y

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
RUN tar -xf Python-3.10.4.tgz
RUN cd Python-3.10.4/ && ./configure --enable-optimizations
RUN cd Python-3.10.4/ && make -j $(nproc)
RUN cd Python-3.10.4/ && make altinstall

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# RUN echo export PATH="$HOME/.cargo/bin:$PATH" >> /root/.bashrc

WORKDIR /app

COPY requirements.txt ./
RUN export PATH="$HOME/.cargo/bin:$PATH" && python3.10 -m pip install -r /app/requirements.txt

# Building from source does not finish in less than an hour
# RUN export PATH="$HOME/.cargo/bin:$PATH" && cargo install --locked --git https://github.com/MystenLabs/sui.git --rev ebcb58ff27de1e887ade69eab13149af3f2fc3b1 sui
RUN wget https://github.com/MystenLabs/sui/releases/download/mainnet-v1.17.3/sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN tar -xf sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN rm sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN cp target/release/sui-ubuntu-x86_64 /usr/bin/sui
RUN rm -rf target
# Initializes the SUI client with default settings
RUN echo -e "y\n\n1" | sui client

COPY server.py ./
COPY NsmUtil.py ./
COPY run.sh ./
COPY libnsm.so ./

# TODO: debug only
COPY sui_debug.py ./

RUN chmod +x run.sh

CMD ["/app/run.sh"]
