# Metasploitable image
FROM tleemcjr/metasploitable2:latest

# Move the entrypoint script and run it when the
#   container starts
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
