
## Fluxo implementado

![img.png](docs/img.png)

## Executar a solução
### 1. Subir aplicação, banco e worker
`docker-compose up`

### 2. Rodar migrations
`docker exec -it lucas_case_app alembic upgrade head` 


### Executar testes e análise estática: 

`docker run -it --rm --volume $PWD:/app python:3.9-buster  /bin/bash -c "cd /app; pip3 install -r requirements_dev.txt; python -m pytest; prospector"`

### Endpoints

Collection do postman em `docs/simple-transfer-case.postman_collection.json`

`POST http://localhost:8088/v0/users` - Criação de usuários (Obs: cada novo usuário recebe 20 reais para poder realizar as transferências)
```
{
    "name": "nome teste",
    "email": "testando@email.com",
    "doc_number": "68540259079",
    "password": "123456"
}
```

`POST http://localhost:8088/v0/transfers` - Realização de transferência
```
{
    "from_user": "369f9c7f-af0b-4f4c-aab8-55c39e700efc",
    "to_user": "de60b059-34d3-4050-b906-5a64a7563667",
    "value": 8.00
}
```

`POST http://localhost:8088/v0/authentication` - Autenticação
```
{
    "email": "testando@email.com",
    "password": "123456"
}
```

