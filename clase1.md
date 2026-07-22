# Actividad de Clase: Analizando Agentes de IA con Hugging Face Spaces

## Objetivo

Explorar aplicaciones reales de Inteligencia Artificial en **Hugging
Face Spaces** y analizarlas desde la perspectiva de los **agentes
racionales**.

Al finalizar la actividad, los estudiantes deberán ser capaces de:

-   Identificar los componentes **PEAS** de un agente.
-   Clasificar las propiedades del entorno.
-   Proponer qué tipo de programa de agente podría implementarse detrás
    del sistema.
-   Justificar sus respuestas.

------------------------------------------------------------------------

## Instrucciones

1.  Ingresen a **https://huggingface.co/spaces**.
2.  Exploren diferentes Spaces.
3.  Seleccionen uno que les parezca interesante.
4.  Interactúen con el sistema durante algunos minutos.
5.  Completen la siguiente ficha de análisis.

------------------------------------------------------------------------

# Ficha de análisis

## 1. Nombre del Space

**Nombre:**keita ashizawa

**Enlace:**https://huggingface.co/spaces/r3gm/wan2-2-fp8da-aoti-preview-2c

------------------------------------------------------------------------

## 2. ¿Qué hace el agente?

Describa en dos o tres líneas cuál es la función del sistema.
Este sistema es para crear un video desde una foto. Si da una foto y prompt en que como quiero crearlo por el sistema, él crea un video.


------------------------------------------------------------------------

## 3. Análisis PEAS

  Elemento          Respuesta
  ----------------- ----------------------------------------------------
  **Performance**   ¿Qué significa que el agente haga bien su trabajo?
  Crear un video
  **Environment**   ¿Con qué interactúa el agente?
  un prompt para crear un video, una foto
  **Actuators**     ¿Qué acciones produce?
  pensar a partir de un prompt como crear un video
  **Sensors**       ¿Qué información recibe como entrada?
  analizar que significa el prompt como es la situación de la foto.

------------------------------------------------------------------------

## 4. Clasificación del entorno

Complete la siguiente tabla y justifique brevemente cada respuesta.

  Propiedad      Clasificación     Justificación
  -------------- ----------------- ---------------
  Observable     Total
  Determinista   Sí          
  Episódico      Sí          
  Estático       Sí           
  Discreto       No           
  Conocido       Sí           

------------------------------------------------------------------------

## 5. ¿Qué tipo de programa de agente creen que es?

Seleccione la opción que consideren más adecuada y explique por qué.
-   Agente basado en objetivos
 En esta programa, tiene un objetivo, crear un video. Además la programa recibe un prompt. Por eso, ella puedo saber un objetivo claramente.
 Entonces, esta programa es de agente basado en objetivos.


> **Importante:** No existe una única respuesta correcta. Lo importante
> es justificar la elección a partir del comportamiento observado.

------------------------------------------------------------------------

# Discusión en clase

Después de las presentaciones, discutiremos preguntas como:

-   ¿Dos Spaces diferentes pueden compartir el mismo tipo de entorno?
-   ¿Es posible saber con certeza qué tipo de agente implementa un Space
    únicamente observándolo?
-   ¿Qué diferencia existe entre el comportamiento observable de un
    agente y su implementación interna?

------------------------------------------------------------------------

# Reto adicional

Encuentre un Space que pueda clasificarse como:

1.  **Totalmente observable, determinista y episódico.**
2.  **Parcialmente observable, estocástico y secuencial.**

Justifique su respuesta.

------------------------------------------------------------------------

# Rúbrica (10 puntos)

| Criterio | Puntos |
|-----------|:------:|
| Descripción correcta del Space | 2 |
| Identificación de PEAS | 3 |
| Clasificación del entorno | 3 |
| Justificación del tipo de agente | 2 |
| **Total** | **10** |

------------------------------------------------------------------------


