# Métricas dos ensaios PLECS

Fonte: CSVs com hash conferido contra o registro `_execucao.json`; janelas em número inteiro de ciclos de 60 Hz.
Gerado por `analisar_resultados.py`. Valores de classe S; as comparações com A vêm de `parametros.json`.

## Curvas de regulação

| Rede | Po nominal (W) | Po medida (W) | Vo eficaz (V) | DHT (%) | M efetivo |
|---|---|---|---|---|---|
| 176 | 0 | 0.0 | 114.755 | 0.15 | 0.699 |
| 176 | 210 | 209.1 | 114.758 | 0.15 | 0.705 |
| 176 | 420 | 418.3 | 114.762 | 0.15 | 0.708 |
| 176 | 630 | 627.4 | 114.767 | 0.16 | 0.712 |
| 176 | 840 | 836.7 | 114.771 | 0.17 | 0.715 |
| 176 | 1050 | 1045.9 | 114.776 | 0.18 | 0.718 |
| 176 | 1260 | 1255.2 | 114.781 | 0.20 | 0.722 |
| 176 | 1470 | 1464.5 | 114.785 | 0.21 | 0.725 |
| 176 | 1680 | 1673.9 | 114.790 | 0.22 | 0.728 |
| 176 | 1890 | 1883.3 | 114.795 | 0.24 | 0.731 |
| 176 | 2100 | 2092.7 | 114.800 | 0.25 | 0.734 |
| 220 | 0 | 0.0 | 114.812 | 0.14 | 0.570 |
| 220 | 210 | 209.3 | 114.815 | 0.14 | 0.574 |
| 220 | 420 | 418.7 | 114.818 | 0.14 | 0.577 |
| 220 | 630 | 628.0 | 114.821 | 0.15 | 0.579 |
| 220 | 840 | 837.4 | 114.824 | 0.15 | 0.582 |
| 220 | 1050 | 1046.9 | 114.828 | 0.16 | 0.584 |
| 220 | 1260 | 1256.3 | 114.831 | 0.16 | 0.586 |
| 220 | 1470 | 1465.8 | 114.835 | 0.16 | 0.589 |
| 220 | 1680 | 1675.3 | 114.838 | 0.17 | 0.591 |
| 220 | 1890 | 1884.8 | 114.842 | 0.18 | 0.593 |
| 220 | 2100 | 2094.4 | 114.846 | 0.18 | 0.596 |
| 264 | 0 | 0.0 | 114.850 | 0.13 | 0.479 |
| 264 | 210 | 209.5 | 114.852 | 0.13 | 0.481 |
| 264 | 420 | 418.9 | 114.854 | 0.13 | 0.484 |
| 264 | 630 | 628.4 | 114.857 | 0.14 | 0.485 |
| 264 | 840 | 837.9 | 114.860 | 0.14 | 0.487 |
| 264 | 1050 | 1047.5 | 114.862 | 0.14 | 0.489 |
| 264 | 1260 | 1257.0 | 114.865 | 0.14 | 0.491 |
| 264 | 1470 | 1466.6 | 114.868 | 0.14 | 0.493 |
| 264 | 1680 | 1676.2 | 114.870 | 0.15 | 0.495 |
| 264 | 1890 | 1885.8 | 114.873 | 0.15 | 0.497 |
| 264 | 2100 | 2095.5 | 114.876 | 0.15 | 0.498 |
| bat | 0 | 0.0 | 114.780 | 0.14 | 0.684 |
| bat | 210 | 208.9 | 114.704 | 0.14 | 0.813 |
| bat | 420 | 417.8 | 114.704 | 0.15 | 0.823 |
| bat | 630 | 626.8 | 114.704 | 0.16 | 0.830 |
| bat | 840 | 835.7 | 114.703 | 0.18 | 0.836 |
| bat | 1050 | 1044.6 | 114.702 | 0.19 | 0.842 |
| bat | 1260 | 1253.4 | 114.700 | 0.20 | 0.848 |
| bat | 1470 | 1462.3 | 114.699 | 0.22 | 0.854 |
| bat | 1680 | 1671.2 | 114.697 | 0.23 | 0.860 |
| bat | 1890 | 1880.0 | 114.695 | 0.25 | 0.866 |
| bat | 2100 | 2088.8 | 114.693 | 0.27 | 0.873 |

- RV em 176: -0.039%
- RV em 220: -0.029%
- RV em 264: -0.022%
- RV em bat: 0.077%

## diag_cc_sem_5ms

```json
{
 "modelo": "elevador_sem_amortecedor",
 "status": "executado",
 "duracao_real_s": 0.163,
 "erro": null,
 "descricao": "Diagnostico do CC-CC (sem amortecedores RC), 5 ms, corrente inicial em Lb de 53.6 A",
 "janela_s": [
  0.004,
  0.005
 ],
 "v_bus_media_V": 200.90865482200002,
 "v_C8_media_V": 134.829499219,
 "v_C7_media_V": 66.07915560485,
 "i_bat_media_A": 48.2077181696,
 "i_D17_min_A": 0.0,
 "i_sec_pico_A": 31.8538146
}
```

## diag_cc_sem_20ms

```json
{
 "modelo": "elevador_sem_amortecedor",
 "status": "falhou",
 "duracao_real_s": 90.059,
 "erro": "<Fault -34000: \"Simulation error: Simulation exceeded maximum runtime of 90 seconds. This limit is specified by the circuit parameter 'Timeout'. To disable the limit, set the value to 0.\">",
 "descricao": "Diagnostico do CC-CC (sem amortecedores RC), 20 ms, corrente inicial em Lb de 53.6 A"
}
```

## diag_cc_sem_partida_5ms

```json
{
 "modelo": "elevador_sem_amortecedor",
 "status": "executado",
 "duracao_real_s": 0.206,
 "erro": null,
 "descricao": "Diagnostico do CC-CC (sem amortecedores RC), 5 ms, corrente inicial em Lb de 0.0 A",
 "janela_s": [
  0.004,
  0.005
 ],
 "v_bus_media_V": 201.0193721805,
 "v_C8_media_V": 134.96537051849998,
 "v_C7_media_V": 66.0540016627,
 "i_bat_media_A": 62.191372297550004,
 "i_D17_min_A": 0.0,
 "i_sec_pico_A": 38.11318448
}
```

## diag_cc_amort_20ms

```json
{
 "modelo": "elevador_bateria",
 "status": "executado",
 "duracao_real_s": 2.752,
 "erro": null,
 "descricao": "Diagnostico do CC-CC (com amortecedores RC), 20 ms, corrente inicial em Lb de 53.6 A",
 "janela_s": [
  0.019,
  0.02
 ],
 "v_bus_media_V": 202.937564385,
 "v_C8_media_V": 136.194113424,
 "v_C7_media_V": 66.74345096725,
 "i_bat_media_A": 50.94035321735001,
 "i_D17_min_A": 0.0,
 "i_sec_pico_A": 30.34995044
}
```

## diag_cc_amort_partida_5ms

```json
{
 "modelo": "elevador_bateria",
 "status": "executado",
 "duracao_real_s": 0.634,
 "erro": null,
 "descricao": "Diagnostico do CC-CC (com amortecedores RC), 5 ms, corrente inicial em Lb de 0.0 A",
 "janela_s": [
  0.004,
  0.005
 ],
 "v_bus_media_V": 201.01698065649998,
 "v_C8_media_V": 134.96958892249995,
 "v_C7_media_V": 66.04739173295002,
 "i_bat_media_A": 62.335742798050006,
 "i_D17_min_A": 0.0,
 "i_sec_pico_A": 38.20101007
}
```

## ret_176_planilha

```json
{
 "execucao": "ret_176_planilha_execucao.json",
 "sha256_csv": "efc4e9b71bbfa620c9ac586faa2d65c1052c7060c97d8032be8d91710a229fbb",
 "sha256_modelo": "892930d0d87602888a0bcb71fbc9cb73239d8aee33f13a51a03f5a2242a07b04",
 "amostras": 19001,
 "descricao": "Retificador ideal da secao 3 a 176 V, carga equivalente a 2250 W",
 "janela_s": [
  0.1,
  0.15
 ],
 "v_bus_media_V": 231.276209358956,
 "v_bus_min_V": 212.0180453,
 "v_bus_max_V": 248.8780526,
 "ondulacao_bus_Vpp": 36.86000729999998,
 "i_D1_pico_A": 96.01532826,
 "i_D1_media_A": 4.907038259422506,
 "i_D1_ef_A": 17.98417564883319,
 "i_C4_ef_A": 23.4609957790104,
 "i_rede_ef_A": 25.435876207794653,
 "duracao_pulso_ms": 1.615333333333325,
 "P_entrada_W": 2276.731874046047,
 "P_barramento_W": 2275.3078627098967,
 "FP_entrada": 0.5085721126120172,
 "comparacao_A": {
  "Ichg_A": 55.3406476,
  "ID1pk_2Ichg_A": 110.6812952,
  "ID1med_A": 4.886278131,
  "ID1ef_A": 16.4441417,
  "IC1ef_A": 21.10252915,
  "VC1min_V": 211.571587,
  "tC1_ms": 1.471576001
 }
}
```

## ret_176_anexo

```json
{
 "execucao": "ret_176_anexo_execucao.json",
 "sha256_csv": "dc9f8540a55f84e5542521c7e99ed035ff8e7626a3e4438ba28de2f64c072f53",
 "sha256_modelo": "892930d0d87602888a0bcb71fbc9cb73239d8aee33f13a51a03f5a2242a07b04",
 "amostras": 19001,
 "descricao": "Retificador com 1880 uF, ESR, 0,1 ohm e diodos reais a 176 V, carga equivalente a 2250 W",
 "janela_s": [
  0.1,
  0.15
 ],
 "v_bus_media_V": 227.99158610766403,
 "v_bus_min_V": 210.6651675,
 "v_bus_max_V": 244.4525016,
 "ondulacao_bus_Vpp": 33.78733410000001,
 "i_D1_pico_A": 66.27642357,
 "i_D1_media_A": 4.838670047901173,
 "i_D1_ef_A": 15.816744511309512,
 "i_C4_ef_A": 20.119206084805477,
 "i_rede_ef_A": 22.36825408915374,
 "duracao_pulso_ms": 1.9193333333333331,
 "P_entrada_W": 2307.5377001903453,
 "P_barramento_W": 2231.012681704981,
 "FP_entrada": 0.5861436641416952,
 "comparacao_A": {
  "Ichg_A": 55.3406476,
  "ID1pk_2Ichg_A": 110.6812952,
  "ID1med_A": 4.886278131,
  "ID1ef_A": 16.4441417,
  "IC1ef_A": 21.10252915,
  "VC1min_V": 211.571587,
  "tC1_ms": 1.471576001
 }
}
```

## ret_264_anexo

```json
{
 "execucao": "ret_264_anexo_execucao.json",
 "sha256_csv": "9186ec3f68df289a71a759e16298508b2d46040ee90b9ef320ceb690f8bcd5e3",
 "sha256_modelo": "892930d0d87602888a0bcb71fbc9cb73239d8aee33f13a51a03f5a2242a07b04",
 "amostras": 19001,
 "descricao": "Retificador com 1880 uF, ESR, 0,1 ohm e diodos reais a 264 V, carga equivalente a 2250 W",
 "janela_s": [
  0.1,
  0.15
 ],
 "v_bus_media_V": 357.29636813816,
 "v_bus_min_V": 345.4214323,
 "v_bus_max_V": 368.8412604,
 "ondulacao_bus_Vpp": 23.419828100000018,
 "i_D1_pico_A": 58.4133238,
 "i_D1_media_A": 3.081908056083972,
 "i_D1_ef_A": 11.904543653274947,
 "i_C4_ef_A": 15.652678744042495,
 "i_rede_ef_A": 16.835567296379814,
 "duracao_pulso_ms": 1.3633333333333368,
 "P_entrada_W": 2259.840841526261,
 "P_barramento_W": 2215.3994566885985,
 "FP_entrada": 0.5084475935993424,
 "comparacao_A": {
  "Ichg_A": 55.3406476,
  "ID1pk_2Ichg_A": 110.6812952,
  "ID1med_A": 4.886278131,
  "ID1ef_A": 16.4441417,
  "IC1ef_A": 21.10252915,
  "VC1min_V": 211.571587,
  "tC1_ms": 1.471576001
 }
}
```

## elev_42

```json
{
 "execucao": "elev_42_execucao.json",
 "sha256_csv": "cd77a64e3c605dd38dc95300fd8b455f87f04af04b3048ec73a22d055dbc93f0",
 "sha256_modelo": "2a15b66b24f54a4185423528ca23ff2279b7828b7e14ed8de5326391aa6ee32e",
 "amostras": 17801,
 "descricao": "CC-CC em malha aberta, bateria de 42 V, D = 0.70, carga de 2250 W em 210 V",
 "janela_s": [
  0.08,
  0.1
 ],
 "v_bus_media_V": 202.90540857141127,
 "v_bus_pp_V": 1.0385262000000068,
 "v_C8_media_V": 136.1901131407131,
 "v_C7_media_V": 66.71529542920905,
 "i_bat_media_A": 51.12613908635105,
 "i_bat_ef_A": 51.24415135993362,
 "i_bat_pico_A": 56.37525301,
 "dILb_pp_A": 10.509092800000005,
 "v_S1_max_V": 142.0281785,
 "i_S1_ef_A": 24.857621200373284,
 "i_S1_pico_A": 40.2006179,
 "i_S2_ef_A": 24.84235040497706,
 "i_D17_ef_A": 10.34835519427511,
 "i_D17_media_A": 5.1243255571288895,
 "i_sec_ef_A": 16.55661905514434,
 "D_medida": 0.7023749999999975,
 "P_bateria_W": 2147.2978416267442,
 "P_carga_W": 2100.551072852493,
 "rendimento_modelo": 0.9782299558691694,
 "comparacao_A": {
  "Vbus_V": 210.0,
  "VC8_V": 140.0,
  "VC7_V": 70.0,
  "Iib_A": 53.57142857,
  "dILb_pp_A": 10.71428571,
  "V_chave_V": 140.0,
  "D": 0.7
 }
}
```

## elev_56

```json
{
 "execucao": "elev_56_execucao.json",
 "sha256_csv": "abe9a55822f1cfa7ab67663b2220a37f9a80c608032a79ab21665ae47bc355c5",
 "sha256_modelo": "2a15b66b24f54a4185423528ca23ff2279b7828b7e14ed8de5326391aa6ee32e",
 "amostras": 17801,
 "descricao": "CC-CC em malha aberta, bateria de 56 V, D = 0.60, carga de 2250 W em 210 V",
 "janela_s": [
  0.08,
  0.1
 ],
 "v_bus_media_V": 205.9375992875944,
 "v_bus_pp_V": 0.8010045000000048,
 "v_C8_media_V": 137.7814359269131,
 "v_C7_media_V": 68.15616336010575,
 "i_bat_media_A": 39.330872481077186,
 "i_bat_ef_A": 39.409122849882046,
 "i_bat_pico_A": 42.87217882,
 "dILb_pp_A": 7.026003240000001,
 "v_S1_max_V": 142.7866784,
 "i_S1_ef_A": 18.984994493218117,
 "i_S1_pico_A": 31.65084757,
 "i_S2_ef_A": 18.954874251902837,
 "i_D17_ef_A": 9.055256009659505,
 "i_D17_media_A": 5.2126088320625605,
 "i_sec_ef_A": 14.620484228637434,
 "D_medida": 0.602625000000002,
 "P_bateria_W": 2202.5288589403226,
 "P_carga_W": 2163.7945304379396,
 "rendimento_modelo": 0.9824137021655104,
 "comparacao_A": {
  "Vbus_V": 210.0,
  "VC8_V": 140.0,
  "VC7_V": 70.0,
  "Iib_A": 40.17857143,
  "dILb_pp_A": 7.142857143,
  "V_chave_V": 140.0,
  "D": 0.6
 }
}
```

## inv_373_res

```json
{
 "execucao": "inv_373_res_execucao.json",
 "sha256_csv": "b4a6d3b413117aaca4d8a3d8deb436ae376a89907bda03ac9b81529bcaa19153",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 17801,
 "descricao": "Inversor com barramento ideal de 373.35 V, 2100 W resistiva",
 "janela_s": [
  0.05,
  0.1
 ],
 "Vo_ef_V": 114.87397182757756,
 "Vo1_ef_V": 114.87369673290297,
 "DHT_vo_pct": 0.13257758108872197,
 "Io_ef_A": 18.24085766818469,
 "Io_pico_A": 25.81519505,
 "Po_W": 2095.3997698859007,
 "vc_pico_V": 2.453737851,
 "vc_livre_pico_V": 2.453737851,
 "I_QA_ef_A": 11.950410673264189,
 "I_QA_pico_A": 29.13738661,
 "I_Lo_pico_A": 29.13738661,
 "M_efetivo": 0.49074757020000004,
 "fator_crista": 1.4152401997536719,
 "So_VA": 2095.3997698859002,
 "dILo_pp_no_pico_A": 6.282111329999999,
 "vAB_niveis_V": [
  -0.0,
  370.0
 ],
 "comparacao_A": {
  "M_pico": 0.43560661252651656,
  "dILo_max_A": 6.276665742
 }
}
```

## inv_2116_res

```json
{
 "execucao": "inv_2116_res_execucao.json",
 "sha256_csv": "8a911233e6c6d5f3449b45d3ac8412f2ef41702e7bd845c2318506a87205fd1b",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 17801,
 "descricao": "Inversor com barramento ideal de 211.57 V, 2100 W resistiva",
 "janela_s": [
  0.05,
  0.1
 ],
 "Vo_ef_V": 114.75163414849632,
 "Vo1_ef_V": 114.75138677673934,
 "DHT_vo_pct": 0.13155971513873732,
 "Io_ef_A": 18.22143164731144,
 "Io_pico_A": 25.78109349,
 "Po_W": 2090.939058054115,
 "vc_pico_V": 4.065021905,
 "vc_livre_pico_V": 4.065021905,
 "I_QA_ef_A": 13.55063914346733,
 "I_QA_pico_A": 27.29319504,
 "I_Lo_pico_A": 27.29319504,
 "M_efetivo": 0.813004381,
 "fator_crista": 1.414877490913508,
 "So_VA": 2090.9390580541153,
 "dILo_pp_no_pico_A": 2.960192920000001,
 "vAB_niveis_V": [
  -0.0,
  210.0
 ],
 "comparacao_A": {
  "M_pico": 0.7686976891038306,
  "dILo_max_A": 3.616855631
 }
}
```

## inv_373_vazio

```json
{
 "execucao": "inv_373_vazio_execucao.json",
 "sha256_csv": "5b53e6d3a3a6eb57635ed3eeab996ba77244d678278727642f9ff21a865d6102",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 17801,
 "descricao": "Inversor com barramento ideal de 373.35 V, vazio",
 "janela_s": [
  0.05,
  0.1
 ],
 "Vo_ef_V": 114.85045534669176,
 "Vo1_ef_V": 114.8501854912541,
 "DHT_vo_pct": 0.12947400719260865,
 "Io_ef_A": 0.0,
 "Io_pico_A": 0.0,
 "Po_W": 0.0,
 "vc_pico_V": 2.412693586,
 "vc_livre_pico_V": 2.412693586,
 "I_QA_ef_A": 2.0220483358569257,
 "I_QA_pico_A": 5.306177478,
 "I_Lo_pico_A": 5.306177478,
 "M_efetivo": 0.4825387172,
 "fator_crista": null,
 "So_VA": 0.0,
 "dILo_pp_no_pico_A": 6.255490683,
 "vAB_niveis_V": [
  -0.0,
  370.0
 ],
 "comparacao_A": {
  "M_pico": 0.43560661252651656,
  "dILo_max_A": 6.276665742
 }
}
```

## inv_2116_vazio

```json
{
 "execucao": "inv_2116_vazio_execucao.json",
 "sha256_csv": "e976891ecebbf331872b83a8060bb331f3fa8682d4f2e79e95a3192d936d161f",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 17801,
 "descricao": "Inversor com barramento ideal de 211.57 V, vazio",
 "janela_s": [
  0.05,
  0.1
 ],
 "Vo_ef_V": 114.7071989628088,
 "Vo1_ef_V": 114.70695335824064,
 "DHT_vo_pct": 0.1302691637614818,
 "Io_ef_A": 0.0,
 "Io_pico_A": 0.0,
 "Po_W": 0.0,
 "vc_pico_V": 4.005930378,
 "vc_livre_pico_V": 4.005930378,
 "I_QA_ef_A": 1.880836818944105,
 "I_QA_pico_A": 4.703119148,
 "I_Lo_pico_A": 4.721112226,
 "M_efetivo": 0.8011860756000001,
 "fator_crista": null,
 "So_VA": 0.0,
 "dILo_pp_no_pico_A": 2.96819186815,
 "vAB_niveis_V": [
  -0.0,
  210.0
 ],
 "comparacao_A": {
  "M_pico": 0.7686976891038306,
  "dILo_max_A": 3.616855631
 }
}
```

## inv_2116_nl

```json
{
 "execucao": "inv_2116_nl_execucao.json",
 "sha256_csv": "5e18588e8a8968125a6131eee7ab0eeadd64775ddec6d3da42198a22e1fc987a",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 17801,
 "descricao": "Inversor com barramento ideal de 211.57 V, carga nao linear do Anexo 01",
 "janela_s": [
  0.05,
  0.1
 ],
 "Vo_ef_V": 114.77602088999774,
 "Vo1_ef_V": 114.76776384948916,
 "DHT_vo_pct": 1.1853257421058427,
 "Io_ef_A": 27.69160708419927,
 "Io_pico_A": 76.26762575,
 "Po_W": 2142.0610342470663,
 "vc_pico_V": 4.327811524,
 "vc_livre_pico_V": 4.327811524,
 "I_QA_ef_A": 21.78939760378729,
 "I_QA_pico_A": 79.10569386,
 "I_Lo_pico_A": 79.10569386,
 "M_efetivo": 0.8655623048000001,
 "fator_crista": 2.7541783876284316,
 "So_VA": 3178.3324731736648,
 "dILo_pp_no_pico_A": 3.6483043367,
 "vAB_niveis_V": [
  -10.0,
  -0.0,
  200.0,
  210.0
 ],
 "comparacao_A": {
  "M_pico": 0.7686976891038306,
  "dILo_max_A": 3.616855631
 }
}
```

## inv_degrau_2116

```json
{
 "execucao": "inv_degrau_2116_execucao.json",
 "sha256_csv": "917819ede8df1ed0c4536f89d1cc815995624ac80b2c130defedae8556cfd12f",
 "sha256_modelo": "2ed9250a0a8f328a305258e5dcfc3a5d64269835ba029a371b9fafb3293e01ec",
 "amostras": 15002,
 "descricao": "Inversor a 211,57 V, degrau de vazio para 2100 W no pico da tensao",
 "janela_s": [
  0.06666666666666668,
  0.1
 ],
 "Vo_ef_V": 114.75160317346759,
 "Vo1_ef_V": 114.75702816809729,
 "DHT_vo_pct": 0.13745486158743803,
 "Io_ef_A": 18.221426728492315,
 "Io_pico_A": 25.78104653,
 "Po_W": 2090.93792988108,
 "vc_pico_V": 4.063051321,
 "vc_livre_pico_V": 4.063051321,
 "I_QA_ef_A": 13.663510546192176,
 "I_QA_pico_A": 27.02694174,
 "I_Lo_pico_A": 27.02694174,
 "M_efetivo": 0.8126102641999999,
 "fator_crista": 1.4148752956697364,
 "So_VA": 2090.937929202366,
 "degrau": {
  "erro_min_V": -25.357951802222374,
  "erro_max_V": 7.373433985779343,
  "Vo_ef_antes_V": 114.70718005656428,
  "Vo_ef_depois_V": 114.75160317346759
 },
 "comparacao_A": {
  "M_pico": 0.7686976891038306,
  "dILo_max_A": 3.616855631
 }
}
```

## nb_176_nl

```json
{
 "execucao": "nb_176_nl_execucao.json",
 "sha256_csv": "5ea5df6c26bbf860b297ca6100db01dba069e900892c771fe1728bfc60e24b9a",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 176 V com carga nao linear do Anexo 01; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 176.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 247.3016,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 164.8677,
  "VC7_0": 82.4339,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00004510629785,
   "Iin_ef_A": 24.62355235407405,
   "Iin_pico_A": 82.81340448,
   "Pin_W": 2400.738324655968,
   "FP": 0.5539637405193796,
   "DHT_iin_pct": 146.05418125487753
  },
  "b_barramento": {
   "Vbus_media_V": 240.84085521656706,
   "Vbus_min_V": 223.7547621,
   "Vbus_max_V": 243.8740003,
   "Vbus_pp_V": 20.119238200000012,
   "Ibat_media_A": 3.3367047718413526e-18,
   "Ibat_ef_A": 2.110151387745838e-16,
   "Ibat_pico_A": 1.736671593e-15,
   "Pbat_W": 1.401416004173368e-16,
   "VC8_media_V": 161.63732760815023,
   "VC7_media_V": 79.20352760839822
  },
  "c_saida": {
   "Vo_ef_V": 114.81978007440368,
   "Vo1_ef_V": 114.81271108898214,
   "DHT_vo_pct": 1.0400870397672382,
   "Io_ef_A": 27.56909191457791,
   "Io_pico_A": 73.214664,
   "fator_crista": 2.6556792014352038,
   "Po_W": 2143.4991196409796,
   "So_VA": 3165.4770704828566,
   "M_efetivo": 0.7802709057999999,
   "vc_livre_pico_V": 3.901354529,
   "I_QA_ef_A": 21.48244700562565,
   "I_Lo_pico_A": 76.21154812,
   "FP_carga": 0.677148837888759
  },
  "diodo_D1": {
   "pico_A": 82.81340448,
   "media_A": 4.889887398536084,
   "ef_A": 17.27174820170537,
   "IC4_ef_A": 19.690827387696704
  },
  "rendimento_rede": 0.8928499610419426
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00009041289877,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.1033545407525,
   "Vbus_min_V": 180.4583116,
   "Vbus_max_V": 219.9046045,
   "Vbus_pp_V": 39.4462929,
   "Ibat_media_A": 55.33522923519759,
   "Ibat_ef_A": 78.52170628713786,
   "Ibat_pico_A": 157.7392183,
   "Pbat_W": 2324.0796278782987,
   "VC8_media_V": 138.962800745938,
   "VC7_media_V": 68.14055379380659
  },
  "c_saida": {
   "Vo_ef_V": 114.73063196024495,
   "Vo1_ef_V": 114.72387311912486,
   "DHT_vo_pct": 1.0114582222795063,
   "Io_ef_A": 27.24053536555918,
   "Io_pico_A": 73.47278226,
   "fator_crista": 2.697185693086388,
   "Po_W": 2132.0700988258004,
   "So_VA": 3125.323837426007,
   "M_efetivo": 0.869752802,
   "vc_livre_pico_V": 4.34876401,
   "I_QA_ef_A": 21.421584187733625,
   "I_Lo_pico_A": 76.03681549,
   "FP_carga": 0.6821917374750379
  },
  "rendimento_bateria": 0.9173825514628396
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.82
   ],
   [
    0.0833333,
    114.82
   ],
   [
    0.0916667,
    114.82
   ],
   [
    0.1,
    114.68
   ],
   [
    0.108333,
    114.76
   ],
   [
    0.116667,
    114.72
   ],
   [
    0.125,
    114.73
   ],
   [
    0.133333,
    114.73
   ],
   [
    0.141667,
    114.73
   ],
   [
    0.15,
    114.73
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.67652402625802,
  "Vo_ef_semiciclo_max_V": 114.82003724101533,
  "Vbus_min_apos_V": 174.1648621,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 198.9408148
 }
}
```

## nb_264_lin

```json
{
 "execucao": "nb_264_lin_execucao.json",
 "sha256_csv": "4c6b8929cc199e20645a6603e56657987d273a0fd17e08e1df22f5f6d7f88eb3",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 264 V com carga resistiva 2100 W; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 264.0,
  "phi_rede": 0,
  "carga": 1,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 371.7524,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 247.8349,
  "VC7_0": 123.9175,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 264.00006765677205,
   "Iin_ef_A": 16.30705886110335,
   "Iin_pico_A": 62.38271909,
   "Pin_W": 2169.059214010409,
   "FP": 0.5038389418220789,
   "DHT_iin_pct": 168.4962085852655
  },
  "b_barramento": {
   "Vbus_media_V": 358.9062640331927,
   "Vbus_min_V": 348.546921,
   "Vbus_max_V": 368.7181709,
   "Vbus_pp_V": 20.17124990000002,
   "Ibat_media_A": 1.282184152473954e-18,
   "Ibat_ef_A": 2.1229198571345074e-16,
   "Ibat_pico_A": 1.625874811e-15,
   "Pbat_W": 5.385173440390607e-17,
   "VC8_media_V": 241.4118320167676,
   "VC7_media_V": 117.49443201676758
  },
  "c_saida": {
   "Vo_ef_V": 114.87586598957967,
   "Vo1_ef_V": 114.87489950805336,
   "DHT_vo_pct": 0.15192264571520714,
   "Io_ef_A": 18.241158442509676,
   "Io_pico_A": 25.85829902,
   "fator_crista": 1.417579870351827,
   "Po_W": 2095.468883496,
   "So_VA": 2095.4688727364314,
   "M_efetivo": 0.503164097,
   "vc_livre_pico_V": 2.515820485,
   "I_QA_ef_A": 12.001092853427334,
   "I_Lo_pico_A": 29.15199913,
   "FP_carga": 1.0000000051346831
  },
  "diodo_D1": {
   "pico_A": 62.38271909,
   "media_A": 2.9542831920945933,
   "ef_A": 11.5584111359653,
   "IC4_ef_A": 15.923254095382553
  },
  "rendimento_rede": 0.9660726963841866
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 264.000135616674,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 203.8798699618865,
   "Vbus_min_V": 190.626019,
   "Vbus_max_V": 215.2059163,
   "Vbus_pp_V": 24.5798973,
   "Ibat_media_A": 52.25410166584514,
   "Ibat_ef_A": 66.44698736584684,
   "Ibat_pico_A": 119.4388204,
   "Pbat_W": 2194.672269965496,
   "VC8_media_V": 136.7965273891015,
   "VC7_media_V": 67.08334257231584
  },
  "c_saida": {
   "Vo_ef_V": 114.6925617728842,
   "Vo1_ef_V": 114.69130732420003,
   "DHT_vo_pct": 0.2696690642020581,
   "Io_ef_A": 18.21205153424126,
   "Io_pico_A": 25.72498141,
   "fator_crista": 1.4125251821099538,
   "Po_W": 2088.7868564793375,
   "So_VA": 2088.7868456019164,
   "M_efetivo": 0.8731995471999999,
   "vc_livre_pico_V": 4.365997736,
   "I_QA_ef_A": 13.61058729457631,
   "I_Lo_pico_A": 26.91843607,
   "FP_carga": 1.0000000052075304
  },
  "rendimento_bateria": 0.9517534280925584
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.88
   ],
   [
    0.0833333,
    114.88
   ],
   [
    0.0916667,
    114.88
   ],
   [
    0.1,
    114.83
   ],
   [
    0.108333,
    114.81
   ],
   [
    0.116667,
    114.78
   ],
   [
    0.125,
    114.74
   ],
   [
    0.133333,
    114.67
   ],
   [
    0.141667,
    114.72
   ],
   [
    0.15,
    114.69
   ],
   [
    0.158333,
    114.69
   ],
   [
    0.166667,
    114.69
   ],
   [
    0.175,
    114.69
   ],
   [
    0.183333,
    114.69
   ],
   [
    0.191667,
    114.69
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.6670807691173,
  "Vo_ef_semiciclo_max_V": 114.87591378508304,
  "Vbus_min_apos_V": 190.6543523,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 123.5545297
 }
}
```

## nb_264_nl

```json
{
 "execucao": "nb_264_nl_execucao.json",
 "sha256_csv": "443b647cd0717eed3b0e8223024c8ba24ac5ffe22e2031ae0251ae191b596f98",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 264 V com carga nao linear do Anexo 01; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 264.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 371.7524,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 247.8349,
  "VC7_0": 123.9175,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 264.00006765677205,
   "Iin_ef_A": 17.44862918332091,
   "Iin_pico_A": 71.358892,
   "Pin_W": 2268.4080528580425,
   "FP": 0.4924428419770377,
   "DHT_iin_pct": 172.54171145544927
  },
  "b_barramento": {
   "Vbus_media_V": 365.6280189015687,
   "Vbus_min_V": 349.8182895,
   "Vbus_max_V": 368.4384319,
   "Vbus_pp_V": 18.62014240000002,
   "Ibat_media_A": 5.50655958510695e-18,
   "Ibat_ef_A": 2.133493292934718e-16,
   "Ibat_pico_A": 1.672411895e-15,
   "Pbat_W": 2.312755025744919e-16,
   "VC8_media_V": 244.77270945237757,
   "VC7_media_V": 120.85530945237909
  },
  "c_saida": {
   "Vo_ef_V": 114.89288687767045,
   "Vo1_ef_V": 114.88902636217645,
   "DHT_vo_pct": 0.722554080609182,
   "Io_ef_A": 27.20655447964197,
   "Io_pico_A": 71.03974527,
   "fator_crista": 2.611126128564254,
   "Po_W": 2138.015112739791,
   "So_VA": 3125.839586160683,
   "M_efetivo": 0.5327577552,
   "vc_livre_pico_V": 2.663788776,
   "I_QA_ef_A": 18.027027308636637,
   "I_Lo_pico_A": 74.38203761,
   "FP_carga": 0.6839810725430767
  },
  "diodo_D1": {
   "pico_A": 71.358892,
   "media_A": 3.08332843368429,
   "ef_A": 12.358794424090071,
   "IC4_ef_A": 18.45968964200805
  },
  "rendimento_rede": 0.9425178640351038
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 264.000135616674,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.14214826466517,
   "Vbus_min_V": 180.3474545,
   "Vbus_max_V": 220.3741567,
   "Vbus_pp_V": 40.02670219999999,
   "Ibat_media_A": 55.1850493467361,
   "Ibat_ef_A": 78.30942510111429,
   "Ibat_pico_A": 158.5777587,
   "Pbat_W": 2317.772072562916,
   "VC8_media_V": 138.98846352058985,
   "VC7_media_V": 68.1536847434935
  },
  "c_saida": {
   "Vo_ef_V": 114.73035568669461,
   "Vo1_ef_V": 114.72359976211847,
   "DHT_vo_pct": 1.0112060161993772,
   "Io_ef_A": 27.238779384780496,
   "Io_pico_A": 73.47042226,
   "fator_crista": 2.6972729292359983,
   "Po_W": 2131.886638672497,
   "So_VA": 3125.114847287271,
   "M_efetivo": 0.8701586636,
   "vc_livre_pico_V": 4.350793318,
   "I_QA_ef_A": 21.417891218136603,
   "I_Lo_pico_A": 76.03730969,
   "FP_carga": 0.6821786535375053
  },
  "rendimento_bateria": 0.9197999509568372
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.89
   ],
   [
    0.0833333,
    114.89
   ],
   [
    0.0916667,
    114.89
   ],
   [
    0.1,
    114.85
   ],
   [
    0.108333,
    114.83
   ],
   [
    0.116667,
    114.8
   ],
   [
    0.125,
    114.75
   ],
   [
    0.133333,
    114.68
   ],
   [
    0.141667,
    114.76
   ],
   [
    0.15,
    114.72
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.6751312942496,
  "Vo_ef_semiciclo_max_V": 114.89301154194871,
  "Vbus_min_apos_V": 173.8878651,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 200.9631363
 }
}
```

## nb_220_lin

```json
{
 "execucao": "nb_220_lin_execucao.json",
 "sha256_csv": "741d89dcec15c682313666ed04980cebacaae620d010529d8687d4bc273f3455",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 220 V com carga resistiva 2100 W; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 220.0,
  "phi_rede": 0,
  "carga": 1,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 309.527,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 206.3513,
  "VC7_0": 103.1757,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 220.00005638295815,
   "Iin_ef_A": 18.244178720530844,
   "Iin_pico_A": 64.8287528,
   "Pin_W": 2150.6751772327534,
   "FP": 0.5358308479924638,
   "DHT_iin_pct": 154.0109491931388
  },
  "b_barramento": {
   "Vbus_media_V": 295.2297311916434,
   "Vbus_min_V": 283.7235789,
   "Vbus_max_V": 306.5129139,
   "Vbus_pp_V": 22.789334999999994,
   "Ibat_media_A": 1.4261600978649122e-18,
   "Ibat_ef_A": 2.1382621044132343e-16,
   "Ibat_pico_A": 1.796023317e-15,
   "Pbat_W": 5.989872411032631e-17,
   "VC8_media_V": 199.20266559592557,
   "VC7_media_V": 96.02706559643815
  },
  "c_saida": {
   "Vo_ef_V": 114.845479981217,
   "Vo1_ef_V": 114.8444631214235,
   "DHT_vo_pct": 0.1829191372556784,
   "Io_ef_A": 18.236333443023053,
   "Io_pico_A": 25.86350252,
   "fator_crista": 1.4182402729587613,
   "Po_W": 2094.360478132192,
   "So_VA": 2094.3604673615023,
   "M_efetivo": 0.5979860452,
   "vc_livre_pico_V": 2.989930226,
   "I_QA_ef_A": 12.01196996543692,
   "I_Lo_pico_A": 28.57929592,
   "FP_carga": 1.0000000051427105
  },
  "diodo_D1": {
   "pico_A": 64.8287528,
   "media_A": 3.551323404533488,
   "ef_A": 12.97126954945807,
   "IC4_ef_A": 17.06767607208021
  },
  "rendimento_rede": 0.973815339621383
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 220.0001130162098,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 203.87971808005565,
   "Vbus_min_V": 190.6260165,
   "Vbus_max_V": 215.2060861,
   "Vbus_pp_V": 24.5800696,
   "Ibat_media_A": 52.255045986228545,
   "Ibat_ef_A": 66.44762740758767,
   "Ibat_pico_A": 119.4388169,
   "Pbat_W": 2194.711931421599,
   "VC8_media_V": 136.7964301738395,
   "VC7_media_V": 67.08328790659235
  },
  "c_saida": {
   "Vo_ef_V": 114.69256296745604,
   "Vo1_ef_V": 114.69130852212106,
   "DHT_vo_pct": 0.26966798150429355,
   "Io_ef_A": 18.212051724272268,
   "Io_pico_A": 25.7249806,
   "fator_crista": 1.4125251228951217,
   "Po_W": 2088.7869000301025,
   "So_VA": 2088.786889152663,
   "M_efetivo": 0.8731995755999999,
   "vc_livre_pico_V": 4.365997878,
   "I_QA_ef_A": 13.610587743804869,
   "I_Lo_pico_A": 26.91843581,
   "FP_carga": 1.000000005207539
  },
  "rendimento_bateria": 0.9517362484456515
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.85
   ],
   [
    0.0833333,
    114.85
   ],
   [
    0.0916667,
    114.85
   ],
   [
    0.1,
    114.77
   ],
   [
    0.108333,
    114.71
   ],
   [
    0.116667,
    114.66
   ],
   [
    0.125,
    114.7
   ],
   [
    0.133333,
    114.69
   ],
   [
    0.141667,
    114.69
   ],
   [
    0.15,
    114.69
   ],
   [
    0.158333,
    114.69
   ],
   [
    0.166667,
    114.69
   ],
   [
    0.175,
    114.69
   ],
   [
    0.183333,
    114.69
   ],
   [
    0.191667,
    114.69
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.66170653289456,
  "Vo_ef_semiciclo_max_V": 114.84553667703659,
  "Vbus_min_apos_V": 190.3855448,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 123.0850056
 }
}
```

## nb_220_nl

```json
{
 "execucao": "nb_220_nl_execucao.json",
 "sha256_csv": "f78a44a1d90732dff9496a3e702f7659cb49f989d9c14a803ea8a70835d933af",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 220 V com carga nao linear do Anexo 01; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 220.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 309.527,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 206.3513,
  "VC7_0": 103.1757,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 220.00005638295815,
   "Iin_ef_A": 19.65668701447983,
   "Iin_pico_A": 75.73936448,
   "Pin_W": 2242.993245856953,
   "FP": 0.5186744452078074,
   "DHT_iin_pct": 160.3258681162839
  },
  "b_barramento": {
   "Vbus_media_V": 303.3049155973203,
   "Vbus_min_V": 286.6065448,
   "Vbus_max_V": 306.1638276,
   "Vbus_pp_V": 19.557282799999996,
   "Ibat_media_A": -1.4757030602065544e-18,
   "Ibat_ef_A": 2.0984771003195334e-16,
   "Ibat_pico_A": 1.834944707e-15,
   "Pbat_W": -6.197952852867528e-17,
   "VC8_media_V": 203.2402577976305,
   "VC7_media_V": 100.06465779781627
  },
  "c_saida": {
   "Vo_ef_V": 114.86394893257794,
   "Vo1_ef_V": 114.85887942053218,
   "DHT_vo_pct": 0.8561455729938078,
   "Io_ef_A": 27.356346451952874,
   "Io_pico_A": 72.21790643,
   "fator_crista": 2.6398958851043726,
   "Po_W": 2140.4775082808683,
   "So_VA": 3142.2579818390245,
   "M_efetivo": 0.6338339352,
   "vc_livre_pico_V": 3.169169676,
   "I_QA_ef_A": 18.233713440256807,
   "I_Lo_pico_A": 75.68389873,
   "FP_carga": 0.6811908890523819
  },
  "diodo_D1": {
   "pico_A": 75.73936448,
   "media_A": 3.6978412590743726,
   "ef_A": 14.003488248865063,
   "IC4_ef_A": 18.739373310971995
  },
  "rendimento_rede": 0.954295119806784
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 220.0001130162098,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.1068743025609,
   "Vbus_min_V": 180.4598244,
   "Vbus_max_V": 219.9473952,
   "Vbus_pp_V": 39.487570799999986,
   "Ibat_media_A": 55.321572716640446,
   "Ibat_ef_A": 78.50218237726449,
   "Ibat_pico_A": 157.8045963,
   "Pbat_W": 2323.506054098899,
   "VC8_media_V": 138.96512843607533,
   "VC7_media_V": 68.14174586611531
  },
  "c_saida": {
   "Vo_ef_V": 114.7306063208388,
   "Vo1_ef_V": 114.72384774559082,
   "DHT_vo_pct": 1.0114354103395893,
   "Io_ef_A": 27.240377053499937,
   "Io_pico_A": 73.47260562,
   "fator_crista": 2.6971948837455604,
   "Po_W": 2132.053521573833,
   "So_VA": 3125.304975756312,
   "M_efetivo": 0.8697335902000001,
   "vc_livre_pico_V": 4.348667951,
   "I_QA_ef_A": 21.421275359145174,
   "I_Lo_pico_A": 76.03683954,
   "FP_carga": 0.6821905503983284
  },
  "rendimento_bateria": 0.917601879200046
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.86
   ],
   [
    0.0833333,
    114.86
   ],
   [
    0.0916667,
    114.86
   ],
   [
    0.1,
    114.79
   ],
   [
    0.108333,
    114.73
   ],
   [
    0.116667,
    114.68
   ],
   [
    0.125,
    114.76
   ],
   [
    0.133333,
    114.72
   ],
   [
    0.141667,
    114.73
   ],
   [
    0.15,
    114.73
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.68292797641344,
  "Vo_ef_semiciclo_max_V": 114.8640594139072,
  "Vbus_min_apos_V": 175.3811791,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 190.8083927
 }
}
```

## nb_176_lin

```json
{
 "execucao": "nb_176_lin_execucao.json",
 "sha256_csv": "90f3c3a5bdea27581e5452ac1683c05948851cc341b7b1ab3b9c838a03a9746b",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 176 V com carga resistiva 2100 W; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 176.0,
  "phi_rede": 0,
  "carga": 1,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 247.3016,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 164.8677,
  "VC7_0": 82.4339,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00004510629785,
   "Iin_ef_A": 21.86774339573995,
   "Iin_pico_A": 67.76234592,
   "Pin_W": 2251.0295083415563,
   "FP": 0.5848768608157736,
   "DHT_iin_pct": 134.3755567294846
  },
  "b_barramento": {
   "Vbus_media_V": 230.84904483141577,
   "Vbus_min_V": 217.9775888,
   "Vbus_max_V": 244.2477475,
   "Vbus_pp_V": 26.270158699999996,
   "Ibat_media_A": 2.292286922346703e-18,
   "Ibat_ef_A": 2.1607266293606246e-16,
   "Ibat_pico_A": 1.673316707e-15,
   "Pbat_W": 9.627605073856152e-17,
   "VC8_media_V": 156.64142241455318,
   "VC7_media_V": 74.20762241546548
  },
  "c_saida": {
   "Vo_ef_V": 114.80047106537349,
   "Vo1_ef_V": 114.7992861232976,
   "DHT_vo_pct": 0.2546351764962057,
   "Io_ef_A": 18.229186469466544,
   "Io_pico_A": 25.870844,
   "fator_crista": 1.4191990434314254,
   "Po_W": 2092.7192046208133,
   "So_VA": 2092.7191938332917,
   "M_efetivo": 0.7350712306,
   "vc_livre_pico_V": 3.675356153,
   "I_QA_ef_A": 13.237530784300805,
   "I_Lo_pico_A": 27.87473713,
   "FP_carga": 1.000000005154787
  },
  "diodo_D1": {
   "pico_A": 67.76234592,
   "media_A": 4.64281541412325,
   "ef_A": 15.410416956223463,
   "IC4_ef_A": 17.472322414259718
  },
  "rendimento_rede": 0.9296720442206118
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00009041289877,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 203.87971554636994,
   "Vbus_min_V": 190.6260165,
   "Vbus_max_V": 215.2060894,
   "Vbus_pp_V": 24.580072900000005,
   "Ibat_media_A": 52.255063309212055,
   "Ibat_ef_A": 66.44763909897767,
   "Ibat_pico_A": 119.4388189,
   "Pbat_W": 2194.7126589869063,
   "VC8_media_V": 136.79642851077466,
   "VC7_media_V": 67.08328703737253
  },
  "c_saida": {
   "Vo_ef_V": 114.6925629877443,
   "Vo1_ef_V": 114.6913085432543,
   "DHT_vo_pct": 0.2696677084969293,
   "Io_ef_A": 18.212051727271128,
   "Io_pico_A": 25.72498082,
   "fator_crista": 1.4125251347424435,
   "Po_W": 2088.7869007435474,
   "So_VA": 2088.7868898661013,
   "M_efetivo": 0.873199573,
   "vc_livre_pico_V": 4.365997865,
   "I_QA_ef_A": 13.610587577208713,
   "I_Lo_pico_A": 26.91843586,
   "FP_carga": 1.0000000052075424
  },
  "rendimento_bateria": 0.9517359332623274
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.8
   ],
   [
    0.0833333,
    114.8
   ],
   [
    0.0916667,
    114.8
   ],
   [
    0.1,
    114.66
   ],
   [
    0.108333,
    114.7
   ],
   [
    0.116667,
    114.69
   ],
   [
    0.125,
    114.69
   ],
   [
    0.133333,
    114.69
   ],
   [
    0.141667,
    114.69
   ],
   [
    0.15,
    114.69
   ],
   [
    0.158333,
    114.69
   ],
   [
    0.166667,
    114.69
   ],
   [
    0.175,
    114.69
   ],
   [
    0.183333,
    114.69
   ],
   [
    0.191667,
    114.69
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.66045532184019,
  "Vo_ef_semiciclo_max_V": 114.80090208346603,
  "Vbus_min_apos_V": 190.3712389,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 123.4968443
 }
}
```

## nb_220_rl3k

```json
{
 "execucao": "nb_220_rl3k_execucao.json",
 "sha256_csv": "92beb5a3c75fac10130ac2ddb3a763603b5fab7d9a32418eea0b9f32815e5963",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Rede de 220 V com carga RL de 3 kVA com FP 0,7; falta da rede em 0,1 s (cruzamento por zero)",
 "ModelVars": {
  "Vrms": 220.0,
  "phi_rede": 0,
  "carga": 3,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 309.527,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 206.3513,
  "VC7_0": 103.1757,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 220.00005638295815,
   "Iin_ef_A": 18.22831005170096,
   "Iin_pico_A": 62.87995671,
   "Pin_W": 2181.792711434977,
   "FP": 0.5440568559374246,
   "DHT_iin_pct": 150.7035818305517
  },
  "b_barramento": {
   "Vbus_media_V": 289.870982108761,
   "Vbus_min_V": 282.3212823,
   "Vbus_max_V": 306.5295477,
   "Vbus_pp_V": 24.208265400000016,
   "Ibat_media_A": 8.917878835025035e-18,
   "Ibat_ef_A": 2.0540685126115836e-16,
   "Ibat_pico_A": 1.588650751e-15,
   "Pbat_W": 3.745509110710515e-16,
   "VC8_media_V": 196.52329105445781,
   "VC7_media_V": 93.34769105383285
  },
  "c_saida": {
   "Vo_ef_V": 114.80924795996238,
   "Vo1_ef_V": 114.80826258386796,
   "DHT_vo_pct": 0.16746416497777714,
   "Io_ef_A": 26.043555420558047,
   "Io_pico_A": 36.82961632,
   "fator_crista": 1.4141547006645545,
   "Po_W": 2093.025773931822,
   "So_VA": 2990.041012037871,
   "M_efetivo": 0.6084810428,
   "vc_livre_pico_V": 3.042405214,
   "I_QA_ef_A": 16.20484400421269,
   "I_Lo_pico_A": 36.03386765,
   "FP_carga": 0.6999990185771112
  },
  "diodo_D1": {
   "pico_A": 62.87995671,
   "media_A": 3.604226746727369,
   "ef_A": 12.951617696697529,
   "IC4_ef_A": 19.375907014543586
  },
  "rendimento_rede": 0.959314678686972
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 220.0001130162098,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 205.01299208713658,
   "Vbus_min_V": 187.8586649,
   "Vbus_max_V": 218.3626951,
   "Vbus_pp_V": 30.50403019999999,
   "Ibat_media_A": 53.02956981721614,
   "Ibat_ef_A": 70.25870164995297,
   "Ibat_pico_A": 131.3982644,
   "Pbat_W": 2227.241932323078,
   "VC8_media_V": 137.55311536400026,
   "VC7_media_V": 67.45987672278662
  },
  "c_saida": {
   "Vo_ef_V": 114.60307913148613,
   "Vo1_ef_V": 114.60185100852824,
   "DHT_vo_pct": 0.26113679866966943,
   "Io_ef_A": 25.99684815622985,
   "Io_pico_A": 36.7321224,
   "fator_crista": 1.4129452224075696,
   "Po_W": 2085.5180149593657,
   "So_VA": 2979.3188464176387,
   "M_efetivo": 0.8510443995999999,
   "vc_livre_pico_V": 4.255221998,
   "I_QA_ef_A": 17.70943762065069,
   "I_Lo_pico_A": 35.64287466,
   "FP_carga": 0.6999982621756018
  },
  "rendimento_bateria": 0.9363679736328016
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.81
   ],
   [
    0.0833333,
    114.81
   ],
   [
    0.0916667,
    114.81
   ],
   [
    0.1,
    114.72
   ],
   [
    0.108333,
    114.66
   ],
   [
    0.116667,
    114.61
   ],
   [
    0.125,
    114.6
   ],
   [
    0.133333,
    114.6
   ],
   [
    0.141667,
    114.6
   ],
   [
    0.15,
    114.6
   ],
   [
    0.158333,
    114.6
   ],
   [
    0.166667,
    114.6
   ],
   [
    0.175,
    114.6
   ],
   [
    0.183333,
    114.6
   ],
   [
    0.191667,
    114.6
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.60249904668026,
  "Vo_ef_semiciclo_max_V": 114.80929403130308,
  "Vbus_min_apos_V": 187.3849724,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 136.3587796
 }
}
```

## nb_176_nl_anexo

```json
{
 "execucao": "nb_176_nl_anexo_execucao.json",
 "sha256_csv": "0f22fd6dc9dd4cbbd1c1e0a311e114540050f03c6c6bfb32819c3d3ea660f227",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Como nb_176_nl, mas com o CC-CC sempre comandado (D = 0,7), como no circuito PSIM do Anexo 01",
 "ModelVars": {
  "Vrms": 176.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 1,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 247.3016,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 164.8677,
  "VC7_0": 82.4339,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00004510629785,
   "Iin_ef_A": 22.908906097253123,
   "Iin_pico_A": 78.17713178,
   "Pin_W": 2203.3904272509144,
   "FP": 0.5464800689104482,
   "DHT_iin_pct": 149.24872032718753
  },
  "b_barramento": {
   "Vbus_media_V": 242.11354807006566,
   "Vbus_min_V": 225.5538732,
   "Vbus_max_V": 245.501724,
   "Vbus_pp_V": 19.947850799999998,
   "Ibat_media_A": 4.537164495874551,
   "Ibat_ef_A": 5.922610181679501,
   "Ibat_pico_A": 10.90649862,
   "Pbat_W": 190.56090882673115,
   "VC8_media_V": 162.1995683450089,
   "VC7_media_V": 79.91397972471016
  },
  "c_saida": {
   "Vo_ef_V": 114.81657575737508,
   "Vo1_ef_V": 114.80975932874512,
   "DHT_vo_pct": 1.0187255526626298,
   "Io_ef_A": 27.53393954807974,
   "Io_pico_A": 73.2111416,
   "fator_crista": 2.6589417570325806,
   "Po_W": 2142.780029640458,
   "So_VA": 3161.352656021083,
   "M_efetivo": 0.7728395878,
   "vc_livre_pico_V": 3.864197939,
   "I_QA_ef_A": 21.453458672850783,
   "I_Lo_pico_A": 76.26573013,
   "FP_carga": 0.6778048078753058
  },
  "diodo_D1": {
   "pico_A": 78.17713178,
   "media_A": 4.47614144677334,
   "ef_A": 16.05402272094934,
   "IC4_ef_A": 19.65701544083344
  },
  "rendimento_rede": 0.9724922116113223
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00009041289877,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.10339113529483,
   "Vbus_min_V": 180.4583585,
   "Vbus_max_V": 219.9050487,
   "Vbus_pp_V": 39.446690200000006,
   "Ibat_media_A": 55.3350872909476,
   "Ibat_ef_A": 78.52150314292074,
   "Ibat_pico_A": 157.738911,
   "Pbat_W": 2324.073666219799,
   "VC8_media_V": 138.96282490887543,
   "VC7_media_V": 68.1405662268976
  },
  "c_saida": {
   "Vo_ef_V": 114.73063156388655,
   "Vo1_ef_V": 114.72387272816071,
   "DHT_vo_pct": 1.0114577553076392,
   "Io_ef_A": 27.24053354091,
   "Io_pico_A": 73.47277608,
   "fator_crista": 2.69718564688383,
   "Po_W": 2132.069910631093,
   "So_VA": 3125.323617285839,
   "M_efetivo": 0.8697525819999999,
   "vc_livre_pico_V": 4.34876291,
   "I_QA_ef_A": 21.421581500571055,
   "I_Lo_pico_A": 76.0368372,
   "FP_carga": 0.6821917253108883
  },
  "rendimento_bateria": 0.9173848237345212
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.82
   ],
   [
    0.0833333,
    114.82
   ],
   [
    0.0916667,
    114.82
   ],
   [
    0.1,
    114.68
   ],
   [
    0.108333,
    114.76
   ],
   [
    0.116667,
    114.72
   ],
   [
    0.125,
    114.73
   ],
   [
    0.133333,
    114.73
   ],
   [
    0.141667,
    114.73
   ],
   [
    0.15,
    114.73
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.67536178003918,
  "Vo_ef_semiciclo_max_V": 114.81683126283137,
  "Vbus_min_apos_V": 173.8708738,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 200.8794158
 }
}
```

## nb_176_nl_pico

```json
{
 "execucao": "nb_176_nl_pico_execucao.json",
 "sha256_csv": "8222cdde9b564d8b802db47f137c4e2a850ba94a5f9b3a944b9a0a58dc6439c3",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 18902,
 "descricao": "Como nb_176_nl, com a falta no pico positivo da tensao da rede",
 "ModelVars": {
  "Vrms": 176.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1041667,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 247.3016,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 164.8677,
  "VC7_0": 82.4339,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 175.9999996296797,
   "Iin_ef_A": 24.81963268604102,
   "Iin_pico_A": 82.78930837,
   "Pin_W": 2421.3773797739855,
   "FP": 0.5543122343679354,
   "DHT_iin_pct": 146.0575541858333
  },
  "b_barramento": {
   "Vbus_media_V": 240.83019166898336,
   "Vbus_min_V": 223.7547621,
   "Vbus_max_V": 243.783923,
   "Vbus_pp_V": 20.029160899999994,
   "Ibat_media_A": 4.933906546579685e-19,
   "Ibat_ef_A": 1.5928475225096226e-16,
   "Ibat_pico_A": 8.336627525e-16,
   "Pbat_W": 2.0722407495634677e-17,
   "VC8_media_V": 161.63199583373998,
   "VC7_media_V": 79.19819583405365
  },
  "c_saida": {
   "Vo_ef_V": 114.81972764907357,
   "Vo1_ef_V": 114.80121252624538,
   "DHT_vo_pct": 1.0417309326083841,
   "Io_ef_A": 27.569142949709637,
   "Io_pico_A": 73.21460744,
   "fator_crista": 2.655672233756222,
   "Po_W": 2143.463499311853,
   "So_VA": 3165.481485004037,
   "M_efetivo": 0.7802709057999999,
   "vc_livre_pico_V": 3.901354529,
   "I_QA_ef_A": 21.90333900399445,
   "I_Lo_pico_A": 76.21154812,
   "FP_carga": 0.6771366408131493
  },
  "diodo_D1": {
   "pico_A": 82.78928468,
   "media_A": 4.974688174742581,
   "ef_A": 17.550157471074446,
   "IC4_ef_A": 19.36516228912194
  },
  "rendimento_rede": 0.8852248795319657
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00009041289877,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.10096851486549,
   "Vbus_min_V": 180.4467332,
   "Vbus_max_V": 219.9034359,
   "Vbus_pp_V": 39.456702699999994,
   "Ibat_media_A": 55.34448969338749,
   "Ibat_ef_A": 78.53497015192501,
   "Ibat_pico_A": 157.7875721,
   "Pbat_W": 2324.4685671222746,
   "VC8_media_V": 138.96122265781148,
   "VC7_media_V": 68.1397458558276
  },
  "c_saida": {
   "Vo_ef_V": 114.7306489220126,
   "Vo1_ef_V": 114.72388989269108,
   "DHT_vo_pct": 1.0114743091140364,
   "Io_ef_A": 27.240642792902356,
   "Io_pico_A": 73.47292463,
   "fator_crista": 2.6971802827334024,
   "Po_W": 2132.081275009047,
   "So_VA": 3125.336624682433,
   "M_efetivo": 0.8697658122,
   "vc_livre_pico_V": 4.348829061,
   "I_QA_ef_A": 21.421793561724957,
   "I_Lo_pico_A": 76.03717602,
   "FP_carga": 0.682192522293719
  },
  "rendimento_bateria": 0.9172338594574304
 },
 "transferencia": {
  "instante_s": 0.1041667,
  "Vo_ef_semiciclos": [
   [
    0.0833333,
    114.82
   ],
   [
    0.0916667,
    114.82
   ],
   [
    0.1,
    114.8
   ],
   [
    0.108333,
    114.68
   ],
   [
    0.116667,
    114.76
   ],
   [
    0.125,
    114.72
   ],
   [
    0.133333,
    114.73
   ],
   [
    0.141667,
    114.73
   ],
   [
    0.15,
    114.73
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.68226333571265,
  "Vo_ef_semiciclo_max_V": 114.81972557437993,
  "Vbus_min_apos_V": 175.2981341,
  "Iin_pico_A": 47.62542380577361,
  "Ibat_pico_A": 191.5215986
 }
}
```

## nb_220_retorno

```json
{
 "execucao": "nb_220_retorno_execucao.json",
 "sha256_csv": "7831915d277a9a87a5f870c812f2fa98166336f7e6c3144c0cd7c0652b7bf2e6",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 25451,
 "descricao": "Rede de 220 V, resistiva; falta em 0,1 s e retorno em 0,2 s, ambos no cruzamento por zero",
 "ModelVars": {
  "Vrms": 220.0,
  "phi_rede": 0,
  "carga": 1,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 0.2,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 309.527,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 206.3513,
  "VC7_0": 103.1757,
  "Tstop": 0.3
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 219.99999953696386,
   "Iin_ef_A": 18.143023586648443,
   "Iin_pico_A": 64.29026358,
   "Pin_W": 2136.7771896671743,
   "FP": 0.5353365475965141,
   "DHT_iin_pct": 154.2100065047948
  },
  "b_barramento": {
   "Vbus_media_V": 295.23784307358665,
   "Vbus_min_V": 283.7235911,
   "Vbus_max_V": 306.5113248,
   "Vbus_pp_V": 22.78773369999999,
   "Ibat_media_A": -2.6718695711183496e-18,
   "Ibat_ef_A": 1.7840906181179863e-16,
   "Ibat_pico_A": 7.648944816e-16,
   "Pbat_W": -1.122185219869707e-16,
   "VC8_media_V": 199.20672153598335,
   "VC7_media_V": 96.03112153767633
  },
  "c_saida": {
   "Vo_ef_V": 114.84553665766194,
   "Vo1_ef_V": 114.83308826376052,
   "DHT_vo_pct": 0.18390971233081393,
   "Io_ef_A": 18.236342442855182,
   "Io_pico_A": 25.8631048,
   "fator_crista": 1.418217763844027,
   "Po_W": 2094.3625452932906,
   "So_VA": 2094.362534522601,
   "M_efetivo": 0.5956304762,
   "vc_livre_pico_V": 2.978152381,
   "I_QA_ef_A": 11.740589801677066,
   "I_Lo_pico_A": 28.3248469,
   "FP_carga": 1.0000000051427054
  },
  "diodo_D1": {
   "pico_A": 64.29026358,
   "media_A": 3.505844194164959,
   "ef_A": 12.828604842477931,
   "IC4_ef_A": 17.214640727371016
  },
  "rendimento_rede": 0.9801501791674918
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 219.9999429036829,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 203.8808525908815,
   "Vbus_min_V": 190.6264027,
   "Vbus_max_V": 215.206086,
   "Vbus_pp_V": 24.5796833,
   "Ibat_media_A": 52.25498334301715,
   "Ibat_ef_A": 66.44936154832818,
   "Ibat_pico_A": 119.4388167,
   "Pbat_W": 2194.7093004067206,
   "VC8_media_V": 136.7892131283295,
   "VC7_media_V": 67.09163946316053
  },
  "c_saida": {
   "Vo_ef_V": 114.69249015071573,
   "Vo1_ef_V": 114.6799354023762,
   "DHT_vo_pct": 0.25913655043839046,
   "Io_ef_A": 18.21204016167492,
   "Io_pico_A": 25.72498066,
   "fator_crista": 1.4125260229842438,
   "Po_W": 2088.784247744787,
   "So_VA": 2088.78423686734,
   "M_efetivo": 0.8729711778,
   "vc_livre_pico_V": 4.364855889,
   "I_QA_ef_A": 13.73424861979338,
   "I_Lo_pico_A": 26.675444,
   "FP_carga": 1.0000000052075493
  },
  "rendimento_bateria": 0.9517361808954363
 },
 "apos_retorno": {
  "janela_s": [
   0.26666666666666666,
   0.3
  ],
  "a_entrada": {
   "Vin_ef_V": 219.9999995369639,
   "Iin_ef_A": 18.143023158918442,
   "Iin_pico_A": 64.2902545,
   "Pin_W": 2136.777174889001,
   "FP": 0.5353365565148724,
   "DHT_iin_pct": 154.2100027778445
  },
  "b_barramento": {
   "Vbus_media_V": 295.23784351660663,
   "Vbus_min_V": 283.7235899,
   "Vbus_max_V": 306.511324,
   "Vbus_pp_V": 22.787734100000023,
   "Ibat_media_A": 4.740323953759887e-18,
   "Ibat_ef_A": 1.70076274725939e-16,
   "Ibat_pico_A": 6.552717124e-16,
   "Pbat_W": 1.9909360605791527e-16,
   "VC8_media_V": 196.64825298623333,
   "VC7_media_V": 98.58959053086635
  },
  "c_saida": {
   "Vo_ef_V": 114.84553651613403,
   "Vo1_ef_V": 114.83308812580896,
   "DHT_vo_pct": 0.18390795989283848,
   "Io_ef_A": 18.236342420171336,
   "Io_pico_A": 25.86310149,
   "fator_crista": 1.418217584102427,
   "Po_W": 2094.3625401072,
   "So_VA": 2094.362529336511,
   "M_efetivo": 0.5956302960000001,
   "vc_livre_pico_V": 2.97815148,
   "I_QA_ef_A": 11.740589804957656,
   "I_Lo_pico_A": 28.32488089,
   "FP_carga": 1.000000005142705
  }
 },
 "transferencia": {
  "instante_s": 0.2,
  "Vo_ef_semiciclos": [
   [
    0.175,
    114.69
   ],
   [
    0.183333,
    114.69
   ],
   [
    0.191667,
    114.69
   ],
   [
    0.2,
    114.98
   ],
   [
    0.208333,
    114.85
   ],
   [
    0.216667,
    114.85
   ],
   [
    0.225,
    114.85
   ],
   [
    0.233333,
    114.85
   ],
   [
    0.241667,
    114.85
   ],
   [
    0.25,
    114.85
   ],
   [
    0.258333,
    114.85
   ],
   [
    0.266667,
    114.85
   ],
   [
    0.275,
    114.85
   ],
   [
    0.283333,
    114.85
   ],
   [
    0.291667,
    114.85
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.69239429428428,
  "Vo_ef_semiciclo_max_V": 114.98320880807651,
  "Vbus_min_apos_V": 208.0127739,
  "Iin_pico_A": 134.1186703,
  "Ibat_pico_A": 40.21825092
 }
}
```

## conv_176_nl

```json
{
 "execucao": "conv_176_nl_execucao.json",
 "sha256_csv": "ff7ec793fc4362aab194d012692aa85bd2bf168c0305b0ea59b7f03d28f0d6b3",
 "sha256_modelo": "3bacaebd645529b57244c6e942b2677908c3174dd282875859b0618549fdb4ae",
 "amostras": 22551,
 "descricao": "Refinamento numerico de nb_176_nl (passo maximo 1 us, RelTol 1e-7)",
 "ModelVars": {
  "Vrms": 176.0,
  "phi_rede": 0,
  "carga": 2,
  "Rres": 6.297619,
  "tcarga": 0,
  "tfalta": 0.1,
  "tretorno": 100,
  "tdet": 0,
  "modo_cc": 0,
  "Vbat": 42.0,
  "Db": 0.7,
  "Vbus0": 247.3016,
  "ILb0": 0,
  "VC3_0": 140.0,
  "VC8_0": 164.8677,
  "VC7_0": 82.4339,
  "Tstop": 0.2
 },
 "rede": {
  "janela_s": [
   0.06666666666666667,
   0.1
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00004510629785,
   "Iin_ef_A": 24.623567911256668,
   "Iin_pico_A": 82.81340122,
   "Pin_W": 2400.7389844045706,
   "FP": 0.5539635427598816,
   "DHT_iin_pct": 146.05424793311204
  },
  "b_barramento": {
   "Vbus_media_V": 240.8408729443413,
   "Vbus_min_V": 223.7547677,
   "Vbus_max_V": 243.8740568,
   "Vbus_pp_V": 20.119289100000003,
   "Ibat_media_A": -1.2063675370629484e-18,
   "Ibat_ef_A": 3.637205201197076e-16,
   "Ibat_pico_A": 1.617973075e-15,
   "Pbat_W": -5.066743655664383e-17,
   "VC8_media_V": 161.63733647247125,
   "VC7_media_V": 79.20353647219179
  },
  "c_saida": {
   "Vo_ef_V": 114.81977965806131,
   "Vo1_ef_V": 114.8127105557205,
   "DHT_vo_pct": 1.0400966996613115,
   "Io_ef_A": 27.56911037460802,
   "Io_pico_A": 73.21488571,
   "fator_crista": 2.65568546518763,
   "Po_W": 2143.498698722128,
   "So_VA": 3165.479178581265,
   "M_efetivo": 0.7802755433999999,
   "vc_livre_pico_V": 3.901377717,
   "I_QA_ef_A": 21.48246250971874,
   "I_Lo_pico_A": 76.21182666,
   "FP_carga": 0.6771482539597125
  },
  "diodo_D1": {
   "pico_A": 82.81340122,
   "media_A": 4.889887659341111,
   "ef_A": 17.271753942427292,
   "IC4_ef_A": 19.690838493675507
  },
  "rendimento_rede": 0.8928495403484095
 },
 "bateria": {
  "janela_s": [
   0.16666666666666666,
   0.2
  ],
  "a_entrada": {
   "Vin_ef_V": 176.00009041289877,
   "Iin_ef_A": 0.0,
   "Iin_pico_A": 0.0,
   "Pin_W": 0.0,
   "FP": null,
   "DHT_iin_pct": null
  },
  "b_barramento": {
   "Vbus_media_V": 207.10335349597287,
   "Vbus_min_V": 180.4583084,
   "Vbus_max_V": 219.9046032,
   "Vbus_pp_V": 39.446294800000004,
   "Ibat_media_A": 55.335232413973415,
   "Ibat_ef_A": 78.5217109637768,
   "Ibat_pico_A": 157.7392263,
   "Pbat_W": 2324.0797613868835,
   "VC8_media_V": 138.96280035217208,
   "VC7_media_V": 68.14055314327332
  },
  "c_saida": {
   "Vo_ef_V": 114.73063263672769,
   "Vo1_ef_V": 114.72387376872383,
   "DHT_vo_pct": 1.011460556357489,
   "Io_ef_A": 27.24053931297569,
   "Io_pico_A": 73.47277533,
   "fator_crista": 2.6971850478379538,
   "Po_W": 2132.0702144967363,
   "So_VA": 3125.3243087433525,
   "M_efetivo": 0.8697527429999999,
   "vc_livre_pico_V": 4.348763715,
   "I_QA_ef_A": 21.421587086197782,
   "I_Lo_pico_A": 76.0368556,
   "FP_carga": 0.6821916716073574
  },
  "rendimento_bateria": 0.9173825485337188
 },
 "transferencia": {
  "instante_s": 0.1,
  "Vo_ef_semiciclos": [
   [
    0.075,
    114.82
   ],
   [
    0.0833333,
    114.82
   ],
   [
    0.0916667,
    114.82
   ],
   [
    0.1,
    114.68
   ],
   [
    0.108333,
    114.76
   ],
   [
    0.116667,
    114.72
   ],
   [
    0.125,
    114.73
   ],
   [
    0.133333,
    114.73
   ],
   [
    0.141667,
    114.73
   ],
   [
    0.15,
    114.73
   ],
   [
    0.158333,
    114.73
   ],
   [
    0.166667,
    114.73
   ],
   [
    0.175,
    114.73
   ],
   [
    0.183333,
    114.73
   ],
   [
    0.191667,
    114.73
   ]
  ],
  "Vo_ef_semiciclo_min_V": 114.67652441570164,
  "Vo_ef_semiciclo_max_V": 114.82003667905468,
  "Vbus_min_apos_V": 174.1648485,
  "Iin_pico_A": 0.0,
  "Ibat_pico_A": 198.9409045
 }
}
```

## verificacao_convergencia

```json
{
 "rede.Vo_ef_V": {
  "base": 114.81978007440368,
  "refinado": 114.81977965806131,
  "dif_rel": 3.6260509744050257e-09
 },
 "rede.DHT_vo_pct": {
  "base": 1.0400870397672382,
  "refinado": 1.0400966996613115,
  "dif_rel": 9.287496130365716e-06
 },
 "rede.Vbus_media_V": {
  "base": 240.84085521656706,
  "refinado": 240.8408729443413,
  "dif_rel": 7.360783084086943e-08
 },
 "rede.Ibat_media_A": {
  "base": 3.3367047718413526e-18,
  "refinado": -1.2063675370629484e-18,
  "dif_rel": 4.5430723089043e-09
 },
 "rede.Iin_ef_A": {
  "base": 24.62355235407405,
  "refinado": 24.623567911256668,
  "dif_rel": 6.318005040441824e-07
 },
 "bateria.Vo_ef_V": {
  "base": 114.73063196024495,
  "refinado": 114.73063263672769,
  "dif_rel": 5.896269603652399e-09
 },
 "bateria.DHT_vo_pct": {
  "base": 1.0114582222795063,
  "refinado": 1.011460556357489,
  "dif_rel": 2.307631244736004e-06
 },
 "bateria.Vbus_media_V": {
  "base": 207.1033545407525,
  "refinado": 207.10335349597287,
  "dif_rel": 5.04472576218649e-09
 },
 "bateria.Ibat_media_A": {
  "base": 55.33522923519759,
  "refinado": 55.335232413973415,
  "dif_rel": 5.7445784336268455e-08
 },
 "bateria.Iin_ef_A": {
  "base": 0.0,
  "refinado": 0.0,
  "dif_rel": 0.0
 }
}
```
