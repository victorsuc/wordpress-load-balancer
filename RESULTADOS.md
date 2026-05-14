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

## Página grande

Tamanho aproximado da resposta:

```text
1 MB
```

### 1 container WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 0 | 0 | N/A | N/A | N/A | N/A | 0,00 | 0 bytes |
| 100 | 16.367 | 0 | 0,00% | 306 ms | 270 ms | 540 ms | 54,57 | 1.078.664 bytes |
| 1000 | 16.494 | 1.778 | 10,78% | 11.872 ms | 2.600 ms | 63.000 ms | 54,91 | 962.406 bytes |

#### Análise

O arquivo de resultado do teste com `10` usuários não registrou requisições (`Request Count = 0`). Por isso, esse resultado não deve ser usado na análise comparativa e precisa ser reexecutado para gerar dados válidos.

Com `100` usuários simultâneos, a página grande foi atendida sem falhas. O tempo médio foi de `306 ms`, a mediana ficou em `270 ms` e o P95 ficou em `540 ms`.

Com `1000` usuários simultâneos, a página grande apresentou degradação significativa. Foram registradas `1.778` falhas, com taxa de falha de `10,78%`. O tempo médio subiu para `11.872 ms`, a mediana ficou em `2.600 ms` e o P95 chegou a `63.000 ms`.

### Comparativo entre páginas - 1 container WordPress

| Usuários | Página | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 1.300 | 0 | 0,00% | 55 ms | 80 ms | 6,40 | 85.279 bytes |
| 10 | média | 1.898 | 0 | 0,00% | 79 ms | 110 ms | 6,33 | 523.285 bytes |
| 10 | grande | 0 | 0 | N/A | N/A | N/A | 0,00 | 0 bytes |
| 100 | pequena | 18.496 | 0 | 0,00% | 102 ms | 200 ms | 61,65 | 85.279 bytes |
| 100 | média | 17.392 | 0 | 0,00% | 204 ms | 410 ms | 57,96 | 523.285 bytes |
| 100 | grande | 16.367 | 0 | 0,00% | 306 ms | 540 ms | 54,57 | 1.078.664 bytes |
| 1000 | pequena | 26.683 | 1.694 | 6,35% | 6.647 ms | 60.000 ms | 88,91 | 79.876 bytes |
| 1000 | média | 19.688 | 1.878 | 9,54% | 9.803 ms | 62.000 ms | 65,49 | 473.386 bytes |
| 1000 | grande | 16.494 | 1.778 | 10,78% | 11.872 ms | 63.000 ms | 54,91 | 962.406 bytes |

#### Resumo observado

Com `100` usuários simultâneos, as três páginas não apresentaram falhas com 1 container WordPress, mas o aumento do tamanho da resposta impactou diretamente a latência. A média subiu de `102 ms` na página pequena para `204 ms` na média e `306 ms` na grande. O P95 também cresceu na mesma direção: `200 ms`, `410 ms` e `540 ms`.

Com `1000` usuários simultâneos, as três páginas apresentaram falhas e degradação de tempo de resposta. Conforme o tamanho da página aumentou, a taxa de falha e o tempo médio também aumentaram: a página pequena teve `6,35%` de falhas e média de `6.647 ms`, a média teve `9,54%` e `9.803 ms`, e a grande teve `10,78%` e `11.872 ms`.

O throughput também caiu conforme a página ficou maior. Em `1000` usuários, a página pequena atingiu `88,91 req/s`, a média `65,49 req/s` e a grande `54,91 req/s`. Isso indica que o tamanho da resposta tem impacto direto na capacidade de vazão da aplicação.

De forma geral, com 1 container WordPress, a página grande foi a mais pesada entre as três. Em carga moderada (`100` usuários), o sistema ainda conseguiu responder sem falhas, mas com maior latência. Em carga pesada (`1000` usuários), a página grande apresentou a pior combinação de tempo médio, P95 e throughput.

### 2 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.890 | 0 | 0,00% | 94 ms | 89 ms | 130 ms | 6,30 | 1.078.664 bytes |
| 100 | 15.762 | 0 | 0,00% | 379 ms | 310 ms | 900 ms | 52,52 | 1.078.664 bytes |
| 1000 | 19.296 | 9.555 | 49,52% | 10.293 ms | 2.400 ms | 58.000 ms | 64,26 | 544.825 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a página grande com 2 containers foi atendida sem falhas. O teste com `10` usuários apresentou média de `94 ms` e P95 de `130 ms`. Com `100` usuários, a média subiu para `379 ms` e o P95 para `900 ms`.

Com `1000` usuários simultâneos, houve degradação forte. Foram registradas `9.555` falhas, com taxa de falha de `49,52%`. O tempo médio ficou em `10.293 ms`, a mediana em `2.400 ms` e o P95 em `58.000 ms`.

### Comparativo da página grande - 1 container contra 2 containers

| Usuários | Containers | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 0 | 0 | N/A | N/A | N/A | 0,00 | 0 bytes |
| 10 | 2 | 1.890 | 0 | 0,00% | 94 ms | 130 ms | 6,30 | 1.078.664 bytes |
| 100 | 1 | 16.367 | 0 | 0,00% | 306 ms | 540 ms | 54,57 | 1.078.664 bytes |
| 100 | 2 | 15.762 | 0 | 0,00% | 379 ms | 900 ms | 52,52 | 1.078.664 bytes |
| 1000 | 1 | 16.494 | 1.778 | 10,78% | 11.872 ms | 63.000 ms | 54,91 | 962.406 bytes |
| 1000 | 2 | 19.296 | 9.555 | 49,52% | 10.293 ms | 58.000 ms | 64,26 | 544.825 bytes |

#### Resumo observado

O teste de `10` usuários com 1 container não registrou requisições, então a comparação para essa carga deve considerar apenas que o resultado de 2 containers foi válido e sem falhas.

Com `100` usuários, a página grande não apresentou falhas em 1 ou 2 containers. No entanto, a configuração com 2 containers teve latência maior: a média subiu de `306 ms` para `379 ms`, e o P95 subiu de `540 ms` para `900 ms`. O throughput também caiu levemente, de `54,57 req/s` para `52,52 req/s`.

Com `1000` usuários, o uso de 2 containers teve comportamento misto. A média caiu de `11.872 ms` para `10.293 ms`, o P95 caiu de `63.000 ms` para `58.000 ms`, e o throughput subiu de `54,91 req/s` para `64,26 req/s`. Porém, a taxa de falha aumentou de `10,78%` para `49,52%`, o que indica que a melhora de tempo e vazão veio acompanhada de uma quantidade muito maior de requisições falhando.

### Comparativo entre páginas - 2 containers WordPress

| Usuários | Página | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 1.266 | 0 | 0,00% | 58 ms | 86 ms | 6,44 | 85.279 bytes |
| 10 | média | 1.905 | 0 | 0,00% | 78 ms | 110 ms | 6,35 | 523.285 bytes |
| 10 | grande | 1.890 | 0 | 0,00% | 94 ms | 130 ms | 6,30 | 1.078.664 bytes |
| 100 | pequena | 18.221 | 0 | 0,00% | 123 ms | 230 ms | 60,74 | 85.279 bytes |
| 100 | média | 17.381 | 0 | 0,00% | 204 ms | 400 ms | 57,93 | 523.285 bytes |
| 100 | grande | 15.762 | 0 | 0,00% | 379 ms | 900 ms | 52,52 | 1.078.664 bytes |
| 1000 | pequena | 25.449 | 4.997 | 19,64% | 7.791 ms | 37.000 ms | 84,74 | 69.012 bytes |
| 1000 | média | 20.911 | 4.186 | 20,02% | 9.794 ms | 42.000 ms | 69,63 | 419.020 bytes |
| 1000 | grande | 19.296 | 9.555 | 49,52% | 10.293 ms | 58.000 ms | 64,26 | 544.825 bytes |

#### Resumo observado

Com `10` usuários simultâneos, as três páginas foram atendidas sem falhas com 2 containers. A latência aumentou conforme o tamanho da página cresceu: a média foi de `58 ms` na pequena, `78 ms` na média e `94 ms` na grande. O P95 seguiu o mesmo comportamento: `86 ms`, `110 ms` e `130 ms`.

Com `100` usuários simultâneos, nenhuma página apresentou falhas, mas a diferença de latência ficou mais expressiva. A página grande teve média de `379 ms`, contra `204 ms` da média e `123 ms` da pequena. O P95 da grande chegou a `900 ms`, mais que o dobro da média (`400 ms`) e quase quatro vezes o da pequena (`230 ms`).

Com `1000` usuários simultâneos, as três páginas apresentaram falhas. A página pequena e a média tiveram taxas de falha próximas (`19,64%` e `20,02%`), enquanto a página grande subiu para `49,52%`. A página grande também teve o maior P95 (`58.000 ms`) e o menor throughput entre as três (`64,26 req/s`). Isso reforça que, com 2 containers, o aumento do tamanho da resposta tem impacto direto na latência, na taxa de falhas e na vazão sob carga pesada.

### 3 containers WordPress

| Usuários | Requests | Falhas | Falha % | Média | Mediana | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1.884 | 0 | 0,00% | 93 ms | 88 ms | 120 ms | 6,28 | 1.078.664 bytes |
| 100 | 15.809 | 0 | 0,00% | 374 ms | 320 ms | 750 ms | 52,68 | 1.078.664 bytes |
| 1000 | 19.766 | 12.071 | 61,07% | 10.662 ms | 1.800 ms | 60.000 ms | 64,17 | 420.229 bytes |

#### Análise

Com `10` e `100` usuários simultâneos, a página grande com 3 containers foi atendida sem falhas. Em `10` usuários, a média ficou em `93 ms` e o P95 em `120 ms`. Em `100` usuários, a média subiu para `374 ms` e o P95 ficou em `750 ms`.

Com `1000` usuários simultâneos, houve degradação severa. Foram registradas `12.071` falhas, com taxa de falha de `61,07%`. O tempo médio ficou em `10.662 ms`, a mediana em `1.800 ms` e o P95 em `60.000 ms`.

### Comparativo da página grande - 1, 2 e 3 containers

| Usuários | Containers | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 1 | 0 | 0 | N/A | N/A | N/A | 0,00 | 0 bytes |
| 10 | 2 | 1.890 | 0 | 0,00% | 94 ms | 130 ms | 6,30 | 1.078.664 bytes |
| 10 | 3 | 1.884 | 0 | 0,00% | 93 ms | 120 ms | 6,28 | 1.078.664 bytes |
| 100 | 1 | 16.367 | 0 | 0,00% | 306 ms | 540 ms | 54,57 | 1.078.664 bytes |
| 100 | 2 | 15.762 | 0 | 0,00% | 379 ms | 900 ms | 52,52 | 1.078.664 bytes |
| 100 | 3 | 15.809 | 0 | 0,00% | 374 ms | 750 ms | 52,68 | 1.078.664 bytes |
| 1000 | 1 | 16.494 | 1.778 | 10,78% | 11.872 ms | 63.000 ms | 54,91 | 962.406 bytes |
| 1000 | 2 | 19.296 | 9.555 | 49,52% | 10.293 ms | 58.000 ms | 64,26 | 544.825 bytes |
| 1000 | 3 | 19.766 | 12.071 | 61,07% | 10.662 ms | 60.000 ms | 64,17 | 420.229 bytes |

#### Resumo observado

O teste de `10` usuários com 1 container não registrou requisições, então a comparação nessa carga fica restrita aos cenários com 2 e 3 containers. Neles, os resultados foram muito próximos: `94 ms` de média e `130 ms` de P95 com 2 containers, contra `93 ms` de média e `120 ms` de P95 com 3 containers.

Com `100` usuários, nenhuma configuração apresentou falhas. A melhor latência foi observada com 1 container: média de `306 ms` e P95 de `540 ms`. Com 2 e 3 containers, os tempos ficaram maiores. A configuração com 3 containers melhorou em relação a 2 no P95 (`750 ms` contra `900 ms`), mas ainda ficou pior que 1 container.

Com `1000` usuários, todas as configurações apresentaram falhas. O uso de 2 e 3 containers aumentou a vazão em relação a 1 container, mas também aumentou muito a taxa de falha. A falha subiu de `10,78%` com 1 container para `49,52%` com 2 containers e `61,07%` com 3 containers. O P95 melhorou levemente ao sair de 1 container (`63.000 ms`) para 2 (`58.000 ms`) e 3 (`60.000 ms`), mas essa melhora veio acompanhada de uma quantidade muito maior de falhas.

De forma geral, para a página grande, adicionar containers não resultou em uma melhora global. Em carga moderada, 1 container teve melhor latência. Em carga pesada, 2 e 3 containers aumentaram a vazão e reduziram um pouco o P95, mas pioraram bastante a taxa de falha.

### Comparativo entre páginas - 3 containers WordPress

| Usuários | Página | Requests | Falhas | Falha % | Média | P95 | Req/s | Tamanho médio |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | pequena | 1.930 | 0 | 0,00% | 57 ms | 80 ms | 6,43 | 85.279 bytes |
| 10 | média | 1.910 | 0 | 0,00% | 79 ms | 110 ms | 6,37 | 523.285 bytes |
| 10 | grande | 1.884 | 0 | 0,00% | 93 ms | 120 ms | 6,28 | 1.078.664 bytes |
| 100 | pequena | 18.271 | 0 | 0,00% | 119 ms | 230 ms | 60,90 | 85.279 bytes |
| 100 | média | 17.472 | 0 | 0,00% | 195 ms | 360 ms | 58,24 | 523.285 bytes |
| 100 | grande | 15.809 | 0 | 0,00% | 374 ms | 750 ms | 52,68 | 1.078.664 bytes |
| 1000 | pequena | 19.799 | 3.762 | 19,00% | 9.497 ms | 44.000 ms | 65,89 | 69.537 bytes |
| 1000 | média | 21.104 | 9.864 | 46,74% | 8.971 ms | 46.000 ms | 70,24 | 279.068 bytes |
| 1000 | grande | 19.766 | 12.071 | 61,07% | 10.662 ms | 60.000 ms | 64,17 | 420.229 bytes |

#### Resumo observado

Com `10` usuários simultâneos, as três páginas foram atendidas sem falhas com 3 containers. A latência aumentou conforme o tamanho da página cresceu: a média foi de `57 ms` na pequena, `79 ms` na média e `93 ms` na grande. O P95 também cresceu: `80 ms`, `110 ms` e `120 ms`.

Com `100` usuários simultâneos, nenhuma página apresentou falhas, mas o impacto do tamanho da página ficou mais evidente. A página grande teve média de `374 ms`, contra `195 ms` da média e `119 ms` da pequena. O P95 da grande chegou a `750 ms`, acima dos `360 ms` da média e dos `230 ms` da pequena.

Com `1000` usuários simultâneos, todas as páginas apresentaram falhas. A taxa de falha aumentou conforme o tamanho da resposta cresceu: `19,00%` na pequena, `46,74%` na média e `61,07%` na grande. O P95 também seguiu essa tendência: `44.000 ms`, `46.000 ms` e `60.000 ms`. Isso mostra que, com 3 containers, a página grande foi a mais afetada em carga pesada.

De forma geral, com 3 containers WordPress, o tamanho da página teve impacto claro no comportamento da aplicação. Em cargas leves e moderadas, o efeito apareceu principalmente na latência. Em carga pesada, apareceu também na taxa de falha e na queda de estabilidade.
