"""Analisa exclusivamente CSVs do PLECS com registro de execucao bem-sucedido e hash conferido.

Calcula, por integracao trapezoidal em janelas declaradas (numero inteiro de ciclos de 60 Hz):
valores eficazes, medios, picos, DHT, fator de crista, potencias e fator de potencia,
ondulacao do barramento, esforcos dos diodos da ponte, correntes da bateria e de Lb,
indice de modulacao efetivo, transferencia rede/bateria e curvas de regulacao.
Compara cada resultado S com o valor analitico A de desenvolvimento/calculos/parametros.json.
Saidas: metricas.json, metricas.md e graficos PNG/PDF em resultados PLECS/graficos
(copiados para artigo/figuras). Ensaios ausentes ou com falha sao listados como pendentes.
Uso: python "resultados PLECS/analisar_resultados.py"
"""
from pathlib import Path
import json, hashlib, shutil, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
GRAF = OUT / 'graficos'
FIG = ROOT / 'artigo' / 'figuras'
GRAF.mkdir(exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
ENS = json.loads((ROOT / 'simulação PLECS/ensaios.json').read_text(encoding='utf-8'))
T60 = 1 / 60
COR = ['#2a78d6', '#eb6834', '#1baf7a', '#6250d6', '#e34948', '#008300', '#eda100']
plt.rcParams.update({'font.size': 8.5, 'axes.labelsize': 8.5, 'legend.fontsize': 7.2, 'xtick.labelsize': 8,
                     'ytick.labelsize': 8, 'axes.grid': True, 'grid.alpha': .3, 'grid.linewidth': .5,
                     'lines.linewidth': 1.0, 'axes.spines.top': False, 'axes.spines.right': False,
                     'font.family': 'serif', 'savefig.dpi': 300})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def carregar(nome):
    log = OUT / f'{nome}_execucao.json'
    if not log.exists():
        return None, None
    reg = json.loads(log.read_text(encoding='utf-8'))
    arq = OUT / f'{nome}.csv'
    if reg.get('status') != 'executado' or not arq.exists():
        return None, reg
    modelo = ROOT / 'simulação PLECS' / f"{ENS[nome]['modelo']}.plecs"
    if reg.get('sha256_modelo') != sha(modelo):
        return None, dict(reg, status='desatualizado (o modelo mudou depois da execucao)')
    if sha(arq) != reg['sha256_csv']:
        raise RuntimeError(f'{nome}: hash do CSV difere do registro')
    d = np.genfromtxt(arq, delimiter=',', names=True)
    return d, reg


# ---------------------------------------------------------------------------
# Ferramentas de janela (grade de saida pode ser nao uniforme)
# ---------------------------------------------------------------------------
def recorte(t, x, a, b):
    m = (t > a) & (t < b)
    tt = np.r_[a, t[m], b]
    xx = np.r_[np.interp(a, t, x), x[m], np.interp(b, t, x)]
    return tt, xx


def media(t, x, a, b):
    tt, xx = recorte(t, x, a, b)
    return float(np.trapezoid(xx, tt) / (b - a))


def eficaz(t, x, a, b):
    tt, xx = recorte(t, x, a, b)
    return float(math.sqrt(np.trapezoid(xx * xx, tt) / (b - a)))


def extremos(t, x, a, b):
    tt, xx = recorte(t, x, a, b)
    return float(xx.min()), float(xx.max())


def uniforme(t, x, a, b, passo):
    n = int(round((b - a) / passo))
    tu = a + passo * np.arange(n)
    return tu, np.interp(tu, t, x)


def dht(t, x, a, b, nh=40):
    """DHT ate a harmonica nh, por DFT sobre numero inteiro de ciclos (janela [a, b))."""
    passo = np.median(np.diff(t[(t >= a) & (t <= b)]))
    tu, xu = uniforme(t, x, a, b, passo)
    ciclos = int(round((b - a) * 60))
    X = np.fft.rfft(xu) / len(xu) * 2
    h = np.abs(X[ciclos * np.arange(1, nh + 1)])
    return float(math.sqrt(np.sum(h[1:] ** 2)) / h[0] * 100), float(h[0] / math.sqrt(2))


def ef_por_semiciclo(t, x, a, b):
    """Valor eficaz em cada semiciclo de 60 Hz entre a e b (para observar a transferencia)."""
    k0 = int(math.ceil(a * 120 - 1e-9))
    res = []
    while (k0 + 1) / 120 <= b + 1e-12:
        ta, tb = k0 / 120, (k0 + 1) / 120
        res.append((ta, eficaz(t, x, ta, tb)))
        k0 += 1
    return res


def pulsos(t, x, a, b, limiar):
    """Duracao media dos pulsos de corrente acima do limiar."""
    tt, xx = recorte(t, x, a, b)
    on = xx > limiar
    bordas = np.flatnonzero(np.diff(on.astype(int)))
    dur = []
    for i in range(len(bordas) - 1):
        if on[bordas[i] + 1]:
            dur.append(tt[bordas[i + 1]] - tt[bordas[i]])
    return float(np.mean(dur)) if dur else None


def ondulacao_chaveamento(t, x, a, b, periodo):
    """Maior excursao pico a pico dentro de um periodo de chaveamento na janela."""
    m = (t >= a) & (t <= b)
    tt, xx = t[m], x[m]
    k = np.floor((tt - a) / periodo).astype(int)
    vals = [np.ptp(xx[k == i]) for i in np.unique(k) if np.sum(k == i) > 10]
    return float(max(vals)) if vals else None


def r(x, n=5):
    if x is None:
        return None
    return float(f'{x:.{n}g}')


# ---------------------------------------------------------------------------
# Graficos
# ---------------------------------------------------------------------------
def virgula(*eixos):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, p: ('%g' % v).replace('.', ','))
    for e in eixos:
        e.set_major_formatter(fmt)


def salvar(fig, nome):
    fig.tight_layout(pad=.4, h_pad=.3)
    for ext in ('png', 'pdf'):
        fig.savefig(GRAF / f'{nome}.{ext}', dpi=300)
        shutil.copy2(GRAF / f'{nome}.{ext}', FIG / f'{nome}.{ext}')
    plt.close(fig)
    return nome


def painel_nobreak(casos, nome, t0=0.05, t1=0.2, tfalta=0.1):
    """Seis paineis empilhados: (a) entrada, (b) barramento e bateria, (c) saida."""
    rot = [('v_rede_V', 'Rede (V)'), ('i_rede_A', 'Entrada (A)'), ('v_bus_V', 'Barramento (V)'),
           ('i_bat_A', 'Bateria (A)'), ('v_o_V', 'Saída (V)'), ('i_o_A', 'Carga (A)')]
    fig, ax = plt.subplots(6, 1, figsize=(3.45, 6.4), sharex=True)
    for j, (lab, d) in enumerate(casos):
        t = d['tempo_s']
        m = (t >= t0) & (t <= t1)
        for i, (col, yl) in enumerate(rot):
            ax[i].plot(t[m] * 1e3, d[col][m], color=COR[j], lw=.8, label=lab if i == 0 else None,
                       alpha=1 if j == 0 else .85)
            ax[i].set_ylabel(yl)
    for a in ax:
        a.axvline(tfalta * 1e3, color='0.35', lw=.6, ls=':')
    ax[-1].set_xlabel('Tempo (ms)')
    if len(casos) > 1:
        ax[0].legend(loc='upper right', ncol=len(casos), frameon=False, fontsize=7)
    # as letras vao como titulo a esquerda, fora do eixo, para nao cair sobre o rotulo do eixo y
    for a, letra in zip(ax[::2], 'abc'):
        a.set_title(f'({letra})', loc='left', fontsize=8.5, pad=2)
    return salvar(fig, nome)


# ---------------------------------------------------------------------------
# Analise por grupo
# ---------------------------------------------------------------------------
def analisar_retificador(nome, d, reg):
    a, b = reg['janelas']['regime']
    t = d['tempo_s']
    vmin, vmax = extremos(t, d['v_bus_V'], a, b)
    iD = d['i_D1_A']
    res = dict(janela_s=[a, b], v_bus_media_V=media(t, d['v_bus_V'], a, b), v_bus_min_V=vmin, v_bus_max_V=vmax,
               ondulacao_bus_Vpp=vmax - vmin, i_D1_pico_A=extremos(t, iD, a, b)[1], i_D1_media_A=media(t, iD, a, b),
               i_D1_ef_A=eficaz(t, iD, a, b), i_C4_ef_A=eficaz(t, d['i_C4_A'], a, b), i_rede_ef_A=eficaz(t, d['i_rede_A'], a, b),
               duracao_pulso_ms=(pulsos(t, iD, a, b, 0.01 * extremos(t, iD, a, b)[1]) or 0) * 1e3,
               P_entrada_W=media(t, d['v_rede_V'] * d['i_rede_A'], a, b),
               P_barramento_W=media(t, d['v_bus_V'] * d['i_ponte_A'], a, b))
    res['FP_entrada'] = res['P_entrada_W'] / (eficaz(t, d['v_rede_V'], a, b) * res['i_rede_ef_A'])
    rp = P['retificador']['planilha']
    res['comparacao_A'] = dict(Ichg_A=rp['Ichg'], ID1pk_2Ichg_A=rp['ID1pk_2Ichg'], ID1med_A=rp['ID1med'], ID1ef_A=rp['ID1ef'],
                               IC1ef_A=rp['IC1ef'], VC1min_V=rp['VC1min'], tC1_ms=rp['tC1_s'] * 1e3)
    return res


def analisar_elevador(nome, d, reg):
    a, b = reg['janelas']['regime']
    da, db = reg['janelas']['detalhe']
    t = d['tempo_s']
    mv = reg['opcoes']['ModelVars']
    vmin, vmax = extremos(t, d['v_bus_V'], a, b)
    res = dict(janela_s=[a, b], v_bus_media_V=media(t, d['v_bus_V'], a, b), v_bus_pp_V=vmax - vmin,
               v_C8_media_V=media(t, d['v_C8_V'], a, b), v_C7_media_V=media(t, d['v_C7_V'], a, b),
               i_bat_media_A=media(t, d['i_bat_A'], a, b), i_bat_ef_A=eficaz(t, d['i_bat_A'], a, b),
               i_bat_pico_A=extremos(t, d['i_bat_A'], da, db)[1],
               dILb_pp_A=ondulacao_chaveamento(t, d['i_bat_A'], da, db, 0.5 / 2e4),
               v_S1_max_V=extremos(t, d['v_S1_V'], da, db)[1], i_S1_ef_A=eficaz(t, d['i_S1_A'], da, db),
               i_S1_pico_A=extremos(t, d['i_S1_A'], da, db)[1], i_S2_ef_A=eficaz(t, d['i_S2_A'], da, db),
               i_D17_ef_A=eficaz(t, d['i_D17_A'], da, db), i_D17_media_A=media(t, d['i_D17_A'], da, db),
               i_sec_ef_A=eficaz(t, d['i_sec_A'], da, db), D_medida=media(t, d['gate_S1'], da, db))
    res['P_bateria_W'] = mv['Vbat'] * res['i_bat_media_A']
    res['P_carga_W'] = eficaz(t, d['v_bus_V'], a, b) ** 2 / mv['Rcarga']
    res['rendimento_modelo'] = res['P_carga_W'] / res['P_bateria_W']
    pc = P['cc_cc']['pontos'][str(int(mv['Vbat']))]
    res['comparacao_A'] = dict(Vbus_V=pc['Vbus'], VC8_V=pc['VC8'], VC7_V=pc['VC7'], Iib_A=pc['Iib'], dILb_pp_A=pc['dILb_pp'],
                               V_chave_V=pc['V_chave'], D=pc['D'])
    return res


def analisar_diagnostico(nome, d, reg):
    """Ensaios curtos do CC-CC: tempo de relogio e valores medios no ultimo milissegundo."""
    a, b = reg['janelas']['final']
    t = d['tempo_s']
    return dict(janela_s=[a, b], v_bus_media_V=media(t, d['v_bus_V'], a, b), v_C8_media_V=media(t, d['v_C8_V'], a, b),
                v_C7_media_V=media(t, d['v_C7_V'], a, b), i_bat_media_A=media(t, d['i_bat_A'], a, b),
                i_D17_min_A=extremos(t, d['i_D17_A'], a, b)[0], i_sec_pico_A=max(abs(x) for x in extremos(t, d['i_sec_A'], a, b)))


def analisar_inversor(nome, d, reg):
    t = d['tempo_s']
    jan = reg['janelas']
    if 'regime' in jan:
        a, b = jan['regime']
    else:
        a, b = jan['depois']
    vo = d['v_o_V']
    th, v1 = dht(t, vo, a, b)
    Irms = eficaz(t, d['i_o_A'], a, b)
    imin, imax = extremos(t, d['i_o_A'], a, b)
    res = dict(janela_s=[a, b], Vo_ef_V=eficaz(t, vo, a, b), Vo1_ef_V=v1, DHT_vo_pct=th, Io_ef_A=Irms,
               Io_pico_A=max(abs(imin), abs(imax)), Po_W=media(t, vo * d['i_o_A'], a, b),
               vc_pico_V=max(abs(x) for x in extremos(t, d['v_c_V'], a, b)),
               vc_livre_pico_V=max(abs(x) for x in extremos(t, d['v_c_livre_V'], a, b)),
               I_QA_ef_A=eficaz(t, d['i_QA_A'], a, b), I_QA_pico_A=extremos(t, d['i_QA_A'], a, b)[1],
               I_Lo_pico_A=max(abs(x) for x in extremos(t, d['i_Lo_A'], a, b)))
    res['M_efetivo'] = res['vc_pico_V'] / 5.0
    res['fator_crista'] = res['Io_pico_A'] / Irms if Irms > 0.1 else None
    res['So_VA'] = res['Vo_ef_V'] * Irms
    if 'detalhe' in jan:
        da, db = jan['detalhe']
        res['dILo_pp_no_pico_A'] = ondulacao_chaveamento(t, d['i_Lo_A'], da, db, 1 / 2e4)
        res['vAB_niveis_V'] = sorted(set(np.round(d['v_AB_V'][(t >= da) & (t <= db)], -1).tolist()))[:6]
    if 'degrau' in jan:
        ta, tb = jan['degrau']
        e = vo - d['v_ref_V'] / P['malha']['Hv']
        emin, emax = extremos(t, e, ta, tb)
        res['degrau'] = dict(erro_min_V=emin, erro_max_V=emax,
                             Vo_ef_antes_V=eficaz(t, vo, *jan['antes']), Vo_ef_depois_V=eficaz(t, vo, *jan['depois']))
    Vcc = reg['opcoes']['ModelVars'].get('Vcc')
    res['comparacao_A'] = dict(M_pico=162.6346 / Vcc if Vcc else None,
                               dILo_max_A=P['inversor']['ondulacao_Lo']['373,35 V (pico a 264 V)']['dILo_max_App'] if Vcc and Vcc > 300 else
                               P['inversor']['ondulacao_Lo']['211,57 V (vale a 176 V)']['dILo_max_App'])
    return res


def analisar_nobreak(nome, d, reg):
    t = d['tempo_s']
    jan = reg['janelas']
    mv = reg['opcoes']['ModelVars']
    res = dict(ModelVars=mv)
    for modo in ('rede', 'bateria', 'apos_retorno'):
        if modo not in jan:
            continue
        a, b = jan[modo]
        vo = d['v_o_V']
        th, v1 = dht(t, vo, a, b)
        Io = eficaz(t, d['i_o_A'], a, b)
        imin, imax = extremos(t, d['i_o_A'], a, b)
        bmin, bmax = extremos(t, d['v_bus_V'], a, b)
        Vin = eficaz(t, d['v_rede_V'], a, b)
        Iin = eficaz(t, d['i_rede_A'], a, b)
        Pin = media(t, d['v_rede_V'] * d['i_rede_A'], a, b)
        m = dict(janela_s=[a, b],
                 a_entrada=dict(Vin_ef_V=Vin, Iin_ef_A=Iin, Iin_pico_A=max(abs(x) for x in extremos(t, d['i_rede_A'], a, b)),
                                Pin_W=Pin, FP=Pin / (Vin * Iin) if Iin > 0.05 else None,
                                DHT_iin_pct=dht(t, d['i_rede_A'], a, b)[0] if Iin > 0.5 else None),
                 b_barramento=dict(Vbus_media_V=media(t, d['v_bus_V'], a, b), Vbus_min_V=bmin, Vbus_max_V=bmax, Vbus_pp_V=bmax - bmin,
                                   Ibat_media_A=media(t, d['i_bat_A'], a, b), Ibat_ef_A=eficaz(t, d['i_bat_A'], a, b),
                                   Ibat_pico_A=extremos(t, d['i_bat_A'], a, b)[1], Pbat_W=mv['Vbat'] * media(t, d['i_bat_A'], a, b),
                                   VC8_media_V=media(t, d['v_C8_V'], a, b), VC7_media_V=media(t, d['v_C7_V'], a, b)),
                 c_saida=dict(Vo_ef_V=eficaz(t, vo, a, b), Vo1_ef_V=v1, DHT_vo_pct=th, Io_ef_A=Io, Io_pico_A=max(abs(imin), abs(imax)),
                              fator_crista=max(abs(imin), abs(imax)) / Io if Io > 0.1 else None, Po_W=media(t, vo * d['i_o_A'], a, b),
                              So_VA=eficaz(t, vo, a, b) * Io, M_efetivo=max(abs(x) for x in extremos(t, d['v_c_V'], a, b)) / 5,
                              vc_livre_pico_V=max(abs(x) for x in extremos(t, d['v_c_livre_V'], a, b)),
                              I_QA_ef_A=eficaz(t, d['i_QA_A'], a, b), I_Lo_pico_A=max(abs(x) for x in extremos(t, d['i_Lo_A'], a, b))))
        m['c_saida']['FP_carga'] = m['c_saida']['Po_W'] / m['c_saida']['So_VA'] if m['c_saida']['So_VA'] > 1 else None
        if modo == 'rede':
            m['diodo_D1'] = dict(pico_A=extremos(t, d['i_D1_A'], a, b)[1], media_A=media(t, d['i_D1_A'], a, b),
                                 ef_A=eficaz(t, d['i_D1_A'], a, b), IC4_ef_A=eficaz(t, d['i_C4_A'], a, b))
        if m['a_entrada']['Pin_W'] > 10 and modo == 'rede':
            m['rendimento_rede'] = m['c_saida']['Po_W'] / m['a_entrada']['Pin_W']
        if modo == 'bateria' and m['b_barramento']['Pbat_W'] > 10:
            m['rendimento_bateria'] = m['c_saida']['Po_W'] / m['b_barramento']['Pbat_W']
        res[modo] = m
    tr = jan.get('transferencia') or jan.get('retorno')
    if tr:
        a, b = tr
        tfal = mv['tfalta'] if 'transferencia' in jan else mv['tretorno']
        sc = ef_por_semiciclo(t, d['v_o_V'], tfal - 3 / 120, tfal + 12 / 120)
        bmin, _ = extremos(t, d['v_bus_V'], tfal, tfal + 0.06)
        res['transferencia'] = dict(instante_s=tfal, Vo_ef_semiciclos=[[r(x, 6), r(y, 5)] for x, y in sc],
                                    Vo_ef_semiciclo_min_V=min(y for _, y in sc), Vo_ef_semiciclo_max_V=max(y for _, y in sc),
                                    Vbus_min_apos_V=bmin,
                                    Iin_pico_A=max(abs(x) for x in extremos(t, d['i_rede_A'], tfal, tfal + 0.02)),
                                    Ibat_pico_A=extremos(t, d['i_bat_A'], tfal, tfal + 0.06)[1])
    return res


def analisar_regulacao():
    tabela = {}
    for V in ('176', '220', '264', 'bat'):
        pts = []
        for n in sorted(ENS):
            if not n.startswith(f'reg_{V}_'):
                continue
            d, reg = carregar(n)
            if d is None:
                continue
            a, b = reg['janelas']['regime']
            t = d['tempo_s']
            Pnom = int(n.split('_')[-1])
            pts.append(dict(ensaio=n, Po_nominal_W=Pnom, Vo_ef_V=eficaz(t, d['v_o_V'], a, b),
                            Po_medida_W=media(t, d['v_o_V'] * d['i_o_A'], a, b), DHT_vo_pct=dht(t, d['v_o_V'], a, b)[0],
                            Vbus_min_V=extremos(t, d['v_bus_V'], a, b)[0], M_efetivo=max(abs(x) for x in extremos(t, d['v_c_V'], a, b)) / 5,
                            sha256_csv=reg['sha256_csv']))
        if pts:
            pts.sort(key=lambda p: p['Po_nominal_W'])
            ent = dict(pontos=pts)
            nl = [p for p in pts if p['Po_nominal_W'] == 0]
            fl = [p for p in pts if p['Po_nominal_W'] == 2100]
            if nl and fl:
                ent['RV_pct'] = (nl[0]['Vo_ef_V'] - fl[0]['Vo_ef_V']) / fl[0]['Vo_ef_V'] * 100
            ent['completo'] = len(pts) == 11
            tabela[V] = ent
    return tabela


# ---------------------------------------------------------------------------
def main():
    M, figs, pendentes = {}, [], []
    for nome, e in ENS.items():
        if e['grupo'].startswith('regulacao'):
            continue
        d, reg = carregar(nome)
        if e['grupo'] == 'diagnostico':
            r = reg or {}
            ent = dict(modelo=e['modelo'], status=r.get('status', 'nao executado'), duracao_real_s=r.get('duracao_real_s'),
                       erro=(r.get('erro') or '')[:300] or None, descricao=e['descricao'])
            if d is not None:
                ent.update(analisar_diagnostico(nome, d, reg))
            M[nome] = ent
            continue
        if d is None:
            pendentes.append(dict(ensaio=nome, status=(reg or {}).get('status', 'nao executado'), erro=(reg or {}).get('erro')))
            continue
        base = dict(execucao=f'{nome}_execucao.json', sha256_csv=reg['sha256_csv'], sha256_modelo=reg['sha256_modelo'],
                    amostras=reg['amostras'], descricao=e['descricao'])
        if e['modelo'] == 'retificador_barramento':
            base.update(analisar_retificador(nome, d, reg))
        elif e['modelo'].startswith('elevador'):
            base.update(analisar_elevador(nome, d, reg))
        elif e['modelo'] == 'inversor_malha_fechada':
            base.update(analisar_inversor(nome, d, reg))
        else:
            base.update(analisar_nobreak(nome, d, reg))
        M[nome] = base
    reg_tab = analisar_regulacao()
    if reg_tab:
        M['regulacao'] = reg_tab
    for n in ENS:
        if ENS[n]['grupo'].startswith('regulacao') and not (OUT / f'{n}.csv').exists():
            pendentes.append(dict(ensaio=n, status='nao executado'))
    # convergencia numerica
    if 'conv_176_nl' in M and 'nb_176_nl' in M:
        cmp = {}
        for modo in ('rede', 'bateria'):
            for grupo, chave in (('c_saida', 'Vo_ef_V'), ('c_saida', 'DHT_vo_pct'), ('b_barramento', 'Vbus_media_V'),
                                 ('b_barramento', 'Ibat_media_A'), ('a_entrada', 'Iin_ef_A')):
                x0 = M['nb_176_nl'][modo][grupo][chave]
                x1 = M['conv_176_nl'][modo][grupo][chave]
                if x0 is not None and x1 is not None:
                    cmp[f'{modo}.{chave}'] = dict(base=x0, refinado=x1, dif_rel=abs(x0 - x1) / max(abs(x1), 1e-9))
        M['verificacao_convergencia'] = cmp
    # ------------------------- graficos ---------------------------------
    def tem(*ns):
        return all(n in M for n in ns)

    if tem('nb_176_nl'):
        d, _ = carregar('nb_176_nl')
        figs.append(painel_nobreak([('176 V, não linear', d)], 'nb_176_nl'))
    if tem('nb_264_lin', 'nb_264_nl'):
        d1, _ = carregar('nb_264_lin')
        d2, _ = carregar('nb_264_nl')
        figs.append(painel_nobreak([('linear', d1), ('não linear', d2)], 'nb_264'))
    if tem('nb_220_lin', 'nb_220_nl'):
        d1, _ = carregar('nb_220_lin')
        d2, _ = carregar('nb_220_nl')
        figs.append(painel_nobreak([('linear', d1), ('não linear', d2)], 'nb_220'))
    if tem('nb_176_nl', 'nb_176_nl_anexo'):
        d1, _ = carregar('nb_176_nl')
        d2, _ = carregar('nb_176_nl_anexo')
        fig, ax = plt.subplots(2, 1, figsize=(3.45, 2.9), sharex=True)
        for j, (lab, d) in enumerate((('CC-CC em espera', d1), ('CC-CC sempre comandado', d2))):
            t = d['tempo_s']
            m = (t >= 0.05) & (t <= 0.2)
            ax[0].plot(t[m] * 1e3, d['v_bus_V'][m], color=COR[j], lw=.8, label=lab)
            ax[1].plot(t[m] * 1e3, d['i_bat_A'][m], color=COR[j], lw=.8)
        ax[0].set_ylabel('Barramento (V)')
        ax[1].set_ylabel('Bateria (A)')
        ax[1].set_xlabel('Tempo (ms)')
        ax[0].legend(frameon=False, loc='upper right', fontsize=7)
        for a in ax:
            a.axvline(100, color='0.35', lw=.6, ls=':')
        figs.append(salvar(fig, 'cc_espera_vs_anexo'))
    if tem('nb_176_nl'):
        d, _ = carregar('nb_176_nl')
        t = d['tempo_s']
        m = (t >= 0.09) & (t <= 0.13)
        fig, ax = plt.subplots(3, 1, figsize=(3.45, 3.6), sharex=True)
        ax[0].plot(t[m] * 1e3, d['v_o_V'][m], color=COR[0], lw=.8, label='$v_o$')
        ax[0].plot(t[m] * 1e3, d['v_ref_V'][m] / P['malha']['Hv'], color=COR[1], lw=.8, ls='--', label='$v_{ref}/H_v$')
        ax[0].legend(frameon=False, loc='lower left', ncol=2, fontsize=7)
        ax[0].set_ylabel('Saída (V)')
        ax[1].plot(t[m] * 1e3, d['v_bus_V'][m], color=COR[2], lw=.8)
        ax[1].set_ylabel('Barramento (V)')
        ax[2].plot(t[m] * 1e3, d['i_bat_A'][m], color=COR[3], lw=.6)
        ax[2].set_ylabel('Bateria (A)')
        ax[2].set_xlabel('Tempo (ms)')
        for a in ax:
            a.axvline(100, color='0.35', lw=.6, ls=':')
        figs.append(salvar(fig, 'transferencia_176_nl'))
    if 'regulacao' in M:
        fig, ax = plt.subplots(figsize=(3.45, 2.4))
        rot = {'176': '176 V', '220': '220 V', '264': '264 V', 'bat': 'bateria 42 V'}
        mk = {'176': 'o', '220': 's', '264': '^', 'bat': 'D'}
        for j, (V, ent) in enumerate(M['regulacao'].items()):
            xs = [p['Po_nominal_W'] for p in ent['pontos']]
            ys = [p['Vo_ef_V'] for p in ent['pontos']]
            ax.plot(xs, ys, marker=mk[V], ms=3.5, lw=1, color=COR[j], label=rot[V])
        ax.set_xlabel('Potência de saída nominal (W)')
        ax.set_ylabel('$V_o$ eficaz (V)')
        # legenda numa linha acima do eixo, porque as quatro curvas ocupam toda a area util
        ax.legend(frameon=False, fontsize=7, ncol=4, loc='lower center', bbox_to_anchor=(0.5, 1.0),
                  columnspacing=1.2, handlelength=1.6)
        virgula(ax.yaxis)
        figs.append(salvar(fig, 'regulacao'))
    if tem('ret_176_planilha', 'ret_176_anexo'):
        fig, ax = plt.subplots(2, 1, figsize=(3.45, 2.9), sharex=True)
        for j, n in enumerate(('ret_176_planilha', 'ret_176_anexo')):
            d, _ = carregar(n)
            t = d['tempo_s']
            m = (t >= 0.1) & (t <= 0.1 + 2 * T60)
            lab = 'condições da seção 3' if j == 0 else '1880 µF, 0,1 Ω, diodos reais'
            ax[0].plot((t[m] - 0.1) * 1e3, d['v_bus_V'][m], color=COR[j], lw=.9, label=lab)
            ax[1].plot((t[m] - 0.1) * 1e3, d['i_D1_A'][m], color=COR[j], lw=.9)
        ax[1].axhline(P['retificador']['planilha']['Ichg'], color='0.4', lw=.6, ls=':')
        ax[0].set_ylabel('Barramento (V)')
        ax[1].set_ylabel('$i_{D1}$ (A)')
        ax[1].set_xlabel('Tempo a partir de 100 ms (ms)')
        ax[0].legend(frameon=False, fontsize=7, loc='lower right')
        figs.append(salvar(fig, 'retificador_176'))
    if tem('elev_42'):
        d, reg = carregar('elev_42')
        t = d['tempo_s']
        a, b = reg['janelas']['detalhe']
        m = (t >= b - 3 / 2e4) & (t <= b)
        fig, ax = plt.subplots(3, 1, figsize=(3.45, 3.4), sharex=True)
        tt = (t[m] - (b - 3 / 2e4)) * 1e6
        ax[0].plot(tt, d['gate_S1'][m], color=COR[0], lw=.8)
        ax[0].set_ylabel('Gate S1')
        ax[1].plot(tt, d['i_bat_A'][m], color=COR[1], lw=.8, label='$L_b$')
        ax[1].plot(tt, d['i_S1_A'][m], color=COR[2], lw=.8, label='$S_1$')
        # folga no topo para que a legenda nao caia sobre a corrente de Lb
        alto = max(float(np.max(d['i_bat_A'][m])), float(np.max(d['i_S1_A'][m])))
        ax[1].set_ylim(top=alto * 1.45)
        ax[1].legend(frameon=False, fontsize=7, ncol=2, loc='upper right')
        ax[1].set_ylabel('Corrente (A)')
        ax[2].plot(tt, d['v_S1_V'][m], color=COR[3], lw=.8)
        ax[2].set_ylabel('$v_{S1}$ (V)')
        ax[2].set_xlabel('Tempo (µs)')
        figs.append(salvar(fig, 'elevador_42'))
    if tem('inv_2116_nl', 'inv_2116_res'):
        fig, ax = plt.subplots(2, 1, figsize=(3.45, 2.9), sharex=True)
        for j, n in enumerate(('inv_2116_res', 'inv_2116_nl')):
            d, reg = carregar(n)
            t = d['tempo_s']
            m = (t >= 0.1 - 2 * T60) & (t <= 0.1)
            lab = 'resistiva 2100 W' if j == 0 else 'não linear'
            ax[0].plot((t[m] - t[m][0]) * 1e3, d['v_o_V'][m], color=COR[j], lw=.9, label=lab)
            ax[1].plot((t[m] - t[m][0]) * 1e3, d['i_o_A'][m], color=COR[j], lw=.9)
        ax[0].set_ylabel('$v_o$ (V)')
        ax[1].set_ylabel('$i_o$ (A)')
        ax[1].set_xlabel('Tempo (ms)')
        ax[0].legend(frameon=False, fontsize=7, loc='lower left', ncol=2)
        figs.append(salvar(fig, 'inversor_2116'))
    if tem('inv_degrau_2116'):
        d, reg = carregar('inv_degrau_2116')
        t = d['tempo_s']
        ta = reg['opcoes']['ModelVars']['tcarga']
        m = (t >= ta - 0.01) & (t <= ta + 0.02)
        fig, ax = plt.subplots(2, 1, figsize=(3.45, 2.7), sharex=True)
        ax[0].plot((t[m] - ta) * 1e3, d['v_o_V'][m], color=COR[0], lw=.8, label='$v_o$')
        ax[0].plot((t[m] - ta) * 1e3, d['v_ref_V'][m] / P['malha']['Hv'], color=COR[1], lw=.8, ls='--', label='$v_{ref}/H_v$')
        ax[0].legend(frameon=False, fontsize=7, ncol=2, loc='lower left')
        ax[0].set_ylabel('Saída (V)')
        ax[1].plot((t[m] - ta) * 1e3, d['i_o_A'][m], color=COR[2], lw=.8)
        ax[1].set_ylabel('$i_o$ (A)')
        ax[1].set_xlabel('Tempo após o degrau (ms)')
        figs.append(salvar(fig, 'degrau_2116'))
    if tem('nb_220_retorno'):
        d, reg = carregar('nb_220_retorno')
        t = d['tempo_s']
        m = (t >= 0.19) & (t <= 0.24)
        fig, ax = plt.subplots(3, 1, figsize=(3.45, 3.4), sharex=True)
        ax[0].plot(t[m] * 1e3, d['i_rede_A'][m], color=COR[0], lw=.8)
        ax[0].set_ylabel('Entrada (A)')
        ax[1].plot(t[m] * 1e3, d['v_bus_V'][m], color=COR[1], lw=.8)
        ax[1].set_ylabel('Barramento (V)')
        ax[2].plot(t[m] * 1e3, d['v_o_V'][m], color=COR[2], lw=.8)
        ax[2].set_ylabel('Saída (V)')
        ax[2].set_xlabel('Tempo (ms)')
        figs.append(salvar(fig, 'retorno_220'))
    M['_figuras'] = figs
    M['_pendentes'] = pendentes
    (OUT / 'metricas.json').write_text(json.dumps(M, indent=1, ensure_ascii=False, default=float), encoding='utf-8')
    linhas = ['# Métricas dos ensaios PLECS', '',
              'Fonte: CSVs com hash conferido contra o registro `_execucao.json`; janelas em número inteiro de ciclos de 60 Hz.',
              'Gerado por `analisar_resultados.py`. Valores de classe S; as comparações com A vêm de `parametros.json`.', '']
    if pendentes:
        linhas += ['## Ensaios pendentes ou com falha', '']
        linhas += [f"- `{p['ensaio']}`: {p['status']}" + (f" ({str(p['erro'])[:200]})" if p.get('erro') else '') for p in pendentes]
        linhas.append('')
    if 'regulacao' in M:
        linhas += ['## Curvas de regulação', '', '| Rede | Po nominal (W) | Po medida (W) | Vo eficaz (V) | DHT (%) | M efetivo |', '|---|---|---|---|---|---|']
        for V, ent in M['regulacao'].items():
            for p in ent['pontos']:
                linhas.append(f"| {V} | {p['Po_nominal_W']} | {p['Po_medida_W']:.1f} | {p['Vo_ef_V']:.3f} | {p['DHT_vo_pct']:.2f} | {p['M_efetivo']:.3f} |")
        linhas.append('')
        for V, ent in M['regulacao'].items():
            if 'RV_pct' in ent:
                linhas.append(f"- RV em {V}: {ent['RV_pct']:.3f}%")
        linhas.append('')
    for n, v in M.items():
        if n in ('regulacao', '_figuras', '_pendentes'):
            continue
        linhas += [f'## {n}', '', '```json', json.dumps(v, indent=1, ensure_ascii=False, default=float), '```', '']
    (OUT / 'metricas.md').write_text('\n'.join(linhas), encoding='utf-8')
    print(f'{len([k for k in M if not k.startswith("_")])} grupos analisados; {len(figs)} figuras; {len(pendentes)} pendentes.')


if __name__ == '__main__':
    main()
