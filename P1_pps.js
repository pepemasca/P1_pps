var names = ["Ana", "Pedro", "Carmen"]; // Apartado 2. de esta manera se declaran las variables, concretamente un array de strings
    console.log(names);

names.forEach(function(nombre) { // Apartado 6. la función forEach() es un método que se aplica a las listas, en este caso a la lista names. Recorre cada elemento de la lista y aplica la función que se le pasa como argumento
    var nombres = nombre.toUpperCase(); // la función toUpperCase() convierte el string en mayúsculas
    console.log(nombres);
    });

function calcularProvisionales(notas) {   // Apartado 7. la función propia calcularNotaFinal() recibe como argumento una lista de números decimales (floats) y devuelve la nota sobre 8 y redondeada al entero más cercano
    return notas.map(nota => Math.round(nota * 0.8));
  }
  
  let notas = [5.3, 7.2, 8.9]; // Notas provisionales sobre 10
  console.log(notas);
  let notasProvisionales = calcularProvisionales(notas);
  console.log(notasProvisionales); // [4, 6, 7]

var notas_finales = [4, 6]; // de esta manera se declaran las variables, concretamente un array de números enteros (integers). Se trata de las notas finales sobre 8 y redondeadas al entero más cercano, aunque falta una nota   

notas_finales.push(7); // la función push() añade un elemento olvidado al final de la lista      

// Apartado 9. las estructuras anteriores son listas

const PERSONAS = {
    "ANA_prueba": {
      edad: 30,
      ciudad: "Madrid",
      profesion: "Ingeniera"
    },
    "PEDRO_prueba": {
      edad: 25,
      ciudad: "Barcelona",
      profesion: "Programador"
    },
    "CARMEN_prueba": {
      edad: 35,
      ciudad: "Valencia",
      profesion: "Abogada"
    }
  };

  console.log(PERSONAS);

// Apartados 3 y 9. Las anteriores constantes toman una estructura de diccionario, es decir, un conjunto de pares clave-valor  

// Apartado 4. A modo de simplificación y aprovechando la POO, se puede definir una clase que contenga las variables anteriores integradas en un objeto por cada persona

class Alumno {
    constructor(nombre, edad, ciudad, profesion, nivel_ingles, experiencia_profesional, notas_provisionales, notas_finales) {
      this.nombre = nombre;
      this.edad = edad;
      this.ciudad = ciudad;
      this.profesion = profesion;
      this.nivel_ingles = nivel_ingles;
      this.experiencia_profesional = experiencia_profesional;
      this.notas_provisionales = notas_provisionales;
      this.notas_finales = notas_finales;
    }
  
    // Apartado 8. Método para determinar si el alumno ha aprobado o suspendido
    estado() {
        if (this.notas_finales >= 5) {
            return "Aprobado";
        } else {
            return "Suspendido";
        }
    }
}

  // Apartado 5. Crear objetos para Ana, Pedro y Carmen
  const ANA = new Alumno("Ana", 30, "Madrid", "Ingeniera", "C1", "5 años", 5.3, 4);
  const PEDRO = new Alumno("Pedro", 25, "Barcelona", "Programador", "C2", "2 años", 7.2, 6);
  const CARMEN = new Alumno("Carmen", 35, "Valencia", "Abogada", "B2", "10 años", 8.9, 7);
  
// Array de alumnos
const alumnos = [ANA, PEDRO, CARMEN];

// Usar console.table() para mostrar los datos en formato tabular
console.table(alumnos);

// Apartado 9. structura de bucles con "for...of" para mostrar el estado de cada alumno
for (const alumno of alumnos) {
    const estado = alumno.estado();
    console.log(`${alumno.nombre} - Nota Final: ${alumno.notas_finales} - Estado: ${estado}`);
}

