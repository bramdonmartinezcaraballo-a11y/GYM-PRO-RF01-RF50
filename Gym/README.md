# GYM PRO - RF01 a RF50

Sistema de gestion de gimnasio en Python con Tkinter y SQLite.

## Ejecucion

```bash
python main.py
```

No requiere paquetes externos.

## Requerimientos incluidos

RF01 Registrar clientes.
RF02 Consultar clientes por identificacion.
RF03 Modificar datos del cliente.
RF04 Eliminar clientes.
RF05 Registrar empleados.
RF06 Consultar y buscar empleados por identificacion.
RF07 Registrar entrenadores y especialidades.
RF08 Registrar membresias mensual, trimestral y anual.
RF09 Asignar membresia a un cliente.
RF10 Consultar estado de membresia (Activa, Vencida, Por vencer o Inactiva).
RF11 Renovar membresia.
RF12 Registrar pagos.
RF13 Consultar historial de pagos.
RF14 Registrar ingreso.
RF15 Registrar salida.
RF16 Controlar acceso segun cliente y membresia.
RF17 Registrar maquinas.
RF18 Consultar maquinas.
RF19 Controlar mantenimiento y estado de maquinas.
RF20 Registrar rutinas.
RF21 Asignar entrenador a un cliente.
RF22 Consultar la rutina asignada a un cliente.
RF23 Registrar/consultar asistencia (historial de ingresos y salidas).
RF24 Generar reportes basicos (clientes, membresias, pagos, asistencias).
RF25 Controlar usuarios del sistema: login y accesos segun tipo de usuario (Administrador, Empleado, Entrenador).
RF26 Membresia Normal: $50.000, 2 clases.
RF27 Membresia Gold: $70.000, 4 clases.
RF28 Membresia Platino: $100.000, 6 clases.
RF29 Un cliente solo puede tener asignada una de las tres membresias (Normal, Gold o Platino) a la vez.
RF30 El sistema registra cuantas clases tiene disponibles cada cliente segun la membresia adquirida.
RF31 Se descuenta una clase disponible cada vez que el cliente participa en una clase.
RF32 Se impide la participacion cuando el cliente ya uso todas sus clases disponibles.
RF33 El sistema muestra al cliente cuantas clases le quedan disponibles.
RF34 Se puede registrar la participacion de un cliente en una clase.
RF35 Se registra la fecha de cada clase realizada.
RF36 Se registra el instructor (entrenador) encargado de cada clase.
RF37 El sistema permite registrar todos los instructores que se necesiten (al menos 4).
RF38 Cada clase realizada queda asociada a uno de los instructores registrados.
RF39 Se establece un pago de $10.000 por cada clase realizada por un instructor.
RF40 El sistema calcula automaticamente cuanto dinero se le debe pagar a cada instructor.
RF41 Se puede consultar cuantas clases realizo cada instructor durante un mes.
RF42 Se puede consultar el valor total a pagar a cada instructor al finalizar el mes.
RF43 El sistema contabiliza el numero total de clases realizadas durante el mes.
RF44 El sistema contabiliza el numero total de personas que participaron en clases durante el mes.
RF45 El sistema calcula cuantas personas participaron segun cada tipo de membresia: Normal, Gold y Platino.
RF46 El sistema calcula los ingresos obtenidos por cada tipo de membresia.
RF47 El sistema calcula el ingreso total obtenido por la venta de todas las membresias durante el mes.
RF48 El sistema genera un resumen mensual que incluye las clases realizadas, los participantes, los ingresos por membresia y los pagos a los instructores.
RF49 El sistema permite desactivar a un cliente sin eliminar sus registros historicos.
RF50 El sistema permite consultar el estado de un cliente (activo o desactivado) y asegura que un cliente desactivado no pueda inscribirse en nuevas clases.

## Interfaz

Toda la aplicacion funciona dentro de una sola ventana. El menu lateral cambia el panel central y no abre ventanas nuevas.

## Validaciones

- Nombre, identificacion, telefono, correo y fecha de nacimiento del cliente.
- Identificacion y telefono solo aceptan numeros.
- El correo debe tener formato usuario@dominio.com.
- Las fechas usan YYYY-MM-DD.
- Los precios y pagos deben ser positivos.
- Las identificaciones duplicadas no se aceptan.
- Se valida la existencia del cliente, membresia y entrenador antes de asignar.
- El acceso se bloquea para clientes desactivados o con membresia que no este activa.

## Correcciones realizadas

- RF06: se agrego un cuadro de busqueda de empleados por identificacion (antes solo se listaban todos).
- RF10: se agrego el estado "Por vencer" (membresias que vencen en 7 dias o menos); antes solo existian Activa, Vencida e Inactiva.
- Se corrigio un error en la consulta de estado de membresia: si un cliente no tenia membresia asignada, el sistema mostraba "Membresía: None | Inicio: None..." en vez del mensaje correcto de "cliente sin membresía asignada".
- Se elimino codigo muerto en el formulario de creacion de membresias (un combobox se creaba y se destruia sin usarse).
- Se agrego una barra de scroll vertical (con soporte de rueda del mouse) a toda el area de contenido, para que ningun formulario o resultado quede oculto fuera de la ventana.
- La busqueda de clientes ahora solo pide la Identificacion; los campos editables (nombre, telefono, correo, fecha) y los botones de modificar/eliminar aparecen automaticamente despues de encontrar al cliente.

## Correcciones de la segunda revision (bugs reales encontrados y reproducidos)

- **BUG CRITICO - Registrar entrada/salida**: el control de acceso (RF16) exigia que el estado guardado de la membresia fuera exactamente "Activa". Al agregar el estado "Por vencer" (RF10), cualquier cliente con membresia proxima a vencer (7 dias o menos) quedaba bloqueado aunque su membresia todavia fuera valida. Se corrigio `registrar_ingreso` para verificar las fechas reales (fecha_inicio/fecha_fin) en vez del texto de estado, que puede quedar desactualizado.
- **BUG - Maquinas a mantenimiento**: se hizo mas robusto el flujo de cambio de estado. Ahora, ademas de seleccionar la fila en la tabla, aparece un campo "ID maquina" que se autocompleta al hacer clic en una fila, o se puede escribir manualmente, evitando fallos si la seleccion de la tabla no registraba el clic.
- **BUG - Crear membresias**: se rediseño el formulario. Ya no se pide escribir tipo/precio libremente (fuente de errores de formato); ahora se elige un Plan (Normal, Gold o Platino) y el precio y las clases incluidas se completan automaticamente segun RF26-RF28.
- **BUG - Gestionar/eliminar entrenadores**: esta funcionalidad no existia en el codigo original. Se agrego buscar, modificar y eliminar entrenador por identificacion (antes solo se podian registrar, nunca eliminar).
- Se agrego tambien buscar, modificar y eliminar empleados, por consistencia con clientes y entrenadores.

## Nuevos requerimientos agregados (RF22 a RF28)

- **RF22** — Consultar rutina: en el modulo Rutinas se puede buscar por identificacion del cliente y ver las rutinas que tiene asignadas.
- **RF23** — Registrar asistencia: en el modulo Accesos, el boton "VER ASISTENCIA" muestra el historial de ingresos y salidas de un cliente.
- **RF24** — Generar reportes: nuevo modulo "Reportes" (solo Administrador) con totales de clientes, membresias por estado, dinero recaudado, asistencias y maquinas en mantenimiento.
- **RF25** — Control de usuarios del sistema: se agrego pantalla de inicio de sesion con tres roles (Administrador, Empleado, Entrenador). El menu lateral solo muestra los modulos permitidos para cada rol. Usuarios de prueba: `admin/admin123`, `empleado/empleado123`, `entrenador/entrenador123`.
- **RF26, RF27, RF28** — Planes de membresia predefinidos: Normal ($50.000 / 2 clases), Gold ($70.000 / 4 clases) y Platino ($100.000 / 6 clases). Se agrego la columna "clases incluidas" a la tabla de membresias y se muestra en el listado.


## Nuevos requerimientos agregados (RF29 a RF36) - sistema de clases

- Se agrego una tabla `clases_realizadas` que guarda cada participacion de un cliente en una clase: cliente, instructor (entrenador) y fecha.
- Cada cliente ahora tiene un contador `clases_disponibles`, que se establece automaticamente segun el plan (Normal=2, Gold=4, Platino=6) cada vez que se le asigna o renueva una membresia (RF29, RF30).
- Al registrar la participacion de un cliente en una clase, el sistema descuenta 1 clase disponible (RF31, RF34, RF35, RF36 con fecha e instructor).
- Si el cliente ya no tiene clases disponibles, el sistema bloquea el registro con un mensaje claro (RF32).
- Nuevo modulo "Clases" en el menu lateral (visible para Administrador, Empleado y Entrenador) donde se puede:
  - Registrar la participacion de un cliente en una clase.
  - Consultar cuantas clases le quedan disponibles a un cliente (RF33).
  - Ver el historial de clases realizadas por un cliente.
  - Ver el listado completo de todas las clases realizadas en el gimnasio.
- La consulta de estado de membresia (modulo Membresias) ahora tambien muestra las clases disponibles actuales del cliente, ademas de las clases incluidas en su plan.
- El modulo de Reportes ahora incluye tambien el total de clases realizadas.
- Se corrigio la migracion de la base de datos para que, si alguien actualiza el sistema conservando una base de datos anterior, los clientes con membresia ya asignada no generen errores (se les asigna un valor por defecto seguro en vez de fallar).
- Todo el modulo nuevo funciona dentro de la misma ventana con barra lateral, igual que el resto del sistema; no abre ventanas ni pestañas nuevas.

## Correcciones y mejoras de esta revision (RF37 a RF43 + organizacion de la interfaz)

- **BUG CRITICO corregido - la pantalla de inicio de sesion no desaparecia**: al ingresar con usuario y contraseña, el codigo anterior dibujaba la aplicacion principal encima de la pantalla de login sin eliminarla primero. Ahora, al construir la aplicacion principal, se limpia completamente la ventana antes de mostrar el panel de control, por lo que la pantalla de login ya no vuelve a aparecer ni queda detras de la app una vez que se inicia sesion.
- **Sub-barra lateral dentro de cada modulo**: ademas de la barra lateral principal (navegacion entre modulos), ahora cada modulo (Clientes, Empleados, Entrenadores, Membresias, Accesos, Maquinas, Rutinas, Clases, Reportes) tiene su propia barra lateral mas angosta a la izquierda del contenido, donde se elige que accion realizar (por ejemplo "Registrar", "Buscar / gestionar", "Listado"). Esto evita que todo quede apilado en una sola pantalla larga y hace mas facil encontrar cada funcion.
- Todo sigue funcionando dentro de la misma ventana y pestaña, sin abrir ventanas nuevas; solo cambia el contenido dentro del area principal.

### Nuevos requerimientos agregados (RF37 a RF43) - pagos a instructores

- Se agrego la constante de pago por clase: $10.000 por cada clase realizada por un instructor (RF39).
- Nueva seccion "Pagos a instructores" disponible tanto en el modulo Clases como en Reportes: se escribe un mes (formato YYYY-MM) y el sistema muestra, para cada instructor, cuantas clases realizo ese mes y cuanto dinero se le debe pagar (RF40, RF41, RF42), calculado automaticamente.
- Se muestra tambien el total de clases realizadas en el mes y el total de dinero a pagar a todos los instructores juntos (RF43).
- El modulo de Entrenadores ahora aclara que se puede registrar la cantidad de instructores que se necesite (RF37); cada clase ya quedaba asociada a un instructor desde la revision anterior (RF38).

## Correcciones y mejoras de esta revision (RF44 a RF50)

- Se agrego una columna `membresia_id` a la tabla de pagos, para poder calcular con precision los ingresos por cada tipo de membresia (RF46), incluso si el cliente cambia de plan mas adelante. La migracion es compatible con bases de datos creadas en versiones anteriores del sistema (no genera errores con datos viejos).
- Nueva seccion "Resumen mensual (RF44-48)" dentro del modulo Reportes: al escribir un mes (YYYY-MM) se muestran juntos: las clases realizadas, los participantes unicos, los participantes y los ingresos por cada tipo de membresia, el ingreso total por venta de membresias, y los pagos a cada instructor — todo en una sola vista, tal como pide RF48.
- En el modulo Accesos, la seccion "Activar / desactivar" ahora tambien incluye "Consultar estado del cliente" (RF50), que muestra claramente si el cliente esta Activo o Desactivado. Un cliente desactivado ya no podia participar en clases (verificado); ahora tambien se puede consultar su estado de forma explicita.
- Se revisaron y probaron con datos reales todos los calculos de RF44 a RF47 (participantes totales, participantes por tipo de membresia, ingresos por tipo y total del mes), incluyendo el caso de un mes sin ningun dato (debe devolver ceros sin errores).
