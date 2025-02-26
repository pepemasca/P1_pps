#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {
    // Inicializamos la semilla para números aleatorios
    srand(static_cast<unsigned int>(time(0)));
    int numeroSecreto = rand() % 100 + 1; // Número aleatorio entre 1 y 100
    int intento;

    cout << "¡Bienvenido al juego de Adivina el Número!" << endl;
    cout << "He seleccionado un número entre 1 y 100. ¿Puedes adivinarlo?" << endl;

    // Bucle principal del juego
    do {
        cout << "Introduce tu intento: ";
        cin >> intento;
        
        if (intento > numeroSecreto) {
            cout << "Demasiado alto. Intenta de nuevo." << endl;
        } else if (intento < numeroSecreto) {
            cout << "Demasiado bajo. Intenta de nuevo." << endl;
        }
    } while (intento != numeroSecreto);

    cout << "¡Felicidades! Has adivinado el número." << endl;
    return 0;
}
