# multiplayer browsergame backend
standalone backend for running multiplayer games in local network

## Tldr;


## Installation

Open Project in VS Code Devcontainer
https://code.visualstudio.com/docs/remote/containers

## Usage
```
uvicorn server:app --reload --port 80
```

### With docker
```
docker build -t frittenburger/bomberman --build-arg ARCH=amd64 .
```
For Raspberry Pi using ARCH arm32v6
```
docker build -t frittenburger/bomberman --build-arg ARCH=arm32v6 .
```
Run image
```
docker run -it --rm --name bomberman -p 8066:8066 -d frittenburger/bomberman
``` 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Authors and acknowledgment

- http://getskeleton.com/
- https://www.makeareadme.com/
- https://handlebarsjs.com/
- https://jquery.com/

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

