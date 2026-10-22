FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# the tag --no-cache-dir is used to prevent pip from caching the packages it installs, which reduces the size of the Docker image.

COPY . . /app/

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh    
# every script file needs a permission level if it is to be executed, so we need to give it permission to execute
# "+x" means that we have permission to "execute" the file. 

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]