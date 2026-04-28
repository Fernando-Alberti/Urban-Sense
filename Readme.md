**UrbanSense - Sistema de Segurança e Ocorrências Urbanas**



O UrbanSense é uma plataforma que permite aos usuários reportar e visualizar ocorrências de segurança em sua região. O sistema utiliza geolocalização para calcular o nível de risco de uma área em tempo real, baseando-se no histórico de incidentes, proximidade e horário atual.



**Tecnologias Utilizadas**



**Backend**



**FastAPI:** Framework principal para a construção da API



**Pydantic:** Validação de dados e esquemas



**Fórmula de Haversine:** Implementação para cálculo automático de distância entre coordenadas geográficas (latitude e longitude)





**Frontend**



**HTML5 / CSS3:** Interface responsiva com gradientes e layouts em cards



**JavaScript (ES6+):** Lógica de consumo de API (Fetch API) e manipulação de DOM



**Leaflet.js:** Biblioteca para mapas interativos e renderização de círculos de proximidade



**OpenStreetMap (Nominatim):** Geocodificação reversa para identificar cidades e bairros a partir de coordenadas





**Funcionalidades**



**1. Registro de Ocorrências:** Permite enviar o tipo de incidente, descrição, cidade e coordenadas exatas





**2. Mapa Interativo:** Visualização da posição do usuário e de incidentes próximos com ícones diferenciados





**3. Cálculo de Risco Dinâmico:** O backend processa as ocorrências em um raio específico e retorna um nível de risco (Baixo, Médio ou Alto)





**4. Visualização por Proximidade:** O mapa exibe círculos coloridos representando diferentes raios de distância (500m, 1000m e 2000m), cujas cores mudam conforme a densidade de ocorrências





**5. Listagem Agrupada:** Página que lista ocorrências filtradas pela cidade do usuário e agrupadas por bairro







**Regras do Algoritmo de Risco**



O nível de risco é calculado através de um sistema de pontos no backend:



**Quantidade:** até 3 ocorrências (+2 pontos), até 6 (+4 pontos), mais de 6 (+6 pontos)



**Recência:** ocorrências nas últimas 48h somam pontos extras



**Tendência:** se o número de crimes recentes for maior que o histórico anterior, o risco aumenta (+3 pontos)



**Horário crítico:**



**23h às 06h:** +5 pontos



**18h às 23h:** +3 pontos



**12h às 18h:** +1 ponto







**Níveis finais:**



**Baixo:** menor que 5 pontos



**Médio:** menor que 14 pontos



**Alto:** maior ou igual a 14 pontos





**Principais Endpoints da API**



**GET /:** verifica se a API está online



**POST /ocorrencia:** registra um novo evento no sistema



**GET /ocorrencias**: lista todas as ocorrências, com filtro opcional por cidade



**GET /dados-mapa:** retorna análise completa de risco e ocorrências próximas





**Como Executar**



**Backend**



Certifique-se de ter o Python instalado e as dependências necessárias.



**Exemplo:**



python uvicorn main:app --reload



**Frontend**



Basta abrir o arquivo index.html em um navegador. O frontend está configurado para se comunicar com o backend local em http://127.0.0.1:8000.





\---



**Nota:** Este projeto utiliza armazenamento em memória (lista de ocorrências), o que significa que os dados são resetados ao reiniciar o servidor backend.

