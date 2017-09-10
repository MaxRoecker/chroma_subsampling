from cv

ENV HOME=/root/
WORKDIR "$HOME"

RUN echo "root:root" | chpasswd


CMD ["/bin/bash"]
