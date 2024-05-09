docker build --network=host -t python-django:v0 .
docker run -t -i -v <local path e.g./home/abhishek/Downloads/fac_rec_django/faces>:/code/images --network=host python-django:v0