# Assessorias Esportivas de Fortaleza

- `assessorias_esportivas_fortaleza.csv`: 33 assessorias com modalidades, telefone/WhatsApp, e-mail, Instagram, site, endereço, bairro, locais de treino, latitude/longitude e link do Google Maps. Codificado em UTF-8 com BOM, então abre direto no Excel.
- `mapa.html`: mapa interativo autônomo, com Leaflet e os dados embutidos. Basta abrir no navegador. Tem busca, filtro por modalidade e um clique na lista leva até o pino.
- `COMO_RODAR.md` + `consultas_maps.txt`: passo a passo para rodar o scraper do Google Maps no seu computador e obter a lista completa com coordenadas exatas.
- `gerar_csv.py`: fonte dos dados. Edite a lista `D` e rode `python3 gerar_csv.py` para gerar de novo o CSV e o `mapa.html` (a partir de `mapa.template.html` + `vendor/`).

**Limitações:** os dados vêm de pesquisa web (Wellhub, sites oficiais, cadastros de CNPJ) feita em out/2026, porque o Google Maps não estava acessível no ambiente onde o scraper rodaria. As coordenadas são aproximadas, estimadas pelo endereço (nível de quadra ou bairro). Confirme telefones e e-mails antes de entrar em contato e siga a LGPD.

Leaflet 1.9.4 © Vladimir Agafonkin, licença BSD-2 (`vendor/LEAFLET-LICENSE`).
