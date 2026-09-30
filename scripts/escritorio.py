"""Despacho-archivo de los años cincuenta, modelado por código.
Uso: blender --background --factory-startup --python scripts/escritorio.py
Genera assets/escritorio.glb (texturas JPEG pequeñas incrustadas; sin Draco: ~400 KB y sin descompresor externo).
Coordenadas de Blender: x derecha, y hacia el fondo, z arriba; la superficie de la mesa está en z=0.
"""
import bpy, bmesh, math, pathlib
import numpy as np

root = pathlib.Path(__file__).resolve().parent.parent
bpy.ops.wm.read_factory_settings(use_empty=True)
rng = np.random.default_rng(7)

# ---------- texturas generadas ----------
def smooth_noise(n, cells, seed):
    r = np.random.default_rng(seed).random((cells + 1, cells + 1))
    x = np.linspace(0, cells, n, endpoint=False)
    i = x.astype(int); f = x - i; f = f * f * (3 - 2 * f)
    a = r[i][:, i]; b = r[i][:, i + 1]; c = r[i + 1][:, i]; d = r[i + 1][:, i + 1]
    fx = f[None, :]; fy = f[:, None]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy

def fbm(n, seed, oct=5, base=4):
    v = np.zeros((n, n)); amp = .5; tot = 0
    for o in range(oct):
        v += amp * smooth_noise(n, base * 2 ** o, seed + o); tot += amp; amp *= .5
    return v / tot

def image(name, rgb):
    h, w, _ = rgb.shape
    img = bpy.data.images.new(name, w, h, alpha=False)
    px = np.ones((h, w, 4), np.float32); px[..., :3] = np.clip(rgb, 0, 1)
    img.pixels.foreach_set(px.ravel())
    img.file_format = 'JPEG'
    img.pack()
    return img

N = 512
yy, xx = np.mgrid[0:N, 0:N] / N
warp = fbm(N, 3, 4, 3)
grain = np.sin((yy * 38 + warp * 5.5 + fbm(N, 11, 3, 2) * 2) * math.pi) * .5 + .5
grain = grain ** 3
fine = fbm(N, 21, 5, 16)
wood_l = .55 + .3 * fine - .35 * grain
wood = np.stack([wood_l * .30, wood_l * .155, wood_l * .075], -1)
wood_img = image('madera', wood)

lea = .7 + .3 * fbm(256, 40, 5, 24)
leather_img = image('piel', np.stack([lea * .07, lea * .12, lea * .09], -1))

pap = .93 + .07 * fbm(256, 50, 4, 8)
paper_img = image('papel', np.stack([pap * .91, pap * .87, pap * .78], -1))

man = .9 + .1 * fbm(256, 60, 4, 10)
manila_img = image('manila', np.stack([man * .70, man * .56, man * .36], -1))

# ---------- materiales ----------
def mat(name, color=(1, 1, 1), rough=.6, metal=0., tex=None, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    if tex:
        t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = tex
        m.node_tree.links.new(t.outputs['Color'], bsdf.inputs['Base Color'])
    if emit:
        bsdf.inputs['Emission Color'].default_value = (*emit, 1)
        bsdf.inputs['Emission Strength'].default_value = 4
    return m

M = dict(
    madera=mat('madera', rough=.42, tex=wood_img),
    piel=mat('piel', rough=.7, tex=leather_img),
    laton=mat('laton', (.62, .47, .24), .32, 1.),
    laton_oscuro=mat('laton_oscuro', (.30, .22, .11), .45, 1.),
    laca=mat('laca', (.018, .018, .02), .22),
    teclas=mat('teclas', (.55, .52, .45), .4),
    caucho=mat('caucho', (.03, .03, .03), .8),
    papel=mat('papel', rough=.85, tex=paper_img),
    manila=mat('manila', rough=.8, tex=manila_img),
    cuerda=mat('cuerda', (.36, .06, .05), .9),
    tinta_roja=mat('tinta_roja', (.28, .02, .02), .5),
    vidrio=mat('vidrio', (.02, .025, .03), .08),
    madera_clara=mat('madera_clara', (.33, .19, .09), .5),
    bombilla=mat('bombilla', (1, .85, .6), .3, emit=(1, .78, .5)),
)

def obj(o, m, name=None, bevel=0, seg=2):
    if name: o.name = name
    o.data.materials.clear(); o.data.materials.append(M[m])
    if bevel:
        b = o.modifiers.new('bisel', 'BEVEL'); b.width = bevel; b.segments = seg; b.limit_method = 'ANGLE'
    for p in o.data.polygons: p.use_smooth = True
    return o

def box(name, m, size, loc, rot=(0, 0, 0), bevel=0, seg=2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return obj(o, m, name, bevel, seg)

def cyl(name, m, r, d, loc, rot=(0, 0, 0), v=32, r2=None, cap='NGON', bevel=0):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot, end_fill_type=cap)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=v, radius1=r, radius2=r2, depth=d, location=loc, rotation=rot, end_fill_type=cap)
    return obj(bpy.context.active_object, m, name, bevel)

def rod(name, m, r, a, b, v=16):
    """Cilindro entre los puntos a y b."""
    from mathutils import Vector
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.active_object
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return obj(o, m, name)

def sphere(name, m, r, loc, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    return obj(bpy.context.active_object, m, name)

def parent(children, name):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e)
    for c in children: c.parent = e
    return e

# ---------- mesa ----------
box('Mesa', 'madera', (2.4, 1.3, .05), (0, 0, -.025), bevel=.012, seg=3)
box('Faldon', 'madera', (2.3, 1.2, .1), (0, 0, -.1), bevel=.006)
box('Vade', 'piel', (.86, .56, .006), (.02, -.04, .003), bevel=.003)

# ---------- lámpara de latón (tipo banquero, pantalla de latón) ----------
L = []
L.append(cyl('Lampara_base', 'laton', .11, .025, (.68, .36, .0125), bevel=.006))
L.append(cyl('Lampara_base2', 'laton_oscuro', .075, .012, (.68, .36, .031)))
L.append(cyl('Lampara_tubo', 'laton', .011, .36, (.68, .36, .215)))
L.append(sphere('Lampara_rotula', 'laton', .02, (.68, .36, .40)))
hx, hy, hz = .52, .13, .40
L.append(rod('Lampara_brazo', 'laton', .009, (.68, .36, .40), (hx + .01, hy + .02, hz + .075)))
L.append(sphere('Lampara_rotula2', 'laton', .016, (hx + .01, hy + .02, hz + .075)))
L.append(cyl('Lampara_pantalla', 'laton', .16, .15, (hx, hy, hz), rot=(math.radians(-18), math.radians(-8), 0), r2=.045, cap='NOTHING', v=48))
sh = bpy.context.active_object
sol = sh.modifiers.new('grosor', 'SOLIDIFY'); sol.thickness = .004
L.append(sphere('Lampara_bombilla', 'bombilla', .035, (hx - .005, hy - .012, hz - .045)))
parent(L, 'Lampara')

# ---------- máquina de escribir ----------
T = []
cx, cy, rz = .08, .42, math.radians(-4)
def tw(p):  # posición local de la máquina a mundo
    x, y, z = p; c, s = math.cos(rz), math.sin(rz)
    return (cx + x * c - y * s, cy + x * s + y * c, z)
T.append(box('Maquina_cuerpo', 'laca', (.40, .30, .09), tw((0, .03, .058)), (0, 0, rz), bevel=.022, seg=4))
T.append(box('Maquina_frente', 'laca', (.40, .12, .045), tw((0, -.14, .03)), (math.radians(14), 0, rz), bevel=.015, seg=3))
for row in range(4):
    n = 11 - (row % 2)
    for k in range(n):
        x = (k - (n - 1) / 2) * .031 + (row % 2) * .0
        y = -.19 + row * .034; z = .045 + row * .014
        T.append(cyl(f'Tecla_{row}_{k}', 'teclas', .0115, .006, tw((x, y, z + .018)), rot=(0, 0, 0), v=14))
        T.append(cyl(f'Vastago_{row}_{k}', 'laton_oscuro', .0025, .03, tw((x, y + .004, z)), rot=(math.radians(-25), 0, rz), v=6))
T.append(box('Barra_espacio', 'teclas', (.20, .016, .008), tw((0, -.225, .038)), (0, 0, rz), bevel=.004))
T.append(cyl('Rodillo', 'caucho', .026, .52, tw((0, .15, .125)), rot=(0, math.radians(90), rz), v=28))
T.append(cyl('Perilla_izq', 'laca', .022, .025, tw((-.285, .15, .125)), rot=(0, math.radians(90), rz), bevel=.006))
T.append(cyl('Perilla_der', 'laca', .022, .025, tw((.285, .15, .125)), rot=(0, math.radians(90), rz), bevel=.006))
T.append(box('Carro', 'laton', (.50, .03, .012), tw((0, .185, .105)), (0, 0, rz), bevel=.003))
T.append(cyl('Palanca', 'laton', .004, .09, tw((-.30, .12, .15)), rot=(0, math.radians(70), rz + math.radians(20)), v=8))
# hoja en la máquina, ligeramente curvada
bpy.ops.mesh.primitive_grid_add(x_subdivisions=2, y_subdivisions=10, size=1, location=(0, 0, 0))
pg = bpy.context.active_object; pg.name = 'Maquina_hoja'
bm = bmesh.new(); bm.from_mesh(pg.data)
for v in bm.verts:
    u = v.co.y + .5
    v.co.x *= .215; v.co.z = .15 + u * .24; v.co.y = .17 + math.sin(u * 1.2) * .03 + u * .02
    wx, wy, wz = tw((v.co.x, v.co.y, v.co.z)); v.co.x, v.co.y, v.co.z = wx, wy, wz
bm.to_mesh(pg.data); bm.free(); obj(pg, 'papel')
T.append(pg)
parent(T, 'Maquina')

# ---------- carpetas de expediente ----------
F = []
for k, (dx, dy, r) in enumerate([(-.02, .0, 3), (.015, .012, -2), (-.01, -.006, 6)]):
    z = .012 + k * .01
    F.append(box(f'Carpeta_{k}', 'manila', (.36, .46, .006), (.02 + dx, -.08 + dy, z), (0, 0, math.radians(r)), bevel=.002))
    F.append(box(f'Hojas_{k}', 'papel', (.34, .44, .004), (.02 + dx + .004, -.08 + dy + .004, z - .004), (0, 0, math.radians(r + .6))))
F.append(box('Pestana', 'manila', (.12, .03, .006), (.08, .165, .033), (0, 0, math.radians(6))))
F.append(box('Cinta', 'cuerda', (.012, .47, .002), (.02, -.08, .038), (0, 0, math.radians(6))))
parent(F, 'Carpetas')

# ---------- sello de goma y tampón ----------
S = []
S.append(box('Tampon', 'laca', (.14, .09, .018), (.62, -.30, .009), (0, 0, math.radians(8)), bevel=.004))
S.append(box('Tampon_tinta', 'tinta_roja', (.12, .07, .002), (.62, -.30, .019), (0, 0, math.radians(8))))
S.append(box('Sello_base', 'madera_clara', (.08, .045, .022), (.43, -.33, .02), (0, 0, math.radians(-10)), bevel=.004))
S.append(box('Sello_goma', 'tinta_roja', (.076, .041, .008), (.43, -.33, .004), (0, 0, math.radians(-10))))
S.append(cyl('Sello_mango', 'madera_clara', .012, .07, (.43, -.33, .066), bevel=.002))
S.append(sphere('Sello_pomo', 'madera_clara', .024, (.43, -.33, .108)))
parent(S, 'Sello')

# ---------- tintero y pluma ----------
I = []
I.append(box('Tintero', 'vidrio', (.06, .06, .05), (.42, .06, .025), (0, 0, math.radians(20)), bevel=.012, seg=3))
I.append(cyl('Tintero_tapa', 'laton', .018, .018, (.42, .06, .058)))
I.append(cyl('Pluma', 'laca', .006, .15, (.38, -.1, .007), rot=(0, math.radians(90), math.radians(35)), v=12))
I.append(cyl('Pluma_capuchon', 'laton', .0065, .03, (.435, -.062, .007), rot=(0, math.radians(90), math.radians(35)), v=12))
parent(I, 'Tintero')

# ---------- papeles sueltos ----------
for k, (x, y, r) in enumerate([(-.55, -.24, 22), (-.40, -.36, -9), (.30, -.05, 14), (-.72, .02, -30)]):
    box(f'Papel_{k}', 'papel', (.21, .28, .0015), (x, y, .001 + k * .0006), (0, 0, math.radians(r)))

# ---------- exportación ----------
out = root / 'assets' / 'escritorio.glb'
bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', export_apply=True,
                          export_draco_mesh_compression_enable=False,
                          export_image_format='JPEG', export_jpeg_quality=78, export_cameras=False, export_lights=False)
print('GLB', out, out.stat().st_size // 1024, 'KB')
