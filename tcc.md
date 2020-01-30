# Introdução

## Motivação do projeto

## Objetivos

# Revisão bibliográfica

## Robô diferencial

http://planning.cs.uiuc.edu/node659.html
http://www.cs.columbia.edu/~allen/F17/NOTES/icckinematics.pdf

Um robô diferencial é um tipo comum de robô móvel no qual duas rodas tracionadas são montadas em um mesmo eixo comum, podendo girar independente uma da outra, e uma terceira roda é montada em tal posição que impede o robô de cair, porém essa não é tracionada e pode girar em seu próprio eixo e na sua transversal, conforme o movimento do robô. Uma grande vantagem desse sistema é a sua simplicidade na modelagem matemática, visto que apenas as duas rodas tracionadas (no mesmo eixo) são as responsáveis pelo movimento linear e angular do robô.
	
								**DIAGRAMA DO ROBO**

Analisando o diagrama, conclui-se sobre a relação do movimento de cada roda e do robô:
* Se as velocidades angulares das rodas forem iguais, o robô possui apenas velocidade linear
* Se as velocidade angulares das rodas forem diferentes, o robô possui velocidade linear e angular
* Se as velocidade angulares das rodas forem inversas, o robô possui apenas velocidade angular

Note que, de acordo com essa modelagem, a direção das velocidades das rodas direita e esquerda e do robô são paralelas em qualquer instante de tempo.

Para simplificar mais adiante o tratamento de perseguição de caminho, é imposta a restrição que as rodas do robô possuem sempre uma velocidade $V$ tal que $V \ge 0$.

Considerando uma condição de não-deslizamento nas rodas tracionadas, temos a cinemática direta do sistema:

$$
V = \frac{V_{R} + V_{L}}{2} \\
\Omega = \frac{V_{R} - V_{L}}{L}
$$

Com simples manipulação algébrica, a cinemática inversa:

$$
V_{R} = V + \frac{{\Omega}{L}}{2} \\
V_{L} = V - \frac{{\Omega}{L}}{2}
$$

Para cada roda, podemos substituir $V=\dot{\theta}R$ e chegar na relação cinemática em $rad/s$. Dessa maneira, temos a cinemática direta:

$$
V = \frac{R}{2} (\dot{\theta_{R}} + \dot{\theta_{L}}) \\
\Omega = \frac{R}{L} (\dot{\theta_{R}} - \dot{\theta_{L}})
$$

e a inversa:

$$
\dot{\theta_{R}} =  \frac{2V+{\Omega}{L}}{2R} \\
\dot{\theta_{L}} = \frac{2V-{\Omega}{L}}{2R}
$$

Com essas equações em mãos, utilizaremos um sistema de visão computacional para fechar uma malha de controle simples, onde as entradas são as velocidades linear e angular do carrinho, e a saída é a velocidade angular (maximizando a velocidade linear), de acordo com o caminho de referência encontrado pelo algoritmo.

## Visão Computacional

gonzales e woods

Uma imagem qualquer pode ser considerada uma função $$f (x,y)$$ onde cada pixel (coordenada $$x,y$$) possui um valor em nível de cinza. <cite> Para imagens digitais, como é o caso deste trabalho, os níveis de cinza dependem do número de bits disponíveis na memória. Como os computadores trabalham com *bytes*, normalmente utilizamos 256 níveis de cinza (8 *bits*). As imagens coloridas, por conseguinte, são simplesmente 3 funções diferentes $$R(x,y)$$, $$G(x,y)$$ e $$B(x,y)$$ que definem o valor entre 0 e 255 de vermelho, verde e azul, respectivamente, de cada pixel $$x,y$$. <cite>

Uma definição de visão computacional pode ser tomada como a análise dessas funções com o objetivo de obtenção de informações, tal qual como a habilidade dos humanos de enxergar, segmentar zonas de interesse, inferir informações a partir da análise dessas zonas, e tomar uma decisão com base na inferência. <cite>

## Breadth First Search

## Steering Behaviour

## Protocolo Socket TCP/IP

Douglas E. Comer, David L. Stevens
Internetworking with TCP/IP, Vol. III: Client-Server Programming and Applications

O framework do protocolo TCP é definido na quarta camada do modelo de rede ISO/OSI, a camada de *transporte*. Ou seja, condições imprescindíveis para sua implementação são as três primeiras camadas do modelo: a primeira camada física (as conexões eletrônicas), a segunda camada de enlace (que permite abstrações para a camada física), e a terceira camada de rede (que implementa o protocolo IP). <cite> Assim, é possível definir a camada mais abstrata, a sétima camada, de aplicação, com um protocolo que seja cabível. O obetivo desse *stack* nada mais é que transmitir dados de maneira ponto-a-ponto seguindo um formato pré-estabelecido e conhecido pelos dois participantes da comunicação. <cite>

## ESP8266

A eletrônica que controla o robô tem como placa de controle a NodeMCU, que por sua vez é controlada pelo microship da Espressif ESP8266. O CI possui pinos de I/O, saídas PWM e entradas analógicas, vem preparado para comunicação serial, SPI e I2C, e, importante para este trabalho, tem todo o *stack* TCP/IP implementado por padrão. <cite>

							Imagem do pinout do nodemcu

# Materiais e Métodos

## Montagem do robô diferencial

## Protocolo de comunicação

## Pipeline do sistema de visão computacional

# Desenvolvimento e resultados

## Desenvolvimento e código

## Ambiente simulado

### Informações gerais

### Resultado

## Ambiente real

### Informações gerais

### Problemas com cores

### Resultado

# Conclusão

## Próximos passos

## Problemas e limitações do sistema