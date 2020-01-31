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

## Motor de passo

hughes eletric motors and drivers

Motores de passo são motores que funcionam muito bem com microcontroladores devido a sua característica única de rotacionar um ângulo conhecido a cada pulso de tensão recebido. <cite> Ou seja, provendo um certo número de pulsos para o motor (ou o seu driver) pode-se controlar a posição, ou mesmo a velocidade, do eixo em um sistema de controle aberto. <cite>

						Esquemático motor de passo

A rotação do eixo ocorre quando o rotor se alinha com o campos magnético induzido pelas bobinas nos dentes do estator. Em um motor de passo com duas fases, como é o caso do utilizado neste trabalho, temos quatro fios que dão acesso as 2 bobinas do estator. Assim sendo, cada pulso enviado ao driver troca a energização das bobinas, o que faz com que o rotor rotacione o equivalente a um pulso <cite>, o que no caso do nosso motor reflete em 1,8 grau.

## Visão computacional

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

O robô foi desenvolvido com simplicidade e baixos custos em mente. A sua lista de componentes contém:

### NodeMCU

O NodeMCU (microchip ESP8266) é o microcontrolador do sistema. Das suas funcionalidades, são utilizadas 3 portas lógicas de saída para pulsos em cada driver de motor e para ativar o modo SLEEP, e o módulo WiFi que mantém um servidor TCP/IP para comunicação. A imagem a seguir ilustra a montagem do circuito.

									Circuito

### 2 x Motores de Passo

Devido às necessidades do sistema de controle desenvolvido adiante, é necessário adequar a velocidade das rodas com grande exatidão. No caso desse tipo de motor, é possível definir quantos passos devem ser acionados por segundo (PPS), e sabendo que o motor tem 200 passos por revolução é trivial transformar a velocidade desejada, em rotação por segundo (RPS), para pps. O motor é um Nema 17 bifásico que possui torque de 3,5 kgf.cm acoplado a uma roda de 63mm de diâmetro. A velocidade dos motores é limitada por software em 1 (uma) rotação por segundo. <cite datasheet>

### 2 x Drivers A4988

Para controlar os motores de passo, utilizamos o driver A4988.

									Pinout A4988

Fora os pinos de alimentação, temos os pinos de direção, pulso e sleep. Como o robô anda apenas para frente (conforme restrição imposta na modelagem matemática), os pinos de direção foram ligados diretamente em Vcc e Ground. Os pinos de pulso foram ligados em saídas lógicas do microcontrolador, e os pinos de sleep a uma terceira saída lógica.

O pino de sleep é importante uma vez que o consumo maior de corrente por parte dos motores de passo ocorre quando não há movimento. <cite> Dessa maneira, controla-se o pino de sleep pela NodeMCU, configurando o pino digital em *LOW* quando os motores estão ambos estacionários (note que a porta SLEEP é invertida). <cite datasheet>

### Bateria NiMH

Para energizar o carrinho, é utilizada uma bateria de níquel metal-hidreto, de 8,4 V e capacidade para 1200 mAh. Em conjunto com a bateria, um capacitor é utilizado para estabilizar a tensão de saída para prevenir danos aos motores e ao driver.

### Carcaça

A carcaça do sistema robótico é uma simples caixa de madeira de dimensões 220 x 120 x 50 (em milímetros). Nela estão a bateria e a protoboard com todos os eletrônicos conectados.

## Protocolo de comunicação

O protocolo de comunicação da aplicação é pré-definido e de conhecimento do sistema de visão computacional e do microcontrolador embarcado no robô.

A mensagem é bem simples e composta de dois bytes apenas. O primeiro byte reflete a velocidade da roda esquerda e o segundo byte da roda direita. Como existem 256 possibilidades para o valor de cada byte, foi definido que o valor enviado deve ser igual a 100 vezes a rotação desejada em RPS. Ou seja, para configurar a roda da esquerda a velocidade máxima (1 RPS) e a da direita a 50% da máxima (0,5 RPS), enviamos dois bytes equivalentes ao número 100 e ao número 50: `\x64\x32`.

Por parte do microcontrolador, esse bytes são recebidos pela rede e atribuidos como *unsigned char*, para depois setarem a velocidade dos motores corretamente no programa.

## Pipeline do sistema de visão computacional

A malha de controle para a velocidade das rodas é baseada inteiramente na identificação de cores. 

							Imagem real exemplo

A princípio, é definido no código:

* Amarelo como ponto de chegada
* Verde como as paredes (ou pontos inacessíveis)
* Azul como a parte dianteira do robô
* Vermelho como a parte traseira do robô

No programa como um todo, as paredes e o ponto de chegada (verde e amarelo, respectivamente) são avaliados apenas na primeira etapa, para encontrar o caminho ideal. Com o caminho encontrado, a posição e angulação (*yaw*) do robô são constantemente avaliados e reajustados conforme necessário, segundo o algoritmo de controle. Isso se traduz em uma forte limitação do sistema: uma vez definido o caminho, mudanças na posição do ponto de chegada ou das paredes não muda em nada o movimento do robô, ou seja, a partir do momento que o robô começa a se movimentar, o ambiente deve permanecer estático.

O robô faz o uso de duas cores para que seja possível identificar não somente a sua posição, mas também a sua angulação. Dessa forma, temos que a posição do robô $$(x,y,yaw)$$ é dada por (conforme definida na função `get_robot_xyyaw`):

$$
x = \frac{x_{azul} + x_{vermelho}}{2} \\
y = \frac{y_{azul} + y_{vermelho}}{2} \\
{yaw} = \tan{(\frac{y_{azul}-y_{vermelho}}{x_{azul}-x_{vermelho}})}
$$

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