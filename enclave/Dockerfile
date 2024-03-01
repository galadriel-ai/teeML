FROM amazonlinux:2023.3.20240219.0

# Install python for running the server and net-tools for modifying network config
RUN yum update -y
WORKDIR /tmp
RUN yum groupinstall "Development Tools" -y
RUN yum install openssl-devel bzip2-devel libffi-devel wget net-tools git iproute -y
#RUN yum install \
#    openssl-devel-1:3.0.8-1.amzn2023.0.11.x86_64  \
#    bzip2-devel-1.0.8-6.amzn2023.0.2.x86_64  \
#    libffi-devel-3.4.4-1.amzn2023.0.1.x86_64  \
#    wget-1.21.3-1.amzn2023.0.3.x86_64  \
#    net-tools-2.0-0.59.20160912git.amzn2023.0.3.x86_64  \
#    git-2.40.1-1.amzn2023.0.1.x86_64 -y \

RUN wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
RUN tar -xf Python-3.10.4.tgz
RUN cd Python-3.10.4/ && ./configure --enable-optimizations
RUN cd Python-3.10.4/ && make -j $(nproc)
RUN cd Python-3.10.4/ && make altinstall

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN echo export PATH="$HOME/.cargo/bin:$PATH" >> /root/.bashrc

WORKDIR /app

COPY requirements.txt ./
RUN export PATH="$HOME/.cargo/bin:$PATH" && python3.10 -m pip install -r /app/requirements.txt

# Building from source does not finish in less than an hour
#  RUN export PATH="$HOME/.cargo/bin:$PATH" && cargo install --locked --git https://github.com/MystenLabs/sui.git --rev ebcb58ff27de1e887ade69eab13149af3f2fc3b1 sui
RUN wget https://github.com/MystenLabs/sui/releases/download/mainnet-v1.17.3/sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN tar -xf sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN rm sui-mainnet-v1.17.3-ubuntu-x86_64.tgz
RUN cp target/release/sui-ubuntu-x86_64 /usr/bin/sui
RUN rm -rf target

# Remove custom pysui ssl verification
# TODO: is this needed?
RUN sed -i 's/http2=True/http2=False/' /usr/local/lib/python3.10/site-packages/pysui/sui/sui_clients/sync_client.py
RUN sed -i 's/http2=True/http2=False, verify=False/' /usr/local/lib/python3.10/site-packages/pysui/sui/sui_clients/common.py
RUN sed -i 's/verify=ssl.SSLContext(ssl.PROTOCOL_SSLv23)/verify=False/' /usr/local/lib/python3.10/site-packages/pysui/sui/sui_clients/sync_client.py

COPY server.py ./
COPY NsmUtil.py ./
COPY run.sh ./
COPY libnsm.so ./
COPY traffic_forwarder.py ./
COPY settings.py ./
COPY guess_encoding.py ./
COPY oracle.py ./
# TODO: is this non deterministic?
# COPY .env ./
COPY oracles ./oracles

# TODO: debug only
COPY proxy_checks/openai_call.py ./proxy_checks/
COPY proxy_checks/sui_debug.py ./proxy_checks/
COPY check_proxies.py ./

RUN chmod +x run.sh

CMD ["/app/run.sh"]
