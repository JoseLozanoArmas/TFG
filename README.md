# CODE-ULL
## Introducción
En este repositorio podrán encontrar todo lo necesario para poder desarrollar correctamente la aplicación web "CODE-ULL", la cual se trata de un sistema para la ejecución, validación y puntuación de código. El cual permite a los docentes desarrollar pruebas en base a bloques, que luego sus alumnos podrán resolver, haciendo que el propio sistema corrija sus entradas en base a las pruebas desarrolladas por los docentes, para luego reflejarlo todo en un ranking teniendo en cuenta los puntos y tiempo desarrollado.
## Activar el sistema
Para poder activar el sistema correctamente se recomienda situarse en la raíz del repositorio, teniendo dos terminales activas, donde una gestionará la parte del Frontend y otra la del Backend, activando ambas al usar los siguientes comandos en dichas terminales:
```bash
# npm start
# python3 server.py
```

## Roles del sistema
La aplicación contempla el poder utilizar tres tipos de usuarios, siendo estos:
* **Monitores**: Su labor es la de crear los bloques de preguntas, las entradas a las mismas y las pruebas asociadas a cada una
* **Administradores**: Tienen la misma tarea que el anterior, más funcionalidades extras relacionadas con el manejo de la memoria y los usuarios permitidos.
* **Alumnos**: Ellos se limitarán a acceder al contenido generado por los dos roles anteriores y desarrollar las distintas pruebas se que se les indiquen.

## Método de uso

### Administradores y monitores (Docentes)
En el caso de acceder a la plataforma actuando cómo docente, se deberá registrar en la pantalla principal e introducir las credenciales adecuadas. Una vez pasada esta pantalla se pasará a un panel de control donde los monitores tendrán acceso a ver los rankings de los usuarios y los bloques de preguntas. En caso de ser administrador aparte podrán ver un apartado desde el que configurar algunas opciones de la aplicación.

Si se accede a la zona de bloque de preguntas, desde aquí los docentes podran crear los distintos bloques al pulsar el botón de "más" ubicado en esta pantalla, donde una vez creado el mismo si se pulsa dicha entrada se pasará a una pantalla desde la que gestionar la creación de las preguntas de cada bloque.

En caso de crear dichas preguntas, si se accede al interior de la misma el docente deberá añadir un título y descripción a la pregunta, además de sus respectivas pruebas, las cuales se tratarán de ficheros de entrada y ficheros con el resultado esperado, sumado a los puntos de la pregunta. La estructura de dichos ficheros será la siguiente:

```txt
info_1
info_2
info_3
```

Donde "info" hace referencia a cualquier tipo de entrada o resultado esperado, pudiendo haber más de una entrada por línea. Una vez registrado todos estos apartados los docentes deberán darle al botón de confirmar para registrarlo todo.

### Usuarios (Alumnos)
Por la parte de los usuarios estos deberán indicar un nombre para registrarse y luego seleccionar el bloque que los docentes le indiquen, para acto seguido proceder a empezar a desarollar los cuestionarios. Cada alumno al entrar a una pregunta deberá subir un código cuya extensión será en python, javacript, c, c++ o ruby. En caso contrario se asumirá la entrada cómo **errónea**. Una vez subido el código este deberá pulsar el botón de confirmar para poder corregir la misma, en caso de superar correctamente la pregunta se le mandará una notificación al usuario felicitandole, y moviendolo automáticamente a la pantalla con el resto de preguntas para que pueda seguir desarrollandolas. En caso contrario tambíen se le avisará pero se le mantendrá en la misma por si se diese el caso de querer intentarlo de nuevo, aunque siempre podrá dejar esa pregunta pendiente e intentar el resto. 

De cara a los rankings, en caso de que el usuario supere todas las pruebas de una pregunta se registrará la hora en la que terminó la misma, para luego poder hacer un correcto ordenamiento en los rankings, en caso contrario solo se registrarán los puntos de las pruebas resueltas. Independientemente de esto, cualquier usuario podrá ver las clasificaciones de los mismos si se pulsa el botón de "finalizar intento" localizado en la página donde se puede ver la lista de preguntas.