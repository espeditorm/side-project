# Como rodar o scraper do Google Maps no seu computador

O ambiente na nuvem onde este levantamento foi feito não consegue acessar o Google, por isso o scraper
([google-maps-scraper-kit](https://github.com/Mahanaicoach/google-maps-scraper-kit)) precisa rodar na sua máquina.
Leva uns 10 minutos.

## 1. Instale o Docker Desktop
https://www.docker.com/products/docker-desktop. Abra o programa e espere ele ficar "running".
No Windows, rode os comandos abaixo no PowerShell; no Mac/Linux, no Terminal.

## 2. Baixe o kit e ligue o scraper
```bash
git clone https://github.com/Mahanaicoach/google-maps-scraper-kit
cd google-maps-scraper-kit
docker compose up -d
```
Teste: abra http://localhost:8080 no navegador. Se abrir uma página, está funcionando.
(Mac M1/M2/M3: se não subir, descomente a linha `platform: linux/amd64` no `docker-compose.yml`.)

## 3. Rode a busca de Fortaleza
Copie o arquivo `consultas_maps.txt` desta pasta para dentro de `google-maps-scraper-kit/` e rode:
```bash
python3 scripts/scrape.py --keywords-file consultas_maps.txt -3.7319 -38.5267 --depth 10 --max-time 1800 --fields title,phone,emails,website,category,address,latitude,longitude,link,review_rating,review_count --out assessorias_maps.csv
```
(No Windows use `py` no lugar de `python3`.)

- `-3.7319 -38.5267` é o centro de Fortaleza; as buscas por bairro cobrem o resto da cidade.
- A extração de e-mail já vem ligada (o scraper visita o site de cada empresa). Isso deixa a busca mais lenta, de 15 a 30 minutos.
- O resultado sai em `assessorias_maps.csv`, com nome, telefone, e-mail, site, endereço e latitude/longitude.

## 4. Mais fácil: use o Claude Code
Dentro da pasta `google-maps-scraper-kit`, rode `claude` e peça:
> "Rode as buscas do arquivo consultas_maps.txt em Fortaleza, CE, com e-mails, e junte com assessorias_esportivas_fortaleza.csv."

O kit já traz as instruções para o Claude operar o scraper.

## Cuidados
- Rode uma busca por vez. Muitas buscas seguidas podem fazer o Google bloquear seu IP por algumas horas (sua conta não é afetada).
- Telefones e e-mails são dados pessoais: use para contato comercial legítimo e siga a LGPD.
- Para desligar: `docker compose stop`.
