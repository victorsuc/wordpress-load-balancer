# WordPress com Nginx e MySQL em Docker Compose

Este projeto utiliza **Docker Compose** para criar um ambiente com múltiplos contêineres, simulando uma arquitetura com **balanceamento de carga**.

A aplicação é composta por:

- **1 contêiner Nginx**
- **3 contêineres WordPress**
- **1 contêiner MySQL**

## Objetivo do projeto

O objetivo é disponibilizar uma estrutura em que o **Nginx** receba as requisições do usuário e distribua o tráfego entre três instâncias do **WordPress**, enquanto todas elas utilizam o mesmo banco de dados **MySQL** e a mesma pasta de arquivos compartilhada.

Dessa forma, independentemente de qual contêiner WordPress responda, o conteúdo exibido será o mesmo.

---

## O que o `docker-compose.yml` faz

O arquivo `docker-compose.yml` é responsável por definir e orquestrar todos os serviços do projeto.

Este projeto não utiliza um `Dockerfile` próprio. A estrutura foi montada diretamente no Docker Compose, usando imagens prontas:

- `mysql:latest` para o banco de dados
- `wordpress:latest` para as três instâncias WordPress
- `nginx:latest` para o balanceador de carga
- `locustio/locust` para os testes de carga

### Serviços criados

#### MySQL
O serviço `mysql` executa o banco de dados da aplicação.  
Ele é utilizado pelos três contêineres do WordPress e **não fica acessível diretamente pela máquina hospedeira**, apenas pela rede interna do Docker.

#### WordPress
Os serviços `wordpress1`, `wordpress2` e `wordpress3` executam três instâncias da aplicação WordPress.  
Todos se conectam ao mesmo banco MySQL e compartilham a mesma pasta da máquina hospedeira em `/var/www/html`.

Esses contêineres **não possuem portas publicadas**, portanto **não podem ser acessados diretamente** pelo navegador da máquina hospedeira.

A repetição dos três serviços WordPress permite simular três servidores de aplicação diferentes. Como todos usam o mesmo banco e o mesmo volume `./html`, qualquer página criada no WordPress fica disponível igualmente nas três instâncias.

#### Nginx
O serviço `nginx` atua como ponto de entrada da aplicação.  
Ele é o único contêiner com porta exposta para a máquina hospedeira, permitindo o acesso pelo navegador através da porta 80.

Além disso, o Nginx também monta a mesma pasta compartilhada dos contêineres WordPress, mas no caminho `/usr/share/nginx/html`, conforme exigido no projeto.

No `docker-compose.yml`, o Nginx depende dos três serviços WordPress:

```yaml
depends_on:
  - wordpress1
  - wordpress2
  - wordpress3
```

Ele também publica a porta `80` da máquina hospedeira para a porta `80` do contêiner:

```yaml
ports:
  - "80:80"
```

Com isso, o acesso pelo navegador ou pelo Locust entra sempre pelo Nginx, e não diretamente por um contêiner WordPress.

---

## O que o `nginx.conf` faz

O arquivo `nginx.conf` define a configuração do Nginx.

### Funções principais

#### 1. Configuração do upstream
O bloco `upstream wordpress` cria um grupo com os três servidores WordPress:

- `wordpress1`
- `wordpress2`
- `wordpress3`

Esse grupo permite que o Nginx faça o **balanceamento de carga** entre eles.

No arquivo `nginx.conf`, essa estrutura foi definida assim:

```nginx
upstream wordpress {
  server wordpress1;
  server wordpress2;
  server wordpress3;
}
```

Como os serviços estão na mesma rede Docker (`wpnet`), o Nginx consegue acessar os contêineres pelo nome dos serviços: `wordpress1`, `wordpress2` e `wordpress3`.

#### 2. Escuta na porta 80
O Nginx é configurado para escutar na porta 80, recebendo as requisições vindas do navegador.

#### 3. Encaminhamento das requisições
Quando o usuário acessa a aplicação, o Nginx encaminha a requisição para um dos contêineres WordPress definidos no upstream.

O encaminhamento é feito com:

```nginx
proxy_pass http://wordpress;
```

Nesse caso, `wordpress` é o nome do upstream configurado no próprio `nginx.conf`, não o nome de um único contêiner.

#### 4. Cabeçalho de identificação
A configuração adiciona o cabeçalho:

`X-Upstream`

Esse cabeçalho informa qual servidor WordPress respondeu à requisição, sendo útil para testar e comprovar o balanceamento de carga.

---

## Comunicação entre os contêineres

Todos os contêineres estão conectados à mesma rede Docker, o que permite a comunicação interna entre eles.

Fluxo da aplicação:

1. O usuário acessa o Nginx
2. O Nginx recebe a requisição
3. O Nginx encaminha para um dos contêineres WordPress
4. O WordPress consulta ou grava dados no MySQL
5. A resposta retorna ao usuário

---

## Compartilhamento de arquivos

Os três contêineres WordPress compartilham a mesma pasta da máquina hospedeira em:

`/var/www/html`

O contêiner Nginx também utiliza essa mesma pasta, porém mapeada para:

`/usr/share/nginx/html`

Isso garante que os arquivos da aplicação permaneçam sincronizados entre os serviços.

---

## Segurança e isolamento

O projeto foi configurado para que:

- **apenas o Nginx** seja acessível pela máquina hospedeira
- os contêineres **WordPress não sejam acessados diretamente**
- o contêiner **MySQL também não seja acessado diretamente**

Isso atende aos requisitos da atividade e mantém a arquitetura mais organizada.

---

## Como executar

Na pasta do projeto, execute:

```bash
docker compose up -d
```

## Testes de carga com Locust

O arquivo `locust/locustfile.py` possui quatro cenários:

- `pequena`: consulta apenas a página pequena
- `media`: consulta apenas a página média
- `grande`: consulta apenas a página grande
- `misto`: consulta a pequena, depois a média e depois a grande no mesmo teste

As páginas foram definidas com tamanhos diferentes para representar três categorias de carga:

- página pequena: aproximadamente `85 KB`
- página média: aproximadamente `500 KB`
- página grande: aproximadamente `1 MB`

Esses tamanhos foram definidos pelo conteúdo HTML das páginas no WordPress. Isso é importante porque o Locust, por padrão, não se comporta como um navegador completo: ao chamar uma página, ele não baixa automaticamente imagens, CSS, JavaScript e outros recursos externos. Por isso, a diferença entre pequena, média e grande foi baseada no tamanho da resposta da própria página.

Os caminhos das páginas ficam no início do arquivo `locust/locustfile.py`:

```python
PAGINA_PEQUENA = "/2026/05/13/pagina-pequena/"
PAGINA_MEDIA = "/2026/05/13/pagina-media/"
PAGINA_GRANDE = "/2026/05/13/pagina-grande/"
```

Para conferir o tamanho baixado de cada página, pode ser usado:

```bash
curl -s -o /dev/null -w "%{size_download} bytes\n" http://localhost/2026/05/13/pagina-pequena/
curl -s -o /dev/null -w "%{size_download} bytes\n" http://localhost/2026/05/13/pagina-media/
curl -s -o /dev/null -w "%{size_download} bytes\n" http://localhost/2026/05/13/pagina-grande/
```

Com o Docker Compose em execução, acesse o Locust em:

```text
http://localhost:8089
```

Para rodar pela interface web, informe a tag desejada no campo de tags:

```text
pequena
media
grande
misto
```

Também é possível executar direto pelo terminal:

```bash
docker compose run --rm locust -f /mnt/locust/locustfile.py --host=http://nginx --headless --users 20 --spawn-rate 5 --run-time 1m --tags pequena
docker compose run --rm locust -f /mnt/locust/locustfile.py --host=http://nginx --headless --users 20 --spawn-rate 5 --run-time 1m --tags media
docker compose run --rm locust -f /mnt/locust/locustfile.py --host=http://nginx --headless --users 20 --spawn-rate 5 --run-time 1m --tags grande
docker compose run --rm locust -f /mnt/locust/locustfile.py --host=http://nginx --headless --users 20 --spawn-rate 5 --run-time 1m --tags misto
```
