exec(open('/home/claude/maestra/datos2.py').read())
import re,random
random.seed(7)
ESTILO="""Character lineup sheet for a fantasy tactics game (aetherpunk, Greek-inspired world). Use the attached layout image exactly: 4 columns, one character per column, numbered 1 to 4 from left to right.
Rules for every character, no exceptions:
- Full body, standing, facing the viewer, relaxed neutral pose, arms slightly away from the body, weapon held at the side.
- Top of the head touches the upper line and the soles of the feet touch the lower line of its column. Same height for adults; children and elderly may be shorter but feet stay on the lower line.
- Head clearly visible and not covered, unless the description says helmet or hood.
- Anime/manga illustration, clean dark lineart, flat cel shading with one shadow tone, saturated but not neon colors, dense small details (straps, buckles, tools, gears).
- Solid flat background #A9CBA6 everywhere. No scenery, no shadows on the floor, no text, no numbers, no guide lines in the final image.
- Characters do not touch or overlap each other and stay inside their own column.
- Same art style, line weight and lighting in all 4 columns.
Characters:"""
NACION={'Elirio':'Elyrian refugee clothing, Greek-inspired: layered linen tunics, wrapped cloaks, bronze clasps, worn leather sandals or boots, patched and practical',
'Kaldholt':'Kaldholt northern clothing: wool and fur, quilted coats, iron fittings, braided details, cold-weather boots',
'Ferannor':'Ferannor industrial empire clothing: black leather, brass buckles, rivets, tinted lenses, starched uniform lines',
'Lusse':'Lusse factory-worker clothing: grey canvas overalls, rust-stained, tool belts, soot',
'Cassaria':'Cassaria clothing: warm colors, embroidered sashes, mining gear mixed with festive fabrics',
'Ordun':'Ordun nomad clothing: many travel layers, wide scarves, beads, sun-faded fabrics',
'Tradición dracónica':'old draconic order clothing: ritual robes with scale motifs, ember-orange and bone tones',
'Orden dracónica':'old draconic order clothing: ritual robes with scale motifs, ember-orange and bone tones',
'Mercenario':'mercenary clothing: mismatched armor pieces, practical leather, no insignia',
'Sombra Rota':'gang clothing: dark hooded jackets, crossbow straps, nets, rough patched leather',
'Quebrados':'desperate raiders: torn rags, improvised armor, scavenged tools',
'Hijos del Hielo':'Kaldholt irregular militia: furs, torches, oil flasks, crude iron',
'Culto del Lete':'Lethe cult robes: pale grey and faded blue, frayed edges, small glass fragments sewn in',
'Tierras Grises':'poor southern coast clothing: sun-bleached, salt-stained, simple',
'Theira':'harbor clothing: oilskin coat, rope, brass whistle',
'Hollin':'market town clothing from Kaldholt, apron and wool',
'Ardel':'Cassarian craftsman clothing, sawdust apron',
'Consejo elirio':'Elyrian council robes, faded but formal, bronze pin of two flames',
'Saqueadores':'raiders: torn rags, improvised armor',
'Banda de la sal de Hollin':'salt-smuggler gang: heavy coats crusted with salt, hooks',
'Compañía de Cassaria':'Cassarian company enforcer: embroidered coat, ledger, pistol belt',
'Compañía de Ferannor en Velde':'Ferannor mining overseer: canvas and brass, lamp on the belt',
'Mercenarios de Kaldholt':'Kaldholt mercenaries: fur over chainmail',
'Antigua guardia elíria':'Elyrian temple guard: bronze scale armor, faded crest',
'Elirios del sur':'starving southern refugees: rags, sickles',
'Ex culto':'former Lethe cultist: grey robe torn off at the sleeves'}
def nacion(o):
    for k in NACION:
        if o.startswith(k) or k in o: return NACION[k]
    return NACION['Elirio']
PELOS=['black','dark brown','light brown','blonde','auburn','red','pink','green','blue','light blue','purple','silver white','grey']
FEM={'Nemira','Corina','Elana','Sael','Marisol','Margit','Neli','Thessa','Astrid','Ingrid','Riona','Phaedra','Selene','Ianna','Ines','Paloma','Livia','Greta','Auria','Malva','Ottilie','Brandt','Henrike Maurer','Maren','Aldana','Sigra','Petra','Ragnhild','Lotte','Demetria','Ilse','Sofronia','Lysa','Madre de Nemira','Dione','Agna Brask','Nuri','Hedda'}
EDAD={'Demetria':'elderly woman, around 70','Aristeo':'elderly man, around 70','Orestion':'man in his fifties, imposing','Orestion quemado':'man in his fifties, hollow empty stare, burnt ritual clothes','Sofronia':'very old woman','Kairon niño':'boy around 8','Aiyo':'child around 9','Yorgos':'old man, around 65','Henrike Maurer':'woman in her fifties, precise and calm','Brandt':'woman in her forties, hard face','Oren vacío':'man in his thirties, blank empty eyes, slack posture'}
ARMA={'Bastión':'heavy mace and industrial shield','Guardia de Chatarra':'scrap-metal blade and improvised shield','Escudo de Kaldholt':'short spear and round shield','Deslizador':'short sword, light boots with small aether skates','Jinete de Grifo':'lance','Explorador':'light bow','Correo de la Diáspora':'throwing daggers on a bandolier, message satchel','Filo':'sword','Custodio Elirio':'ceremonial glaive','Furia de Cassaria':'axe','Artillero':'flintlock spark rifle','Cazador':'bow and quiver','Mecánico de Batalla':'big wrench and blowtorch','Tejedor':'improvised aether focus that glows cyan','Sacerdote de la Llama Vieja':'ritual lamp','Susurrador del Olvido':'glowing fissure shard','Guardián del Recuerdo':'locket reliquary and a journal','Jinete de Alce':'lance','Jinete de Búho Nival':'short bow and daggers','Aeronauta':'grappling hooks and supply pouches','Cantor':'no weapon, hands open as if singing','Curandero de las Grises':'walking staff and herb satchel','Artificiero':'large riveted brass mechanical gauntlet on the right hand','Saqueador':'club and torch','Recolector':'collection canister and hooked pole','Guardia de lente':'halberd, violet lens over one eye','Matón de Sombra Rota':'crossbow and weighted net','Vacío':'no weapon','Civil':'sickle or stones','Andador de Ferannor':'piston rifle','Andador de Asedio':'heavy piston cannon'}
MONTURA={'Jinete de Grifo':'riding a griffin (whole mount fits in the column, character still facing the viewer)','Jinete de Alce':'riding a large northern elk','Jinete de Búho Nival':'riding a giant snow owl','Aeronauta':'standing in the basket of a small aether balloon, seen from the front','Andador de Ferannor':'riding a two-legged mechanical piston walker','Andador de Asedio':'riding a heavy four-legged piston walker'}
def base(c):
    c=c.split(' →')[0].split(' (')[0].replace(' con arma física','')
    return c
def arma(c):
    b=base(c); a=ARMA.get(b)
    if not a:
        for k in ARMA:
            if c.startswith(k): a=ARMA[k]; b=k
    if 'con arma física' in c: a='ritual lamp and a temple guard spear'
    return a or 'no weapon', MONTURA.get(b,'')
def slot(n,nombre,clase,origen,nota,i):
    sexo='woman' if nombre in FEM else 'man'
    edad=EDAD.get(nombre, f'young {sexo}, around {random.choice([18,20,23,26,29,33])}')
    pelo=random.choice(PELOS) if nombre not in('Kairon',) else 'dark brown'
    a,m=arma(clase)
    if nombre=='Kairon': return f"CHARACTER {n}. Kairon: young man, around 20, lean. Dark brown hair. Long cream coat, maroon sash tied at the waist, Elyrian clothing underneath. Weapon: {a}."
    if clase=='NPC': return f"CHARACTER {n}. {nombre}: {edad}. {pelo.capitalize()} hair. {nacion(origen)}. No weapon. {nota}."
    return f"CHARACTER {n}. {nombre}: {edad}. {pelo.capitalize()} hair. {nacion(origen)}. Weapon: {a}.{(' '+m.capitalize()+'.') if m else ''}"
def gen_slot(n,clase,i):
    sexo=['man','woman'][i%2]
    a,m=arma(clase)
    return f"{n}. Generic {clase} soldier: {sexo}, around 25, average build, face visible. Hair short, plain brown. Neutral off-white clothing with grey-blue accents so it can be recolored later. Weapon: {a}.{(' '+m.capitalize()+'.') if m else ''}"
ESTILO2="""Character sheet for a fantasy tactics game (aetherpunk, Greek-inspired world). Use the attached layout image exactly: two characters, CHARACTER 1 on the left half and CHARACTER 2 on the right half. Each character has three panels.
- Panel A: portrait from the waist up, head and shoulders large, three-quarter view turned toward the right side of the image, face looking right, calm expression. The top of the head sits just below the thin line, never cut. Only the bottom edge cuts the body (at the waist). Same scale as a game dialogue portrait.
- Panel B: the same character, same outfit, same framing, but turned toward the left side of the image. Redraw it, do not mirror: asymmetric details (scars, hair parting, a gauntlet or weapon on one hand, a pauldron on one shoulder) stay on the same side of the body.
- Panel C: full body, standing, facing the viewer, neutral relaxed pose, weapon held at the side. Top of the head on the upper thin line, soles of the feet on the lower thin line.
Rules for everything:
- Anime/manga illustration, clean dark lineart, flat cel shading with one shadow tone, saturated but not neon colors, dense small details (straps, buckles, tools, gears).
- The same character must look identical in A, B and C (face, hair, colors, outfit).
- Solid flat background #A9CBA6 inside every panel. No scenery, no floor shadow.
- Remove all guide lines, panel borders, labels and text from the final image. Nothing may cross from one panel into another.
Characters:"""
lotes=[]
items=[('pj',n,c,o,no) for _,n,e,c,g,o,no in J]+[('en',n,c,f,no) for _,n,e,c,a,f,no in E]
for k in range(0,len(items),2): lotes.append(('Personajes',items[k:k+2]))
vis=set(); clases=[]
for b,p in C:
    if b not in vis: vis.add(b); clases.append(b)
    clases.append(p+' ('+b+')')
clases+=[n for n,_ in ENEM]
for k in range(0,len(clases),4): lotes.append(('Genéricos',clases[k:k+4]))
out=[]
for li,(t,grupo) in enumerate(lotes,1):
    lines=[]
    for j,it in enumerate(grupo,1):
        if t=='Personajes':
            _,n,c,o,no=it; lines.append(slot(j,n,c,o,no,li))
        else:
            c=it; nm=c.split(' (')[0]; bb=c.split(' (')[1][:-1] if '(' in c else c
            a,m=arma(bb); sx=['man','woman'][j%2]
            if nm=='Vacío': lines.append(f"{j}. Generic Vacío (a person who burned all their memories with aether): around 35, gaunt, ash-grey skin, blank glassy eyes, torn clothes of no nation, cyan cracks of light on the skin. No weapon."); continue
            if nm=='Civil': lines.append(f"{j}. Generic civilian refugee: woman, around 40, thin, worn southern clothing, holding a sickle. Neutral off-white clothing with grey-blue accents."); continue
            lines.append(f"{j}. Generic {nm}: {sx}, around 25, average build, face visible. Short plain brown hair. Neutral off-white clothing with grey-blue accents so it can be recolored later. Weapon: {a}.{(' '+m.capitalize()+'.') if m else ''}")
    nombres=', '.join((it[1] if t=='Personajes' else it.split(' (')[0]) for it in grupo)
    molde='molde_2pj_1344x768.png' if t=='Personajes' else 'molde_4x_1344x768.png'
    out.append(f"===== LOTE {li:02d} · {t} · {nombres} · molde {molde} =====\n{ESTILO2 if t=='Personajes' else ESTILO}\n"+'\n'.join(lines)+'\n')
open('lotes_nano_banana.txt','w').write('\n'.join(out))
print(len(lotes)); print(out[0]); print(out[-1][-600:])
