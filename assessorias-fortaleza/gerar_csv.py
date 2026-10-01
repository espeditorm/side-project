"""Gera assessorias_esportivas_fortaleza.csv a partir dos dados levantados em pesquisa web (out/2026).

Coordenadas são aproximadas (nível de quadra/bairro), estimadas a partir do endereço,
porque a geocodificação automática não estava disponível no ambiente.
"""
import csv
from pathlib import Path
from urllib.parse import quote_plus

COLS = ["nome", "modalidades", "telefone_whatsapp", "email", "instagram", "site",
        "endereco", "bairro", "locais_de_treino", "latitude", "longitude",
        "link_google_maps", "fonte", "observacoes"]

D = [
    ("KM Assessoria Esportiva", "Corrida, natação, ciclismo", "(85) 98820-0826", "", "@kmassessoriaesportiva", "kmassessoriaesportiva.com",
     "R. Deputado Moreira da Rocha, 925 (CIAA) / R. João Cordeiro, 2095", "Meireles / Aldeota", "Beira Mar, Cocó, Iguatemi, Cambeba", -3.7310, -38.4920,
     "kmassessoriaesportiva.com; instagram", "Desde 2008; presencial e online"),
    ("AG Assessoria Esportiva", "Corrida, funcional", "(85) 98841-2772", "", "@agassessoriaesportiva", "",
     "Av. Beira Mar, 1680, CEP 60165-121", "Meireles", "Beira Mar (corrida); Praça da OAB (funcional)", -3.7238, -38.4975,
     "Wellhub; instagram", "Parceira Wellhub"),
    ("MR Assessoria Esportiva", "Corrida de rua", "(85) 99628-2046", "mrassessoria.ce@gmail.com", "", "mrassessoriaesportiva.com.br",
     "R. Gergelim", "Jangurussu", "", -3.8380, -38.5250, "mrassessoriaesportiva.com.br", ""),
    ("GT FIT Assessoria Esportiva (Gustavo Portela)", "Corrida, funcional", "(85) 99770-5727", "", "@gtfitconsultoria", "gtfit.com.br",
     "Av. Beira-Mar, 2200/2340 (em frente aos hotéis Ponta Mar / Bourbon)", "Meireles", "Beira Mar", -3.7246, -38.4925,
     "gtfit.com.br", "Fontes citam nº 2200 e 2340"),
    ("XSTEAM Run", "Corrida (equipe com nutrição, médico, fisioterapia)", "(85) 99611-5127", "", "", "xsteam.com.br",
     "Av. Beira Mar, 2001, esq. Av. Barão de Studart, CEP 60165-120", "Meireles / Praia de Iracema", "Beira Mar", -3.7240, -38.4950,
     "xsteam.com.br", "Presencial e online"),
    ("Limiar Assessoria / Consultoria Esportiva", "Corrida", "(85) 99104-4139", "", "", "soulimiar.com.br",
     "Av. Padre Antônio Tomás, 850, Loja 43/44, CEP 60140-160", "Aldeota", "Aterro da Beira Mar", -3.7430, -38.4930, "soulimiar.com.br", ""),
    ("Runners Assessoria Esportiva", "Corrida, natação, ciclismo, duathlon, triathlon", "(85) 99653-4883 / (85) 99706-8807", "", "", "runnersce.com.br",
     "", "Vários (5 núcleos)", "5 núcleos, incl. Maraponga (estac. Detran, ter/qui 19h)", -3.7900, -38.5650,
     "Facebook Runnersceara; runnersassessoriaesportiva.com.br", "Fundada em out/2014; +220 alunos. Coordenada = núcleo Maraponga"),
    ("Stark Assessoria Esportiva", "Corrida, ciclismo, natação, maratona", "(85) 99790-8536", "", "", "starkassessoriaesportiva.blogspot.com",
     "Av. Washington Soares, 909, CEP 60811-341", "Edson Queiroz", "Lago Jacarey, Iguatemi, Via Corpvs, Beira Mar, Cambeba, Unifor (natação)", -3.7600, -38.4850,
     "acmp-ce.org.br; econodata (CNPJ 56.637.186/0001-49)", "+20 anos, +1.800 alunos; novo CT no Guararapes (2026). Treinos seg-sáb a partir de 5h30"),
    ("For Time / Fortime Assessoria Esportiva", "Corrida, caminhada, funcional, kids", "(85) 98711-3397 / (85) 99998-0137 / (85) 3247-5800", "faleconosco@fortimeassessoria.com", "", "fortimeassessoria.com",
     "R. Des. Floriano Benevides Magalhães, 422", "Edson Queiroz", "Unifor (ter/qui 19h), Beira Mar (ter/qui 5h30), Iguatemi (seg/qua/sex 5h30), Caucaia, Longões (sáb), Praça da OAB", -3.7700, -38.4790,
     "fortimeassessoria.com/horarios", "Fundada em mar/2014"),
    ("Triativo Assessoria Esportiva", "Triathlon, corrida", "(85) 99927-0027", "", "", "",
     "R. Des. Floriano Benevides Magalhães, 422", "Edson Queiroz", "", -3.7700, -38.4790,
     "encontrafortaleza.com", "Mesmo endereço da For Time; registro CNPJ 'TFA Assessoria Esportiva / Tio Flavinho' na Av. Washington Soares, 3663"),
    ("RunTri Assessoria Esportiva", "Triathlon, natação, ciclismo, corrida, caminhada", "", "", "", "",
     "Av. Washington Soares, 85 (entrada principal, Centauro), CEP 60811-341", "Edson Queiroz (Iguatemi)", "Iguatemi; Centro Administrativo do Cambeba; Eusébio (Shopping Buena Vista)", -3.7550, -38.4890,
     "Wellhub; Facebook runtriassessoria", "Telefone não encontrado"),
    ("Zona Alvo Assessoria Esportiva (Rafael Pinho)", "Triathlon, ciclismo, corrida, duathlon", "", "", "", "zonaalvoassessoria.com",
     "Av. Padre Antônio Tomás, 850, loja 33, CEP 60140-160", "Aldeota", "", -3.7430, -38.4930, "TrainingPeaks", "Treinador desde 2004"),
    ("Unimed Ativa", "Corrida, caminhada", "(85) 4020-2111 (central Unimed)", "", "@unimedativaoficial", "unimedfortaleza.com.br/unimed-ativa",
     "Aterro da Beira Mar, em frente ao Ideal Clube", "Meireles", "Beira Mar (seg/qua/sex 6h e 18h30)", -3.7240, -38.5040,
     "unimedfortaleza.com.br", "Exclusiva para clientes Unimed; R$ 40-60"),
    ("JS Team Assessoria Esportiva", "Atividades ao ar livre", "", "", "", "",
     "Av. Beira Mar, 4050, CEP 60165-121", "Mucuripe", "", -3.7258, -38.4830, "Wellhub", "Parceira Wellhub"),
    ("BE Assessoria Esportiva", "Treinamento / qualidade de vida", "", "", "", "",
     "Av. Historiador Raimundo Girão, 800", "Praia de Iracema", "", -3.7220, -38.5100, "Wellhub", "Parceira Wellhub"),
    ("Ricardo Lima Assessoria Esportiva", "Funcional ao ar livre", "", "", "", "",
     "Av. Rui Barbosa, 1680, CEP 60115-221 (também Av. Des. Moreira, 1500; Av. Santos Dumont, 485; R. Joãozito Arruda - Parque Iracema)", "Aldeota", "Aldeota, Centro, Parque Iracema", -3.7375, -38.5010,
     "Wellhub", "Várias unidades"),
    ("Renato Ribeiro Assessoria Esportiva", "Funcional, corrida", "", "", "", "",
     "Av. Beira Mar (Praia Mansa, em frente ao Bourbon), CEP 60165-120", "Meireles", "Praia Mansa", -3.7246, -38.4925, "Wellhub", "Parceira Wellhub"),
    ("TP Costa Assessoria Esportiva", "Treinamento", "", "", "", "",
     "Av. Gen. Afonso Albuquerque Lima, 769, CEP 60822-325", "Cambeba", "", -3.8090, -38.4880, "Wellhub", "Parceira Wellhub"),
    ("Diogo Porto Assessoria Esportiva", "", "", "", "", "",
     "R. Dr. Gilberto Studart, 331", "Cocó", "", -3.7470, -38.4850, "busca web", "Contato não encontrado"),
    ("Corra Assessoria", "Corrida", "", "", "", "",
     "Av. das Flamboyants, 420", "Cocó", "", -3.7500, -38.4800, "Wellhub", "Endereço/bairro a confirmar"),
    ("Tiron Assessoria (Julyana Ferro - CREF 6364-G)", "Caminhada, corrida, funcional", "", "", "", "",
     "", "", "", "", "", "Facebook tironassessoria", "Endereço não encontrado"),
    ("A M Assessoria Esportiva", "", "(85) 3269-0116 / (85) 98918-3045", "", "", "",
     "", "", "", "", "", "cnpj.biz (CNPJ 18.142.048/0001-08)", "Ativa; e-mail existe no cadastro mas veio ofuscado"),
    ("Get Up Assessoria Esportiva", "Condicionamento físico", "(85) 98804-9673", "", "", "",
     "", "", "", "", "", "cnpj.biz (CNPJ 20.365.560/0001-57)", "E-mail existe no cadastro mas veio ofuscado"),
    ("REDES Assessoria e Consultoria Esportiva", "", "(85) 8721-7544", "", "", "",
     "Av. Senador Virgílio Távora, 318, Sala 106, CEP 60170-250", "Meireles", "", -3.7300, -38.4980, "guiapj.com.br (CNPJ 09.504.288/0001-06)", "Telefone antigo, verificar"),
    ("B6 Assessoria Esportiva", "", "", "", "", "",
     "Av. Alanis Maria Laurindo de Oliveira, 460, CEP 60533-604", "Conjunto Ceará I", "", -3.7690, -38.6050, "solutudo (CNPJ 28.084.897/0001-06)", ""),
    ("Mascarenhas Assessoria Esportiva", "Natação", "", "", "", "",
     "Av. Humberto Monte, 2929, Sala 602", "Pici", "", -3.7450, -38.5770, "solutudo", ""),
    ("TM Assessoria Esportiva & Treinamento Personalizado", "Natação / personal", "", "", "", "",
     "", "", "", "", "", "solutudo", "Endereço não encontrado"),
    ("North Shopping Jóquei - assessoria gratuita", "Corrida, caminhada", "", "", "", "",
     "North Shopping Jóquei", "Jóquei Clube", "", -3.7660, -38.5600, "O Povo (set/2026)", "Iniciativa do shopping, gratuita"),
]

out = Path(__file__).with_name("assessorias_esportivas_fortaleza.csv")
with out.open("w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(COLS)
    for (nome, mod, tel, email, ig, site, end, bairro, locais, lat, lon, fonte, obs) in D:
        q = f"{nome.split(' (')[0]} {end} {bairro} Fortaleza CE".replace("  ", " ")
        link = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)
        w.writerow([nome, mod, tel, email, ig, site, end, bairro, locais, lat, lon, link, fonte, obs])
print(f"{len(D)} linhas -> {out}")

# --- Mapa: embute Leaflet (vendor/) e os dados no template, gerando um HTML autônomo ---
import json
base = Path(__file__).parent
with out.open(encoding="utf-8-sig") as f:
    linhas = list(csv.DictReader(f))
html = (base / "mapa.template.html").read_text(encoding="utf-8")
html = (html.replace("/*LEAFLET_CSS*/", (base / "vendor/leaflet.css").read_text(encoding="utf-8"))
            .replace("/*LEAFLET_JS*/", (base / "vendor/leaflet.js").read_text(encoding="utf-8"))
            .replace("/*DADOS*/", json.dumps(linhas, ensure_ascii=False)))
(base / "mapa.html").write_text('<!doctype html>\n<html lang="pt-BR">\n' + html + "\n</html>\n", encoding="utf-8")
print(f"mapa.html gerado ({len(linhas)} assessorias)")
