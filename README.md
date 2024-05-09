```bash
docker build --network=host -t python-django:v0 .


```bash
docker run -t -i -v /path/to/your/local/fac_rec_django/faces:/code/images --network=host python-django:v0