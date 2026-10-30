import os, secrets
from datetime import date, datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash
import database as db
import validaciones as val

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=bool(os.environ.get('RENDER')))

ROLES = {
    'Inicio': ['Administrador', 'Empleado', 'Entrenador'],
    'Clientes': ['Administrador', 'Empleado', 'Entrenador'],
    'Empleados': ['Administrador'],
    'Entrenadores': ['Administrador', 'Entrenador'],
    'Membresías y pagos': ['Administrador', 'Empleado'],
    'Accesos': ['Administrador', 'Empleado'],
    'Máquinas': ['Administrador', 'Empleado'],
    'Rutinas': ['Administrador', 'Empleado', 'Entrenador'],
    'Clases': ['Administrador', 'Empleado', 'Entrenador'],
    'Reportes': ['Administrador'],
    'Usuarios': ['Administrador'],
}

# La cuenta inicial de producción se configura mediante variables de entorno en Render.
def ensure_admin():
    con = db.obtener_conexion()
    try:
        count = con.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0]
        if count == 0:
            user = os.environ.get('GYM_ADMIN_USER', 'admin')
            password = os.environ.get('GYM_ADMIN_PASSWORD')
            if not password:
                raise RuntimeError('Configura GYM_ADMIN_PASSWORD en las variables de entorno antes de iniciar.')
            con.execute('INSERT INTO usuarios(usuario,contrasena,tipo) VALUES(?,?,?)',
                        (user, generate_password_hash(password), 'Administrador'))
            con.commit()
    finally:
        con.close()

ensure_admin()


def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapped


def role_required(module):
    def deco(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if session.get('rol') not in ROLES[module]:
                abort(403)
            return fn(*args, **kwargs)
        return wrapped
    return deco


def csrf_check():
    token = request.form.get('_csrf', '')
    if not token or token != session.get('_csrf'):
        abort(400, 'Formulario vencido. Recarga la página e inténtalo de nuevo.')


def csrf_token():
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_urlsafe(32)
    return session['_csrf']

app.jinja_env.globals['csrf_token'] = csrf_token
app.jinja_env.globals['roles'] = ROLES
app.jinja_env.globals['today'] = lambda: date.today().isoformat()
app.jinja_env.globals['current_month'] = lambda: date.today().strftime('%Y-%m')

@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'usuario' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        csrf_check()
        rol = db.validar_usuario(request.form.get('usuario','').strip(), request.form.get('contrasena',''))
        if rol:
            session.clear()
            session['usuario'] = request.form.get('usuario','').strip()
            session['rol'] = rol
            session['_csrf'] = secrets.token_urlsafe(32)
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    csrf_check(); session.clear(); return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', report=db.reporte_general())

@app.route('/<module>')
@login_required
def module_page(module):
    key = {'clientes':'Clientes','empleados':'Empleados','entrenadores':'Entrenadores','membresias':'Membresías y pagos','accesos':'Accesos','maquinas':'Máquinas','rutinas':'Rutinas','clases':'Clases','reportes':'Reportes','usuarios':'Usuarios'}.get(module)
    if not key: abort(404)
    if session.get('rol') not in ROLES[key]: abort(403)
    db.actualizar_estados_membresia()
    data = {'module': module, 'title': key, 'tables': [], 'forms': []}
    def field(name,label,kind='text',required=True,options=None,placeholder=''):
        return {'name':name,'label':label,'kind':kind,'required':required,'options':options,'placeholder':placeholder}
    def form(title,action,fields,button='Guardar'):
        data['forms'].append({'title':title,'action':action,'fields':fields,'button':button})
    def table(title,headers,rows): data['tables'].append({'title':title,'headers':headers,'rows':rows})

    if module == 'clientes':
        form('Registrar cliente','cliente_crear',[field('identificacion','Identificación'),field('nombre','Nombre'),field('telefono','Teléfono'),field('correo','Correo','email'),field('fecha','Fecha de nacimiento','date')])
        form('Buscar cliente','cliente_buscar',[field('identificacion','Identificación')],'Buscar')
        form('Modificar cliente','cliente_actualizar',[field('identificacion','Identificación'),field('nombre','Nombre'),field('telefono','Teléfono'),field('correo','Correo','email'),field('fecha','Fecha de nacimiento','date')],'Actualizar')
        form('Activar / desactivar cliente','cliente_estado',[field('identificacion','Identificación'),field('estado','Acción','select',True,[('Activo','Activar'),('Desactivado','Desactivar')])],'Aplicar')
        form('Eliminar cliente','cliente_eliminar',[field('identificacion','Identificación')],'Eliminar')
        table('Clientes registrados',['ID','Identificación','Nombre','Teléfono','Correo','Nacimiento','Estado'],db.todos_clientes())
    elif module == 'empleados':
        form('Registrar empleado','empleado_crear',[field('identificacion','Identificación'),field('nombre','Nombre'),field('telefono','Teléfono'),field('cargo','Cargo')])
        form('Buscar empleado','empleado_buscar',[field('identificacion','Identificación')],'Buscar')
        form('Actualizar empleado','empleado_actualizar',[field('identificacion','Identificación'),field('nombre','Nombre'),field('telefono','Teléfono'),field('cargo','Cargo')],'Actualizar')
        form('Eliminar empleado','empleado_eliminar',[field('identificacion','Identificación')],'Eliminar')
        table('Empleados',['Identificación','Nombre','Teléfono','Cargo'],db.todos_empleados())
    elif module == 'entrenadores':
        form('Registrar entrenador','entrenador_crear',[field('identificacion','Identificación'),field('nombre','Nombre'),field('especialidad','Especialidad')])
        form('Buscar entrenador','entrenador_buscar',[field('identificacion','Identificación')],'Buscar')
        form('Actualizar entrenador','entrenador_actualizar',[field('identificacion','Identificación'),field('nombre','Nombre'),field('especialidad','Especialidad')],'Actualizar')
        form('Eliminar entrenador','entrenador_eliminar',[field('identificacion','Identificación')],'Eliminar')
        table('Entrenadores',['ID','Identificación','Nombre','Especialidad'],db.todos_entrenadores())
    elif module == 'membresias':
        plans=[(k,k) for k in db.PLANES_MEMBRESIA]
        form('Crear membresía','membresia_crear',[field('nombre','Nombre del titular'),field('tipo','Plan','select',True,plans),field('inicio','Fecha de inicio','date'),field('fin','Fecha de fin','date')])
        mems=[(str(r[0]),f'#{r[0]} · {r[1]} · {r[2]} · ${r[3]:,.0f}') for r in db.membresias()]
        form('Asignar / renovar y registrar pago','membresia_asignar',[field('identificacion','Identificación del cliente'),field('membresia_id','Membresía','select',True,mems),field('fecha','Fecha de pago','date'),field('valor','Valor','number'),field('concepto','Concepto')])
        form('Consultar estado de membresía','membresia_estado',[field('identificacion','Identificación')],'Consultar')
        form('Registrar pago adicional','pago_crear',[field('identificacion','Identificación'),field('fecha','Fecha','date'),field('valor','Valor','number'),field('concepto','Concepto')])
        form('Consultar pagos del cliente','pagos_buscar',[field('identificacion','Identificación')],'Consultar')
        table('Membresías',['ID','Titular','Plan','Precio','Clases','Inicio','Fin','Estado'],db.membresias())
    elif module == 'accesos':
        form('Registrar ingreso','ingreso',[field('identificacion','Identificación')],'Registrar ingreso')
        form('Registrar salida','salida',[field('identificacion','Identificación')],'Registrar salida')
        form('Consultar asistencia','asistencia',[field('identificacion','Identificación')],'Consultar')
        form('Consultar estado del cliente','cliente_estado_consulta',[field('identificacion','Identificación')],'Consultar')
    elif module == 'maquinas':
        form('Registrar máquina','maquina_crear',[field('nombre','Nombre'),field('marca','Marca'),field('estado','Estado','select',True,[(x,x) for x in ['Disponible','Mantenimiento','Fuera de servicio']])])
        form('Cambiar estado','maquina_estado',[field('id','ID de máquina','number'),field('estado','Nuevo estado','select',True,[(x,x) for x in ['Disponible','Mantenimiento','Fuera de servicio']])],'Actualizar')
        table('Máquinas',['ID','Nombre','Marca','Estado'],db.maquinas())
    elif module == 'rutinas':
        form('Registrar rutina','rutina_crear',[field('identificacion','ID del cliente'),field('nombre','Nombre de rutina'),field('descripcion','Descripción'),field('fecha','Fecha','date')])
        form('Consultar rutinas del cliente','rutina_buscar',[field('identificacion','Identificación')],'Consultar')
        table('Todas las rutinas',['ID','Identificación','Cliente','Rutina','Descripción','Fecha'],db.rutinas())
        form('Asignar entrenador al cliente','asignar_entrenador',[field('identificacion','ID del cliente'),field('entrenador_id','ID del entrenador','number')],'Asignar')
    elif module == 'clases':
        ents=[(str(r[0]),f'{r[0]} · {r[2]} ({r[3]})') for r in db.todos_entrenadores()]
        form('Registrar participación en clase','clase_crear',[field('identificacion','ID del cliente'),field('entrenador_id','Entrenador','select',True,ents),field('fecha','Fecha','date')])
        form('Consultar clases disponibles','clases_disponibles',[field('identificacion','ID del cliente')],'Consultar')
        form('Consultar historial del cliente','clases_historial',[field('identificacion','ID del cliente')],'Consultar')
        form('Pagos a instructores por mes','pagos_instructores',[field('mes','Mes (YYYY-MM)','month')],'Consultar')
        table('Clases realizadas',['ID','Identificación','Cliente','Entrenador','Fecha'],db.todas_clases_realizadas())
    elif module == 'reportes':
        form('Resumen mensual (RF44–RF48)','resumen_mensual',[field('mes','Mes (YYYY-MM)','month')],'Generar resumen')
        table('Indicadores generales',['Indicador','Valor'],list(db.reporte_general().items()))
    elif module == 'usuarios':
        form('Crear usuario del sistema','usuario_crear',[field('usuario','Usuario'),field('contrasena','Contraseña','password'),field('tipo','Rol','select',True,[(x,x) for x in ['Administrador','Empleado','Entrenador']])])
        con=db.obtener_conexion(); rows=con.execute('SELECT usuario,tipo FROM usuarios ORDER BY usuario').fetchall(); con.close()
        table('Usuarios',['Usuario','Rol'],rows)
    return render_template('module.html', **data)

def validar(*resultados):
    for ok, mensaje in resultados:
        if not ok:
            raise ValueError(mensaje)


@app.route('/accion/<action>', methods=['POST'])
@login_required
def action(action):
    csrf_check()
    module_map = {
      'cliente_':'Clientes','empleado_':'Empleados','entrenador_':'Entrenadores','membresia_':'Membresías y pagos','pagos_':'Membresías y pagos',
      'ingreso':'Accesos','salida':'Accesos','asistencia':'Accesos','cliente_estado':'Accesos','maquina_':'Máquinas','rutina_':'Rutinas','asignar_entrenador':'Rutinas',
      'clase_':'Clases','clases_':'Clases','pagos_instructores':'Clases','resumen_mensual':'Reportes','usuario_':'Usuarios'
    }
    module = {'cliente_estado_consulta':'Accesos','pagos_instructores':'Clases','pago_crear':'Membresías y pagos'}.get(action) or next((v for prefix,v in module_map.items() if action.startswith(prefix)), None)
    if not module or session.get('rol') not in ROLES[module]: abort(403)
    f=request.form
    msg=''; ok=False
    try:
      if action=='cliente_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.texto(f['nombre'],'nombre'),val.numeros(f['telefono'],'teléfono'),val.correo(f['correo']),val.fecha(f['fecha'],'fecha de nacimiento'))
        ok,msg=db.insertar_cliente(f['identificacion'].strip(),f['nombre'].strip(),f['telefono'].strip(),f['correo'].strip(),f['fecha'])
      elif action=='cliente_buscar':
        r=db.buscar_cliente(f['identificacion'].strip()); msg=(f'Encontrado: {r[2]} · {r[3]} · {r[4]} · estado {r[6]}' if r else 'No se encontró el cliente.'); ok=bool(r)
      elif action=='cliente_actualizar':
        validar(val.numeros(f['identificacion'],'identificación'),val.texto(f['nombre'],'nombre'),val.numeros(f['telefono'],'teléfono'),val.correo(f['correo']),val.fecha(f['fecha'],'fecha de nacimiento'))
        ok,msg=db.actualizar_cliente(f['identificacion'],f['nombre'],f['telefono'],f['correo'],f['fecha'])
      elif action=='cliente_eliminar': ok,msg=db.eliminar_cliente(f['identificacion'])
      elif action=='cliente_estado':
        fn=db.activar_cliente if f['estado']=='Activo' else db.desactivar_cliente; ok,msg=fn(f['identificacion'])
      elif action=='empleado_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.texto(f['nombre'],'nombre'),val.numeros(f['telefono'],'teléfono'),val.texto(f['cargo'],'cargo'))
        ok,msg=db.insertar_empleado(f['identificacion'],f['nombre'],f['telefono'],f['cargo'])
      elif action=='empleado_buscar':
        r=db.buscar_empleado(f['identificacion']); msg=f'Encontrado: {r}' if r else 'Empleado no encontrado.'; ok=bool(r)
      elif action=='empleado_actualizar': ok,msg=db.actualizar_empleado(f['identificacion'],f['nombre'],f['telefono'],f['cargo'])
      elif action=='empleado_eliminar': ok,msg=db.eliminar_empleado(f['identificacion'])
      elif action=='entrenador_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.texto(f['nombre'],'nombre'),val.texto(f['especialidad'],'especialidad'))
        ok,msg=db.insertar_entrenador(f['identificacion'],f['nombre'],f['especialidad'])
      elif action=='entrenador_buscar':
        r=db.buscar_entrenador(f['identificacion']); msg=f'Encontrado: {r}' if r else 'Entrenador no encontrado.'; ok=bool(r)
      elif action=='entrenador_actualizar': ok,msg=db.actualizar_entrenador(f['identificacion'],f['nombre'],f['especialidad'])
      elif action=='entrenador_eliminar': ok,msg=db.eliminar_entrenador(f['identificacion'])
      elif action=='membresia_crear':
        validar(val.texto(f['nombre'],'nombre'),val.fecha(f['inicio'],'fecha de inicio'),val.fecha(f['fin'],'fecha de fin'))
        if f['fin'] < f['inicio']: raise ValueError('La fecha final no puede ser anterior a la inicial.')
        plan=db.PLANES_MEMBRESIA[f['tipo']]; ok,msg=db.crear_membresia(f['nombre'],f['tipo'],plan['precio'],plan['clases'],f['inicio'],f['fin'])
      elif action=='membresia_asignar':
        validar(val.numeros(f['identificacion'],'identificación'),val.fecha(f['fecha'],'fecha de pago'),val.positivo(f['valor'],'valor'))
        ok,msg=db.asignar_membresia_y_pago(f['identificacion'],int(f['membresia_id']),f['fecha'],float(f['valor']),f['concepto'])
      elif action=='membresia_estado':
        r=db.estado_membresia(f['identificacion']); msg=f'Estado: {r}' if r else 'Cliente no encontrado o sin membresía.'; ok=bool(r)
      elif action=='pago_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.fecha(f['fecha'],'fecha de pago'),val.positivo(f['valor'],'valor'))
        ok,msg=db.registrar_pago(f['identificacion'],f['fecha'],float(f['valor']),f['concepto'])
      elif action=='pagos_buscar':
        r=db.pagos_cliente(f['identificacion']); msg='Pagos: '+str(r); ok=True
      elif action=='ingreso': ok,msg=db.registrar_ingreso(f['identificacion'],datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      elif action=='salida': ok,msg=db.registrar_salida(f['identificacion'],datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      elif action=='asistencia':
        r=db.asistencia_cliente(f['identificacion']); msg='Historial: '+str(r); ok=True
      elif action=='cliente_estado_consulta':
        r=db.estado_cliente(f['identificacion']); msg=f'{r[0]}: {r[1]}' if r else 'Cliente no encontrado.'; ok=bool(r)
      elif action=='maquina_crear':
        validar(val.texto(f['nombre'],'nombre'),val.texto(f['marca'],'marca'))
        ok,msg=db.registrar_maquina(f['nombre'],f['marca'],f['estado'])
      elif action=='maquina_estado': ok,msg=db.cambiar_estado_maquina(int(f['id']),f['estado'])
      elif action=='rutina_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.texto(f['nombre'],'nombre'),val.fecha(f['fecha'],'fecha'))
        ok,msg=db.registrar_rutina(f['identificacion'],f['nombre'],f['descripcion'],f['fecha'])
      elif action=='rutina_buscar':
        r=db.rutinas_cliente(f['identificacion']); msg='Rutinas: '+str(r); ok=True
      elif action=='asignar_entrenador': ok,msg=db.asignar_entrenador(f['identificacion'],int(f['entrenador_id']))
      elif action=='clase_crear':
        validar(val.numeros(f['identificacion'],'identificación'),val.fecha(f['fecha'],'fecha'))
        ok,msg=db.registrar_participacion_clase(f['identificacion'],int(f['entrenador_id']),f['fecha'])
      elif action=='clases_disponibles':
        r=db.clases_disponibles_cliente(f['identificacion']); msg=f'Clases disponibles: {r}' if r is not None else 'Cliente no encontrado.'; ok=r is not None
      elif action=='clases_historial':
        r=db.clases_realizadas_cliente(f['identificacion']); msg='Historial: '+str(r); ok=True
      elif action=='pagos_instructores':
        validar(val.anio_mes(f['mes']))
        r=db.resumen_pagos_instructores(f['mes']); msg=f'Resumen {f["mes"]}: '+str(r)+f' · Total a pagar: ${db.total_pagar_instructores_mes(f["mes"]):,.0f}'; ok=True
      elif action=='resumen_mensual':
        validar(val.anio_mes(f['mes']))
        msg=str(db.resumen_mensual(f['mes'])); ok=True
      elif action=='usuario_crear':
        con=db.obtener_conexion(); con.execute('INSERT INTO usuarios(usuario,contrasena,tipo) VALUES(?,?,?)',(f['usuario'].strip(),generate_password_hash(f['contrasena']),f['tipo'])); con.commit(); con.close(); ok=True; msg='Usuario creado correctamente.'
      else: abort(404)
    except (ValueError, KeyError) as e:
      msg='Verifica los campos ingresados y sus formatos.'; ok=False
    except Exception as e:
      app.logger.exception('Error en acción %s', action); msg='No se pudo completar la operación. Verifica los datos e inténtalo nuevamente.'; ok=False
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('module_page',module={'Clientes':'clientes','Empleados':'empleados','Entrenadores':'entrenadores','Membresías y pagos':'membresias','Accesos':'accesos','Máquinas':'maquinas','Rutinas':'rutinas','Clases':'clases','Reportes':'reportes','Usuarios':'usuarios'}[module]))

@app.errorhandler(403)
def forbidden(e): return render_template('error.html', code=403, message='Tu rol no tiene permiso para acceder a este módulo.'),403
@app.errorhandler(404)
def not_found(e): return render_template('error.html', code=404, message='La página solicitada no existe.'),404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
