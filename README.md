```
git clone https://github.com/Abhabhish/face_rec_docker.git
```

```
cd face_rec_docker
```

```
docker build --network=host -t python-django:v0 .
```


```
docker run -t -i -v /path/to/your/local/fac_rec_django/faces:/code/images --network=host python-django:v0
```