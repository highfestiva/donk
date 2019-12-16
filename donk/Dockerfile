FROM alpine
ARG http_proxy
ARG https_proxy
ENV http_proxy ${http_proxy:-http://httppxgot.srv.volvo.com:8080}
ENV https_proxy ${https_proxy:-https://httppxgot.srv.volvo.com:8080}
RUN apk add python3
RUN pip3 install --upgrade pip
RUN pip3 install flask
WORKDIR /usr/local/donk
COPY . /usr/local/donk
CMD [ "./donk.py" ]
