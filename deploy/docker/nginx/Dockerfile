FROM nginx:1.21.6

RUN apt update && apt upgrade -y && apt install -y wget \
    && wget https://github.com/progrium/entrykit/releases/download/v0.4.0/entrykit_0.4.0_linux_x86_64.tgz  \
    && tar -xvzf entrykit_0.4.0_linux_x86_64.tgz  \
    && rm entrykit_0.4.0_linux_x86_64.tgz  \
    && mv entrykit /usr/local/bin/  \
    && entrykit --symlink  \
    && rm /etc/nginx/conf.d/* \
    && apt autoremove -y
COPY etc/nginx/nginx.conf.tmpl /etc/nginx/
COPY etc/nginx/conf.d /etc/nginx/conf.d/

ENTRYPOINT [ \
  "render", \
      "/etc/nginx/nginx.conf", \
      "--", \
  "render", \
      "/etc/nginx/conf.d/upstream.conf", \
      "--", \
  "render", \
      "/etc/nginx/conf.d/public.conf", \
      "--" \
]

CMD nginx -g "daemon off;"
