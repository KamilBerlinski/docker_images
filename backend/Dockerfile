FROM archlinux:latest
RUN pacman -Sy --noconfirm python-pip
WORKDIR /app 
COPY requirements.txt .
RUN pip install --break-system-packages -r requirements.txt
WORKDIR /