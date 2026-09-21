import pymupdf as fitz, os, sys
pdf, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
doc = fitz.open(pdf)
k = 72 / 110  # coordinates below were measured on a 110-dpi render
crops = {
    "fig00-cabecalho-capa":        (1,  (130, 100, 800, 320)),
    "fig01-forward-topologia":     (2,  (170, 495, 720, 808)),
    "fig02-forward-formas-onda":   (3,  (100, 205, 770, 1135)),
    "fig03a-forward-etapa1":       (4,  (180, 185, 760, 522)),
    "fig03b-forward-etapa2":       (4,  (180, 527, 760, 862)),
    "fig03c-forward-etapa3":       (4,  (180, 870, 760, 1212)),
    "fig04a-forward-psim-isolado": (7,  (100, 130, 785, 470)),
    "fig04b-forward-psim-buck-eq": (7,  (190, 510, 730, 848)),
    "fig05a-forward-degrau-20-100":(7,  (225, 925, 775, 1200)),
    "fig05b-forward-degrau-100-20":(8,  (220, 75, 775, 355)),
    "fig06-fullbridge-topologia":  (9,  (70, 430, 625, 660)),
    "fig07-fullbridge-formas-onda":(10, (100, 155, 665, 880)),
    "fig08a-fullbridge-psim-isolado":(13,(110, 105, 775, 505)),
    "fig08b-fullbridge-psim-buck-eq":(13,(75, 565, 690, 840)),
    "fig09a-fullbridge-degrau-20-100":(14,(185, 195, 795, 500)),
    "fig09b-fullbridge-degrau-100-20":(14,(185, 585, 795, 888)),
    "fig10-pushpull-topologia":    (15, (100, 110, 615, 378)),
    "fig11-pushpull-formas-onda":  (15, (100, 505, 675, 1212)),
    "fig13a-pushpull-psim-isolado":(18, (85, 450, 795, 785)),
    "fig13b-pushpull-psim-boost-eq":(18,(180, 870, 705, 1170)),
    "fig14a-pushpull-degrau-20-100":(19,(130, 112, 830, 462)),
    "fig14b-pushpull-degrau-100-20":(19,(130, 522, 830, 882)),
    "fig15-flyback-topologia":     (20, (175, 452, 565, 748)),
    "fig16-flyback-formas-onda":   (21, (125, 195, 775, 1155)),
    "fig17a-flyback-etapa1":       (22, (290, 215, 630, 532)),
    "fig17b-flyback-etapa2":       (22, (270, 540, 660, 892)),
    "fig17c-flyback-etapa3":       (22, (270, 905, 660, 1212)),
    "fig18a-flyback-mcd-psim-isolado":(24,(100, 800, 785, 1105)),
    "fig18b-flyback-mcd-psim-buckboost-eq":(25,(130, 70, 795, 385)),
    "fig19a-flyback-mcd-degrau-20-100":(25,(100, 530, 695, 822)),
    "fig19b-flyback-mcd-degrau-100-20":(25,(135, 870, 695, 1145)),
    "fig20a-flyback-mcc-psim-isolado":(26,(95, 275, 745, 562)),
    "fig20b-flyback-mcc-psim-buckboost-eq":(26,(100, 660, 765, 980)),
    "fig21a-flyback-mcc-degrau-20-100":(27,(150, 140, 750, 455)),
    "fig21b-flyback-mcc-degrau-100-20":(27,(150, 512, 750, 818)),
}
for name, (pg, (x0, y0, x1, y1)) in crops.items():
    page = doc[pg - 1]
    clip = fitz.Rect(x0 * k, y0 * k, x1 * k, y1 * k)
    page.get_pixmap(dpi=220, clip=clip).save(os.path.join(out, name + ".png"))
    print(name)

