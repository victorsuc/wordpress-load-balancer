# WordPress com Nginx e MySQL em Docker Compose

Este projeto utiliza **Docker Compose** para criar um ambiente com múltiplos contêineres, simulando uma arquitetura com **balanceamento de carga**.

A aplicação é composta por:

- **1 contêiner Nginx**
- **3 contêineres WordPress**
- **1 contêiner MySQL**

Os resultados consolidados dos testes de carga ficam no arquivo [`RESULTADOS.md`](RESULTADOS.md), incluindo tabelas, comparativos entre cenários e observações parciais.

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

Para os testes comparando 1, 2 e 3 containers WordPress, foram criados três arquivos de configuração:

- `nginx-1wp.conf`: envia todas as requisições apenas para `wordpress1`
- `nginx-2wp.conf`: balanceia entre `wordpress1` e `wordpress2`
- `nginx-3wp.conf`: balanceia entre `wordpress1`, `wordpress2` e `wordpress3`

O arquivo `nginx.conf` continua sendo a configuração ativa montada no container Nginx. Para alternar entre as configurações, use:

```bash
./scripts/use-nginx-upstream.sh 1
./scripts/use-nginx-upstream.sh 2
./scripts/use-nginx-upstream.sh 3
```

O script copia a configuração escolhida para `nginx.conf`, valida a configuração com `nginx -t` e recarrega o Nginx.

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

Na versão usada neste projeto, a UI pode não exibir um campo de tags. Nesse caso, a tag do cenário deve ser informada no comando que inicia o Locust, e a execução continua sendo iniciada e acompanhada pela interface web.

Exemplos de tags usadas nos comandos:

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

## Relatórios dos testes

O Locust já calcula automaticamente métricas como:

- quantidade de requisições
- quantidade de falhas
- taxa de requisições por segundo
- tempo médio de resposta
- tempo mínimo e máximo
- mediana
- percentis, incluindo P95
- tamanho médio da resposta

Esses dados podem ser vistos pela interface web e também exportados em CSV, que pode ser aberto como planilha no Excel, LibreOffice ou Google Sheets.

### Exportando pela interface web

Após executar um teste na interface do Locust, use a área de download/exportação da própria UI para baixar os dados em CSV.

Esse modo é útil para uma execução manual, mas depende de baixar os arquivos depois do teste.

### Salvando CSV automaticamente

Para já salvar os dados da execução em arquivos CSV, inicie o Locust com `--csv`.

Como a UI do Locust continua disponível, o teste ainda pode ser iniciado e acompanhado pelo navegador em:

```text
http://localhost:8089
```

Antes de iniciar um cenário dessa forma, pare o contêiner `locust` que sobe com o `docker compose up -d`:

```bash
docker compose stop locust
```

Depois execute um dos comandos abaixo.

Cenário pequeno:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags pequena --csv /mnt/locust/reports/pequena
```

Cenário médio:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags media --csv /mnt/locust/reports/media
```

Cenário grande:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags grande --csv /mnt/locust/reports/grande
```

Cenário misto:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags misto --csv /mnt/locust/reports/misto
```

Depois que o teste for executado pela UI, os arquivos serão salvos em:

```text
locust/reports/
```

Para cada prefixo, o Locust gera arquivos como:

- `pequena_stats.csv`: estatísticas principais por endpoint, incluindo média, mediana, P95, falhas e tamanho médio
- `pequena_failures.csv`: detalhes das falhas encontradas
- `pequena_exceptions.csv`: exceções registradas durante o teste

Para os outros cenários, o prefixo muda para `media`, `grande` ou `misto`.

O arquivo principal para análise em planilha é o `*_stats.csv`. Os arquivos `*_failures.csv` e `*_exceptions.csv` são gerados pelo próprio Locust como apoio para investigar erros, mas podem ser ignorados quando o objetivo for analisar apenas o resumo total.

Para manter somente o arquivo de estatísticas depois de uma execução, remova os CSVs auxiliares:

```bash
rm -f locust/reports/*_failures.csv locust/reports/*_exceptions.csv locust/reports/*_stats_history.csv
```

Os arquivos CSV gerados ficam fora do versionamento do Git, pois são resultados de execução.

## Matriz de testes

O objetivo dos testes é identificar o ponto de estresse da aplicação para cargas pesadas. Neste projeto, será considerado ponto de estresse quando a taxa de falha chegar em torno de `3%`.

A matriz combina:

- 4 cenários de página: `pequena`, `media`, `grande` e `misto`
- 3 quantidades de usuários simultâneos: `10`, `100` e `1000`
- 3 quantidades de containers WordPress no balanceamento: `1`, `2` e `3`

Total:

```text
4 cenários x 3 cargas x 3 configurações de containers = 36 execuções
```

### Execuções da página pequena

| Cenário | Containers WordPress | Usuários simultâneos | Prefixo do CSV |
| --- | ---: | ---: | --- |
| pequena | 1 | 10 | `pequena_1wp_10users` |
| pequena | 1 | 100 | `pequena_1wp_100users` |
| pequena | 1 | 1000 | `pequena_1wp_1000users` |
| pequena | 2 | 10 | `pequena_2wp_10users` |
| pequena | 2 | 100 | `pequena_2wp_100users` |
| pequena | 2 | 1000 | `pequena_2wp_1000users` |
| pequena | 3 | 10 | `pequena_3wp_10users` |
| pequena | 3 | 100 | `pequena_3wp_100users` |
| pequena | 3 | 1000 | `pequena_3wp_1000users` |

### Execuções da página média

| Cenário | Containers WordPress | Usuários simultâneos | Prefixo do CSV |
| --- | ---: | ---: | --- |
| media | 1 | 10 | `media_1wp_10users` |
| media | 1 | 100 | `media_1wp_100users` |
| media | 1 | 1000 | `media_1wp_1000users` |
| media | 2 | 10 | `media_2wp_10users` |
| media | 2 | 100 | `media_2wp_100users` |
| media | 2 | 1000 | `media_2wp_1000users` |
| media | 3 | 10 | `media_3wp_10users` |
| media | 3 | 100 | `media_3wp_100users` |
| media | 3 | 1000 | `media_3wp_1000users` |

### Execuções da página grande

| Cenário | Containers WordPress | Usuários simultâneos | Prefixo do CSV |
| --- | ---: | ---: | --- |
| grande | 1 | 10 | `grande_1wp_10users` |
| grande | 1 | 100 | `grande_1wp_100users` |
| grande | 1 | 1000 | `grande_1wp_1000users` |
| grande | 2 | 10 | `grande_2wp_10users` |
| grande | 2 | 100 | `grande_2wp_100users` |
| grande | 2 | 1000 | `grande_2wp_1000users` |
| grande | 3 | 10 | `grande_3wp_10users` |
| grande | 3 | 100 | `grande_3wp_100users` |
| grande | 3 | 1000 | `grande_3wp_1000users` |

### Execuções do cenário misto

| Cenário | Containers WordPress | Usuários simultâneos | Prefixo do CSV |
| --- | ---: | ---: | --- |
| misto | 1 | 10 | `misto_1wp_10users` |
| misto | 1 | 100 | `misto_1wp_100users` |
| misto | 1 | 1000 | `misto_1wp_1000users` |
| misto | 2 | 10 | `misto_2wp_10users` |
| misto | 2 | 100 | `misto_2wp_100users` |
| misto | 2 | 1000 | `misto_2wp_1000users` |
| misto | 3 | 10 | `misto_3wp_10users` |
| misto | 3 | 100 | `misto_3wp_100users` |
| misto | 3 | 1000 | `misto_3wp_1000users` |

### Procedimento recomendado

Para cada quantidade de containers, configure o Nginx antes de iniciar o grupo de testes:

```bash
./scripts/use-nginx-upstream.sh 1
```

Depois execute os testes de `10`, `100` e `1000` usuários para cada cenário.

Exemplo para página pequena com 1 container e 10 usuários, salvando o resumo com o prefixo da matriz:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags pequena --csv /mnt/locust/reports/pequena_1wp_10users
```

Na UI do Locust, configure:

```text
Number of users: 10
Ramp up: 10
Host: http://nginx
```

Ao terminar esse teste, repita mudando o prefixo do CSV e os usuários na UI. Por exemplo:

```bash
docker compose run --rm --service-ports locust -f /mnt/locust/locustfile.py --host=http://nginx --tags pequena --csv /mnt/locust/reports/pequena_1wp_100users
```

Na UI:

```text
Number of users: 100
Ramp up: 100
Host: http://nginx
```

Para trocar para 2 containers:

```bash
./scripts/use-nginx-upstream.sh 2
```

Para trocar para 3 containers:

```bash
./scripts/use-nginx-upstream.sh 3
```

### Análise dos resultados

Depois das execuções, use os arquivos `*_stats.csv` como base para a planilha. As principais colunas para análise são:

- `Name`: endpoint testado
- `Request Count`: total de requisições
- `Failure Count`: total de falhas
- `Median Response Time`: mediana do tempo de resposta
- `Average Response Time`: tempo médio de resposta
- `95%`: P95
- `Requests/s`: requisições por segundo
- `Failures/s`: falhas por segundo
- `Average Content Size`: tamanho médio da resposta

Caso a planilha não traga a taxa de falha pronta, calcule:

```text
taxa de falha (%) = (Failure Count / Request Count) * 100
```

O ponto de estresse será a primeira configuração em que a taxa de falha ficar próxima ou acima de `3%`.

Gráficos recomendados:

- taxa de falha (%) por quantidade de usuários, comparando 1, 2 e 3 containers
- P95 por quantidade de usuários, comparando 1, 2 e 3 containers
- tempo médio de resposta por quantidade de usuários, comparando 1, 2 e 3 containers
- requisições por segundo por quantidade de usuários, comparando 1, 2 e 3 containers

As conclusões devem comparar se adicionar containers reduziu falhas, reduziu P95, aumentou throughput ou apenas postergou o ponto de estresse.
