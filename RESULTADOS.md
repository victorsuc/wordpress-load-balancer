# Resultados dos Testes de Carga

Este arquivo consolida os resultados obtidos nos testes de carga com Locust. Ele deve ser atualizado conforme novas execuções forem realizadas.

Critério adotado para ponto de estresse:

```text
Taxa de falha próxima ou acima de 3%
```

## Página pequena

Tamanho aproximado da resposta:

```text
85 KB
```

### 1 container WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.300 | 0 | 0,00% | 55 ms | 51 ms | 80 ms | 6,40 | 85.279 bytes |
| 100 | 18.496 | 0 | 0,00% | 102 ms | 83 ms | 200 ms | 61,65 | 85.279 bytes |
| 1000 | 26.683 | 1.694 | 6,35% | 6.647 ms | 1.500 ms | 60.000 ms | 88,91 | 79.876 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a aplicação permaneceu estável, sem falhas registradas e com tempos de resposta baixos.

Com `1000` usuários simultâneos, a aplicação entrou em ponto de estresse. A taxa de falha foi de `6,35%`, acima do limite definido de aproximadamente `3%`. Além disso, o P95 subiu para `60.000 ms`, indicando que 5% das requisições mais lentas ficaram extremamente demoradas.

Conclusão parcial:

```text
Para a página pequena com 1 container WordPress, o ponto de estresse está entre 100 e 1000 usuários simultâneos.
```

## Próximos resultados

As próximas seções devem ser preenchidas conforme os novos testes forem executados.

### Página pequena - 2 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.266 | 0 | 0,00% | 58 ms | 54 ms | 86 ms | 6,44 | 85.279 bytes |
| 100 | 18.221 | 0 | 0,00% | 123 ms | 89 ms | 230 ms | 60,74 | 85.279 bytes |
| 1000 | 25.449 | 4.997 | 19,64% | 7.791 ms | 3.500 ms | 37.000 ms | 84,74 | 69.012 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a aplicação permaneceu estável, sem falhas registradas. Os tempos de resposta ficaram baixos, embora o cenário com `100` usuários tenha apresentado média e P95 um pouco maiores do que no teste com 1 container.

Com `1000` usuários simultâneos, a aplicação entrou em ponto de estresse de forma clara. A taxa de falha foi de `19,64%`, muito acima do limite definido de aproximadamente `3%`. O P95 ficou em `37.000 ms`, indicando forte degradação do tempo de resposta nas requisições mais lentas.

Conclusão parcial:

```text
Para a página pequena com 2 containers WordPress, o ponto de estresse também está entre 100 e 1000 usuários simultâneos.
```

Comparando com 1 container, o teste com 2 containers não melhorou o comportamento em 1000 usuários nesta execução. A taxa de falha aumentou de `6,35%` para `19,64%`, apesar do P95 ter ficado menor (`60.000 ms` com 1 container contra `37.000 ms` com 2 containers).

### Página pequena - 3 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.930 | 0 | 0,00% | 57 ms | 52 ms | 80 ms | 6,43 | 85.279 bytes |
| 100 | 18.271 | 0 | 0,00% | 119 ms | 100 ms | 230 ms | 60,90 | 85.279 bytes |
| 1000 | 19.799 | 3.762 | 19,00% | 9.497 ms | 5.000 ms | 44.000 ms | 65,89 | 69.537 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a aplicação permaneceu estável, sem falhas registradas. Os resultados ficaram próximos dos testes com 1 e 2 containers para essas cargas.

Com `1000` usuários simultâneos, a aplicação entrou novamente em ponto de estresse. A taxa de falha foi de `19,00%`, muito acima do limite definido de aproximadamente `3%`. O P95 ficou em `44.000 ms`, indicando forte degradação do tempo de resposta nas requisições mais lentas.

Conclusão parcial:

```text
Para a página pequena com 3 containers WordPress, o ponto de estresse também está entre 100 e 1000 usuários simultâneos.
```

Comparando os testes de `1000` usuários, o uso de 3 containers não eliminou o gargalo. A taxa de falha ficou próxima da execução com 2 containers (`19,00%` contra `19,64%`) e acima da execução com 1 container (`6,35%`). Isso indica que, nessa carga, o limite provavelmente está em recursos compartilhados, como MySQL, CPU, memória, disco ou rede Docker, e não apenas na quantidade de containers WordPress.

## Comparativo da página pequena

Esta seção compara os resultados obtidos para a página pequena variando a quantidade de containers WordPress e a quantidade de usuários simultâneos.

### 10 usuários simultâneos

| Containers | Requests | Falhas | Falha % | Média | P95 | Req/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.300 | 0 | 0,00% | 55 ms | 80 ms | 6,40 |
| 2 | 1.266 | 0 | 0,00% | 58 ms | 86 ms | 6,44 |
| 3 | 1.930 | 0 | 0,00% | 57 ms | 80 ms | 6,43 |

Com `10` usuários, os três cenários tiveram comportamento estável, sem falhas. Os tempos médios ficaram muito próximos, entre `55 ms` e `58 ms`, e o P95 ficou entre `80 ms` e `86 ms`. Nessa carga, adicionar containers não trouxe diferença relevante de desempenho.

### 100 usuários simultâneos

| Containers | Requests | Falhas | Falha % | Média | P95 | Req/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 18.496 | 0 | 0,00% | 102 ms | 200 ms | 61,65 |
| 2 | 18.221 | 0 | 0,00% | 123 ms | 230 ms | 60,74 |
| 3 | 18.271 | 0 | 0,00% | 119 ms | 230 ms | 60,90 |

Com `100` usuários, também não houve falhas em nenhum dos cenários. O melhor tempo médio foi observado com `1` container (`102 ms`). Com `2` e `3` containers, a média subiu para `123 ms` e `119 ms`, respectivamente, e o P95 ficou em `230 ms`. A quantidade de requisições por segundo permaneceu muito parecida, em torno de `61 req/s`.

### 1000 usuários simultâneos

| Containers | Requests | Falhas | Falha % | Média | P95 | Req/s |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 26.683 | 1.694 | 6,35% | 6.647 ms | 60.000 ms | 88,91 |
| 2 | 25.449 | 4.997 | 19,64% | 7.791 ms | 37.000 ms | 84,74 |
| 3 | 19.799 | 3.762 | 19,00% | 9.497 ms | 44.000 ms | 65,89 |

Com `1000` usuários, todos os cenários apresentaram falhas e forte aumento no tempo de resposta. O cenário com `1` container teve a menor taxa de falha (`6,35%`) e a maior taxa de requisições por segundo (`88,91 req/s`), mas teve o maior P95 (`60.000 ms`). O cenário com `2` containers reduziu o P95 para `37.000 ms`, porém teve a maior taxa de falha (`19,64%`). O cenário com `3` containers teve comportamento próximo ao de `2` containers em falhas (`19,00%`), mas com menor throughput (`65,89 req/s`) e maior média de resposta (`9.497 ms`).

### Resumo observado

Para cargas leves e moderadas (`10` e `100` usuários), a página pequena foi atendida sem falhas em todos os cenários. As diferenças entre 1, 2 e 3 containers foram pequenas, e o uso de mais containers WordPress não apresentou ganho claro.

Para carga pesada (`1000` usuários), a aplicação apresentou degradação significativa em todos os cenários. O aumento de containers WordPress não melhorou automaticamente o resultado geral: com `2` e `3` containers, a taxa de falha ficou maior do que com `1` container. Porém, houve melhora no P95 em comparação com 1 container: o P95 caiu de `60.000 ms` com 1 container para `37.000 ms` com 2 containers e `44.000 ms` com 3 containers. Isso indica que a distribuição entre mais containers ajudou parte das requisições mais lentas, mesmo sem reduzir a taxa total de falhas. O gargalo geral ainda pode estar em recursos compartilhados, como MySQL, CPU, memória, disco, rede Docker ou no próprio ambiente de execução, e não apenas na quantidade de instâncias WordPress disponíveis.

De forma geral, nos testes da página pequena, a configuração com `1` container apresentou os melhores resultados em taxa de falha e throughput na carga de `1000` usuários. As configurações com `2` e `3` containers mantiveram estabilidade em cargas menores, mas não demonstraram vantagem sob carga pesada nesta bateria de testes.

## Página média

Tamanho aproximado da resposta:

```text
500 KB
```

### 1 container WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.898 | 0 | 0,00% | 79 ms | 74 ms | 110 ms | 6,33 | 523.285 bytes |
| 100 | 17.392 | 0 | 0,00% | 204 ms | 170 ms | 410 ms | 57,96 | 523.285 bytes |
| 1000 | 19.688 | 1.878 | 9,54% | 9.803 ms | 2.100 ms | 62.000 ms | 65,49 | 473.386 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a página média foi atendida sem falhas. O aumento no tamanho da resposta elevou os tempos de resposta em comparação com a página pequena, principalmente no teste com `100` usuários.

Com `1000` usuários simultâneos, a página média apresentou degradação significativa. Foram registradas `1.878` falhas, com taxa de falha de `9,54%`. O tempo médio subiu para `9.803 ms` e o P95 chegou a `62.000 ms`, indicando forte lentidão nas requisições mais demoradas.

### Comparativo com a página pequena - 1 container WordPress

| Usuários | Página | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 1.300 | 0 | 0,00% | 55 ms | 80 ms | 6,40 | 85.279 bytes |
| 10 | média | 1.898 | 0 | 0,00% | 79 ms | 110 ms | 6,33 | 523.285 bytes |
| 100 | pequena | 18.496 | 0 | 0,00% | 102 ms | 200 ms | 61,65 | 85.279 bytes |
| 100 | média | 17.392 | 0 | 0,00% | 204 ms | 410 ms | 57,96 | 523.285 bytes |
| 1000 | pequena | 26.683 | 1.694 | 6,35% | 6.647 ms | 60.000 ms | 88,91 | 79.876 bytes |
| 1000 | média | 19.688 | 1.878 | 9,54% | 9.803 ms | 62.000 ms | 65,49 | 473.386 bytes |

#### Resumo observado

Comparando a página média com a página pequena usando `1` container WordPress, o aumento do tamanho da resposta impactou diretamente o tempo de resposta.

Com `10` usuários, a página média manteve estabilidade, mas a média subiu de `55 ms` para `79 ms` e o P95 subiu de `80 ms` para `110 ms`.

Com `100` usuários, a diferença ficou mais clara: a média da página média foi aproximadamente o dobro da página pequena (`204 ms` contra `102 ms`), e o P95 também ficou maior (`410 ms` contra `200 ms`). Mesmo assim, não houve falhas em nenhum dos dois casos.

Com `1000` usuários, a página média teve comportamento pior do que a pequena. A taxa de falha subiu de `6,35%` para `9,54%`, o tempo médio aumentou de `6.647 ms` para `9.803 ms`, e o throughput caiu de `88,91 req/s` para `65,49 req/s`. O P95 ficou próximo nos dois cenários, mas ainda maior na página média (`62.000 ms` contra `60.000 ms`).

De forma geral, a página média exigiu mais da aplicação do que a página pequena. Em cargas leves e moderadas, a diferença apareceu principalmente no tempo de resposta. Em carga pesada, a diferença apareceu também em falhas, throughput e tempo médio.

### 2 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.905 | 0 | 0,00% | 78 ms | 74 ms | 110 ms | 6,35 | 523.285 bytes |
| 100 | 17.381 | 0 | 0,00% | 204 ms | 170 ms | 400 ms | 57,93 | 523.285 bytes |
| 1000 | 20.911 | 4.186 | 20,02% | 9.794 ms | 4.400 ms | 42.000 ms | 69,63 | 419.020 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a página média com 2 containers foi atendida sem falhas. Os tempos ficaram praticamente iguais aos observados com 1 container para a mesma página.

Com `1000` usuários simultâneos, houve forte degradação. Foram registradas `4.186` falhas, com taxa de falha de `20,02%`. O tempo médio ficou em `9.794 ms` e o P95 chegou a `42.000 ms`.

### Comparativo com a página pequena - 2 containers WordPress

| Usuários | Página | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 1.266 | 0 | 0,00% | 58 ms | 86 ms | 6,44 | 85.279 bytes |
| 10 | média | 1.905 | 0 | 0,00% | 78 ms | 110 ms | 6,35 | 523.285 bytes |
| 100 | pequena | 18.221 | 0 | 0,00% | 123 ms | 230 ms | 60,74 | 85.279 bytes |
| 100 | média | 17.381 | 0 | 0,00% | 204 ms | 400 ms | 57,93 | 523.285 bytes |
| 1000 | pequena | 25.449 | 4.997 | 19,64% | 7.791 ms | 37.000 ms | 84,74 | 69.012 bytes |
| 1000 | média | 20.911 | 4.186 | 20,02% | 9.794 ms | 42.000 ms | 69,63 | 419.020 bytes |

#### Resumo observado

Comparando página média e página pequena com `2` containers WordPress, a página média apresentou tempos de resposta maiores em todas as cargas.

Com `10` usuários, ambas ficaram sem falhas, mas a média subiu de `58 ms` na página pequena para `78 ms` na página média. O P95 também aumentou de `86 ms` para `110 ms`.

Com `100` usuários, a diferença foi mais evidente: a média subiu de `123 ms` para `204 ms`, e o P95 subiu de `230 ms` para `400 ms`. Ainda assim, não houve falhas em nenhum dos dois testes.

Com `1000` usuários, os dois cenários tiveram taxa de falha parecida: `19,64%` na página pequena e `20,02%` na página média. Porém, a página média teve menor throughput (`69,63 req/s` contra `84,74 req/s`) e maior P95 (`42.000 ms` contra `37.000 ms`). Isso mostra que, com 2 containers, o aumento do tamanho da página prejudicou principalmente latência e vazão.

### Comparativo da página média - 1 container contra 2 containers

| Usuários | Containers | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 1.898 | 0 | 0,00% | 79 ms | 110 ms | 6,33 | 523.285 bytes |
| 10 | 2 | 1.905 | 0 | 0,00% | 78 ms | 110 ms | 6,35 | 523.285 bytes |
| 100 | 1 | 17.392 | 0 | 0,00% | 204 ms | 410 ms | 57,96 | 523.285 bytes |
| 100 | 2 | 17.381 | 0 | 0,00% | 204 ms | 400 ms | 57,93 | 523.285 bytes |
| 1000 | 1 | 19.688 | 1.878 | 9,54% | 9.803 ms | 62.000 ms | 65,49 | 473.386 bytes |
| 1000 | 2 | 20.911 | 4.186 | 20,02% | 9.794 ms | 42.000 ms | 69,63 | 419.020 bytes |

#### Resumo observado

Para `10` e `100` usuários, os resultados da página média com 1 e 2 containers foram praticamente equivalentes. Não houve falhas, o throughput ficou muito próximo e as diferenças de média e P95 foram pequenas.

Com `1000` usuários, o uso de 2 containers teve um comportamento misto. A taxa de falha aumentou de `9,54%` para `20,02%`, mas o P95 melhorou de `62.000 ms` para `42.000 ms`, e o throughput subiu de `65,49 req/s` para `69,63 req/s`. Isso sugere que 2 containers ajudaram a reduzir parte das requisições mais lentas e a aumentar levemente a vazão, mas também aumentaram a quantidade total de falhas sob carga pesada.

### 3 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.910 | 0 | 0,00% | 79 ms | 75 ms | 110 ms | 6,37 | 523.285 bytes |
| 100 | 17.472 | 0 | 0,00% | 195 ms | 170 ms | 360 ms | 58,24 | 523.285 bytes |
| 1000 | 21.104 | 9.864 | 46,74% | 8.971 ms | 3.500 ms | 46.000 ms | 70,24 | 279.068 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a página média com 3 containers foi atendida sem falhas. O comportamento foi parecido com os testes de 1 e 2 containers, com pequena melhora no teste de `100` usuários em média e P95.

Com `1000` usuários simultâneos, houve degradação forte. Foram registradas `9.864` falhas, com taxa de falha de `46,74%`. Apesar do tempo médio (`8.971 ms`) ter ficado menor do que nas execuções com 1 e 2 containers, a quantidade de falhas foi muito maior. O P95 ficou em `46.000 ms`.

### Comparativo da página média - 1, 2 e 3 containers

| Usuários | Containers | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 1.898 | 0 | 0,00% | 79 ms | 110 ms | 6,33 | 523.285 bytes |
| 10 | 2 | 1.905 | 0 | 0,00% | 78 ms | 110 ms | 6,35 | 523.285 bytes |
| 10 | 3 | 1.910 | 0 | 0,00% | 79 ms | 110 ms | 6,37 | 523.285 bytes |
| 100 | 1 | 17.392 | 0 | 0,00% | 204 ms | 410 ms | 57,96 | 523.285 bytes |
| 100 | 2 | 17.381 | 0 | 0,00% | 204 ms | 400 ms | 57,93 | 523.285 bytes |
| 100 | 3 | 17.472 | 0 | 0,00% | 195 ms | 360 ms | 58,24 | 523.285 bytes |
| 1000 | 1 | 19.688 | 1.878 | 9,54% | 9.803 ms | 62.000 ms | 65,49 | 473.386 bytes |
| 1000 | 2 | 20.911 | 4.186 | 20,02% | 9.794 ms | 42.000 ms | 69,63 | 419.020 bytes |
| 1000 | 3 | 21.104 | 9.864 | 46,74% | 8.971 ms | 46.000 ms | 70,24 | 279.068 bytes |

#### Resumo observado

Para `10` usuários, os três cenários da página média foram praticamente equivalentes. Não houve falhas, o P95 ficou em `110 ms` em todos os casos e a vazão ficou próxima de `6,3 req/s`.

Para `100` usuários, também não houve falhas. A configuração com 3 containers apresentou a menor média (`195 ms`) e o menor P95 (`360 ms`), enquanto 1 e 2 containers ficaram com médias de `204 ms` e P95 de `410 ms` e `400 ms`. Nessa carga, 3 containers apresentou pequena melhora de latência.

Para `1000` usuários, a configuração com 3 containers teve o maior número de falhas e a maior taxa de falha (`46,74%`). Mesmo tendo o menor tempo médio (`8.971 ms`) e a maior vazão (`70,24 req/s`), esse resultado precisa ser interpretado com cuidado, porque muitas requisições falharam. O P95 de 3 containers (`46.000 ms`) ficou melhor que o de 1 container (`62.000 ms`), mas pior que o de 2 containers (`42.000 ms`).

De forma geral, para a página média, aumentar de 1 para 2 ou 3 containers não reduziu as falhas sob carga pesada. Em `1000` usuários, 2 containers melhorou o P95 em relação a 1 container, mas aumentou a taxa de falha. Com 3 containers, a taxa de falha aumentou ainda mais, embora a média e a vazão tenham melhorado numericamente.

### Comparativo com a página pequena - 2 containers WordPress

| Usuários | Página | Containers | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 2 | 1.266 | 0 | 0,00% | 58 ms | 86 ms | 6,44 | 85.279 bytes |
| 10 | média | 3 | 1.910 | 0 | 0,00% | 79 ms | 110 ms | 6,37 | 523.285 bytes |
| 100 | pequena | 2 | 18.221 | 0 | 0,00% | 123 ms | 230 ms | 60,74 | 85.279 bytes |
| 100 | média | 3 | 17.472 | 0 | 0,00% | 195 ms | 360 ms | 58,24 | 523.285 bytes |
| 1000 | pequena | 2 | 25.449 | 4.997 | 19,64% | 7.791 ms | 37.000 ms | 84,74 | 69.012 bytes |
| 1000 | média | 3 | 21.104 | 9.864 | 46,74% | 8.971 ms | 46.000 ms | 70,24 | 279.068 bytes |

#### Resumo observado

Comparando a página média com 3 containers contra a página pequena com 2 containers, a página média apresentou maior custo em todas as cargas. Com `10` e `100` usuários, ambas não tiveram falhas, mas a página média teve tempos maiores: em `100` usuários, a média subiu de `123 ms` para `195 ms`, e o P95 subiu de `230 ms` para `360 ms`.

Com `1000` usuários, a diferença foi mais forte. A página média com 3 containers teve taxa de falha de `46,74%`, contra `19,64%` da página pequena com 2 containers. Também teve menor throughput (`70,24 req/s` contra `84,74 req/s`) e maior P95 (`46.000 ms` contra `37.000 ms`). Isso reforça que o tamanho maior da página aumenta a pressão sobre a aplicação, mesmo com mais containers WordPress disponíveis.
