#include "Arduino.h"

// Define o pino de entrada analógica
#define ANALOG_PIN A0

// Define a taxa de transmissão da serial
#define BAUD_RATE 115200

// Cria uma variável para armazenar o valor analógico
int analogValue = 0;

// Função de interrupção do timer
ISR(TIMER2_COMPA_vect) {
    // Lê o valor do pino analógico A0 e armazena na variável analogValue
    analogValue = analogRead(ANALOG_PIN);

    // Converte o valor analógico (10 bits) em dois bytes
    uint8_t byteAlto = (uint8_t(analogValue >> 7) & 0x07) | 0x80;
    uint8_t byteBaixo = analogValue & 0x7F;

    Serial.write(byteAlto);
    Serial.write(byteBaixo);
}



void setup() {
  // Configura o timer
  noInterrupts();
  // Clear registers
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2 = 0;

    // 10000 Hz (16000000/((24+1)*64))
  OCR2A = 24;
  // CTC
  TCCR2A |= (1 << WGM21);
  // Prescaler 64
  TCCR2B |= (1 << CS22);
  // Output Compare Match A Interrupt Enable
  TIMSK2 |= (1 << OCIE2A);
  interrupts();

  // Inicia a comunicação serial
  Serial.begin(BAUD_RATE);
}

void loop() {
  //  All the work is done in the timer interrupt service routine (ISR) 
  return;
}